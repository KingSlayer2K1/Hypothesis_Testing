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

cope_col = [c for c in df.columns if "usually do" in c.lower()][0]

plt.figure(figsize=(8, 5))
ax = sns.countplot(y=df[cope_col], order=df[cope_col].value_counts().index, palette="magma")
wrap_labels(ax, 25)

plt.title('Student Coping Mechanisms During Clashes', fontsize=14)
plt.xlabel('Number of Students', fontsize=12)
plt.ylabel('')
plt.tight_layout()
plt.savefig('images/plot3_coping.png', dpi=300)
print("Saved images/plot3_coping.png")
