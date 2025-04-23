# Zomato-Data-Insights

1. Overview of the Application:
The application is a Food Delivery Management System built using Streamlit and a database like MySQL. It allows users to manage customers, restaurants, orders, delivery persons, deliveries, and generate fake data for testing.

2. Menu Navigation:
The app's sidebar provides options to navigate between different sections of the system, such as "Home", "Manage Customers," "Manage Restaurants," "Manage Orders", "Manage Delivery Persons", "Manage Deliveries", "Insights", "Data Exploration" and "Generate Fake Data".

3. Streamlit Interface:
Streamlit is used to create an interactive web application with components like st.selectbox, st.text_area, st.button, and st.write for rendering input fields, displaying information, and handling user actions.

4. Database Interaction:
The application interacts with a relational database like MySQL to perform CRUD operations and execute SQL queries. It utilizes self.cursor.execute() to run queries and self.cursor.fetchall() to fetch results.

5. Predefined Queries:
Predefined SQL queries are stored in a dictionary (queries), allowing users to select and execute common queries from a dropdown. This simplifies the user experience by eliminating the need to write SQL manually.

6. General Query Execution:
Users can also execute custom SQL queries using a st.text_area input field. The query results are displayed in the app.

7. Fake Data Generation:
The generate_fake_data method is designed to populate the database with fake data. This includes random customer information, restaurant details, orders, and deliveries using the Faker library for generating fake data.

8. Customer Data Generation:
Fake customer data is generated, including fields like name, email, phone number, location, signup date, premium status, preferred cuisine, and ratings.

9. Restaurant Data Generation:
Similar to customers, fake restaurant data is created, including fields like restaurant name, cuisine type, location, owner name, contact number, rating, and active status.

10. Order Data Generation:
The app also generates order records associated with customers and restaurants. Fields include order date, delivery time, order status, total amount, and customer feedback.

11. Delivery Data Generation:
Delivery records are generated with delivery person ID, delivery status, distance, delivery time, estimated time, and vehicle type.

12. Randomized Data:
Randomized data, such as premium status, cuisine types, payment modes, etc., is chosen from predefined lists using rd.choice() and rd.randint(). This adds variety to the generated data.

13. Commit Changes:
After generating the fake data, changes are committed to the database using self.db_connection.commit(). This ensures the data is saved permanently.

14. Error Handling:
The code includes exception handling (using try-except blocks) to catch errors during SQL execution or data generation. Errors are displayed using st.error().

15. Check for Existing Data:
Before generating fake data, the app ensures there are existing delivery persons in the database. If not, it returns an error message: st.error("No delivery persons available in the database.").

16. Dynamic Data Insertion:
Data is dynamically inserted into the database, ensuring that each record (customer, restaurant, order, delivery) is linked appropriately through IDs (like customer_id, restaurant_id, etc.).

17. Last Row ID:
For every new record inserted, the app captures the last inserted ID using self.cursor.lastrowid. This is crucial for linking related records (e.g., associating orders with customers).

18. Real-time Data Feedback:
The results of SQL query execution are displayed in real-time using st.write(), allowing users to immediately view the output of their actions.

19. Commit Rollback on Error:
In case of an error, data changes are rolled back to maintain data integrity using self.db_connection.rollback().

20. Instructions to Run the Project:
Install Dependencies: Install necessary libraries using pip install -r requirements.txt (Faker, Streamlit, and database connector).
Set Up Database: Configure the database and create the necessary tables (Customers, Restaurants, Orders, Deliveries, etc.).
Run the Application: Start the app by running streamlit run app.py. The app will open in the browser, allowing interaction via the sidebar and query execution.
