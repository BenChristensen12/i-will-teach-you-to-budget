import streamlit as st
from utils.functions import *

st.set_page_config(layout = 'wide')

if "completed_all_tasks" not in st.session_state:
    show_progress()
    st.write("Complete the above tasks and then return to this page.")

else:
    st.title("Budget Overview")

    df = pd.DataFrame({"Category": [], "Amount": []})
    for table in ["fixed_costs", "savings_goals", "investments"]:
        table_df = st.session_state[table]
        summed_df = pd.DataFrame({"Category": [st.session_state.config["Headers"][table]], "Amount": [table_df.Amount.sum()]})
        df = pd.concat([df, summed_df])

    total = st.session_state.income.Amount.sum()

    gf = pd.DataFrame({"Category": ["Guilt-Free"], "Amount": [total - df.Amount.sum()]})
    df = pd.concat([df, gf])
    df["Percent"] = (df.Amount / total)

    #chart showing breakout of budget
    labels = ["Total Income", "Fixed Costs", "Savings Goals", "Investments", "Guilt-Free"]
    parents = ["", "Total Income", "Total Income", "Total Income", "Total Income"]    
    values = [int(total), df.loc[df.Category == "Fixed Costs", "Amount"].values[0], df.loc[df.Category == "Savings Goals", "Amount"].values[0],df.loc[df.Category == "Investments", "Amount"].values[0], df.loc[df.Category == "Guilt-Free", "Amount"].values[0]]

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


    sunburst = go.Figure(go.Sunburst(labels = labels, parents = parents, values = values, branchvalues = "total",))
    sunburst.update_layout(width = 800, height = 800)
    st.plotly_chart(sunburst, use_container_width=True, theme= "streamlit")

    labels
    parents
    values

    # Display data
    df["Percent"] = df["Percent"].apply(lambda x: f"{int(x*100)}%")
    df["Goal"] = ["60%-", "10%+", "10%+", "20%+"]
    df.sort_values("Percent", ascending = False, inplace = True)

    st.dataframe(df, hide_index = True)      

    # Update individual tables
    for page in st.session_state.config["Pages"].keys():
        for table in st.session_state.config["Pages"][page]["tables"].keys():
            temp_df = st.session_state[table]
            temp_df["Percent"] = temp_df.Amount / total
            temp_df["Percent"] = temp_df["Percent"].apply(lambda x: f"{int(x*100)}%") 
            temp_df.sort_values("Percent", ascending = False, inplace = True)
            st.session_state[table] = temp_df.copy()      
    #donut chart showing breakdown of fixed costs

    #combined table for budget

    #downlaod budget


    # How to deal with unexpected income?

    # Sort all tables Percent descending

    st.header("Retirement Calculator")
    # Line graph showing increasing assets over time