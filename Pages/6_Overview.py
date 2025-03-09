import streamlit as st
from utils.functions import *

st.set_page_config(layout = 'wide')

if "completed_all_tasks" not in st.session_state:
    show_progress()
    st.write("Complete the above tasks and then return to this page.")

else:
    st.title("Budget Overview")
    labels, parents, values = st.session_state.sunburst_data
    sunburst = go.Figure(go.Sunburst(labels = labels, parents = parents, values = values, branchvalues = "total",))
    sunburst.update_layout(width = 800, height = 800, 
    sunburstcolorway=["#f4e4d4", "#c4442c", "#047c6c", "#142c2c"])
    st.plotly_chart(sunburst, use_container_width=True, theme= "streamlit")
    html_str = sunburst.to_html(full_html = True, include_plotlyjs = "cdn")
    st.download_button("Download Interactive Chart", data = html_str, file_name = "sunburst_chart.html", mime = "text/html")

    st.dataframe(st.session_state.budget_data, hide_index = True)   

    # Update individual tables

    #donut chart showing breakdown of fixed costs

    #combined table for budget

    #downlaod budget


    # How to deal with unexpected income?

    # Sort all tables Percent descending

    st.header("Retirement Calculator")
    # Line graph showing increasing assets over time