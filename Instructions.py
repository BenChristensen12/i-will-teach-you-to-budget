import streamlit as st
from utils.functions import *

st.set_page_config(layout = 'wide')
if "dashboard_initialized" not in st.session_state:
    initialize_dashboard()    
st.title("I Will Teach You to Budget")
if st.session_state.uploaded_file_name is not None:
    st.success("Previous Session Restored!")
st.write("Welcome to I Will Teach You to Budget!")
st.write("""This free-to-use tool will help you create a budget. The hardest part is remembering the logins to all your accounts.
We'll also calculate your net worth and plug-in numbers into an investment calculator to show what you could have in retirement.
Each section of the budget has percentage goals that will guide your budget decisions. These are based on Ramit Sethi's book
*I Will Teach You to Be Rich*, so consider checking out his book if you like this tool.""")
st.markdown("""This budget consists of 5 sections: 1. Net Worth 2. Fixed Costs 3. Savings Goals 4. Investments 5. Guilt-Free Spending.
         To build the budget we've separated each of these sections into pages on the sidebar. When you're finished, guilt-free spending
         is calculated as whatever money is leftover.""")



show_progress()

uploaded_file = st.file_uploader("Upload Previously Completed Budget", type='pkl')
if uploaded_file is not None:
    if uploaded_file.name != st.session_state.uploaded_file_name:  
        loaded_state = pickle.loads(uploaded_file.read())
        for k, v in loaded_state.items():
            st.session_state[k] = v
        
        st.session_state.uploaded_file_name = uploaded_file.name
        st.rerun()