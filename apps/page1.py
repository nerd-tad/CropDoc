#predic details page
from utilss import *
import streamlit as st
import time
from PIL import Image

def app(next_page, df):
	plc = st.empty()
	with plc.container():
		img_data = st.file_uploader(label='Load image for recognition', type=['png', 'jpg']) #here you upload ur images
		if img_data is not None:
			img = Image.open(img_data)
			target_height = 300
			# target_height * original_width / original_height
			new_width = int(target_height * img.size[0] / float(img.size[1]))
			img_res = img.resize((new_width, target_height), Image.ANTIALIAS)
			col1, col2, col3 = st.columns(3)
			with col1:
				st.write('')
			with col2:
				col2=st.image(img_res)
			with col3:
				col3=st.write('')

		

		#radio buttons for selecting the model
		plant_list = df['plant']
		model_selector = st.radio('Pick the Plant', plant_list)
		#print(model_selector)
		v_spacer(2)

		my_write('User Data', '00a0ff')
		v_spacer(1)
		user_s_name = st.text_input(label='Your Name')
		user_s_num = st.text_input(label='Your Number')

		conf = False
		conf_email = False
		if img_data is not None:
		    conf = st.button('Predict')
		    conf_email = st.button('Predict and Send Data As Email')

	if conf == True:
		plc1 = st.empty()
		diseases_details = df.iloc[df.index[df['plant']==model_selector][0]][1]
		#st.write(diseases_details)

		#running the neural network
		prediction = pred_out(img, df, model_selector)
		#RUN ANOTHER PREDICTION TO IDENTIFY IS IT A LEAF OR NOT! a liitle misleading.....................................


		max_ind = np.where(prediction[0]==np.max(prediction))   #prediction.argmax(axis=0)  will also do the thing
		print(f'max_val:{np.max(prediction)}')
		print(prediction)
		disease_name, disease_detail = fn1(max_ind[0][0], diseases_details)
		user_data_dic = {'name':user_s_name, 'tel':user_s_num}##################################################################################################################################################
		plant_data_dic = {'plant':model_selector, 'disease':disease_name}

		#save in database
		db_ret = save_to_fb(img, user_data_dic, plant_data_dic)
		ph_db = st.empty()
		if db_ret == 0:
			#pop up msg, saved data to database successfully!
			with ph_db.container():
				st.success('Saved data to database successfully!!')
				if st.button('Close'):
					ph_db.empty()
		else:
			#popup: data couldn't be saved in database due to connectivity issues.
			with ph_db.container():
				st.warning("Data couldn't be saved in database due to connectivity issues.")
				if st.button('Close'):
					ph_db.empty() #nope, if button==1,pressed app goes to the first page. A bug....

		#sending email if needed
		email_ret = send_email(img, np.max(prediction), user_data_dic, plant_data_dic)
		if email_ret == 0:
			#popup: Image seems suspicious, It can be a new disease, sent an email to authority.
			st.warning('Image seems suspicious, It can be a new disease, sent an email to authority!')
			if st.button('Noted'):
				pass
			elif email_ret == 1:
				pass
			else:
            #pop up: Image seems suspicious, couldn't send mail due to connectivity issues.
				st.warning('Image seems suspicious, It can be a new disease, sent an email to authority!')
				if st.button('Noted'):
					pass


		with plc1.container():
			'''for i in range(101):
				st.progress(i)
				time.sleep(0.2)'''
			with st.spinner('Please wait...'):
				for i in range(10):
					time.sleep(0.1)

			plc1.empty()  #just making it fancy, for buffering..
		#transit to page2
		plc.empty()
		next_page.app(disease_name,disease_detail,email_ret)

	if conf_email == True:
		plc1 = st.empty()
		diseases_details = df.iloc[df.index[df['plant']==model_selector][0]][1]
		#st.write(diseases_details)

		#running the neural network
		prediction = pred_out(img, df, model_selector)
		#RUN ANOTHER PREDICTION TO IDENTIFY IS IT A LEAF OR NOT! a liitle misleading.....................................


		max_ind = np.where(prediction[0]==np.max(prediction))   #prediction.argmax(axis=0)  will also do the thing
		print(f'max_val:{np.max(prediction)}')
		print(prediction)
		disease_name, disease_detail = fn1(max_ind[0][0], diseases_details)
		user_data_dic = {'name':user_s_name, 'tel':user_s_num}##################################################################################################################################################
		plant_data_dic = {'plant':model_selector, 'disease':disease_name}

		#save in database
		db_ret = save_to_fb(img, user_data_dic, plant_data_dic)
		ph_db = st.empty()
		if db_ret == 0:
			#pop up msg, saved data to database successfully!
			with ph_db.container():
				st.success('Saved data to database successfully!!')
				if st.button('Close'):
					ph_db.empty()
		else:
			#popup: data couldn't be saved in database due to connectivity issues.
			with ph_db.container():
				st.warning("Data couldn't be saved in database due to connectivity issues.")
				if st.button('Close'):
					ph_db.empty() #nope, if button==1,pressed app goes to the first page. A bug....

		#sending email if needed pseudo
		email_ret = send_email_pseudo(img, user_data_dic, plant_data_dic)
		if email_ret == 0:
			#popup: Image seems suspicious, It can be a new disease, sent an email to authority.
			st.warning('Image seems suspicious, It can be a new disease, sent an email to authority!')
			if st.button('Noted'):
				pass

		else:
        #pop up: Image seems suspicious, couldn't send mail due to connectivity issues.
			st.warning('Image seems suspicious, It can be a new disease, sent an email to authority!')
			if st.button('Noted'):
				pass


		with plc1.container():
			'''for i in range(101):
				st.progress(i)
				time.sleep(0.2)'''
			with st.spinner('Please wait...'):
				for i in range(10):
					time.sleep(0.1)

			plc1.empty()  #just making it fancy, for buffering..
		#transit to page2
		plc.empty()
		next_page.app(disease_name,disease_detail,email_ret)