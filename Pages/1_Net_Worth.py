import streamlit as st
from utils.functions import *
st.set_page_config(layout = 'wide')

page = os.path.basename(__file__).split('_', 1)[1].split('.')[0]
st.title(page.replace("_", " "))

st.header("Assets")
st.write("""First, we'll start with your assets. You can create new rows in this table. You'll see the first row is filled with an example asset.
Using the example of a car, the asset amount is the full current value of the asset before subtracting debt. We'll list debts in the next table
if you still owe money on the car. Replace this first row with one of your actual assets.""")


st.header("Debts")
st.write("""Now enter your debts. Take the time to login to all your accounts, it'll be worth it. I promise. 
When was the last time you calculated your actual net worth? Replace the first row with your actual debt. You can add additional rows.""")        

edit_data(page)