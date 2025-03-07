import streamlit as st
from utils.functions import *

st.set_page_config(layout = 'wide')
st.title("Income")

st.header("Monthly Income")
st.write("""This is the first table that is a recurring amount instead of fixed. Enter the *monthly* amount of take-home income. If you receive income
weekly, a good estimate is to multiply that number by 52 then divide by 12. The formula is (paycheck amount) x (number of paychecks in a year) / 12
Do this for each of your income streams. If you have variable income, use the smallest amount you think you'd receive. We'll deal with excess income later.""")
df = pd.DataFrame({"Source": ["Day Job"], "Amount": [0]})