import streamlit as st
from utils.functions import *

for k, v in st.session_state.items():
    st.session_state[k] = v     
page = os.path.basename(__file__).split('_', 1)[1].split('.')[0]
every_page_run(page)
st.title(page.replace("_", " "))

edit_data(page)
