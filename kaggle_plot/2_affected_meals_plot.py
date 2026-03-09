import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

os.makedirs('images', exist_ok=True)

file_path = '../Student Meal Habits and Class Schedule Survey.csv'
df = pd.read_csv(file_path)

sns.set_theme(style="whitegrid")

meal_col = [c for c in df.columns if "most frequently affected" in c.lower()][0]

plt.figure(figsize=(8, 4))
sns.countplot(y=df[meal_col], order=df[meal_col].value_counts().index, palette="viridis")

plt.title('Meals Most Frequently Affected by Clashes', fontsize=14)
plt.xlabel('Number of Students', fontsize=12)
plt.ylabel('')
plt.tight_layout()
plt.savefig('images/plot2_affected.png', dpi=300)
print("Saved images/plot2_affected.png")
