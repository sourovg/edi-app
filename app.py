import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os
#import subprocess
from analytics.pyspark_tasks import analyze_data
# Load environment variables from .env
from dotenv import load_dotenv
load_dotenv()

import logging
logging.basicConfig(level=logging.DEBUG)

# Access the DB_PATH variable
#db_path = "./data/education_app.db"  #direct
#db_path = os.getenv("DB_PATH") #issue with abosolute path 
db_path = os.path.abspath(os.getenv("DB_PATH")) # Default to ./data/education_app.db if not set
print(f"Database path: {db_path}")

jdbc_path = os.path.abspath(os.getenv("JDBC_PATH"))
#jdbc_path = st.secrets["JDBC_PATH"]
print(f"JDBC Path: {jdbc_path}")

# Connect to SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Streamlit Navigation
st.sidebar.title("Education App")
page = st.sidebar.radio("Navigate", ["Student Progress", "Psychometric Insights", "Teacher Dashboard"])

# Student Progress Page
if page == "Student Progress":
    st.title("Student Progress Tracker")
    
    # Fetch student progress data
    query = "SELECT * FROM progress"
    data = pd.read_sql_query(query, conn)
    
    st.write("Student Performance Data")
    st.dataframe(data)
    
    # Visualize progress (example: subject-wise scores)
    st.write("Progress Visualization")
    plt.figure(figsize=(10, 6))
    data.groupby('subject')['score'].mean().plot(kind='bar')
    st.pyplot(plt)
    
    # Write PySpark results / Analytics 
    #st.write("Avg. Score by Subject")
    ##result = subprocess.check_output(['python', 'pyspark/pyspark_tasks.py'])
    # try:
    #     result = analyze_data()
    #     # for subject, avg_score in result:
    #     #     st.write(f"{subject}: {avg_score:.2f}")
    #     st.write(result)
    # except Exception as e:
    #     st.error(f"Error running PySpark task: {e}")
    ##st.text(result.decode())
    
# Psychometric Insights Page
elif page == "Psychometric Insights":
    st.title("Psychometric and Behavioral Insights")
    
    # Dummy data visualization
    st.write("Sample Behavioral Trends")
    insights = pd.read_sql_query("SELECT * FROM psychometrics", conn)
    st.dataframe(insights)
    
    # Example visualization
    plt.figure(figsize=(10, 6))
    insights.groupby('trait')['score'].mean().plot(kind='pie', autopct='%1.1f%%')
    st.pyplot(plt)

# Teacher Dashboard Page
elif page == "Teacher Dashboard":
    st.title("Teacher Dashboard")
    
    # Display all students with performance data
    st.write("Student Summary")
    students = pd.read_sql_query("SELECT * FROM students", conn)
    st.dataframe(students)
    
    # Update student notes (mock) - Allow users (e.g. teachers) to update the database via Streamlite!
    st.write("Add Teacher Notes")
    student_id = st.selectbox("Select Student ID", students['id'])
    note = st.text_area("Enter Notes")
    if st.button("Save Note"):
        cursor.execute("UPDATE students SET notes = ? WHERE id = ?", (note, student_id))
        conn.commit()
        st.success("Notes updated!")

# Additional pages follow a similar structure...

# Streamlit Widgets:
# Use widgets like sliders, text inputs, and dropdowns to enhance interactivity:

# student_id = st.selectbox("Select Student ID", options=data['student_id'].unique())
# new_note = st.text_area("Enter Teacher Notes")
# if st.button("Save Note"):
#     # Save notes logic
#     pass

# Integrate SQLite into Streamlit:
# Use sqlite3 to query the database and display results dynamically in Streamlit:
# def fetch_students():
#     query = "SELECT * FROM students"
#     return pd.read_sql_query(query, conn)

# # Query data
# cursor = conn.cursor()
# cursor.execute("SELECT * FROM students")
# students = cursor.fetchall()
# print(students)  # [(1, 'John Doe', '5th', '')]