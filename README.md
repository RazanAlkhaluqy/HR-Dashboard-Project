# HR-Dashboard-Project
🧑‍💼 HR Employee Attrition Analysis 
![Python](https://img.shields.io/badge/Python-3.10-blue.svg)  
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red)  
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)  

An interactive HR analytics dashboard that empowers the HR department to analyze employee data, uncover key attrition insights, and make data-driven retention decisions. 
This project analyzes employee attrition using **SQL, Python(Pandas), and Streamlit**.

---
## Table of Contents
- [Project Overview](#-Project-Overview)
- [Data Source & Dictionary](#data-source--dictionary)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Installation & Usage](#-installation--usage)
- [License](#-license)
- [Author & Acknowledgments](#author--acknowledgments)
---
## 📊 Project Overview
Employee attrition (turnover) is a major challenge for organizations, as it can lead to increased recruitment costs, loss of institutional knowledge, and reduced team productivity.  
This project aims to help HR departments understand the factors that drive employee attrition and make informed decisions to improve retention strategies.
In this project, we:
- Load and clean HR dataset
- Store data in an SQLite database
- Answer business questions with **SQL queries**
- Perform analysis with **Pandas**
- Visualize results in an interactive **Streamlit dashboard**

**Value Provided:**  
- Helps HR identify high-risk employee segments and factors contributing to attrition  
- Provides actionable insights to improve retention strategies and workforce planning  
- Combines SQL, Python, and interactive visualization to create a robust, user-friendly analytics tool
---
## Data Source & Dictionary
Dataset Source: ( https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset).
This dataset contains employee information from Atlas Lab, including HR attributes, performance, and satisfaction. Key columns include:
- **EmployeeID, FirstName, LastName, Gender, Age, Department, Salary, OverTime, Attrition** – basic employee info and turnover status  
- **PerformanceRating, SelfRating, ManagerRating** – employee performance metrics  
- **EnvironmentSatisfaction, JobSatisfaction, RelationshipSatisfaction, WorkLifeBalance** – satisfaction levels  
- **YearsAtCompany, YearsInMostRecentRole, YearsSinceLastPromotion, YearsWithCurrManager** – tenure metrics  
- **EducationLevel, StockOptionLevel, BusinessTravel, DistanceFromHome** – additional HR attributes

---
## 🔑Key Features
- Compare attrition rates across multiple factors
- Visualize attrition trends with interactive charts
- SQL + Pandas dual analysis for validation

---

## 🛠️Tech Stack
- **Python** :
   - `pandas` – data manipulation and analysis  
  - `numpy` – numerical operations  
  - `matplotlib` & `seaborn` – static visualizations  
  - `plotly` – interactive charts  
  - `scikit-learn` – machine learning models
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
---
## 👩‍💻Author & Acknowledgments

**Author:** Razan Zaki  

**Acknowledgments:**  
- I would like to thank [Kaggle](https://www.kaggle.com/) for providing the HR dataset used in this project, which is licensed under the [Open Data Commons Database License (ODbL 1.0)](https://opendatacommons.org/licenses/dbcl/1-0/).  
- Special thanks to my mentors Mr. Osamah Sarraj and director Mr. Mohammed Sharaf, for their guidance and support throughout the project.  

This project was developed as part of an HR analytics analysis and dashboard to help organization understand employee attrition trends.

---
## 📜 License

- The **code** in this repository is licensed under the [MIT License](LICENSE).
- The **dataset** used in this project is licensed under the [Open Data Commons Database License (ODbL 1.0)](https://opendatacommons.org/licenses/dbcl/1-0/).  
  Please make sure to follow the dataset’s license terms if you reuse or distribute the data.

---
### Dashboard page
![Dashboard Screenshot](images/dashboard1.png)
![Dashboard Screenshot](images/dashboard2.png)


