import streamlit as st
import pandas as pd
import json
import os
from matplotlib import pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def initialize_dashboard():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    st.session_state["config"] = json.load(open(repo_dir + "/utils/config.json"))
    st.session_state["dashboard_initialized"] = True

def update_percentages():
    for page in st.session_state.config["Pages"].keys():
        for table in st.session_state.config["Pages"][page]["tables"].keys():
            temp_df = st.session_state[table]
            temp_df["Percent"] = temp_df.Amount / st.session_state.net_income
            temp_df["Percent"] = temp_df["Percent"].apply(lambda x: f"{int(x*100)}%") 
            temp_df.sort_values("Percent", ascending = False, inplace = True)
            st.session_state[table] = temp_df    

def compile_budget():
    df = pd.DataFrame({"Category": [], "Amount": []})
    for table in ["fixed_costs", "savings_goals", "investments"]:
        table_df = st.session_state[table]
        summed_df = pd.DataFrame({"Category": [st.session_state.config["Headers"][table]], "Amount": [table_df.Amount.sum()]})
        df = pd.concat([df, summed_df])

    st.session_state["net_income"] = st.session_state.income.Amount.sum()

    gf = pd.DataFrame({"Category": ["Guilt-Free"], "Amount": [st.session_state.net_income - df.Amount.sum()]})
    df = pd.concat([df, gf])
    df["Percent"] = (df.Amount / st.session_state.net_income)
    # Display data
    df["Percent"] = df["Percent"].apply(lambda x: f"{int(x*100)}%")
    df["Goal"] = ["60%-", "10%+", "10%+", "20%+"]
    st.session_state["budget_data"] = df.copy()
       
    #chart showing breakout of budget
    labels = ["Net Income", "Fixed Costs", "Savings Goals", "Investments", "Guilt-Free"]
    parents = ["", "Net Income", "Net Income", "Net Income", "Net Income"]    
    values = [int(st.session_state.net_income), df.loc[df.Category == "Fixed Costs", "Amount"].values[0], df.loc[df.Category == "Savings Goals", "Amount"].values[0],df.loc[df.Category == "Investments", "Amount"].values[0], df.loc[df.Category == "Guilt-Free", "Amount"].values[0]]

    savings_goals = st.session_state["savings_goals"].copy()
    goals = savings_goals.Goal.tolist()
    labels += goals
    parents += ["Savings Goals" for goal in goals]
    values += savings_goals.Amount.tolist()

    investments = st.session_state["investments"].copy()
    eaches = investments.Investment.tolist()
    labels += eaches
    parents += ["Investments" for each in eaches]
    values += investments.Amount.tolist()

    fixed_costs = st.session_state["fixed_costs"].copy()
    grouped_df = fixed_costs.groupby("Category", as_index = False).Amount.sum()
    categories = grouped_df.Category.tolist()
    labels += categories
    parents += ["Fixed Costs" for category in categories]
    values += grouped_df.Amount.tolist()
    labels += fixed_costs.Fixed_Cost.tolist()
    parents += fixed_costs.Category.tolist()
    values += fixed_costs.Amount.tolist()
    st.session_state["sunburst_data"] = [labels, parents, values]

def show_progress():
    st.header("Progress:")
    completed_tasks = [x in st.session_state for x in ["completed_Net_Worth", "completed_Income", "completed_Fixed_Costs", "completed_Savings_Goals", "completed_Investments"]]
    tasks = ["Net Worth", "Income", "Fixed Costs", "Savings Goals", "Investments"]
    for i, task_completion in enumerate(completed_tasks):
        st.checkbox(tasks[i], value = task_completion, disabled = True)
    if all(completed_tasks):
        st.session_state["completed_all_tasks"] = True

def submit_changes():
    st.session_state["clicked"] = True

def edit_data(page):
    if "clicked" in st.session_state:
        del st.session_state.clicked
        st.session_state[f"completed_{page}"] = True
        st.session_state.update(st.session_state.changed_tables)
        if "completed_all_tasks" in st.session_state:
            compile_budget()
            update_percentages()        

    st.session_state["changed_tables"] = dict()
    tables = st.session_state.config["Pages"][page]["tables"].keys()
    for table in tables:
        if len(tables) > 1:
            st.header(st.session_state.config["Headers"][table])
        st.write(st.session_state.config["Pages"][page]["tables"][table]["preamble"])
        if table in st.session_state:
            df = st.session_state[table].copy()
            df.reset_index(drop = True, inplace = True)
            edited_df = st.data_editor(df, num_rows = 'dynamic', disabled = ["Percent"], hide_index = True)
        else:
            rows = st.session_state.config["Pages"][page]["tables"][table]["rows"]
            columns = st.session_state.config["Pages"][page]["tables"][table]["columns"]            
            df = pd.DataFrame(rows, columns = columns)
            edited_df = st.data_editor(df, num_rows = 'dynamic', disabled = ["Percent"], hide_index = True)
        st.session_state.changed_tables[table] = edited_df
    if f"completed_{page}" not in st.session_state:
        button = st.button("Submit", on_click = submit_changes)
    else:
        button = st.button("Submit Changes", on_click = submit_changes)