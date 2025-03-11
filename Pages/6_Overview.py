import streamlit as st
from utils.functions import *

st.set_page_config(layout = 'wide')

if "completed_all_tasks" not in st.session_state:
    show_progress()
    if "completed_all_tasks" in st.session_state:
        compile_budget()
        update_percentages()
        st.rerun()       
    st.write("Complete the above tasks and then return to this page.")


else:
    st.title("Budget Overview")
    labels, parents, values = st.session_state.sunburst_data
    category_colors = {"Net Income": "rgba(0, 0, 0, 0)",
                       "Fixed Costs": "#c4442c",
                       "Savings Goals": "#047c6c",
                       "Investments": "#142c2c",
                       "Guilt-Free": "#f4e4d4"}
    colors = [category_colors[labels[i]] if labels[i] in category_colors else category_colors.get(parents[i], "#c4442c") for i in range(len(labels))]
    sunburst = go.Figure(go.Sunburst(labels = labels, parents = parents, values = values, branchvalues = "total",marker = dict(colors=colors)))
    sunburst.update_layout(width = 800, height = 800)
    st.plotly_chart(sunburst, use_container_width=True, theme= "streamlit")
    html_str = sunburst.to_html(full_html = True, include_plotlyjs = "cdn")
    st.download_button("Download Interactive Chart", data = html_str, file_name = "sunburst_chart.html", mime = "text/html")

    st.dataframe(st.session_state.budget_data, hide_index = True)   

    #combined table for budget

    #downlaod budget


    # How to deal with unexpected income?

    st.header("Retirement Calculator")
    # Line graph showing increasing assets over time