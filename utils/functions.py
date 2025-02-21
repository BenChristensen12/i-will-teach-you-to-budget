import streamlit as st
import pandas as pd
import json
import os

def initialize_dashboard():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    st.write("Welcome to I Will Teach You to Budget!")
    st.write("""This free-to-use tool will help you create a budget. The hardest part is remembering the logins to all your accounts.
    We'll also calculate your net worth and plug-in numbers into an investment calculator to show what you could have in retirement.
    Each section of the budget has percentage goals that will guide your budget decisions. These are based on Ramit Sethi's book
    *I Will Teach You to Be Rich*, so consider checking out his book if you like this tool.""")
    st.session_state["step"] = 0
    st.session_state["config"] = json.load(open(repo_dir + "/utils/config.json"))
    st.session_state["entry_order"] = st.session_state.config["dashboard"]["entry_order"]
    st.session_state["table_edited"] = False
    st.button("Get Started!")  

def increment_step():
    st.session_state.step += 1

def table_edited():
    st.session_state["table_edited"] = True

def generate_table(table_name):
    if table_name == "assets":
        st.header("Assets")
        st.write("""First, we'll start with your assets. You can create new rows in this table. You'll see the first row is filled with an example asset.
        Using the example of a car, the asset amount is the full current value of the asset before subtracting debt. We'll list debts in the next table
        if you still owe money on the car. Replace this first row with one of your actual assets.""")
        df = pd.DataFrame({"Asset": ["Honda Accord"], "Amount": [3950]})
    elif table_name == "debt": 
        st.header("Debt")
        st.write("""Now enter your debts. Take the time to login to all your accounts, it'll be worth it. I promise. 
        When was the last time you calculated your actual net worth? Replace the first row with your actual debt. You can add additional rows.""")        
        df = pd.DataFrame({"Debt": ["Honda Accord"], "Amount": [600]})
    elif table_name == "income":
        st.header("Monthly Income")
        st.write("""This is the first table that is a recurring amount instead of fixed. Enter the *monthly* amount of take-home income. If you receive income
        weekly, a good estimate is to multiply that number by 52 then divide by 12. The formula is (paycheck amount) x (number of paychecks in a year) / 12
        Do this for each of your income streams. If you have variable income, use the smallest amount you think you'd receive. We'll deal with excess income later.""")
        df = pd.DataFrame({"Source": ["Day Job"], "Amount": [0]})
    elif table_name == "fixed_costs":
        st.header("Monthly Fixed Costs")
        st.write("""Here's the largest table to fill, then we get to the fun part. List all of your recurring expenses, including gym memgerships, subscriptions, etc. 
        Again, these are monthly expenses. DO NOT spend too much time here though. Many recurring expenses are fixed but some are variable. 
        You may need to look at your credit card statements or receipts to estimate how much you spend on these on average, but an approximate is 
        good enough here. This is a budget so it's *forward-looking*. You're deciding how much you'd like to spend on these moving forward. 
        In some sense, what you spent in the past is irrelevant apart from informing how realistic your goal is.\n\nCategories are optional, 
        but make for fun pie charts later on. You can pick your own categories if you like.""")        
        df = pd.DataFrame({"Fixed Cost": ["Rent", "Car Payment", "Utilities"], "Amount": [100, 50, 10], "Category": ["Housing", "Debt", "Housing"]})
    elif table_name == "savings_goals":
        st.header("Monthly Savings Goals")
        st.write("""This is a reward for all your hard work. Now, given your previous responses, we know how much you have left to save for goals that are 
        6-months out or further. A common goal is an emergency fund - advice ranges from 3-6 months of monthly expenses. But, don't stop there. This is where 
        you can really build out your rich life. This could be saving for a vacation, Christmas gifts, a down payment. Take your time on this step.""")          
        df = pd.DataFrame({"Goal": ["Emergency Fund", "Vacation"], "Amount": [100, 20]})
    elif table_name == "investments":
        st.header("Monthly Investment Contributions")
        st.write("""Here is where wealth is created. Did you know money invested today doubles roughly every 10 years? How much can you afford to invest every month? 
        Use the % goal as a guide. If you don't have enough remaining, we'll go back to the other steps to see what you can cut. """)
        df = pd.DataFrame({"Investment": ["Employer Contribution 401k", "Roth IRA"], "Amount": [0, 0]})

    return df


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