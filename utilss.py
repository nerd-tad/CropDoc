#import pyrebase  #gotta find a new library for this, maybe you can make one of yourself using aiohttp
import smtplib
import streamlit as st
import json
import numpy as np
import cv2
import onnxruntime
import os
import pyrebase
import smtplib
from email.message import EmailMessage
from datetime import datetime

pyrebase_config = {
  "apiKey": "AIzaSyBwOquhbRztazjOeARWYN9RR5OZC70-v1g",
  "authDomain": "plant-leaf-sample-database.firebaseapp.com",
  "projectId": "plant-leaf-sample-database",
  "storageBucket": "plant-leaf-sample-database.appspot.com",
  "messagingSenderId": "288056378537",
  "appId": "1:288056378537:web:79a513d8da74faec5c95b8",
  "measurementId": "G-1STJYQ48CP",
  "databaseURL":"xxxxxxxxxx"
}

sender_cred_file = 'credentials.txt'
with open(sender_cred_file, 'r') as fh:
    details=fh.read().splitlines()
sender_address = details[0]
sender_password = details[1]

file_attachment_dir = 'files_to_attach'  #in there img_file.jpg is the image that you wanna send as attachment. also there will be details.txt they are changing constantly.
#make a dir named 2022_07_22_name_plant and save the data to it.

def log_dir_name(user_name,plant_name):
    n = str(datetime.now())
    m = n.replace(':','_').replace(' ','---')
    l = m.split('.')[0]
    l = f'{l}_{user_name}_{plant_name}'
    return l

def fn1_old(max_prob_ind, plant, plant_dis_dic):
    return plant_dis_dic[plant][max_prob_ind]

def fn1(max_prob_ind, dis_details):
    #print(dis_details.split('-_-_'))
    #print("length of dis_details is", len(dis_details.split('-_-_')))
    dis_ = dis_details.split('-_-_')[max_prob_ind]
    try:
        dis_dic = json.loads(dis_,strict=False)
        dis_name = dis_dic['dis']
        dis_desc = dis_dic['des']
        return dis_name, dis_desc
    except Exception as e:
        print(e)
        return dis_details, 0

def send_email(user_img, max_prob, user_data_dic, plant_data_dic):
    #userdic is like ['name':'xxx',tel:'xx']
    #plantdic is like ['plant':'xxx','disease':'xxxx']
    #email body
    if max_prob < 0.45:
        msg = EmailMessage()
        attachment_list = [os.path.join(file_attachment_dir, i) for i in os.listdir('files_to_attach')]
        msg['Subject'] = f"Disease check from user {user_data_dic['name']}."
        msg['To'] = 'e15070@eng.pdn.ac.lk'
        msg['From'] = sender_address
        with open('logginInstance.txt', 'r') as fh:
            db_instance_dir = fh.read() 
        msg.set_content(f"{user_data_dic['name']} checked for a plant disease that might be unknown yet.\nFind details from {db_instance_dir} in database.\nImage file is attached there.")

        #attachments and html headers...
        for f in attachment_list:
            with open(f, 'rb') as f:
                file_data = f.read()
                file_name = os.path.split(f.name)[-1]
                #print(file_name)
            msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename = file_name)  #empty files (in this case __init__.py) won't be attached to the attachment
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_sr:
                smtp_sr.login(sender_address, sender_password)
                smtp_sr.send_message(msg)
            return 0
        except Exception as e:  #email not sent exception
            print(e)
            return 2
    else:
        return 1  #will raise 1 if max_prob higher than 0.45, then not a new disease. No need for an email.

def send_email_pseudo(user_img, user_data_dic, plant_data_dic):
    #userdic is like ['name':'xxx',tel:'xx']
    #plantdic is like ['plant':'xxx','disease':'xxxx']
    #email body
    msg = EmailMessage()
    attachment_list = [os.path.join(file_attachment_dir, i) for i in os.listdir('files_to_attach')]
    msg['Subject'] = f"Disease check from user {user_data_dic['name']}."
    msg['To'] = 'e15070@eng.pdn.ac.lk'
    msg['From'] = sender_address
    with open('logginInstance.txt', 'r') as fh:
        db_instance_dir = fh.read() 
    msg.set_content(f"{user_data_dic['name']} checked for a plant disease that might be unknown yet.\nFind details from {db_instance_dir} in database./nImage file is attached there.")

    #attachments and html headers...
    for f in attachment_list:
        with open(f, 'rb') as f:
            file_data = f.read()
            file_name = os.path.split(f.name)[-1]
            #print(file_name)
        msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename = file_name)  #empty files (in this case __init__.py) won't be attached to the attachment
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_sr:
            smtp_sr.login(sender_address, sender_password)
            smtp_sr.send_message(msg)
        return 0
    except Exception as e:  #email not sent exception
        print(e)
        return 1

def save_to_fb(user_img, user_data_dic, plant_data_dic):
    firebase = pyrebase.initialize_app(pyrebase_config)
    storage = firebase.storage()
    #generate instance folder name

    #writing image on file attachment dir
    user_img_np = np.array(user_img)
    user_img_np = cv2.cvtColor(user_img_np, cv2.COLOR_BGR2RGB)
    cv2.imwrite(os.path.join(file_attachment_dir,'img.jpg'),user_img_np)

    #writing details.txt of file attachment dir
    with open(os.path.join(file_attachment_dir,'details.txt'), 'w') as fh:
        #write_string = f"User's name: {user_data_dic['name']}\nUser's Contact No: {user_data_dic['tel']}\nPlant Type: {plant_data_dic['plant']}\nPredicted Disease: {plant_data_dic['disease']}"
        write_string = f"User's name: {user_data_dic['name']}\nUser's Contact No: {user_data_dic['tel']}\nPlant Type: {plant_data_dic['plant']}"
        print(write_string)
        fh.write(write_string)
    #adding items one by one.
    try:
        logginDir = log_dir_name(user_data_dic['name'], plant_data_dic['plant'])
        with open('logginInstance.txt', 'w') as fh:
            fh.write(logginDir)
        for item in os.listdir(file_attachment_dir):
            path_on_cloud = f'{logginDir}/{item}'
            local_path = os.path.join(file_attachment_dir, item)
            storage.child(path_on_cloud).put(local_path)
        return 0
    except Exception as e:
        print(e)
        return 1
        

def my_header(url):
     st.markdown(f'<p style="background-color:transparent;color:#ffff00;border-color:#ff0000;border-width:6px;font-size:48px;border-radius:2%;">{url}</p>', unsafe_allow_html=True)

def my_write(string, color, size=24):
    st.markdown(f'<p style="background-color:transparent;color:#{color};font-size:{size}px;border-radius:2%;">{string}</p>', unsafe_allow_html=True)

def v_spacer(height):
    for _ in range(height):
        st.write('\n')

#no need if elses or cases. using key of the selected plant.. just write
def pred_out(img, df, model_sel):
    #image data to np array

    #img_path = f'media/{imgData.name}'
    img_ = np.asarray(img)/255.0
    #print(img_.dtype)
    #print('shape of raw image {}'.format(img_.shape))
    
    #preprocessing of image
    img_ = cv2.resize(img_, (224,224))
    img_ = np.expand_dims(img_, axis=0)
    
    #taking the prediction
    model_spec = df.iloc[df.index[df['plant']==model_sel][0]][2]
    sess = onnxruntime.InferenceSession(os.path.join('models',model_spec), None)
    input_name = sess.get_inputs()[0].name
    output_name = sess.get_outputs()[0].name
    pred = sess.run([output_name], {input_name: img_.astype(np.float32)})[0]
    return pred