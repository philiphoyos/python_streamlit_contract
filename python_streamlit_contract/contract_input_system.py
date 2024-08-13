import streamlit as st
from datetime import datetime
import sqlite3

# Database setup
conn = sqlite3.connect('contracts.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''
CREATE TABLE IF NOT EXISTS contracts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    start_date TEXT,
    end_date TEXT,
    value REAL,
    party_a_name TEXT,
    party_a_email TEXT,
    party_b_name TEXT,
    party_b_email TEXT
)
''')
conn.commit()

# Title of the app
st.title("User Contract Input System")

# Input fields for the contract
st.header("Enter Contract Details")

contract_title = st.text_input("Contract Title", "")
contract_description = st.text_area("Contract Description", "")
start_date = st.date_input("Start Date", datetime.today())
end_date = st.date_input("End Date", datetime.today())
contract_value = st.number_input("Contract Value", min_value=0.0, step=0.01)

# Input fields for the parties involved
st.header("Party A Details")
party_a_name = st.text_input("Party A Name", "")
party_a_email = st.text_input("Party A Email", "")

st.header("Party B Details")
party_b_name = st.text_input("Party B Name", "")
party_b_email = st.text_input("Party B Email", "")

# Submit button and data saving
if st.button("Submit Contract"):
    # Insert the contract data into the SQLite database
    c.execute('''
    INSERT INTO contracts (title, description, start_date, end_date, value, party_a_name, party_a_email, party_b_name, party_b_email)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (contract_title, contract_description, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), contract_value, party_a_name, party_a_email, party_b_name, party_b_email))
    
    conn.commit()

    st.success("Contract details submitted successfully!")
    
    # Display the contract summary
    st.subheader("Contract Summary")
    st.write("### Contract Title")
    st.write(contract_title)
    st.write("### Contract Description")
    st.write(contract_description)
    st.write("### Contract Duration")
    st.write(f"Start Date: {start_date}")
    st.write(f"End Date: {end_date}")
    st.write("### Contract Value")
    st.write(f"${contract_value}")
    st.write("### Party A")
    st.write(f"Name: {party_a_name}")
    st.write(f"Email: {party_a_email}")
    st.write("### Party B")
    st.write(f"Name: {party_b_name}")
    st.write(f"Email: {party_b_email}")

# View all contracts in the database
if st.button("View All Contracts"):
    st.subheader("All Contracts")
    c.execute("SELECT * FROM contracts")
    rows = c.fetchall()
    for row in rows:
        st.write(f"ID: {row[0]}, Title: {row[1]}, Start Date: {row[3]}, End Date: {row[4]}, Value: ${row[5]}")
        st.write(f"Party A: {row[6]} ({row[7]})")
        st.write(f"Party B: {row[8]} ({row[9]})")
        st.write("---")

# Close the connection when done
conn.close()
