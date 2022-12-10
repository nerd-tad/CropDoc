import streamlit as st
from utilss import *
import pandas as pd
import base64
from apps import page1
from apps import page2

@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_img_as_page_bg(img_file, img_format):
    bin_str = get_base64_of_bin_file(img_file)
    page_bg_img = '''
    <div class='bg_img'>
    <style>
    .stApp {
    background-image: url("data:image/{img_format};base64,%s");
    background-size: contain;
    background-repeat: repeat-y;
    background-position: center;
    }
    </style>
    </div>
    ''' % bin_str  #contain and cover are options for bgsize, repeat-x and repeat-y and no-repeat are options for bgrepeat
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return 0
set_img_as_page_bg('media/bg-xxx.png', 'png')

dataFrame = pd.read_csv('pdi_localdb_new.csv')
#st.write(dataFrame.iloc[2])
#st.write(dataFrame.loc[dataFrame['plant']=='tomato'])
#st.write(dataFrame.index[dataFrame['plant']=='potato'].tolist())
#print(dataFrame.index[dataFrame['plant']=='potato'][0])

#st.header('Plant disease identifier WebApp')
my_header('Plant Disease Identifier WebApp')
#my_write('fuck', '00ff00')
#st.write('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')  #this doesn't work.... cannot make much of a seperation like this
v_spacer(4)

page1.app(page2,dataFrame)
#loading pandas dataframe
#df = pd.DataFrame()




