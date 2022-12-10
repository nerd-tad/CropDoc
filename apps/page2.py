#import streamlit as st
from utilss import *
from apps import page1

def app(_dis_name, _dis_detail, mail_ret):
	plc = st.empty()
	with plc.container():
		#my_write('You just transitioned pages!!\n', '00ff00')
		#my_write(f'And the data you got is {passed_data}', '00ff00')
		if mail_ret == 2:
			my_write('Plant image was suspicious. Below prediction is the best match and it can be wrong!!!!!', '#ffff00')
		v_spacer(2)
		my_write(_dis_name, '#ffff00')
		v_spacer(3)
		my_write(_dis_detail, '#ffff00')
		back = st.button('Go back!!')
	if back == True:
		plc.empty()
		page1.app()