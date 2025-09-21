# imports libraruies
import pandas as pd
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv('WA_Fn-UseC_-HR-Employee-Attrition.csv') 

# #  local SQLite database file
conn = sqlite3.connect('hr.db') 
cursor = conn.cursor()
# # Insert DataFrame into SQLite table named 'employee'
df.to_sql('employee', conn, index=False, if_exists='replace')  # replace table if it exists
# Confirm insertion
# print(" Data inserted into 'employee' table in hr.db")

################### SQL queries and pandas operations analysis ###################

# 1 first question: How many employees have not left the company?
print(f"1 first question: How many employees are there?")
# SQL way
query='''SELECT COUNT(*) FROM employee WHERE Attrition = 'No';'''
cursor.execute(query)
results = cursor.fetchall() 
print(f"SQL: {results[0][0]}  employees")
# Pandas way
employees=df[df['Attrition'] == 'No'].shape[0]
print(f"Pandas:{ employees}  employees")



# 2. Second question: What is the employee count for each department?
print("2. Second question: What is the employee count for each department?")
#sql way
query2 = '''SELECT Department, COUNT(*) as EmployeeCount
FROM employee
GROUP BY Department;'''
cursor.execute(query2)
results = cursor.fetchall() 
print("Employee count in each Department:(SQL)")
for department, count in results:
    print(f"{department}: {count}")
# Pandas way
dept_counts = df.groupby('Department').size()
print("(Pandas) Employee count in each Department:")
for department, count in dept_counts.items():
    print(f"{department}: {count}")


# 3. Third question: What is the average monthly income for employees in each job role?
print(" 3. Third question: What is the average monthly income for employees in each job role?")
#SQL way
query3 = ''' SELECT JobRole, AVG(MonthlyIncome) as AverageMonthlyIncome FROM employee GROUP BY JobRole; '''
cursor.execute(query3)
results = cursor.fetchall()  
print("(SQL) Average monthly income for each job role:")
for job_role, avg_income in results:
    print(f"{job_role}: ${avg_income:.2f}")
# Pandas way
avg_income_roles = df.groupby('JobRole')['MonthlyIncome'].mean()
print("Pandas:")
for job_role, avg_income in avg_income_roles.items():
    print(f"{job_role}: ${avg_income:.2f}")


#4.four question: who are the top 5 employees by performance rating?
print("4.four question: who are the top 5 employees by performance rating?")
#sql way
query4 = ''' SELECT EmployeeNumber, PerformanceRating FROM employee 
ORDER BY PerformanceRating DESC LIMIT 5; '''
cursor.execute(query4)
results = cursor.fetchall()  
print("(SQL) the top 5 employees by performance rating:")
for emp_num, rating in results:
    print(f"EmployeeNumber: {emp_num}, PerformanceRating: {rating}")
# Pandas way
top5 = df.sort_values('PerformanceRating', ascending=False)[['EmployeeNumber', 'PerformanceRating']].head(5)
print("Pandas:")
for _, row in top5.iterrows():
    print(f"EmployeeNumber: {row['EmployeeNumber']}, PerformanceRating: {row['PerformanceRating']}")


#5. fifth question:which department has the highest average performance rating?
print("5. fifth question:which department has the highest average performance rating?")
#SQL eay
query5 = ''' SELECT Department, AVG(PerformanceRating) as AvgPerformanceRating
FROM employee GROUP BY Department ORDER BY AvgPerformanceRating DESC LIMIT 1; '''
cursor.execute(query5)
results = cursor.fetchall()
print(" (SQL) Department with the highest average performance rating:")
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
ORDER BY AttritionRate DESC;"""
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
query7 = """SELECT Attrition, AVG(MonthlyIncome)
FROM employee 
GROUP BY Attrition;"""
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
query8 = """SELECT PerformanceRating, Attrition, COUNT(*)
FROM employee
GROUP BY PerformanceRating, Attrition
ORDER BY PerformanceRating DESC;"""
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
print("9. How do Job Role and Overtime status affect employee attrition? (SQL Way)")
query_sql = """
SELECT JobRole, OverTime,
       ROUND(SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)*100.0/COUNT(*),2) AS AttritionRate,
       COUNT(*) AS EmployeeCount
FROM employee
GROUP BY JobRole, OverTime
ORDER BY AttritionRate DESC, EmployeeCount DESC;
"""
print("SQL: ")
cursor.execute(query_sql)
sql_results = cursor.fetchall()
sql_df = pd.DataFrame(sql_results, columns=['JobRole', 'OverTime', 'AttritionRate', 'EmployeeCount'])
print(sql_df)
#Pandas way
print("Pandas Way: ")
job_ot_attrition = (
    df.groupby(['JobRole', 'OverTime'])['Attrition']
      .value_counts()
      .unstack(fill_value=0)
)
job_ot_attrition['EmployeeCount'] = job_ot_attrition.sum(axis=1)
job_ot_attrition['AttritionRate'] = (job_ot_attrition['Yes'] / job_ot_attrition['EmployeeCount'] * 100).round(2)
job_ot_attrition = job_ot_attrition.reset_index()
print(job_ot_attrition[['JobRole', 'OverTime', 'AttritionRate', 'EmployeeCount']])


# Connect to database
def get_connection():
    return sqlite3.connect('hr.db')

# Load employees from DB
def load_employees():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM employee", conn)
    conn.close()
    return df

# --- Prepare dataset for ML ---
ml_df = df.copy()

# Encode categorical columns
cat_cols = ml_df.select_dtypes(include=['object']).columns
for col in cat_cols:
    ml_df[col] = LabelEncoder().fit_transform(ml_df[col])

X = ml_df.drop('Attrition', axis=1)
y = ml_df['Attrition']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# --- Train Random Forest model ---
rf = RandomForestClassifier(n_estimators=200, random_state=42)
rf.fit(X_train, y_train)

y_pred = rf.predict(X_test)

# --- Metrics ---
acc = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred, target_names=['Stay','Leave'], output_dict=True)
report_df = pd.DataFrame(report).transpose()

cm = confusion_matrix(y_test, y_pred)
cm_df = pd.DataFrame(cm, index=['Actual Stay','Actual Leave'], columns=['Pred Stay','Pred Leave'])


# Feature importance
feat_importance = pd.DataFrame({
    'Feature': df.drop('Attrition', axis=1).columns,
    'Importance': rf.feature_importances_
}).sort_values(by='Importance', ascending=False)


conn.close()







