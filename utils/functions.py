import streamlit as st
import pandas as pd
import json
import os
from matplotlib import pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import darkdetect
import pickle
from datetime import datetime

def initialize_dashboard():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    st.session_state["config"] = json.load(open(repo_dir + "/utils/config.json"))
    st.session_state["uploaded_file_name"] = None
    st.session_state["dashboard_initialized"] = True

def update_percentages():
    for page in st.session_state.config["Pages"].keys():
        if page != "Net_Worth":
            for table in st.session_state.config["Pages"][page]["tables"].keys():
                temp_df = st.session_state[table]
                temp_df["Percent"] = temp_df.Amount / st.session_state.net_income
                temp_df["Percent"] = temp_df["Percent"].apply(lambda x: f"{int(x*100)}%") 
                temp_df.sort_values("Amount", ascending = False, inplace = True)
                st.session_state[table] = temp_df    

def compile_budget():
    df = pd.DataFrame({"Category": [], "Amount": []})
    for table in ["fixed_costs", "savings_goals", "investments"]:
        table_df = st.session_state[table]
        summed_df = pd.DataFrame({"Category": [st.session_state.config["Headers"][table]], "Amount": [table_df.Amount.sum()]})
        df = pd.concat([df, summed_df])

    st.session_state["net_income"] = st.session_state.income.Amount.sum()
    st.session_state["guilt_free"] = st.session_state.net_income - df.Amount.sum()
    df.loc[len(df)] = {"Category": "Guilt-Free", "Amount": st.session_state.guilt_free}
    df.loc[len(df)] = {"Category": "Net Income", "Amount": st.session_state.net_income}

    df["Percent"] = (df.Amount / st.session_state.net_income)
    # Display data
    df["Percent"] = df["Percent"].apply(lambda x: f"{int(x*100)}%")
    df["Goal"] = ["60%-", "10%+", "10%+", "20%+", ""]
    df.Amount = df.Amount.astype(int).astype(str)
    df = pd.concat([df.iloc[:-1], pd.DataFrame([{col: "" for col in df.columns}]), df.iloc[-1:]], ignore_index = True)
    st.session_state["budget_data"] = df.copy()
    df = df.iloc[:-2].copy()
    df.Amount = df.Amount.astype(int)
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
    labels += fixed_costs["Fixed Cost"].tolist()
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

def button_click(click_phrase):
    st.session_state[click_phrase] = True

def progress_bar(page):
    df = st.session_state.budget_data.copy()
    df = df.loc[df.Category == page.replace("_", " "), ["Amount", "Percent", "Goal"]].copy() 
    goal, goal_type =  list(st.session_state.config["Pages"][page]["goal"].items())[0]
    goal = float(goal)
    value = float(df.Amount.values[0])
    target = int(goal*st.session_state.net_income)
    title = "Progress"
    delta = abs(int(target-value))
    if goal_type == "floor":
        target_word = "Target Min"
        
        if value >= target:
            bar_color = "#047c6c"
            rec = f"You have improved upon the target by ${delta}."
        else:
            bar_color = "#c4442c"
            rec = f"You are ${delta} short of the target."
    elif goal_type == "ceiling":
        target_word = "Target Max"
        if value <= target:
            bar_color = "#047c6c"
            rec = f"You have improved upon the target by ${delta}."
        else:
            bar_color = "#c4442c"
            rec = f"You have overspent the target by ${delta}."
        
    
    # Create the horizontal bar
    fig = go.Figure()
    
    # Add the bar with increased width and better text formatting
    fig.add_trace(
        go.Bar(
            x=[value],
            y=[title],
            orientation='h',
            marker_color=bar_color,
            text=[f"{value:.0f}"],  # Format with 1 decimal place
            textposition='auto',  # Ensure text stays inside bar
            textfont=dict(
                size=14,  # Larger text
                color="white"
            ),
            width=10  # Increased bar width (was 0.4)
        )
    )
    
    # Add vertical target line
    target_color = "white" if darkdetect.isDark() else "black"
    fig.add_shape(
        type="line",
        x0=target,
        y0=-5,
        x1=target,
        y1=5,
        line=dict(
            color=target_color,
            width=4,
            dash="solid"
        )
    )
    
    fig.add_annotation(
        x = target,
        y=6,
        text=f"{target_word}: {target}",
        showarrow=True,
        arrowcolor=target_color,
        font=dict(
            size=14,
            color=target_color),
        align='right',
        xanchor='right'
        )

    # Update layout for transparent background and size
    fig.update_layout(
        width=600,
        height=300,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot background
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper background
        xaxis=dict(
            range=[0, max(value, target)*1.006],  # Add some padding to the right
            showgrid=False
        ),
        yaxis=dict(
            showgrid=False,
            showticklabels=False
        )
    )
    
    st.write(rec)
    # Display in Streamlit
    st.plotly_chart(fig)

def end_demo():
    del st.session_state["completed_all_tasks"]
    for page in st.session_state.config["Pages"].keys():
        del st.session_state[f"completed_{page}"]
        tables = st.session_state.config["Pages"][page]["tables"].keys()
        for table in tables:
            del st.session_state[table]
    del st.session_state.in_demo

def run_demo():
    st.session_state["in_demo"] = True
    for page in st.session_state.config["Pages"].keys():
        st.session_state[f"completed_{page}"] = True
        tables = st.session_state.config["Pages"][page]["tables"].keys()
        for table in tables:
            rows = st.session_state.config["Pages"][page]["tables"][table]["rows"]            
            columns = st.session_state.config["Pages"][page]["tables"][table]["columns"]            
            df = pd.DataFrame(rows, columns = columns)
            st.session_state[table] = df.copy()

def edit_data(page):
    if "clicked_submit" in st.session_state:
        del st.session_state.clicked_submit
        st.session_state[f"completed_{page}"] = True
        st.session_state.update(st.session_state.changed_tables)
        if "completed_all_tasks" in st.session_state:
            compile_budget()
            update_percentages()        

    st.session_state["changed_tables"] = dict()
    tables = st.session_state.config["Pages"][page]["tables"].keys()
    for table in tables:
        if page == "Net_Worth":
            st.header(st.session_state.config["Headers"][table])
        st.write(st.session_state.config["Pages"][page]["tables"][table]["preamble"])
        if table in st.session_state:
            df = st.session_state[table].copy()
            df.reset_index(drop = True, inplace = True)
            edited_df = st.data_editor(df, num_rows = 'dynamic', disabled = ["Percent"], hide_index = True)
        else:
            columns = st.session_state.config["Pages"][page]["tables"][table]["columns"]            
            df = pd.DataFrame(columns = columns)
            edited_df = st.data_editor(df, num_rows = 'dynamic', disabled = ["Percent"], hide_index = True)
        
        st.session_state.changed_tables[table] = edited_df.dropna(subset=[col for col in df.columns if col != "Percent"])
    if f"completed_{page}" not in st.session_state:
        st.button("Submit", on_click = button_click, args=("clicked_submit",))
    else:
        st.button("Submit Changes", on_click = button_click, args=("clicked_submit",))
    if ("completed_all_tasks" in st.session_state) & (page not in ["Net_Worth", "Income"]):
        sum_df = st.session_state.budget_data.copy()
        page_name = page.replace("_", " ")
        sum_df = sum_df.loc[sum_df.Category == page_name, ["Amount", "Percent", "Goal"]].copy()
        sum_df.rename(columns = {"Amount": page_name}, inplace = True)
        progress_bar(page)        
       