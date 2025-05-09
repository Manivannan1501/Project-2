import os
import sqlite3
from datetime import datetime
import pandas as pd
import streamlit as st
import seaborn as sns

DB_NAME = 'food_waste.db'
DATA_DIR = 'data'

st.set_page_config(page_title="Local Food Wastage Management System", layout="wide")

# ---------- Utility Functions ----------

def execute_query(query, params=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    return results

def get_unique_values(table, column):
    try:
        query = f"SELECT DISTINCT {column} FROM {table}"
        results = execute_query(query)
        return [r[0] for r in results]
    except:
        return []

# ---------- Database Setup Functions ----------

def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Providers (
            Provider_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            Type TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Receivers (
            Receiver_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            Type TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS FoodListings (
            Listing_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Food_Name TEXT,
            Quantity INTEGER,
            Expiry_Date TEXT,
            Provider_ID INTEGER,
            Provider_Type TEXT,
            Location TEXT,
            Food_Type TEXT,
            Meal_Type TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Claims (
            Claim_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Listing_ID INTEGER,
            Receiver_ID INTEGER,
            Claim_Date TEXT
        )
    """)
    conn.commit()
    conn.close()

def load_embedded_data_to_db():
    conn = sqlite3.connect(DB_NAME)

    providers = pd.DataFrame({
        "Provider_ID": [1, 2],
        "Name": ["Provider A", "Provider B"],
        "Type": ["Restaurant", "Supermarket"]
    })

    receivers = pd.DataFrame({
        "Receiver_ID": [1, 2],
        "Name": ["Receiver A", "Receiver B"],
        "Type": ["NGO", "Charity"]
    })

    food_listings = pd.DataFrame({
        "Listing_ID": [1, 2],
        "Food_Name": ["Rice", "Bread"],
        "Quantity": [10, 5],
        "Expiry_Date": ["2025-05-10", "2025-05-12"],
        "Provider_ID": [1, 2],
        "Provider_Type": ["Restaurant", "Supermarket"],
        "Location": ["Downtown", "Uptown"],
        "Food_Type": ["Grain", "Bakery"],
        "Meal_Type": ["Lunch", "Breakfast"]
    })

    claims = pd.DataFrame({
        "Claim_ID": [1],
        "Listing_ID": [1],
        "Receiver_ID": [1],
        "Claim_Date": ["2025-05-08"]
    })

    providers.to_sql("Providers", conn, if_exists="replace", index=False)
    receivers.to_sql("Receivers", conn, if_exists="replace", index=False)
    food_listings.to_sql("FoodListings", conn, if_exists="replace", index=False)
    claims.to_sql("Claims", conn, if_exists="replace", index=False)

    conn.commit()
    conn.close()

# ---------- Display Functions ----------

def display_data(table):
    df = pd.read_sql(f"SELECT * FROM {table}", sqlite3.connect(DB_NAME))
    st.dataframe(df)

def display_food_listings():
    st.header("Food Listings")
    df = pd.read_sql("SELECT * FROM FoodListings", sqlite3.connect(DB_NAME))
    st.dataframe(df)

def display_sql_queries():
    st.header("Run SQL Query")
    query = st.text_area("Enter SQL query:")
    if st.button("Execute"):
        try:
            df = pd.read_sql_query(query, sqlite3.connect(DB_NAME))
            st.dataframe(df)
        except Exception as e:
            st.error(f"Error: {e}")

def display_food_wastage_by_type_chart():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql("SELECT Food_Type, SUM(Quantity) as Total FROM FoodListings GROUP BY Food_Type", conn)
    conn.close()
    if df.empty:
        st.warning("No data available.")
        return
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x="Food_Type", y="Total")
    plt.xticks(rotation=45)
    st.pyplot(plt.gcf())

# ---------- Add Listing Function ----------

def add_food_listing():
    st.header("Add Food Listing")
    food_name = st.text_input("Food Name")
    quantity = st.number_input("Quantity", min_value=1, step=1)
    expiry_date = st.date_input("Expiry Date", datetime.now().date())
    provider_id = st.selectbox("Provider", get_unique_values("Providers", "Provider_ID"))
    provider_type = st.selectbox("Provider Type", get_unique_values("Providers", "Type"))
    location = st.text_input("Location")
    food_type = st.selectbox("Food Type", get_unique_values("FoodListings", "Food_Type") or ["Vegetable", "Grain"])
    meal_type = st.selectbox("Meal Type", get_unique_values("FoodListings", "Meal_Type") or ["Breakfast", "Lunch", "Dinner"])
    if st.button("Add Listing"):
        query = """
            INSERT INTO FoodListings (Food_Name, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location, Food_Type, Meal_Type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type)
        execute_query(query, params)
        st.success("Food listing added successfully!")

# ---------- Main Function ----------

def main():
    st.title("Local Food Wastage Management System")
    if not os.path.exists(DB_NAME):
        create_database()
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
        load_embedded_data_to_db()
    menu = ["Home", "View Data", "Add Food Listing", "Food Listings", "SQL Queries", "Food Wastage Chart"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "Home":
        st.write("Welcome to the Local Food Wastage Management System.")
    elif choice == "View Data":
        table = st.selectbox("Select Table to View", ["Providers", "Receivers", "FoodListings", "Claims"])
        display_data(table)
    elif choice == "Add Food Listing":
        add_food_listing()
    elif choice == "Food Listings":
        display_food_listings()
    elif choice == "SQL Queries":
        display_sql_queries()
    elif choice == "Food Wastage Chart":
        display_food_wastage_by_type_chart()

if __name__ == "__main__":
    main()
