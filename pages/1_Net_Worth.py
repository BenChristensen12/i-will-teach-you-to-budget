import streamlit as st
from utils.functions import *
st.set_page_config(layout = 'wide')
for k, v in st.session_state.items():
    st.session_state[k] = v     

page = os.path.basename(__file__).split('_', 1)[1].split('.')[0]
every_page_run(page)
st.title(page.replace("_", " "))

edit_data(page)
if f"completed_{page}" in st.session_state:
    if "changed_tables" in st.session_state:
        st.write(f"Net worth: {int(st.session_state.changed_tables["assets"].Amount.sum() - st.session_state.changed_tables["debt"].Amount.sum())}")
    else:
        st.write(f"Net worth: {int(st.session_state.assets.Amount.sum() - st.session_state.debt.Amount.sum())}")