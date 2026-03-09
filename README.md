# Hypothesis Testing: Class Schedule vs Meal Skipping

**Course:** Research Methodology (RM6201)
**Institute:** IIT Patna
**Group:** 17

---

## 📌 About

This project performs a **Chi-Square Test of Independence** to determine whether there is a statistically significant relationship between **class timing clashes and meal-skipping frequency among IIT Patna students**.

The analysis is based on **114 survey responses** collected from students.
The repository includes the **statistical testing code** and **data visualization scripts** used to analyze the dataset.

---

## 🎯 Hypothesis

**Hypothesis 1:**
IIT Patna students whose **class schedule clashes with mess timing** skip meals more frequently than students **without timing clashes**.

**Statistical Method Used**

* Pearson's Chi-Square Test of Independence

**Result**

* **Statistically Significant**
* **p-value = 0.0185**

Since the p-value is **less than 0.05**, we reject the null hypothesis and conclude that **class timing clashes are associated with increased meal skipping**.

---

## ⚙️ Setup

### 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Run the Statistical Analysis

```bash
python chi_sq.py
```

This script performs the Chi-Square test on the dataset and prints the statistical results.

---

## 📂 Repository Structure

```
.
├── Student Meal Habits and Class Schedule Survey.csv
│   # Raw dataset collected through survey

├── requirements.txt
│   # Python dependencies required to run the project

├── chi_sq.py
│   # Main script that performs the Chi-Square hypothesis testing

├── README.md
│   # Project documentation

└── kaggle_plot/
    ├── 0_main_hypothesis_plot.py
    ├── 1_demographics_plot.py
    ├── 2_affected_meals_plot.py
    ├── 3_coping_mechanisms_plot.py
    ├── 4_proposed_solutions_plot.py
    └── images/
        # Generated visualization PNG files
```

---

## 📊 Data Visualization

The `kaggle_plots` directory contains Python scripts used to generate visual insights from the dataset, including:

* Demographic distribution of respondents
* Meals most frequently skipped
* Common coping mechanisms students use
* Student-proposed solutions to the scheduling issue

Generated plots are saved inside the **`images/`** folder.

---

## 🧪 Statistical Method

The **Chi-Square Test of Independence** is used to evaluate whether two categorical variables are related.

In this project:

* **Variable 1:** Class schedule clash with mess timing
* **Variable 2:** Frequency of skipping meals

The test evaluates whether the observed distribution significantly differs from what would be expected if the variables were independent.

---

## 📈 Dataset

* **Total Responses:** 114
* **Population:** IIT Patna students
* **Data Type:** Survey-based categorical responses

---

## 👨‍💻 Authors

Group 17
Research Methodology Project
**IIT Patna**

---
