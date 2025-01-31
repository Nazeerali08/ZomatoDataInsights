import streamlit as st
import mysql.connector as db
import pandas as pd
import plotly.express as px
from datetime import datetime

# Database connection function
def create_connection():
    return db.connect(
        host="localhost",
        user="root",
        password="@Inshaallah8",
        database="zomato"
    )

# Initialize Streamlit app
st.set_page_config(page_title="Zomato Analytics", layout="wide")

# Sidebar navigation
page = st.sidebar.selectbox("Select Page", ["Data Tables", "CRUD Operations", "Data Insights"])

# Data Tables Page
if page == "Data Tables":
    st.title("Zomato Data Insights")
    
    conn = create_connection()
    cursor = conn.cursor()
    
    # Display tables in tabs
    tabs = st.tabs(["customers", "Restaurants", "ORDERS", "Deliveries"])
    
    with tabs[0]:
        st.header("Customers Table")
        cursor.execute("SELECT * FROM customers")
        customers_data = cursor.fetchall()
        customers_df = pd.DataFrame(customers_data, columns=[i[0] for i in cursor.description])
        st.dataframe(customers_df)
    
    with tabs[1]:
        st.header("Restaurants Table")
        cursor.execute("SELECT * FROM Restaurants")
        restaurants_data = cursor.fetchall()
        restaurants_df = pd.DataFrame(restaurants_data, columns=[i[0] for i in cursor.description])
        st.dataframe(restaurants_df)
    
    with tabs[2]:
        st.header("Orders Table")
        cursor.execute("SELECT * FROM orders")
        orders_data = cursor.fetchall()
        orders_df = pd.DataFrame(orders_data, columns=[i[0] for i in cursor.description])
        st.dataframe(orders_df)
    
    with tabs[3]:
        st.header("Deliveries Table")
        cursor.execute("SELECT * FROM deliveries")
        deliveries_data = cursor.fetchall()
        deliveries_df = pd.DataFrame(deliveries_data, columns=[i[0] for i in cursor.description])
        st.dataframe(deliveries_df)
    
    conn.close()

# CRUD Operations Page
elif page == "CRUD Operations":
    st.title("CRUD Operations")
    
    # Select table for CRUD operations
    table = st.selectbox("Select Table", ["customers", "restaurants", "orders", "deliveries"])
    operation = st.selectbox("Select Operation", ["Create", "Read", "Update", "Delete"])
    
    conn = create_connection()
    cursor = conn.cursor()
    
    if operation == "Create":
        st.subheader(f"Add New {table.title()[:-1]}")
        
        # Dynamic form based on table schema
        cursor.execute(f"DESCRIBE {table}")
        columns = [row[0] for row in cursor.fetchall()]
        
        # Create input fields
        input_values = {}
        for col in columns:
            if col.lower().endswith('_id'):
                continue  # Skip ID fields for creation
            input_values[col] = st.text_input(f"Enter {col}")
        
        if st.button("Add Record"):
            try:
                cols = ", ".join(input_values.keys())
                vals = ", ".join([f"'{v}'" for v in input_values.values()])
                cursor.execute(f"INSERT INTO {table} ({cols}) VALUES ({vals})")
                conn.commit()
                st.success("Record added successfully!")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    elif operation == "Read":
        st.subheader(f"View {table.title()}")
        cursor.execute(f"SELECT * FROM {table}")
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=[i[0] for i in cursor.description])
        st.dataframe(df)
    
    elif operation == "Update":
        st.subheader(f"Update {table.title()}")
        
        # Get primary key for selection
        cursor.execute(f"SHOW KEYS FROM {table} WHERE Key_name = 'PRIMARY'")
        primary_key = cursor.fetchone()[4]
        
        # Get existing records
        cursor.execute(f"SELECT {primary_key} FROM {table}")
        records = cursor.fetchall()
        selected_id = st.selectbox(f"Select {primary_key}", [r[0] for r in records])
        
        # Get current values
        cursor.execute(f"SELECT * FROM {table} WHERE {primary_key} = {selected_id}")
        current_data = cursor.fetchone()
        columns = [i[0] for i in cursor.description]
        
        # Create update fields
        new_values = {}
        for i, col in enumerate(columns):
            if col != primary_key:
                new_values[col] = st.text_input(f"Update {col}", value=current_data[i])
        
        if st.button("Update Record"):
            try:
                update_stmt = ", ".join([f"{k} = '{v}'" for k, v in new_values.items()])
                cursor.execute(f"UPDATE {table} SET {update_stmt} WHERE {primary_key} = {selected_id}")
                conn.commit()
                st.success("Record updated successfully!")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    elif operation == "Delete":
        st.subheader(f"Delete from {table.title()}")
        
        # Get primary key for selection
        cursor.execute(f"SHOW KEYS FROM {table} WHERE Key_name = 'PRIMARY'")
        primary_key = cursor.fetchone()[4]
        
        # Get existing records
        cursor.execute(f"SELECT {primary_key} FROM {table}")
        records = cursor.fetchall()
        selected_id = st.selectbox(f"Select {primary_key} to delete", [r[0] for r in records])
        
        if st.button("Delete Record"):
            try:
                cursor.execute(f"DELETE FROM {table} WHERE {primary_key} = {selected_id}")
                conn.commit()
                st.success("Record deleted successfully!")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    conn.close()

# Data Insights Page
elif page == "Data Insights":
    st.title("Data Insights")
    
    conn = create_connection()
    cursor = conn.cursor()
    
    # List of SQL queries
    queries = {
        "Most Popular Cuisines": """
            SELECT cuisine_type, COUNT(*) as restaurant_count
            FROM restaurants
            GROUP BY cuisine_type
            ORDER BY restaurant_count DESC
            LIMIT 10
        """,
        "Customers With Most Cancellation": """
            SELECT c.name, COUNT(*) as cancellation_count
            FROM customers c
            JOIN orders o ON c.customer_id = o.customer_id
            WHERE o.status = 'Cancelled'
            GROUP BY c.customer_id
            ORDER BY cancellation_count DESC
            LIMIT 10
        """,

        "Canceled Orders Count":"""
            SELECT COUNT(order_id) AS canceled_orders
            FROM orders
            WHERE status = 'Cancelled';
        """,

        "Top Restaurants by Revenue": """
            SELECT r.name, SUM(o.total_amount) as total_revenue
            FROM restaurants r
            JOIN orders o ON r.restaurant_id = o.restaurant_id
            GROUP BY r.restaurant_id
            ORDER BY total_revenue DESC
            LIMIT 5
        """,
        "Number of Orders Per Customer": """
            SELECT c.name, COUNT(*) as order_count
            FROM customers c
            JOIN orders o ON c.customer_id = o.customer_id
            GROUP BY c.customer_id
            ORDER BY order_count DESC
        """, 
        "Top Customers by Order Value": """
            SELECT c.name, 
                   COUNT(o.order_id) as order_count,
                   SUM(o.total_amount) as total_spent
            FROM customers c
            JOIN orders o ON c.customer_id = o.customer_id
            GROUP BY c.customer_id
            ORDER BY total_spent DESC
            LIMIT 5
        """,
        "Inactive Restaurants": """
            SELECT r.name, COUNT(o.order_id) as order_count
            FROM restaurants r
            LEFT JOIN orders o ON r.restaurant_id = o.restaurant_id
            WHERE o.order_id IS NULL
            GROUP BY r.restaurant_id
            ORDER BY order_count DESC
            LIMIT 5
        """,
        "Restaurants with Lowest Average Delivery Time": """
            SELECT restaurant_id, name, average_delivery_time
            FROM restaurants
            WHERE is_active = TRUE
            ORDER BY average_delivery_time ASC
            LIMIT 10
        """,
        "Restaurants with Best Ratings": """
            SELECT restaurant_id, name, rating
            FROM restaurants
            WHERE is_active = TRUE
            ORDER BY rating DESC
            LIMIT 10
        """,
        "Total Revenue Generated by Date":"""
            SELECT DATE(order_date) AS order_date, SUM(total_amount) AS total_revenue
            FROM orders
            GROUP BY DATE(order_date)
            ORDER BY order_date DESC
        """,
        "Order Count by Status":"""
            SELECT status, COUNT(order_id) AS order_count
            FROM orders
            GROUP BY status
        """,
        "Average Order Value by Restaurant":"""
            SELECT 
            restaurants.restaurant_id, 
            restaurants.name, 
            AVG(orders.total_amount) AS avg_order_value
            FROM restaurants
            JOIN orders ON restaurants.restaurant_id = orders.restaurant_id
            GROUP BY restaurants.restaurant_id, restaurants.name
            ORDER BY avg_order_value DESC
            LIMIT 15;
        """,
        "Average Feedback Rating by Restaurant":"""
            SELECT r.restaurant_id, r.name, AVG(o.feedback_rating) AS avg_rating
            FROM restaurants r
            JOIN orders o ON r.restaurant_id = o.restaurant_id
            GROUP BY r.restaurant_id, r.name
            ORDER BY avg_rating DESC
        """,
        "Percentage of Premium Customers":"""
            SELECT 
            (SUM(CASE WHEN is_premium = TRUE THEN 1 ELSE 0 END) * 100.0 / COUNT(customer_id)) AS premium_percentage
            FROM customers

        """,
        "Average Delivery Time by Status":"""
            SELECT status, AVG(TIMESTAMPDIFF(HOUR, order_date, delivery_time)) AS avg_delivery_time
            FROM orders
            WHERE delivery_time IS NOT NULL
            GROUP BY status
        """,  
        "Average Discount Applied per Order":"""
           SELECT AVG(discount_applied) AS avg_discount
           FROM orders;
        """,
        "Percentage of Customers with Repeat Orders":"""
            SELECT 
            (SUM(CASE WHEN total_orders > 1 THEN 1 ELSE 0 END) * 100.0) / COUNT(customer_id) AS repeat_customer_percentage
            FROM (
            SELECT customer_id, COUNT(order_id) AS total_orders
            FROM orders
            GROUP BY customer_id
            ) AS customer_orders;
 
            """, 

        "Delivery Fee Breakdown by Vehicle Type":"""
            SELECT vehicle_type, AVG(delivery_fee) AS avg_fee
            FROM deliveries
            GROUP BY vehicle_type
            ORDER BY avg_fee DESC;
        """,    

        "Delivery Efficiency by Delivery Personnel":"""
            SELECT 
            delivery_persons.delivery_person_id, 
            delivery_persons.name, 
            SUM(CASE WHEN deliveries.delivery_time <= deliveries.estimated_time THEN 1 ELSE 0 END) * 100.0 / COUNT(deliveries.delivery_id) AS efficiency_percentage
            FROM deliveries
            JOIN delivery_persons ON deliveries.delivery_person_id = delivery_persons.delivery_person_id
            GROUP BY delivery_persons.delivery_person_id, delivery_persons.name
            ORDER BY efficiency_percentage DESC
            LIMIT 20;
        """,


        "Average Delivery Time by Area": """
            SELECT r.location,
                   AVG(TIMESTAMPDIFF(Hour, o.order_date, d.delivery_time)) as avg_delivery_time
            FROM restaurants r
            JOIN orders o ON r.restaurant_id = o.restaurant_id
            JOIN deliveries d ON o.order_id = d.order_id
            GROUP BY r.location
            ORDER BY avg_delivery_time DESC
        """
    }
    
    # Query selector
    selected_query = st.selectbox("Select Analysis", list(queries.keys()))
    
    # Execute and display results
    try:
        cursor.execute(queries[selected_query])
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=[i[0] for i in cursor.description])
        
        # Display results
        st.subheader("Results")
        st.dataframe(df)
        
        # Visualizations based on query type

        if selected_query == "Most Popular Cuisines":
            fig = px.pie(df, values='restaurant_count', names='cuisine_type', 
                        title='Distribution of Cuisines')
            st.plotly_chart(fig)
        
        elif selected_query == "Order Count by Status":
            fig = px.pie(df, values='order_count', names='status', 
                         title='Delivery Status')
            st.plotly_chart(fig)

        elif selected_query == "Average Delivery Time by Status":
            fig = px.pie(df,values='avg_delivery_time', names='status', title="Delivery Time")
            st.plotly_chart(fig)

    except Exception as e:
        st.error(f"Error executing query: {str(e)}")
    
    conn.close()