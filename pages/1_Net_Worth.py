import streamlit as st
from utils.functions import *
st.set_page_config(layout = 'wide')
for k, v in st.session_state.items():
    st.session_state[k] = v     

page = os.path.basename(__file__).split('_', 1)[1].split('.')[0]
st.title(page.replace("_", " "))

edit_data(page)