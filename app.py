import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from db_helper import get_databases, create_database, get_tables, drop_table, drop_database

# --- Database Configuration ---
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASS = ""
MYSQL_PORT = 3308

st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>📊 No-Code Database Manager</h1>", unsafe_allow_html=True)

# --- Sidebar Navigation ---
st.sidebar.markdown("## 🧭 Operations")
st.sidebar.markdown("""
    <style>
        .sidebar-radio label {
            display: block;
            padding: 12px 16px;
            margin: 8px 0;
            background: #f0f2f6;
            border-radius: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }
        .sidebar-radio label:hover {
            background: #dbe4f3;
        }
        .sidebar-radio .stRadio > div {flex-direction: column;}
    </style>
""", unsafe_allow_html=True)

st.sidebar.markdown("<div class='sidebar-radio'>", unsafe_allow_html=True)
operation = st.sidebar.radio("Choose Operation", [
    "📥 Store Excel to DB", 
    "✏️ Edit or Update Table Rows", 
    "➕ Append Columns to Table",
    "❌ Delete Table or Database"
])
st.sidebar.markdown("</div>", unsafe_allow_html=True)

# --- Upload Section (Centered) ---
uploaded_file = None
if operation in ["📥 Store Excel to DB", "➕ Append Columns to Table"]:
    st.markdown("""
        <style>.upload-section {display: flex; justify-content: center; margin-bottom: 30px;}</style>
    """, unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='upload-section'>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("📂 Upload Excel File (.xlsx)", type=["xlsx"], key="file_upload")
        st.markdown("</div>", unsafe_allow_html=True)

    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)
            st.markdown("### ✅ Uploaded File Preview")
            st.dataframe(df)
        except Exception as e:
            st.warning(f"⚠️ Error reading Excel file: {e}")

# === Store Excel to DB ===
if operation == "📥 Store Excel to DB" and uploaded_file:
    store_type = st.radio("Where to store data?", [
        "Store as new table in existing database",
        "Store as new table in a new database"
    ])

    if store_type == "Store as new table in existing database":
        databases = get_databases()
        db_choice = st.selectbox("Select Database", ["Choose a Database"] + databases)
        if db_choice == "Choose a Database":
            st.warning("⚠️ Please select a valid database.")
            st.stop()

        table_name = st.text_input("Enter Table Name")

        if st.button("📥 Upload to Existing DB"):
            if db_choice and table_name:
                try:
                    engine = create_engine(f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASS}@{MYSQL_HOST}:{MYSQL_PORT}/{db_choice}")
                    df.to_sql(table_name, con=engine, if_exists='replace', index=False)
                    st.success("✅ Table uploaded successfully!")
                    st.rerun()
                except Exception as e:
                    st.warning(f"⚠️ Failed to upload table: {e}")

    elif store_type == "Store as new table in a new database":
        new_db = st.text_input("New Database Name")
        table_name = st.text_input("Table Name")

        if st.button("📥 Create DB and Upload"):
            if new_db and table_name:
                try:
                    create_database(new_db)
                    engine = create_engine(f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASS}@{MYSQL_HOST}:{MYSQL_PORT}/{new_db}")
                    df.to_sql(table_name, con=engine, if_exists='replace', index=False)
                    st.success("✅ Database and table created successfully!")
                    st.rerun()
                except Exception as e:
                    st.warning(f"⚠️ Failed to create database or upload table: {e}")

# === Edit or Update Rows ===
elif operation == "✏️ Edit or Update Table Rows":
    try:
        databases = get_databases()
        db_choice = st.selectbox("Select Database", ["Choose a Database"] + databases, key="edit_db")
        if db_choice == "Choose a Database":
            st.warning("⚠️ Please select a valid database.")
            st.stop()

        tables = get_tables(db_choice)
        table_choice = st.selectbox("Select Table", ["Choose a Table"] + tables)
        if table_choice == "Choose a Table":
            st.warning("⚠️ Please select a valid table.")
            st.stop()

        engine = create_engine(f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASS}@{MYSQL_HOST}:{MYSQL_PORT}/{db_choice}")
        df_existing = pd.read_sql_table(table_choice, con=engine)
        st.markdown("### Current Data")
        edited_df = st.data_editor(df_existing, num_rows="dynamic")

        if st.button("💾 Save Changes"):
            edited_df.to_sql(table_choice, con=engine, if_exists='replace', index=False)
            st.success("✅ Table updated successfully!")
            st.rerun()
    except Exception as e:
        st.warning(f"⚠️ Error editing table: {e}")

# === Append Excel columns ===
elif operation == "➕ Append Columns to Table" and uploaded_file:
    try:
        databases = get_databases()
        db_choice = st.selectbox("Select Database", ["Choose a Database"] + databases, key="append_db")
        if db_choice == "Choose a Database":
            st.warning("⚠️ Please select a valid database.")
            st.stop()

        tables = get_tables(db_choice)
        table_choice = st.selectbox("Select Table", ["Choose a Table"] + tables)
        if table_choice == "Choose a Table":
            st.warning("⚠️ Please select a valid table.")
            st.stop()

        if st.button("➕ Append Columns"):
            df_new = pd.read_excel(uploaded_file)
            engine = create_engine(f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASS}@{MYSQL_HOST}:{MYSQL_PORT}/{db_choice}")
            df_existing = pd.read_sql_table(table_choice, con=engine)
            df_combined = pd.concat([df_existing, df_new], axis=1)
            df_combined.to_sql(table_choice, con=engine, if_exists='replace', index=False)
            st.success(f"✅ Columns appended to table `{table_choice}`")
            st.rerun()
    except Exception as e:
        st.warning(f"⚠️ Failed to append columns: {e}")

# === Delete Table or Database ===
elif operation == "❌ Delete Table or Database":
    try:
        delete_mode = st.radio("Select Delete Option", ["Delete Table", "Delete Database"])

        if delete_mode == "Delete Table":
            databases = get_databases()
            db_choice = st.selectbox("Select Database", ["Choose a Database"] + databases, key="del_table_db")
            if db_choice == "Choose a Database":
                st.warning("⚠️ Please select a valid database.")
                st.stop()

            tables = get_tables(db_choice)
            table_choice = st.selectbox("Select Table", ["Choose a Table"] + tables)
            if table_choice == "Choose a Table":
                st.warning("⚠️ Please select a valid table.")
                st.stop()

            if st.button("❌ Delete Table"):
                st.session_state.confirm_delete = ("table", db_choice, table_choice)

        elif delete_mode == "Delete Database":
            databases = get_databases()
            db_choice = st.selectbox("Select Database", ["Choose a Database"] + databases, key="del_db")
            if db_choice == "Choose a Database":
                st.warning("⚠️ Please select a valid database.")
                st.stop()

            if st.button("❌ Delete Database"):
                st.session_state.confirm_delete = ("database", db_choice, None)

        if "confirm_delete" in st.session_state:
            mode, db, table = st.session_state.confirm_delete
            if mode == "table":
                st.warning(f"⚠️ Confirm delete table `{table}` from `{db}`?")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Confirm Table Delete"):
                        drop_table(db, table)
                        st.success("✅ Table deleted.")
                        del st.session_state.confirm_delete
                        st.rerun()
                with col2:
                    if st.button("❎ Cancel"):
                        del st.session_state.confirm_delete
                        st.info("Cancelled")
            elif mode == "database":
                st.warning(f"⚠️ Confirm delete database `{db}`?")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Confirm Database Delete"):
                        drop_database(db)
                        st.success("✅ Database deleted.")
                        del st.session_state.confirm_delete
                        st.rerun()
                with col2:
                    if st.button("❎ Cancel"):
                        del st.session_state.confirm_delete
                        st.info("Cancelled")
    except Exception as e:
        st.warning(f"⚠️ Error in delete operation: {e}")
