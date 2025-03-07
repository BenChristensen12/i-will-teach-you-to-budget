import streamlit as st
from utils.functions import *

st.set_page_config(layout = 'wide')
st.title("I Will Teach You to Budget")

st.write("Welcome to I Will Teach You to Budget!")
st.write("""This free-to-use tool will help you create a budget. The hardest part is remembering the logins to all your accounts.
We'll also calculate your net worth and plug-in numbers into an investment calculator to show what you could have in retirement.
Each section of the budget has percentage goals that will guide your budget decisions. These are based on Ramit Sethi's book
*I Will Teach You to Be Rich*, so consider checking out his book if you like this tool.""")
st.markdown("""This budget consists of 5 sections: 1. Net Worth 2. Fixed Costs 3. Savings Goals 4. Investments 5. Guilt-Free Spending.
         To build the budget we've separated each of these sections into pages on the sidebar. When you're finished, guilt-free spending
         is calculated as whatever money is leftover.""")

st.header("Progress:")
completed_tasks = [x in st.session_state for x in ["completed_net_worth", "completed_fixed_costs", "completed_savings", "completed_investments"]]
tasks = ["Net Worth", "Fixed Costs", "Savings Goals", "Investments"]
for i, task_completion in enumerate(completed_tasks):
    st.checkbox(tasks[i], value = task_completion, disabled = True)

if "dashboard_initialized" not in st.session_state:
    initialize_dashboard()
