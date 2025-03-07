import streamlit as st
from utils.functions import *

st.set_page_config(layout = 'wide')
st.title("Fixed Costs")

st.header("Monthly Fixed Costs")
st.write("""Here's the largest table to fill, then we get to the fun part. List all of your recurring expenses, including gym memgerships, subscriptions, etc. 
Again, these are monthly expenses. DO NOT spend too much time here though. Many recurring expenses are fixed but some are variable. 
You may need to look at your credit card statements or receipts to estimate how much you spend on these on average, but an approximate is 
good enough here. This is a budget so it's *forward-looking*. You're deciding how much you'd like to spend on these moving forward. 
In some sense, what you spent in the past is irrelevant apart from informing how realistic your goal is.\n\nCategories are optional, 
but make for fun pie charts later on. You can pick your own categories if you like.""")        

if "fixed_costs" in st.session_state:
    df = st.session_state.income.copy()
    edited_fixed_costs = st.data_editor(df, num_rows = 'dynamic')
else:
    df = pd.DataFrame({"Fixed Cost": ["Rent", "Car Payment", "Utilities"], "Amount": [100, 50, 10], "Category": ["Housing", "Debt", "Housing"]})
    edited_fixed_costs = st.data_editor(df, num_rows = 'dynamic')

def submit_changes():
    st.session_state["completed_fixed_costs"] = True
    st.session_state["fixed_costs"] = edited_fixed_costs.copy()
    st.write("Changes submitted!")

if "completed_fixed_costs" not in st.session_state:
    st.button("Submit", on_click = submit_changes)
else:
    st.button("Submit Changes", on_click = submit_changes)