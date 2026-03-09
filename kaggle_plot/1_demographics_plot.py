import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

os.makedirs('images', exist_ok=True)

file_path = '../Student Meal Habits and Class Schedule Survey.csv'
df = pd.read_csv(file_path)

sns.set_theme(style="whitegrid")

prog_col = [c for c in df.columns if "Program" in c][0]

plt.figure(figsize=(6, 5))
prog_counts = df[prog_col].value_counts()
plt.pie(prog_counts, labels=prog_counts.index, autopct='%1.1f%%', 
        colors=sns.color_palette('pastel'), startangle=140, 
        wedgeprops={'edgecolor': 'gray', 'linewidth': 1})

plt.title('Demographic Profile: Program of Study', fontsize=14, pad=15)
plt.tight_layout()
plt.savefig('images/plot1_demographics.png', dpi=300)
print("Saved images/plot1_demographics.png")
