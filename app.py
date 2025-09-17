import pandas as pd
import sqlite3
import streamlit as st
import plotly.express as px  

df = pd.read_csv('WA_Fn-UseC_-HR-Employee-Attrition.csv') 

# #  local SQLite database file
conn = sqlite3.connect('hr.db') 
cursor = conn.cursor()
# # Insert DataFrame into SQLite table named 'employee'
# df.to_sql('employee', conn, index=False)

# Confirm insertion
# print(" Data inserted into 'employee' table in hr.db")

# 1 first question: How many employees have not left the company?
print("1 first question: How many employees are there?")
# SQL way
query='''
SELECT COUNT(*) FROM employee WHERE Attrition = 'No';'''
cursor.execute(query)
results = cursor.fetchall() 
print("SQL:", results[0][0])
# Pandas way
employees=df[df['Attrition'] == 'No'].shape[0]
print("Pandas:", employees)



# 2. Second question: What is the employee count for each department?
print("2. Second question: What is the employee count for each department?")
query2 = '''SELECT Department, COUNT(*) as EmployeeCount
FROM employee
GROUP BY Department;'''
cursor.execute(query2)
results = cursor.fetchall() 
print("Employee count in eachtment:")
for department, count in results:
    print(f"{department}: {count}")
# Pandas way
dept_counts = df.groupby('Department').size()
print("Pandas:")
for department, count in dept_counts.items():
    print(f"{department}: {count}")


# 3. Third question: What is the average monthly income for employees in each job role?
print(" 3. Third question: What is the average monthly income for employees in each job role?")
query3 = ''' SELECT JobRole, AVG(MonthlyIncome) as AverageMonthlyIncome FROM employee GROUP BY JobRole; '''
cursor.execute(query3)
results = cursor.fetchall()  
print("Average monthly income for each job role:")
for job_role, avg_income in results:
    print(f"{job_role}: ${avg_income:.2f}")
# Pandas way
avg_income_roles = df.groupby('JobRole')['MonthlyIncome'].mean()
print("Pandas:")
for job_role, avg_income in avg_income_roles.items():
    print(f"{job_role}: ${avg_income:.2f}")


#4.four question: who are the top 5 employees by performance rating?
print("4.four question: who are the top 5 employees by performance rating?")
query4 = ''' SELECT EmployeeNumber, PerformanceRating FROM employee 
ORDER BY PerformanceRating DESC LIMIT 5; '''
cursor.execute(query4)
results = cursor.fetchall()  
print("the top 5 employees by performance rating:")
for emp_num, rating in results:
    print(f"EmployeeNumber: {emp_num}, PerformanceRating: {rating}")
# Pandas way
top5 = df.sort_values('PerformanceRating', ascending=False)[['EmployeeNumber', 'PerformanceRating']].head(5)
print("Pandas:")
for _, row in top5.iterrows():
    print(f"EmployeeNumber: {row['EmployeeNumber']}, PerformanceRating: {row['PerformanceRating']}")


#5. fifth question:which department has the highest average performance rating?
print("5. fifth question:which department has the highest average performance rating?")
query5 = ''' SELECT Department, AVG(PerformanceRating) as AvgPerformanceRating
FROM employee GROUP BY Department ORDER BY AvgPerformanceRating DESC LIMIT 1; '''
cursor.execute(query5)
results = cursor.fetchall()
print("Department with the highest average performance rating:")
for department, avg_rating in results:
    print(f"{department}: {avg_rating:.2f}")
# Pandas way
dept_avg_perf = df.groupby('Department')['PerformanceRating'].mean()
best_dept = dept_avg_perf.idxmax()
best_rating = dept_avg_perf.max()
print("Pandas:")
print(f"{best_dept}: {best_rating:.2f}")

# 6. Attrition rate by job role and department, and which roles/departments have the highest turnover
print("6. Attrition rate by job role and department")
# SQL way
query6 = """
SELECT Department, JobRole,
       ROUND(SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)*100.0/COUNT(*),2) AS AttritionRate
FROM employee
GROUP BY Department, JobRole
ORDER BY AttritionRate DESC;
"""
cursor.execute(query6)
results = cursor.fetchall()
print("SQL:")
for dept, role, rate in results:
    print(f"{dept} - {role}: {rate}%")
# Pandas way
attrition_counts = df.groupby(['Department', 'JobRole'])['Attrition'].value_counts().unstack().fillna(0)
attrition_rate = (attrition_counts['Yes'] / attrition_counts.sum(axis=1) * 100).round(2)
print("Pandas:")
for idx, rate in attrition_rate.sort_values(ascending=False).items():
    print(f"{idx[0]} - {idx[1]}: {rate}%")

# 7. Is there a correlation between monthly income and attrition?
print("7. Correlation between monthly income and attrition")
# SQL way
query7 = """
SELECT Attrition, AVG(MonthlyIncome)
FROM employee
GROUP BY Attrition;
"""
cursor.execute(query7)
results = cursor.fetchall()
print("SQL:")
for attrition, avg_income in results:
    print(f"{attrition}: ${avg_income:.2f}")
# Pandas way
income_by_attrition = df.groupby('Attrition')['MonthlyIncome'].mean()
print("Pandas:")
for attrition, avg_income in income_by_attrition.items():
    print(f"{attrition}: ${avg_income:.2f}")

# 8. How does performance rating relate to attrition?
print("8. Performance rating vs attrition")
# SQL way
query8 = """
SELECT PerformanceRating, Attrition, COUNT(*)
FROM employee
GROUP BY PerformanceRating, Attrition
ORDER BY PerformanceRating DESC;
"""
cursor.execute(query8)
results = cursor.fetchall()
print("SQL:")
for rating, attrition, count in results:
    print(f"PerformanceRating: {rating}, Attrition: {attrition}, Count: {count}")
# Pandas way
perf_attrition = df.groupby(['PerformanceRating', 'Attrition']).size().unstack(fill_value=0)
print("Pandas:")
print(perf_attrition)

# 9. How do Job Role and Overtime status affect employee attrition?
st.subheader("Job Role and Overtime vs Attrition")
# SQL version (optional)
query10 = """
SELECT JobRole, OverTime,
       ROUND(SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)*100.0/COUNT(*),2) AS AttritionRate,
       COUNT(*) AS EmployeeCount
FROM employee
GROUP BY JobRole, OverTime
ORDER BY AttritionRate DESC, EmployeeCount DESC;"""
cursor.execute(query10)
results = cursor.fetchall()
# Convert SQL results to DataFrame for Streamlit
sql_df = pd.DataFrame(results, columns=['JobRole', 'OverTime', 'AttritionRate', 'EmployeeCount'])
st.write("Attrition by Job Role and Overtime (from SQL):")
st.dataframe(sql_df)
# Pandas calculation
job_ot_attrition = (
    df.groupby(['JobRole', 'OverTime'])['Attrition']
      .value_counts()
      .unstack(fill_value=0)
)
job_ot_attrition['EmployeeCount'] = job_ot_attrition.sum(axis=1)
job_ot_attrition['AttritionRate'] = (job_ot_attrition['Yes'] / job_ot_attrition['EmployeeCount'] * 100).round(2)
# Reset index for readability
job_ot_attrition = job_ot_attrition.reset_index()




# Dashboard----------------------------------------------------------#
st.title("HR Employee Attrition Dashboard")

# Show basic dataset info
st.header("Dataset Overview")
st.write(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
st.write("First 5 rows:")
st.dataframe(df.head())

# 1. Employees who have not left
st.subheader("Employees Who Have Not Left")
query = "SELECT COUNT(*) FROM employee WHERE Attrition = 'No';"
cursor = sqlite3.connect('hr.db').cursor()
cursor.execute(query)
not_left = cursor.fetchone()[0]
st.metric("Employees Still With Company", not_left)

# 2. Employee count per department
st.subheader("Employee Count by Department")
query2 = "SELECT Department, COUNT(*) FROM employee GROUP BY Department;"
cursor.execute(query2)
dept_data = cursor.fetchall()
dept_df = pd.DataFrame(dept_data, columns=["Department", "EmployeeCount"])
st.bar_chart(dept_df.set_index("Department"))

# 3. Average monthly income per job role
st.subheader("Average Monthly Income by Job Role")
query3 = "SELECT JobRole, AVG(MonthlyIncome) FROM employee GROUP BY JobRole;"
cursor.execute(query3)
income_data = cursor.fetchall()
income_df = pd.DataFrame(income_data, columns=["JobRole", "AverageMonthlyIncome"])
st.bar_chart(income_df.set_index("JobRole"))

# 4. Top 5 employees by performance rating
st.subheader("Top 5 Employees by Performance Rating")
query4 = "SELECT EmployeeNumber, PerformanceRating FROM employee ORDER BY PerformanceRating DESC LIMIT 5;"
cursor.execute(query4)
top5 = cursor.fetchall()
top5_df = pd.DataFrame(top5, columns=["EmployeeNumber", "PerformanceRating"])
st.table(top5_df)

# 5. Department with highest average performance rating
st.subheader("Department with Highest Average Performance Rating")
query5 = """
SELECT Department, AVG(PerformanceRating) as AvgPerformanceRating
FROM employee GROUP BY Department ORDER BY AvgPerformanceRating DESC LIMIT 1;"""
cursor.execute(query5)
best_dept = cursor.fetchone()
if best_dept:
    st.success(f"{best_dept[0]}: {best_dept[1]:.2f}")

# 6. Attrition Rate by Job Role and Department (Pandas)
attrition_counts = df.groupby(['Department', 'JobRole'])['Attrition'].value_counts().unstack().fillna(0)
# If 'Yes' is not in columns, add it with zeros
if 'Yes' not in attrition_counts.columns:
    attrition_counts['Yes'] = 0
attrition_rate = (attrition_counts['Yes'] / attrition_counts.sum(axis=1) * 100).round(2)
attrition_rate_df = attrition_rate.reset_index().rename(columns={0: 'AttritionRate'})
attrition_rate_df['AttritionRate'] = attrition_rate_df[0] if 0 in attrition_rate_df.columns else attrition_rate_df['AttritionRate']
st.write("Attrition Rate by Job Role and Department ")
st.dataframe(attrition_rate_df[['Department', 'JobRole', 'AttritionRate']].sort_values('AttritionRate', ascending=False))

# 7. Is there a correlation between monthly income and attrition?
st.subheader("Average Monthly Income by Attrition Status ")
income_by_attrition = df.groupby('Attrition')['MonthlyIncome'].mean().reset_index()
income_by_attrition['MonthlyIncome'] = income_by_attrition['MonthlyIncome'].round(2)
st.dataframe(income_by_attrition)
# Optional: Visualize with a bar chart
st.bar_chart(income_by_attrition.set_index('Attrition'))

# 8. How does performance rating relate to attrition?
st.subheader("Performance Rating vs Attrition ")
perf_attrition = df.groupby(['PerformanceRating', 'Attrition']).size().unstack(fill_value=0).reset_index()
st.dataframe(perf_attrition)
# Optional: Visualize with a bar chart
st.bar_chart(perf_attrition.set_index('PerformanceRating'))

# 9. Job Role and Overtime status affect employee attrition
# Show Pandas results
st.write("Attrition by Job Role and Overtime ")
st.dataframe(job_ot_attrition[['JobRole', 'OverTime', 'AttritionRate', 'EmployeeCount']].sort_values('AttritionRate', ascending=False))

# Visualization: Bar chart using Plotly
import plotly.express as px
fig = px.bar(
    job_ot_attrition,
    x='JobRole',
    y='AttritionRate',
    color='OverTime',
    barmode='group',
    text='AttritionRate',
    title='Attrition Rate by Job Role and Overtime'
)
st.plotly_chart(fig)


#--------filter--------------------------------------#
# Add a dropdown to select department
st.subheader("Filter Employees by Department")
departments = df['Department'].unique()
selected_dept = st.selectbox("Select Department", departments)

# filter using SQL query
query = "SELECT * FROM employee WHERE Department = ?"
conn = sqlite3.connect('hr.db')
cursor = conn.cursor()
cursor.execute(query, (selected_dept,))
filtered_sql = cursor.fetchall()
# ✅ get real column names from SQLite
col_names = [description[0] for description in cursor.description]
filtered_sql_df = pd.DataFrame(filtered_sql, columns=col_names)
st.write(f"Employees in {selected_dept} Department (from DB):")
st.dataframe(filtered_sql_df)




# -------- Add New Employee Form -------- #
st.header("Add New Employee")

with st.form("add_employee_form"):
    emp_num = st.number_input("Employee Number", min_value=1, step=1)
    age = st.number_input("Age", min_value=18, max_value=100, step=1)
    gender = st.selectbox("Gender", ["Male", "Female"])
    department = st.selectbox("Department", df['Department'].unique())
    job_role = st.selectbox("Job Role", df['JobRole'].unique())
    monthly_income = st.number_input("Monthly Income", min_value=0, step=100)
    performance_rating = st.selectbox("Performance Rating", [1, 2, 3, 4])
    attrition = st.selectbox("Attrition", ["Yes", "No"])
    submit_btn = st.form_submit_button("Add Employee")
    if submit_btn:
        # Insert new employee into database
        insert_query = """
        INSERT INTO employee (EmployeeNumber, Age, Gender, Department, JobRole, MonthlyIncome, PerformanceRating, Attrition)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        try:
            conn = sqlite3.connect('hr.db')
            cursor = conn.cursor()
            cursor.execute(insert_query, (
                emp_num, age, gender, department, job_role, monthly_income, performance_rating, attrition
            ))
            conn.commit()
            st.success("New employee added successfully!")
            cursor.close()
            conn.close()
        except Exception as e:
            st.error(f"Error adding employee: {e}")

# -------- Update Employee Income -------- #
st.header("Update Employee Monthly Income")

with st.form("update_income_form"):
    emp_num_update = st.number_input("Enter Employee Number to Update", min_value=1, step=1)
    new_income = st.number_input("New Monthly Income", min_value=0, step=100)
    update_btn = st.form_submit_button("Update Income")
    if update_btn:
        update_query = """
        UPDATE employee SET MonthlyIncome = ? WHERE EmployeeNumber = ?
        """
        try:
            conn = sqlite3.connect('hr.db')
            cursor = conn.cursor()
            cursor.execute(update_query, (new_income, emp_num_update))
            conn.commit()
            if cursor.rowcount > 0:
                st.success(f"Employee #{emp_num_update}'s income updated to {new_income}.")
            else:
                st.warning("Employee number not found.")
            cursor.close()
            conn.close()
        except Exception as e:
            st.error(f"Error updating income: {e}")




# print("First 5 rows:")
# print(df.head())

# print(f"\n Shape of dataset: {df.shape[0]} rows × {df.shape[1]} columns")

# print("\n Info:")
# print(df.info())

# print("\n Missing values per column:")
# print(df.isnull().sum())

# print("\n Duplicates:", df.duplicated().sum())

# print("\n Summary stats:")
# print(df.describe())







