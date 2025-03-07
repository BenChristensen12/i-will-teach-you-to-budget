import streamlit as st
from utils.functions import *

st.set_page_config(layout = 'wide')
st.title("Savings Goals")



st.header("Monthly Savings Goals")
st.write("""This is a reward for all your hard work. Now, given your previous responses, we know how much you have left to save for goals that are 
6-months out or further. A common goal is an emergency fund - advice ranges from 3-6 months of monthly expenses. But, don't stop there. This is where 
you can really build out your rich life. This could be saving for a vacation, Christmas gifts, a down payment. Take your time on this step.""")          
df = pd.DataFrame({"Goal": ["Emergency Fund", "Vacation"], "Amount": [100, 20]})