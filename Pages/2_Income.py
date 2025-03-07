import streamlit as st
from utils.functions import *

st.set_page_config(layout = 'wide')
st.title("Income")

st.header("Monthly Income")
st.write("""This is the first table that is a recurring amount instead of fixed. Enter the *monthly* amount of take-home income. If you receive income
weekly, a good estimate is to multiply that number by 52 then divide by 12. The formula is (paycheck amount) x (number of paychecks in a year) / 12
Do this for each of your income streams. If you have variable income, use the smallest amount you think you'd receive. We'll deal with excess income later.""")


if "income" in st.session_state:
    df = st.session_state.income.copy()
    edited_income = st.data_editor(df, num_rows = 'dynamic')
else:
    df = pd.DataFrame({"Source": ["Day Job"], "Amount": [0]})
    edited_income = st.data_editor(df, num_rows = 'dynamic')

def submit_changes():
    st.session_state["completed_income"] = True
    st.session_state["income"] = edited_income.copy()

if "completed_income" not in st.session_state:
    st.button("Submit", on_click = submit_changes)
else:
    st.button("Submit Changes", on_click = submit_changes)