import streamlit as st
from utils.functions import *

page = os.path.basename(__file__).split('_', 1)[1].split('.')[0]
st.title(page.replace("_", " "))

edit_data(page)
