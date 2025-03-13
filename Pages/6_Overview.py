import streamlit as st
from utils.functions import *

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
    sunburst.update_layout(width = 400, height = 500)
    
    col1, col2, col3 = st.columns([1,3,3])
    with col2:
        if st.session_state.guilt_free < 0:
            vpadding = (400)/2
            st.markdown(f"<div style='padding-top: {vpadding}px; ;'></div>", unsafe_allow_html=True)   
            st.header(f"Your budget exceeds your net income by ${int(abs(st.session_state.guilt_free))}")
            st.markdown('</div>', unsafe_allow_html=True)        
        else:
            st.plotly_chart(sunburst, use_container_width=True, theme= "streamlit")
            html_str = sunburst.to_html(full_html = True, include_plotlyjs = "cdn")
            st.download_button("Download Interactive Chart", data = html_str, file_name = "sunburst_chart.html", mime = "text/html")
    with col3:
        vpadding = (500+15 - 245.656)/2
        st.markdown(f"<div style='padding-top: {vpadding}px; ;'></div>", unsafe_allow_html=True)
        st.dataframe(st.session_state.budget_data, hide_index = True)  
        st.markdown('</div>', unsafe_allow_html=True)        

    upload_file = pickle.dumps(dict(st.session_state))
    today = datetime.today().strftime("%Y-%m-%d")
    st.download_button("Download Complete Budget File", data = upload_file, file_name = f"i-will-teach-you-to-budget-session-{today}.pkl", mime = "application/octet-stream")






    # Adjust number of layers to show in sunburst?

    # Where to show guit-free spending compared to goal?

    st.header("Retirement Calculator")
    # Line graph showing increasing assets over time