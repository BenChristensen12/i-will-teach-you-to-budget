import streamlit as st
from utils.functions import *

st.set_page_config(layout = 'wide')
st.title("I Will Teach You to Budget")

if "step" not in st.session_state:
    initialize_dashboard()

elif st.session_state.step < len(st.session_state.entry_order):
    table_name = st.session_state.entry_order[st.session_state.step]
    df = generate_table(table_name)
    st.session_state[table_name] = st.data_editor(df, num_rows = 'dynamic')
    st.button("Submit", on_click = increment_step)

else:
    pass