import streamlit as st
import pandas as pd
import json
import os
from matplotlib import pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from streamlit_javascript import st_javascript
import pickle
from datetime import datetime
import time

def initialize_dashboard():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    st.session_state["config"] = json.load(open(repo_dir + "/utils/config.json"))
    st.session_state["uploaded_file_name"] = None
    st.session_state["dashboard_initialized"] = True
    theme_js = """
    document.body.getAttribute('data-theme');
    """    
    st.session_state["theme"] = st_javascript(theme_js)
    st.session_state["previous_page"] = None

def every_page_run(page):
    if st.session_state.previous_page != page:
        st.session_state.previous_page = page
        if "changed_tables" in st.session_state:
            st.session_state.update(st.session_state.changed_tables)
            del st.session_state.changed_tables
            if "completed_all_tasks" in st.session_state:
                compile_budget()
                update_percentages()  
        

def calculate_portfolio(principal, monthly_contribution, annual_return, years):
    monthly_rate = annual_return / 12
    portfolio_values = []

    months = int(12*years)
    for month in range(months + 1):
        if month == 0:
            total_value = principal
        else:
            total_value = total_value * (1 + monthly_rate) + monthly_contribution
        portfolio_values.append(total_value)

    return portfolio_values

def calculate_needed_contribution(portfolio_needed, principal, rate, years):
    months = int(12*years)
    monthly_rate = rate / 12
    return (portfolio_needed - principal * (1 + monthly_rate) ** months) / (((1 + monthly_rate) ** months - 1) / monthly_rate)


def update_percentages():
    for page in st.session_state.config["Pages"].keys():
        if page != "Net_Worth":
            for table in st.session_state.config["Pages"][page]["tables"].keys():
                temp_df = st.session_state[table]
                temp_df["Percent"] = temp_df.Amount / st.session_state.net_income
                temp_df["Percent"] = temp_df.loc[~temp_df.Percent.isna(), "Percent"].apply(lambda x: f"{int(x*100)}%") 
                temp_df.sort_values("Amount", ascending = False, inplace = True)
                st.session_state[table] = temp_df    

def compile_budget():
    df = pd.DataFrame({"Category": [], "Amount": []})
    for table in ["fixed_costs", "investments", "savings_goals"]:
        table_df = st.session_state[table].dropna(subset=[col for col in df.columns if col not in ["Category", "Percent"]])
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
    fixed_costs.loc[fixed_costs.Category == "", "Category"] = "Misc."
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
    if page == "Investments" and "dollar_goal" in st.session_state:
        target = st.session_state.dollar_goal
    else:
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
    target_color = "white" if st.session_state.theme == "dark" else "#808080"
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

def all_progress_bars():
    df = st.session_state.budget_data.copy()
    df = df.iloc[:-2]
    df["goal"] = [.6, .1, .1, .2]
    df["goal_type"] = ["ceiling", "floor", "floor", "floor"]
    df = df.iloc[::-1].reset_index(drop=True)    

    # Create targets for each entry
    df["Target"] = df.goal * st.session_state.net_income
    if "dollar_goal" in st.session_state:
        df.loc[df.Category == "Investments", "Target"] = st.session_state.dollar_goal
    # Create the horizontal bar plot
    fig = go.Figure()

    # Add each bar to the figure
    for idx, row in df.iterrows():
        value = int(row["Amount"])
        target = int(row["Target"])
        goal_type = row["goal_type"]
        category = row["Category"]  # Label for each entry

        if goal_type == "floor":
            target_word = "Target Min"
            if value >= target:
                bar_color = "#047c6c"
            else:
                bar_color = "#c4442c"
        elif goal_type == "ceiling":
            target_word = "Target Max"
            if value <= target:
                bar_color = "#047c6c"
            else:
                bar_color = "#c4442c"

        fig.add_trace(
            go.Bar(
                x=[value],
                y=[category],
                orientation='h',
                marker_color=bar_color,
                text=[f"{value:.0f}"],
                textposition='auto',
                textfont=dict(size=14, color="white"),
                width=0.5  # Consistent bar width
            )
        )

        # Add vertical goal line for each entry
        target_color = "white" if st.session_state.theme == "dark" else "#808080"

        fig.add_shape(
            type="line",
            x0=target,
            y0=idx - 0.4,
            x1=target,
            y1=idx + 0.4,
            line=dict(color=target_color, width=4)
        )

        # Add target annotation without the arrow
        fig.add_annotation(
            x=target,
            y=idx,
            text=f"{target_word}: {target:.0f}",
            showarrow=False,
            font=dict(size=12, color=target_color),
            xanchor='left'
        )

    # Update layout for transparency and improved visibility
    fig.update_layout(
        width=600,
        height=300 + len(df) * 30,  # Dynamic height based on number of entries
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        # xaxis=dict(range=[0, max(df["Amount"].max(), df["Target"].max()) * 1.1], showgrid=False),
        yaxis=dict(showgrid=False, showticklabels=True)
    )

    st.plotly_chart(fig)


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

def end_demo():
    del st.session_state["completed_all_tasks"]
    for page in st.session_state.config["Pages"].keys():
        del st.session_state[f"completed_{page}"]
        tables = st.session_state.config["Pages"][page]["tables"].keys()
        for table in tables:
            del st.session_state[table]
    del st.session_state.in_demo


def edit_data(page): 
    st.session_state["changed_tables"] = dict()
    tables = st.session_state.config["Pages"][page]["tables"].keys()
    for table in tables:
        if page == "Net_Worth":
            st.header(st.session_state.config["Headers"][table])
        st.write(st.session_state.config["Pages"][page]["tables"][table]["preamble"])
        if table not in st.session_state:
            columns = st.session_state.config["Pages"][page]["tables"][table]["columns"]            
            df = pd.DataFrame(dict(zip(columns, [pd.Series(dtype='str') if col!="Amount" else pd.Series(dtype='float') for col in columns])))
            st.session_state[table] = df
        df = st.session_state[table].copy()
        edited_df = st.data_editor(df, num_rows = 'dynamic', disabled = ["Percent"], hide_index = True)
        st.session_state["changed_tables"][table] = edited_df.reset_index(drop=True)
        if not edited_df.equals(st.session_state[table]):
            st.session_state[f"completed_{page}"] = True

    if ("completed_all_tasks" in st.session_state) & (page not in ["Net_Worth", "Income"]):
        sum_df = st.session_state.budget_data.copy()
        page_name = page.replace("_", " ")
        sum_df = sum_df.loc[sum_df.Category == page_name, ["Amount", "Percent", "Goal"]].copy()
        sum_df.rename(columns = {"Amount": page_name}, inplace = True)
        progress_bar(page)        
       