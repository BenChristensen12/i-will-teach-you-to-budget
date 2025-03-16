import streamlit as st
from utils.functions import *

st.set_page_config(layout = 'wide')
if "dashboard_initialized" not in st.session_state:
    initialize_dashboard()    
for k, v in st.session_state.items():
    st.session_state[k] = v     
st.title("I Will Teach You to Budget")


import streamlit as st
from utils.functions import *

if "completed_all_tasks" not in st.session_state:
    if st.session_state.uploaded_file_name is not None:
        st.success("Previous Session Restored!")
    st.write("Welcome to I Will Teach You to Budget!")
    st.write("""This free-to-use tool will help you create a budget. The hardest part is remembering the logins to all your accounts.
    We'll also calculate your net worth and plug-in numbers into an investment calculator to show what you could have in retirement.
    Each section of the budget has percentage goals that will guide your budget decisions. These are based on Ramit Sethi's book
    *I Will Teach You to Be Rich*, so consider checking out his book if you like this tool.""")
    st.markdown("""This budget consists of 5 sections: 1. Net Worth 2. Fixed Costs 3. Savings Goals 4. Investments 5. Guilt-Free Spending.
            To build the budget we've separated each of these sections into pages on the sidebar. When you're finished, guilt-free spending
            is calculated as whatever money is leftover.""")

    uploaded_file = st.file_uploader("Upload Previously Completed Budget", type='pkl')
    if uploaded_file is not None:
        if uploaded_file.name != st.session_state.uploaded_file_name:  
            loaded_state = pickle.loads(uploaded_file.read())
            for k, v in loaded_state.items():
                st.session_state[k] = v
            
            st.session_state.uploaded_file_name = uploaded_file.name
            st.rerun()
    show_progress()
    if "completed_all_tasks" in st.session_state:
        compile_budget()
        update_percentages()
        st.rerun()       
    st.write("Complete the above tasks and then return to this page.")
    st.button("Run Demo", on_click = run_demo)


else:
    upload_file = pickle.dumps(dict(st.session_state))
    today = datetime.today().strftime("%Y-%m-%d")    
    st.download_button("Download Your Saved Progress File", data = upload_file, file_name = f"i-will-teach-you-to-budget-session-{today}.pkl", mime = "application/octet-stream")
    st.header("Budget Overview")
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

    if "in_demo" in st.session_state:
        st.button("Reset Budget", on_click=end_demo)
    

    # Adjust number of layers to show in sunburst?

    # Where to show guit-free spending compared to goal?
        # Add progress bars to overview page showing green and red and the goals

   # Adjust all inputs to be float at 2-decimals instead of int

   # Replace dark detect with just having default to dark?

   