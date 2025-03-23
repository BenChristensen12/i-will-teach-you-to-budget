import streamlit as st
from utils.functions import *

st.set_page_config(layout = 'wide')
for k, v in st.session_state.items():
    st.session_state[k] = v 

page = os.path.basename(__file__).split('_', 1)[1].split('.')[0]
every_page_run(page)
st.title(page.replace("_", " "))
if "clicked_convert_paycheck" in st.session_state:
    source = st.text_input("Enter income source:", value = None)
    if source:
        paycheck = st.number_input("Enter paycheck value:")
        if paycheck:
            recurrence = st.radio("Paycheck frequency:", ["Weekly", "Bi-weekly", "Semi-monthly"], index = None)
            if recurrence == "Weekly":
                monthly_converted = paycheck*52/12
            elif recurrence == "Bi-weekly": 
                monthly_converted = paycheck*(52/2)/12
            elif recurrence == "Semi-monthly":
                monthly_converted = paycheck*2
            if recurrence:
                st.session_state["converted_paycheck"] = {source:monthly_converted}
                st.button("Submit Paycheck", on_click=button_click, args=("clicked_submit_paycheck",))

else:
    st.button("Convert paycheck into monthly income", on_click=button_click, args=("clicked_convert_paycheck",))

if "clicked_submit_paycheck" in st.session_state:
    del st.session_state.clicked_convert_paycheck
    del st.session_state.clicked_submit_paycheck
    source, amount = list(st.session_state.converted_paycheck.items())[0]
    table = list(st.session_state.config["Pages"][page]["tables"].keys())[0]
    if table not in st.session_state:
        rows = st.session_state.config["Pages"][page]["tables"][table]["rows"]
        columns = st.session_state.config["Pages"][page]["tables"][table]["columns"]            
        df = pd.DataFrame(rows, columns = columns)        
    else:
        df = st.session_state[table]

    df = pd.concat([df, pd.DataFrame({"Source": [source], "Amount": [amount]})], ignore_index = True)
    st.session_state[table] = df.copy()
    st.rerun()
        

    


edit_data(page)
if f"completed_{page}"  in st.session_state:
    st.header("Dealing with Unexpected Income")
    if "clicked_unexpected_income" in st.session_state:
        if "clicked_submit_ui_allocation" not in st.session_state:
            if "clicked_change_ui_allocation" in st.session_state:
                del st.session_state.clicked_change_ui_allocation
            st.write("""Choose the places you want unexpected income to go. Every time you get such a paycheck 
                    use these percentages to determine where to send the extra income.
                    Common choices are: taxes, a fun savings goal, investments, and guilt-free spending.
                     Unexpected income lives outside the budget.""")
            col1, col2 = st.columns(2)
            percents = np.array([],dtype=int)
            categories = []
            st.number_input("Number of categories:", step = 1, key="ui_percent_cats")
            cat_num = st.session_state.ui_percent_cats
            if cat_num:
                for cat in range(cat_num):
                    st.text_input(f"Category {cat+1} name:", key = f"cat_{cat}")
                    text = st.session_state[f"cat_{cat}"]
                    if text:
                        percent_available = 100-percents.sum()
                        if cat < cat_num-1:
                            percent = st.number_input(f"Percent contribution to {text}:", min_value=1, max_value=percent_available-(cat_num-cat-1), key=f"cat_{cat}_percent", step=1)
                        else:
                            percent = st.number_input(f"Percent contribution to {text}:", min_value=1, max_value=percent_available, value = percent_available, disabled = True)                    
                        
                        categories.append(text)
                        percents = np.append(percents, percent)
                        text = None
                df = pd.DataFrame({"Categories": categories, "Percent": percents})
                df.Percent = df.Percent.apply(lambda x: f"{int(x)}%") 
                st.session_state["ui_allocation_frame"] = df.copy()
                st.dataframe(data=df, hide_index=True)
            st.button("Submit", on_click=button_click, args=("clicked_submit_ui_allocation",))
        else:
            if "clicked_change_ui_allocation" in st.session_state:
                del st.session_state.clicked_submit_ui_allocation
                st.rerun()
            else:
                paycheck = st.number_input("Enter paycheck value to allocate:", value=None)
                if paycheck:
                    df = st.session_state.ui_allocation_frame.copy()
                    allocations = paycheck*df.Percent.apply(lambda x: float(x[:-1])/100)
                    df.insert(1, "Allocation", allocations)
                    df.Allocation = df.Allocation.round(2)
                    st.dataframe(df, hide_index=True)
                st.button("Change Percent Allocation", on_click=button_click, args=("clicked_change_ui_allocation",))


    else:    
        st.button("Setup Allocation of Unexpected Income", on_click=button_click, args=("clicked_unexpected_income",))