import streamlit as st
from utils.functions import *

st.set_page_config(layout = 'wide')
st.title("Net Worth")

st.header("Assets")
st.write("""First, we'll start with your assets. You can create new rows in this table. You'll see the first row is filled with an example asset.
Using the example of a car, the asset amount is the full current value of the asset before subtracting debt. We'll list debts in the next table
if you still owe money on the car. Replace this first row with one of your actual assets.""")
if "assets" in st.session_state:
    df = st.session_state.assets.copy()
    st.data_editor(df, num_rows = 'dynamic', key = 'assets')
else:
    df = pd.DataFrame({"Asset": ["Honda Accord"], "Amount": [3950]})
    st.data_editor(df, num_rows = 'dynamic', key = "assets")

st.header("Debt")
st.write("""Now enter your debts. Take the time to login to all your accounts, it'll be worth it. I promise. 
When was the last time you calculated your actual net worth? Replace the first row with your actual debt. You can add additional rows.""")        


if "debts" in st.session_state:
    df = st.session_state.debts.copy()
    st.data_editor(df, num_rows = 'dynamic', key = "debts")
else:
    df = pd.DataFrame({"Debt": ["Honda Accord"], "Amount": [600]})
    st.data_editor(df, num_rows = 'dynamic', key = "debts")


if "completed_net_worth" not in st.session_state:
    st.button("Submit", on_click = submit_page("completed_net_worth"))