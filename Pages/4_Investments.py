import streamlit as st
from utils.functions import *

st.set_page_config(layout = 'wide')
st.title("Investments")



st.header("Monthly Investment Contributions")
st.write("""Here is where wealth is created. Did you know money invested today doubles roughly every 10 years? How much can you afford to invest every month? 
Use the % goal as a guide. If you don't have enough remaining, we'll go back to the other steps to see what you can cut. """)
df = pd.DataFrame({"Investment": ["Employer Contribution 401k", "Roth IRA"], "Amount": [0, 0]})