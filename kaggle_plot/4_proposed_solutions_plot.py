import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import textwrap
import os

os.makedirs('images', exist_ok=True)

file_path = '../Student Meal Habits and Class Schedule Survey.csv'
df = pd.read_csv(file_path)

sns.set_theme(style="whitegrid")

def wrap_labels(ax, width, break_long_words=False):
    labels = []
    for label in ax.get_yticklabels():
        text = label.get_text()
        labels.append(textwrap.fill(text, width=width, break_long_words=break_long_words))
    ax.set_yticklabels(labels, rotation=0)

sol_col = [c for c in df.columns if "30 minutes" in c.lower()][0]

plt.figure(figsize=(8, 6))
ax = sns.countplot(y=df[sol_col], order=df[sol_col].value_counts().index, palette="coolwarm")
wrap_labels(ax, 30)

plt.title('Preferred 30-Minute Schedule Adjustments', fontsize=14)
plt.xlabel('Number of Students', fontsize=12)
plt.ylabel('')
plt.tight_layout()
plt.savefig('images/plot4_solutions.png', dpi=300)
print("Saved images/plot4_solutions.png")
