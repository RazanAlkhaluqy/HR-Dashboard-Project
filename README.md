# HR-Dashboard-Project
🧑‍💼 HR Employee Attrition Analysis

This project analyzes employee attrition using **SQL, Pandas, and Streamlit**.  
The goal is to identify key factors that affect employee turnover and provide insights to help HR focus on retention strategies.

---
## 📊 Project Overview
Employee attrition (turnover) is a critical challenge for organizations.  
In this project, we:
- Load and clean HR dataset
- Store data in an SQLite database
- Answer business questions with **SQL queries**
- Perform analysis with **Pandas**
- Visualize results in an interactive **Streamlit dashboard**

---
## 🔑 Key Features
- Compare attrition rates across **job roles, overtime, and education**
- Identify high-risk employee segments
- Visualize attrition trends with interactive charts
- SQL + Pandas dual analysis for validation

---

## 🛠️ Tech Stack
- **Python** (Pandas, SQLite3, Matplotlib/Seaborn)
- **SQL** (for querying HR database)
- **Streamlit** (for interactive dashboard)
- **VSCode** (development environment)
- **Git/GitHub** (version control)

---

## 🚀 Installation & Usage

### 1. Clone the repo
```bash
git clone https://github.com/RazanAlkhaluqy/HR-Dashboard-Project.git
cd HR-Dashboard-Project
```
### 2. Create a virtual environment (recommended)
```bash
conda create -n hrproject python=3.10 -y
conda activate hrproject
```
### 3. Install dependencies
---
```bash
pip install -r requirements.txt
```
(if you don’t have a requirements.txt, you can create one with pip freeze > requirements.txt)

### 4. Set up the database

Make sure your SQLite database (employee.db) is in the project folder.
If not, run your data preparation notebook (analysis.ipynb) first to generate it.

### 5. Run the app (Streamlit)
```bash
 python app.py
```
```bash
streamlit run dashboard.py
```
### 6. Explore the Dashboard

Open the link shown in the terminal (usually http://localhost:8501) to interact with the HR Dashboard.

