import streamlit as st
from utils.functions import *

st.set_page_config(layout = 'wide')

if "initialized" not in st.session_state:
    initialize_dashboard()

if "submitted_income" not in st.session_state:
    enter_income()

if "submitted_fixed_costs" not in st.session_state:
    enter_fixed_costs()

if "submitted_investments" not in st.session_state:
    enter_investments()

if "submitted_savings" not in st.session_state:
    enter_savings()