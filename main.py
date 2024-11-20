import os
import re
import sqlite3
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_gemini_response(question,prompt):
    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content([prompt[0],question])
    return response.text

def retrieval(sql_query,db):
    try:
        conn=sqlite3.connect(db)
        cur=conn.cursor()
        cur.execute(sql_query)
        rows=cur.fetchall()
    except sqlite3.Error as e:
        print(e)
        rows=[]
    finally:
        conn.commit()
        conn.close()
    return rows

prompt="""
You are an intelligent assistant designed to retrieve data from a database called student.db using SQL queries. The database contains a table named student with the following schema:
The sql code  should not have any "```" in beginning or end and sql word in the output.

roll (INTEGER, PRIMARY KEY): Unique identifier for each student.
name (VARCHAR): Name of the student.
branch (VARCHAR): Branch of study (e.g., CSE, ECE, ME).
semester (INTEGER): Current semester of the student.
CGPA (REAL): Current CGPA of the student.

Instructions:
You will be given a natural language query.
You will only generate the command without using any sql in the output.
The sql code  should not have any "```" in beginning or end and sql word in the output.
Translate the query into an SQL statement to retrieve the required data.
Respond with the SQL query and explain the output it retrieves.
If the query is invalid or ambiguous, provide a clarifying question.

For example:
Example 1: How many entries of records are present?, the SQL command will be something like this - SELECT COUNT(*) FROM STUDENT ;
Example 2 Tell me the details of all the students studying in CSE class?, the SQL command will be something like this - SELECT * FROM STUDENT where CLASS="Data Science";
"""

# streamlit
st.title("Gemini Pro Chatbot Assistant to communicate with SQL Database")
question=st.text_input("Ask a question",key="input")
submit=st.button("Submit")
if submit:
    response=get_gemini_response(question,prompt)
    sql_pattern=r"(SELECT|INSERT|UPDATE|DELETE)\s.+?;"
    data=re.search(sql_pattern, response, re.IGNORECASE)
    print(data.group())
    query=data.group() if data else None
    retrieved_data=retrieval(query, "student.db")
    st.subheader("Response from Gemini Pro Chatbot Assistant")
    print(retrieved_data)
    st.markdown(f"```sql\n{response}\n```")
    st.subheader("Data retrieved from the database")
    st.markdown(f"```sql\n{retrieved_data}\n```")
        
# show me all the records in my student database