import streamlit as st
import pandas as pd
import json
import os

def initialize_dashboard():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    st.session_state["config"] = json.load(open(repo_dir + "/utils/config.json"))
    st.session_state["dashboard_initialized"] = True

def submit_changes():
    st.session_state["clicked"] = True

def edit_data(page):
    if "clicked" in st.session_state:
        del st.session_state.clicked
        st.session_state[f"completed_{page}"] = True
        st.session_state.update(st.session_state.changed_tables)

    st.session_state["changed_tables"] = dict()
    for table in st.session_state.config["Pages"][page]["tables"]:
        st.header(st.session_state.config["Headers"][table])
        st.write(st.session_state.config["Pages"][page]["tables"][table]["preamble"])
        if table in st.session_state:
            df = st.session_state[table].copy()
            edited_df = st.data_editor(df, num_rows = 'dynamic')
        else:
            rows = st.session_state.config["Pages"][page]["tables"][table]["rows"]
            columns = st.session_state.config["Pages"][page]["tables"][table]["columns"]            
            df = pd.DataFrame(rows, columns = columns)
            edited_df = st.data_editor(df, num_rows = 'dynamic')
        st.session_state.changed_tables[table] = edited_df
    if f"completed_{page}" not in st.session_state:
        button = st.button("Submit", on_click = submit_changes)
    else:
        button = st.button("Submit Changes", on_click = submit_changes)
