import streamlit as st
import pandas as pd
import json
import os

def initialize_dashboard():
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    st.title("I Will Teach You to Budget")
    st.write("Welcome to I Will Teach You to Budget!")
    st.write("This free-to-use tool will prompt you for recurring expenses and guide you through creating a budget. It will also simulate how much you will have in retirement. The model is based on Ramit Sethi's conscious spending plan layed out in his book I Will Teach You to Be Rich, so consider checking out his book if you like this tool.")
    st.session_state["initialized"] = True
    st.session_state["config"] = json.load(open(repo_dir + "/utils/config.json"))
    st.button("Get Started!")   

def submit_income():
    st.session_state["submitted_income"] = True

def enter_income():
    st.number_input("Enter your net monthly income (add up all paychecks in a given month)", key = "income")    

def submit_fixed_costs():
    st.session_state["submitted_fixed_costs"] = True
    # st.session_state["total_cost"] = 

def enter_fixed_costs():
    st.write("First let's record your monthly recurring costs (aka \"fixed\"). If you have an annual cost, hold that for the savings section.")
    st.session_state["fixed_costs"] = st.data_editor(pd.DataFrame({"Fixed Cost": [], "Amount": [], "Category": []}), num_rows = 'dynamic')
    st.write("Recommended categories: [Housing, Charity, Shopping, Debt, Car, Health, Entertainment]")  
    st.button("Submit", on_click = "submit_fixed_costs")  

def submit_investments():
    st.session_state["submitted_investments"] = True
    st.session_state["total_cost"] += st.investments.Amount.sum()

def enter_investments():
    st.write("Now record your monthly contribution to your retirement account(s). Include your employer's contribution if you have one")
    st.session_state["investments"] = st.data_editor(pd.DataFrame({"Investment": [], "Amount": []}), num_rows = 'dynamic')
    st.button("Submit", on_click = "submit_investments")      

def submit_savings():
    st.session_state["submitted_savings"] = True
    st.session_state["total_cost"] += st.savings.Amount.sum()

def enter_savings():
    st.write("Pick a few savings goals you'd like to contribute to every month. A few common ones are for a vacation or emergency fund.")
    st.session_state["savings"] = st.data_editor(pd.DataFrame({"Savings": [], "Amount": []}), num_rows = 'dynamic')
    st.button("Submit", on_click = "submit_savings")  