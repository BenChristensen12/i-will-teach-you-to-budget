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
    total_income = st.session_state.income.Amount.sum()
    for table_name in st.session_state.entry_order:
        st.header(st.session_state.config["dashboard"]["headers"][table_name])
        if table_name == "income":
            st.session_state[table_name]["Percent"] = 100*st.session_state[table_name].Amount / total_income
            edited_df = st.data_editor(st.session_state[table_name], num_rows = 'dynamic', disabled = ["Percent"], on_change = table_edited)
        elif table_name in ["assets", "debt"]:
            edited_df = st.data_editor(st.session_state[table_name], num_rows = 'dynamic')
        else:
            st.session_state[table_name]["Percent"] = 100*st.session_state[table_name].Amount / total_income
            edited_df = st.data_editor(st.session_state[table_name], num_rows = 'dynamic', disabled = ["Percent"])

        if st.session_state.table_edited:
            st.session_state[table_name] = edited_df
            st.session_state.table_edited = False
            st.rerun()