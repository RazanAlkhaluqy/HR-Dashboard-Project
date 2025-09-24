
# =========================
# HR Attrition Dashboard
# =========================
# This Streamlit app provides a professional HR dashboard for analyzing employee attrition,
# department/job role breakdowns, and predictive analytics using machine learning.
# It uses SQLite for persistent storage and pandas for data manipulation.
# =========================

# --- Import Libraries ---
import pandas as pd
import sqlite3
import streamlit as st
import plotly.express as px  
import plotly.graph_objects as go 
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# --- Streamlit Page Configuration ---
# Set up the Streamlit page with a wide layout, custom title, and sidebar menu links.
st.set_page_config(
    layout="wide",
    page_title="Professional HR Attrition Dashboard",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.yourwebsite.com/help',
        'Report a bug': "https://www.yourwebsite.com/bug",
        'About': "# This is a highly professional HR Attrition Dashboard!"
    }
)

# --- Custom Color Palettes ---
# Define custom color gradients and STC purple shades for consistent branding and visual appeal.
CUSTOM_PURPLE_RED_GRADIENT = [
    "#661B6E",  # Very light purple for lowest attrition
    "#9F7BC4",  # Medium purple
    "#CFB8C8",  # A bit more vibrant purple
    '#FF6961',  # Light red, transitioning
    "#D23737"   # Strong red for highest attrition
]
STC_PURPLE = '#7B3F9B' 
STC_PURPLE_LIGHT = '#B08BCF' 
STC_PURPLE_DARK = '#4F2A66'
STC_PURPLE_GRADIENT = [STC_PURPLE_DARK, STC_PURPLE, STC_PURPLE_LIGHT] # For continuous scales

# --- Custom CSS Styling ---
# Inject custom CSS for a modern, clean, and branded look (inspired by Humanet design).
# Styles sidebar, headers, section boxes, metrics, forms, buttons, expanders, and more.
st.markdown(f"""
    <style>
    
            /* Main app container */
     .stApp {{
         background-color: #F0F2F6; /* Light gray background, matches Humanet */
         color: #333333; /* Darker text */     
     }}
    
     /* --- Sidebar Styling --- */
     /* Target the sidebar container directly */
     .st-emotion-cache-1na27gl {{ /* This class targets the sidebar in recent Streamlit versions */
        /* background-color: white;  White sidebar background */
        box-shadow: 2px 0 5px rgba(0,0,0,0.05); /* Subtle shadow for depth */
         padding: 20px;
         border-radius: 0 10px 10px 0; /* Rounded right corners for the sidebar */
         position: fixed; /* Keep sidebar fixed */
         height: 100vh; /* Full height */
         overflow-y: auto; /* Enable scrolling if content overflows */
     }}
            
             /*  Stable sidebar background styling */
     div[data-testid="stSidebar"] {{
         background-color: white !important;
         padding: 20px;
         box-shadow: 2px 0 5px rgba(0,0,0,0.05);
         border-radius: 0 10px 10px 0;
     }}
            
    /* Sidebar header/title */
     .st-emotion-cache-1xp33y9 {{ /* Adjust spacing for the sidebar header if needed */
         margin-bottom: 20px;
         border: 1px solid #E0E0E0;
     }}
     /* Sidebar expander styling */
     .st-emotion-cache-p2w58t .st-emotion-cache-vk33gh {{ /* Targets the expander header */
         background-color: #FFFFFF; /* White background for expander */
         border-radius: 8px; /* Rounded corners */
         padding: 10px;
         margin-bottom: 5px;
         border: none; /* Remove default border */
         box-shadow: 0 1px 3px rgba(0,0,0,0.05); /* Subtle shadow */
         border-left: 4px solid {STC_PURPLE}; /* Purple accent bar */
         font-weight: 600;
        color: #333333;
     }}
     .st-emotion-cache-p2w58t .st-emotion-cache-vk33gh:hover {{
         background-color: #F5F5F5; /* Slightly darker on hover */
     }}
     /* Sidebar links within expanders */
     .st-emotion-cache-p2w58t div[data-testid="stMarkdownContainer"] a {{
         color: #555555; /* Darker link color */
         padding: 5px 0 5px 15px; /* Indent links */
         display: block; /* Make links block level for padding */
         text-decoration: none; /* No underline */
     }}
     .st-emotion-cache-p2w58t div[data-testid="stMarkdownContainer"] a:hover {{
         color: {STC_PURPLE}; /* Purple on hover */
         background-color: #E6F0F8; /* Light blue background on hover (can change to light purple if preferred) */
         border-radius: 5px;
     }}
    
     /* --- Main Content Styling --- */
    
     /* Headers */
     h1, h2, h3, h4, h5, h6 {{
         color: #0E1117; /* Streamlit's default dark blue/black for headers, but keep it clean */
         font-weight: 600;
         margin-top: 25px;
         margin-bottom: 15px;
         padding-bottom: 5px;
         border-bottom: none; /* Remove default border */
     }}
     h2 {{
         font-size: 1.8em;
         color: #333333;
     }}
     h3 {{
         font-size: 1.4em;
         color: #444444;
     }}
     
     /* Subheader borders - adjusted to be more subtle */
     h3 {{
         border-bottom: 1px solid #E0E0E0;
         padding-bottom: 10px;
         margin-bottom: 20px;
    }} 
            
     /* Section Boxes (for forms or general content blocks) */
     .section-box {{
         border: 1px solid #E0E0E0; /* Lighter border color */
         border-radius: 12px;            /* rounded corners */
         padding: 1.5rem;                /* inside spacing */
         margin-bottom: 1.5rem;          /* space below box */
         background-color: #FFFFFF;      /* White background */
         box-shadow: 0 4px 10px rgba(0,0,0,0.03); /* Softer shadow */
     }}

     /* --- Metric Cards (Top Row) --- */
     /* Target the container for st.metric directly */
     div[data-testid="stMetric"] {{ 
         background-color: #FFFFFF;
         border-radius: 10px; /* Rounded corners, matches Humanet */
         box-shadow: 0 2px 8px rgba(0,0,0,0.08); /* More prominent shadow for metrics */
         padding: 20px;
         text-align: left; /* Align text left */
         border: 1px solid #E0E0E0; /* Subtle border */
         margin-bottom: 15px; /* Space between rows */
     }}
     /* Metric label */
     div[data-testid="stMetric"] label p {{
         font-size: 0.9em; /* Smaller label font */
         color: #666666; /* Lighter color */
         font-weight: 500;
         margin-bottom: 5px;
     }}
     /* Metric value */
     div[data-testid="stMetric"] .st-emotion-cache-1f812w3 {{ /* Target the value itself */
         font-size: 2.2em; /* Larger value font */
         font-weight: 700;
         color: #333333; /* Darker color */
     }}
     /* Metric delta */
     div[data-testid="stMetric"] .st-emotion-cache-1m6a02v {{ /* Target the delta value */
         font-size: 0.9em;
         font-weight: 600;
     }}
       
     /* Button styling */
     .stButton > button {{
         background-color: {STC_PURPLE}; /* STC Purple */
         color: white;
         padding: 10px 20px;
         border-radius: 8px; /* Slightly more rounded */
         border: none;
         cursor: pointer;
         font-weight: bold;
        transition: background-color 0.3s ease; /* Smooth transition */
     }}
     .stButton > button:hover {{
         background-color: {STC_PURPLE_DARK}; /* Darker purple on hover */
     }}
            
     /* Red button specifically for delete */
     div[data-testid="stForm"] .stButton > button[kind="secondary"] {{
         background-color: #E74C3C; /* Red for delete */
     }}
     div[data-testid="stForm"] .stButton > button[kind="secondary"]:hover {{
         background-color: #C0392B; /* Darker red on hover */
     }}
     /* Expander styling (for main content expanders) */
     div[data-testid="stExpander"] {{
        border: 1px solid #E0E0E0; /* Subtle border */
         border-radius: 10px; /* Rounded corners */
         background-color: #FFFFFF; /* White background */
         box-shadow: 0 2px 5px rgba(0,0,0,0.05); /* Subtle shadow */
         margin-bottom: 15px;
     }}
     div[data-testid="stExpander"] .st-emotion-cache-vk33gh {{ /* Expander header */
         background-color: #F8F9FA; /* Light gray header */
         border-bottom: 1px solid #E0E0E0;
         border-radius: 10px 10px 0 0; /* Only top corners rounded */
         padding: 15px;
         font-weight: 600;
         color: #333333;
     }}
     div[data-testid="stExpander"] .st-emotion-cache-vk33gh:hover {{
         background-color: #EFF2F5;
     }}

     /* Dataframe styling */
     .stDataFrame {{
         border: 1px solid #E0E0E0; 
         border-radius: 10px; /* Rounded corners */
         overflow: hidden; 
         box-shadow: 0 2px 5px rgba(0,0,0,0.05); 
     }}

     /* Info/Success/Warning blocks */
     div[data-testid="stBlock"] div[data-testid="stAlert"] {{
        border-radius: 8px;
         border: none; /* Remove default alert border */
         box-shadow: 0 2px 5px rgba(0,0,0,0.05);
     }}
     /* Plotly chart container styling */
      .st-emotion-cache-1ht1j85 {{ /* Targets the block container for charts */
         padding: 1.5rem; /* More padding */
         background-color: #FFFFFF; /* Ensure white background */
         border-radius: 10px; /* Rounded corners */
         box-shadow: 0 2px 8px rgba(0,0,0,0.08); /* Prominent shadow for charts */
         border: 1px solid #E0E0E0; /* Border for charts */
         margin-bottom: 1.5rem; /* Space between chart boxes */
     }}
     /* Plotly chart titles */
     .plotly .plot-container .modebar .g-gtitle {{ /* Targeting Plotly title element */
         font-weight: 600 !important;
         color: #333333 !important;
     }}
            
     /* Style for text and number input boxes */
    input[type="number"], input[type="text"] {{
         background-color: #F8F9FA !important; /* Light gray background */
         border: 1px solid #D0D4D9 !important; /* Subtle border */
         border-radius: 8px !important;
         padding: 8px 12px !important;
         font-size: 14px !important;
         color: #333 !important;
         width: 100% !important;
        box-shadow: inset 0 1px 2px rgba(0,0,0,0.05); /* Inner shadow */
         transition: border-color 0.2s ease, box-shadow 0.2s ease;
     }}
     input[type="number"]:focus, input[type="text"]:focus {{
         border-color: {STC_PURPLE} !important; /* Purple border on focus */
         box-shadow: inset 0 1px 2px rgba(0,0,0,0.05), 0 0 0 0.15rem rgba(123, 63, 155, 0.25) !important; /* Focus ring with purple */
         outline: none !important;
     }}

     /* Style for Streamlit selectbox and radio (visible part) */
     .stSelectbox > div, .stRadio > div {{
         background-color: #F8F9FA !important;
         border: 1px solid #D0D4D9 !important;
         border-radius: 8px !important;
         padding: 6px 10px !important;
         font-size: 14px !important;
         color: #333 !important;
         width: 100% !important;
         box-shadow: inset 0 1px 2px rgba(0,0,0,0.05);
         transition: border-color 0.2s ease, box-shadow 0.2s ease;
     }}
     .stSelectbox > div:focus-within, .stRadio > div:focus-within {{ /* Use focus-within for selectbox container */
         border-color: {STC_PURPLE} !important;
         box-shadow: inset 0 1px 2px rgba(0,0,0,0.05), 0 0 0 0.15rem rgba(123, 63, 155, 0.25) !important;
         outline: none !important;
     }}

     /* Optional: Make entire dropdown label match */
     label {{
         font-weight: 500 !important;
         color: #333333 !important;
         margin-bottom: 5px !important;
     }}
    
     /* Small adjustment for the form elements to give them space */
     .st-emotion-cache-p5m1k4 {{ /* This targets the element that wraps form inputs */
         margin-bottom: 1rem;
     }}


    </style>
""", unsafe_allow_html=True)

# --- Global Variables & Setup ---
DB_NAME = 'data/hr.db'  # SQLite database file
CSV_PATH = 'data/WA_Fn-UseC_-HR-Employee-Attrition.csv'  # Source CSV for initial data

# --- Database Connection (Cached) ---
# Use Streamlit's resource cache to persist the SQLite connection across reruns.
@st.cache_resource
def get_connection():
    return sqlite3.connect(DB_NAME , check_same_thread=False)

# --- Data Loading (Cached) ---
# Loads data from CSV, ensures the SQLite table is populated, and returns a DataFrame.
@st.cache_data
def load_data():
    try:
        df = pd.read_csv(CSV_PATH)
        # Ensure 'hr.db' exists and 'employee' table is populated
        conn = get_connection() # Get connection from cache
        df.to_sql('employee', conn, if_exists='replace', index=False)
        # No need to close conn here as it's a cached resource
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}. Please ensure '{CSV_PATH}' is in the same directory.")
        return pd.DataFrame() # Return empty DataFrame on error

# --- Load Data ---
df = load_data()
if df.empty:
    st.stop() # Stop if data loading failed

# --- SQL Cursor Setup ---
conn = get_connection()
cursor = conn.cursor()

# --- Session State Initialization ---
# Store employee DataFrame in session state for interactive operations (add/update/delete).
if 'employees_df' not in st.session_state:
    st.session_state.employees_df = pd.read_sql("SELECT * FROM employee", conn)

# --- Helper: Refresh Employee Data ---
def refresh_employees_df():
    # Reload employee data from the database into session state.
    st.session_state.employees_df = pd.read_sql("SELECT * FROM employee", get_connection())

# --- Sidebar Navigation ---
# Use expanders for logical grouping of dashboard navigation links.
with st.sidebar.expander("Dashboard Overview", expanded=True):
    st.markdown("[Key HR Metrics](#key-hr-metrics)")
    st.markdown("[Departmental & Job Role Analysis](#departmental-job-role-analysis)")
    st.markdown("[Attrition Insights](#attrition-insights)")
    st.markdown("[Detailed Analysis](#detailed-analysis-overtime-income-impact)")

with st.sidebar.expander("Data & Management", expanded=False):
    st.markdown("[Detailed Data Views](#detailed-data-views)")
    st.markdown("[Interactive Employee Filter](#interactive-employee-filter)")
    st.markdown("[Employee Management Actions](#employee-management-actions)")

with st.sidebar.expander("Machine Learning Model", expanded=False):
    st.markdown("[Attrition Prediction](#machine-learning-attrition-prediction)")

# --- Main Dashboard Title & Intro ---
st.title("📊 HR Employee Attrition & Management Dashboard")
st.markdown("This dashboard provides a comprehensive overview of employee data, attrition trends, and predictive insights.")

# =========================
# SECTION: Key HR Metrics
# =========================
st.markdown("## Key HR Metrics")

col1, col2, col3, col4 = st.columns(4)

# --- Metric 1: Employees Who Have Not Left ---
query_not_left = "SELECT COUNT(*) FROM employee WHERE Attrition = 'No';"
cursor.execute(query_not_left)
not_left_count = cursor.fetchone()[0]
col1.metric("Employees Still With Company", not_left_count, "No Attrition")

# --- Metric 2: Total Employees ---
total_employees = df.shape[0]
col2.metric("Total Employees", total_employees)

# --- Metric 3: Attrition Rate ---
attrition_count = df[df['Attrition'] == 'Yes'].shape[0]
attrition_rate = (attrition_count / total_employees) * 100 if total_employees > 0 else 0
col3.metric("Overall Attrition Rate", f"{attrition_rate:.2f}%", delta=f"{attrition_count} employees left", delta_color="inverse")

# --- Metric 4: Average Monthly Income ---
avg_monthly_income_overall = df['MonthlyIncome'].mean()
col4.metric("Avg. Monthly Income (Overall)", f"${avg_monthly_income_overall:,.2f}")

st.markdown("---")

# =========================
# SECTION: Departmental & Job Role Analysis
# =========================
st.markdown("## Departmental & Job Role Analysis")

col_dept_chart, col_job_chart = st.columns(2)

with col_dept_chart:
    # --- Bar Chart: Employee Count by Department ---
    query_dept_counts = "SELECT Department, COUNT(*) FROM employee GROUP BY Department;"
    cursor.execute(query_dept_counts)
    dept_data = cursor.fetchall()
    dept_df_chart = pd.DataFrame(dept_data, columns=["Department", "EmployeeCount"])
    fig_dept = px.bar(
        dept_df_chart, x="Department", y="EmployeeCount",
        title="Employee Distribution Across Departments",
        color="Department", 
        color_discrete_map={
            'Human Resources': STC_PURPLE_LIGHT, 
            'Research & Development': STC_PURPLE, 
            'Sales': STC_PURPLE_DARK
        },
        template="plotly_white"
    )
    st.plotly_chart(fig_dept, use_container_width=True)

with col_job_chart:
    # --- Bar Chart: Average Monthly Income by Job Role ---
    query_income_roles = "SELECT JobRole, AVG(MonthlyIncome) FROM employee GROUP BY JobRole;"
    cursor.execute(query_income_roles)
    income_data = cursor.fetchall()
    income_df_chart = pd.DataFrame(income_data, columns=["JobRole", "AverageMonthlyIncome"])
    fig_income = px.bar(
        income_df_chart, x="JobRole", y="AverageMonthlyIncome",
        title="Average Income Per Job Role",
        color="AverageMonthlyIncome",
        color_continuous_scale=CUSTOM_PURPLE_RED_GRADIENT,
        template="plotly_white"
    )
    st.plotly_chart(fig_income, use_container_width=True)

# =========================
# SECTION: Attrition Insights
# =========================
st.markdown("## Attrition Insights")

col_attrition_rate, col_perf_attrition = st.columns(2)

with col_attrition_rate:
    # --- Treemap: Attrition Rate by Department & Job Role ---
    attrition_counts = df.groupby(['Department', 'JobRole'])['Attrition'].value_counts().unstack().fillna(0)
    if 'Yes' not in attrition_counts.columns:
        attrition_counts['Yes'] = 0
    attrition_rate_calc = (attrition_counts['Yes'] / attrition_counts.sum(axis=1) * 100).round(2)
    attrition_rate_df_display = attrition_rate_calc.reset_index().rename(columns={0: 'AttritionRate'})
    # Add employee count for better context in treemap
    total_employees_per_group = df.groupby(['Department', 'JobRole']).size().reset_index(name='TotalEmployees')
    attrition_rate_df_display = pd.merge(attrition_rate_df_display, total_employees_per_group, on=['Department', 'JobRole'])
    fig_attrition_rate = px.treemap(
        attrition_rate_df_display, path=['Department', 'JobRole'], values='TotalEmployees',
        color='AttritionRate', hover_data=['AttritionRate', 'TotalEmployees'],
        title='Attrition Rate by Department & Job Role',
        color_continuous_scale=CUSTOM_PURPLE_RED_GRADIENT, 
        template="plotly_white"
    )
    st.plotly_chart(fig_attrition_rate, use_container_width=True)

with col_perf_attrition:
    # --- Grouped Bar: Performance Rating vs Attrition ---
    perf_attrition_data = df.groupby(['PerformanceRating', 'Attrition']).size().unstack(fill_value=0).reset_index()
    if 'Yes' not in perf_attrition_data.columns:
        perf_attrition_data['Yes'] = 0
    if 'No' not in perf_attrition_data.columns:
        perf_attrition_data['No'] = 0
    fig_perf_attrition = go.Figure(data=[
        go.Bar(name='No Attrition', x=perf_attrition_data['PerformanceRating'], y=perf_attrition_data['No'], marker_color=STC_PURPLE_LIGHT),
        go.Bar(name='Yes Attrition', x=perf_attrition_data['PerformanceRating'], y=perf_attrition_data['Yes'], marker_color=STC_PURPLE_DARK)
    ])
    fig_perf_attrition.update_layout(
        barmode='group',
        title='Employee Count by Performance Rating and Attrition',
        xaxis_title="Performance Rating", yaxis_title="Number of Employees",
        template="plotly_white"
    )
    st.plotly_chart(fig_perf_attrition, use_container_width=True)

# =========================
# SECTION: Detailed Analysis - Overtime & Income Impact
# =========================
st.markdown("## Detailed Analysis: Overtime & Income Impact")

col_ot_attrition, col_income_attrition = st.columns(2)

with col_ot_attrition:
    # --- Grouped Bar: Attrition Rate by Job Role and Overtime ---
    job_ot_attrition = (
        df.groupby(['JobRole', 'OverTime'])['Attrition']
          .value_counts()
          .unstack(fill_value=0)
    )
    job_ot_attrition['EmployeeCount'] = job_ot_attrition.sum(axis=1)
    if 'Yes' not in job_ot_attrition.columns:
        job_ot_attrition['Yes'] = 0
    job_ot_attrition['AttritionRate'] = (job_ot_attrition['Yes'] / job_ot_attrition['EmployeeCount'] * 100).round(2)
    job_ot_attrition = job_ot_attrition.reset_index()
    fig_ot_attrition = px.bar(
        job_ot_attrition.sort_values('AttritionRate', ascending=False),
        x='JobRole',
        y='AttritionRate',
        color='OverTime',
        barmode='group',
        text='AttritionRate',
        title='Attrition Rate by Job Role and Overtime',
        color_discrete_map={'Yes': STC_PURPLE_DARK, 'No': STC_PURPLE_LIGHT},
        template="plotly_white",
        height=500
    )  
    fig_ot_attrition.update_traces(texttemplate='%{text:.2s}%', textposition='outside')
    fig_ot_attrition.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    st.plotly_chart(fig_ot_attrition, use_container_width=True)

with col_income_attrition:
    # --- Bar: Average Monthly Income by Attrition Status ---
    income_by_attrition = df.groupby('Attrition')['MonthlyIncome'].mean().reset_index()
    fig_income_corr = px.bar(
        income_by_attrition, x='Attrition', y='MonthlyIncome',
        color='Attrition',
        title='Average Monthly Income by Attrition Status',
        color_discrete_map={'Yes': STC_PURPLE_DARK, 'No': STC_PURPLE_LIGHT},
        template="plotly_white"
    )
    st.plotly_chart(fig_income_corr, use_container_width=True)

st.markdown("---")

# =========================
# SECTION: Detailed Data Views
# =========================
st.markdown("## Detailed Data Views")

with st.expander("View All Employee Data", expanded=False):
    st.dataframe(df)

with st.expander("Top 5 Employees by Performance Rating", expanded=False):
    # --- Table: Top 5 Employees by Performance ---
    query_top5_perf = "SELECT EmployeeNumber, PerformanceRating, Department, JobRole, MonthlyIncome FROM employee ORDER BY PerformanceRating DESC LIMIT 5;"
    cursor.execute(query_top5_perf)
    top5_perf_data = cursor.fetchall()
    top5_perf_df = pd.DataFrame(top5_perf_data, columns=["EmployeeNumber", "PerformanceRating", "Department", "JobRole", "MonthlyIncome"])
    st.table(top5_perf_df)

with st.expander("Department with Highest Average Performance Rating", expanded=False):
    # --- Info: Department with Best Performance ---
    query_best_dept_perf = """
    SELECT Department, AVG(PerformanceRating) as AvgPerformanceRating
    FROM employee GROUP BY Department ORDER BY AvgPerformanceRating DESC LIMIT 1;"""
    cursor.execute(query_best_dept_perf)
    best_dept_perf_result = cursor.fetchone()
    if best_dept_perf_result:
        st.info(f"The department with the highest average performance rating is **{best_dept_perf_result[0]}** with an average of **{best_dept_perf_result[1]:.2f}**.")
    else:
        st.write("No data available for average performance rating by department.")

st.markdown("---")

# =========================
# SECTION: Interactive Employee Filter
# =========================
st.markdown("## Interactive Employee Filter")

departments = df['Department'].unique()
selected_dept_filter = st.selectbox("Select Department to Filter", ['All'] + list(departments), key='filter_dept_selectbox')

filtered_df = st.session_state.employees_df.copy() # Use session state for filtering
if selected_dept_filter != 'All':
    filtered_df = filtered_df[filtered_df['Department'] == selected_dept_filter]

st.dataframe(filtered_df, use_container_width=True)

st.markdown("---")

# =========================
# SECTION: Employee Management Actions (Add, Update, Delete)
# =========================
st.markdown("## Employee Management Actions")

# --- Two Columns: Add Employee | Update/Delete Employee ---
col_add_employee, col_update_delete = st.columns([1, 1])

with col_add_employee:
    # --- Add New Employee Form ---
    st.subheader("Add New Employee")
    with st.form("add_employee_form"):
        try:
            # Determine next available employee number
            if not st.session_state.employees_df.empty:
                max_emp_num = st.session_state.employees_df['EmployeeNumber'].max()
                next_emp_num = max_emp_num + 1 if max_emp_num else 1
            else:
                next_emp_num = 1
        except Exception:
            next_emp_num = 1

        emp_num = st.number_input("Employee Number", min_value=1, step=1, value=int(next_emp_num), key='add_emp_num')
        age = st.number_input("Age", min_value=18, max_value=100, step=1, value=30, key='add_age')
        gender = st.selectbox("Gender", ["Male", "Female"], key='add_gender')
        
        # Provide options for department and job role, fallback to defaults if empty
        dept_options = ['Sales', 'Research & Development', 'Human Resources'] if st.session_state.employees_df.empty else st.session_state.employees_df['Department'].unique()
        job_role_options = [
            'Sales Executive', 'Research Scientist', 'Laboratory Technician', 'Manufacturing Director',
            'Healthcare Representative', 'Manager', 'Sales Representative', 'Research Director', 'Human Resources'
        ] if st.session_state.employees_df.empty else st.session_state.employees_df['JobRole'].unique()

        department = st.selectbox("Department", dept_options, key='add_dept')
        job_role = st.selectbox("Job Role", job_role_options, key='add_job_role')
        monthly_income = st.number_input("Monthly Income", min_value=0, step=100, value=5000, key='add_monthly_income')
        # Uncomment below to add more fields (Performance, Attrition, OverTime)
        # performance_rating = st.selectbox("Performance Rating", [1, 2, 3, 4], index=1, key='add_perf')
        # attrition = st.selectbox("Attrition", ["No", "Yes"], key='add_attrition')
        # overtime_status = st.selectbox("OverTime", ["No", "Yes"], key='add_overtime')
        submit_btn = st.form_submit_button("Add Employee", type="primary")

        if submit_btn:
            insert_query = """
                INSERT INTO employee (EmployeeNumber, Age, Gender, Department, JobRole, MonthlyIncome)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            try:
                conn_manage = get_connection()
                cursor_manage = conn_manage.cursor()
                cursor_manage.execute(insert_query, (
                    int(emp_num), int(age), gender, department, job_role, int(monthly_income)
                ))
                conn_manage.commit()
                refresh_employees_df()
                st.success(f"New employee {emp_num} added successfully!")
            except sqlite3.IntegrityError:
                st.error(f"Error: Employee Number {emp_num} already exists. Please choose a unique number.")
            except Exception as e:
                st.error(f"Error adding employee: {e}")

with col_update_delete: 
    # --- Update Employee Income Form ---
    st.subheader("Update Employee Monthly Income")
    with st.form("update_income_form"):
        emp_num_update = st.number_input("Enter Employee Number to Update", min_value=1, step=1, key='update_emp_num')
        new_income = st.number_input("New Monthly Income", min_value=0, step=100, key='new_income_val')
        update_btn = st.form_submit_button("Update Income", type="secondary")
        if update_btn:
            update_query = "UPDATE employee SET MonthlyIncome = ? WHERE EmployeeNumber = ?"
            try:
                conn_manage = get_connection()
                cursor_manage = conn_manage.cursor()
                cursor_manage.execute(update_query, (int(new_income), int(emp_num_update)))
                conn_manage.commit()
                if cursor_manage.rowcount > 0:
                    st.success(f"Employee #{emp_num_update}'s income updated to {new_income:,.2f}.")
                    refresh_employees_df()
                else:
                    st.warning(f"Employee number {emp_num_update} not found.")
            except Exception as e:
                st.error(f"Error updating income: {e}")

    st.markdown("---")
    # --- Delete Employee Form ---
    st.subheader("Delete Employee")
    with st.form("delete_employee_form"):
        emp_num_delete = st.number_input("Enter Employee Number to Delete", min_value=1, step=1, key='delete_emp_num')
        delete_btn = st.form_submit_button("Delete Employee", type="secondary", key="red")
        if delete_btn:
            delete_query = "DELETE FROM employee WHERE EmployeeNumber = ?"
            try:
                conn_manage = get_connection()
                cursor_manage = conn_manage.cursor()
                cursor_manage.execute(delete_query, (int(emp_num_delete),))
                conn_manage.commit()
                if cursor_manage.rowcount > 0:
                    st.success(f"Employee #{emp_num_delete} deleted successfully!")
                    refresh_employees_df()
                else:
                    st.warning(f"Employee number {emp_num_delete} not found.")
            except Exception as e:
                st.error(f"Error deleting employee: {e}")

# --- Display Updated Employee Table ---
st.subheader("Current Employees")
st.dataframe(st.session_state.employees_df, use_container_width=True)

st.markdown("---")

# =========================
# SECTION: Machine Learning - Attrition Prediction
# =========================
st.markdown("## Machine Learning: Attrition Prediction")
# This section uses a Random Forest Classifier to predict employee attrition and visualize feature importances.

# --- Prepare dataset for ML ---
ml_df = df.copy() # Always use the original loaded df for ML to avoid pollution from management operations
try:
    # --- Encode categorical columns ---
    cat_cols = ml_df.select_dtypes(include=['object']).columns
    for col in cat_cols:
        ml_df[col] = LabelEncoder().fit_transform(ml_df[col])

    X = ml_df.drop('Attrition', axis=1)
    y = ml_df['Attrition']

    # --- Train/test split ---
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # --- Scale features ---
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

    # --- Feature importance visualization ---
    feat_importance = pd.DataFrame({
        'Feature': X.columns,
        'Importance': rf.feature_importances_
    }).sort_values(by='Importance', ascending=False)

    fig_feat_imp = px.bar(
        feat_importance.head(10), x='Importance', y='Feature', orientation='h',
        title='Top 10 Feature Importances for Attrition Prediction',
        color='Importance',
        color_continuous_scale=CUSTOM_PURPLE_RED_GRADIENT,
        template="plotly_white"
    )
    fig_feat_imp.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_feat_imp, use_container_width=True)

except Exception as e:
    st.error(f"Error during Machine Learning model processing: {e}. Please check your data for consistency.")
    st.info("Ensure all necessary columns are present and data types are correct for ML processing.")

# --- End of Dashboard ---
# The connection managed by st.cache_resource is automatically closed by Streamlit when the app stops.