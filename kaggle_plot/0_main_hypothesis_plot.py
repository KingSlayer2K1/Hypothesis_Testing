import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create images directory if it doesn't exist
os.makedirs('images', exist_ok=True)

# Load data (assuming script is run from inside kaggle_plots folder)
file_path = '../Student Meal Habits and Class Schedule Survey.csv'
try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    print(f"Error: Could not find '{file_path}'. Ensure you are running this from the kaggle_plots directory.")
    exit()

clash_col = [col for col in df.columns if "clash" in col.lower() and "mess" in col.lower()][0]
skip_col = [col for col in df.columns if "skip meals" in col.lower()][0]

broader_map = {
    "Never": "Never/Rarely/Sometimes",
    "Rarely": "Never/Rarely/Sometimes",
    "Sometimes": "Never/Rarely/Sometimes",
    "Often/Very often": "Often/Very often",
    "Often": "Often/Very often", 
    "Very often": "Often/Very often"
}

df_plot = df.copy()
df_plot[clash_col] = df_plot[clash_col].replace(broader_map)
df_plot[skip_col] = df_plot[skip_col].replace(broader_map)

plot_data = df_plot.groupby([clash_col, skip_col]).size().reset_index(name='Count')
group_totals = plot_data.groupby(clash_col)['Count'].transform('sum')
plot_data['Percentage'] = (plot_data['Count'] / group_totals) * 100

sns.set_theme(style="whitegrid")
plt.figure(figsize=(8, 5))

sns.barplot(
    data=plot_data, 
    x=clash_col, 
    y='Percentage', 
    hue=skip_col,
    palette="Blues_d"
)

plt.title('Impact of Class Clashes on Meal Skipping Frequency', fontsize=14, pad=15)
plt.xlabel('Frequency of Class/Mess Clashes', fontsize=12)
plt.ylabel('Percentage of Students (%)', fontsize=12)
plt.legend(title='Skip Meals Frequency', bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.savefig('images/clash_vs_skip_plot.png', dpi=300)
print("Saved images/clash_vs_skip_plot.png")
