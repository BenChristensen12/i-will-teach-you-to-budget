import streamlit as st
from utils.functions import *

st.set_page_config(layout = 'wide')
for k, v in st.session_state.items():
    st.session_state[k] = v 
page = os.path.basename(__file__).split('_', 1)[1].split('.')[0]
st.title(page.replace("_", " "))

edit_data(page)
if "change_investment_target" in st.session_state:
    del st.session_state.change_investment_target
    st.session_state["dollar_goal"] = int(st.session_state.needed_contribution)
    compile_budget()
    st.rerun()

st.header("Retirement Calculator")
if "investments" not in st.session_state:
    st.write("Submit the above table to unlock the retirement calculator.")
else:
    if "submit_retirement_assumptions" not in st.session_state:
        st.number_input("How many years until you retire?", value = None, key = "yr_until")
        default_rate = 7 if "rate" not in st.session_state else None
        st.number_input("What percent return rate should we assume on the investments (after inflation)?", value = default_rate, key = "rate")
        st.number_input("How much total do you currently have in your investment portfolio? (Check the Net Worth Page)", value = None, key = "principal")
        if all(st.session_state[k] for k in ["yr_until", "rate", "principal"]):
            st.button("Submit", on_click=button_click, args=("submit_retirement_assumptions",))
    else:
        if "change_retirement_assumptions" not in st.session_state:
            contribution = st.session_state.investments.Amount.sum()
            portfolio_values = calculate_portfolio(st.session_state.principal, contribution, st.session_state.rate/100, st.session_state.yr_until)
            
            retirement_income = (portfolio_values[-1]*.027)/12
            st.write(f"You could expect to have ${retirement_income:.0f} per month through retirement. This assumes 30 years in retirement and a withdrawal rate using the 2.7% rule.")
            dates = pd.date_range(start = pd.Timestamp.now(), periods = 1+(12*st.session_state.yr_until), freq='ME')
            df = pd.DataFrame({'Date': dates, 'Portfolio Value': portfolio_values})
            # Plotting
            fig = px.line(df, x="Date", y='Portfolio Value', title="Retirement Portfolio Growth")
            st.plotly_chart(fig)
            st.button("Change retirement assumptions", on_click=button_click, args=("change_retirement_assumptions",))     
            st.number_input("Target monthly income in retirement:", value = None, key = "monthly_target")
            if st.session_state.monthly_target:
                portfolio_needed = (st.session_state.monthly_target*12)/.027
                st.session_state["needed_contribution"] = calculate_needed_contribution(portfolio_needed, st.session_state.principal, st.session_state.rate/100, st.session_state.yr_until)
                st.write(f"You need to invest {st.session_state.needed_contribution:.2f} monthly to hit that target.")
                st.button("Submit Investment Goal", on_click=button_click, args=("change_investment_target",))
            
        else:
            del st.session_state.change_retirement_assumptions
            del st.session_state.submit_retirement_assumptions
            st.rerun()
