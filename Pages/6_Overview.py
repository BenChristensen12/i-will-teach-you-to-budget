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
    # Plot pie chart
    fig, ax = plt.subplots()
    ax.pie(df['Percent'], labels=df['Category'], autopct='%.0f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Display in Streamlit
    st.pyplot(fig)


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