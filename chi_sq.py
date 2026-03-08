import pandas as pd
from scipy.stats import chi2_contingency

def test_hypothesis_1(csv_file_path):
    # 1. Load the Google Forms CSV data
    try:
        df = pd.read_csv(csv_file_path)
    except FileNotFoundError:
        print(f"Error: Could not find the file '{csv_file_path}'. Please check the path.")
        return

    print("=" * 70)
    print("CHI-SQUARE TEST: CLASS SCHEDULE CLASHES vs MEAL SKIPPING")
    print("=" * 70)
    
    # 2. Identify the relevant columns using keywords
    clash_col = [col for col in df.columns if "clash" in col.lower() and "mess" in col.lower()][0]
    skip_col = [col for col in df.columns if "skip meals" in col.lower()][0]

    # Data Overview
    print(f"\nDATASET OVERVIEW")
    print(f"  • Total responses: {len(df)}")
    print(f"  • Variables analyzed: 2")
    print(f"  • Missing values (clash): {df[clash_col].isna().sum()}")
    print(f"  • Missing values (meals): {df[skip_col].isna().sum()}\n")

    # --- CATEGORY COMBINATION: reduce sparse cells ---
    # merge 'Often' and 'Very often' into a single category for both variables
    combine_map = {"Often": "Often/Very often", "Very often": "Often/Very often"}
    df[clash_col] = df[clash_col].replace(combine_map)
    df[skip_col] = df[skip_col].replace(combine_map)
    print("NOTE: 'Often' and 'Very often' categories have been combined to")
    print("      improve chi-square reliability by avoiding low expected counts.\n")

    # Variable 1: Class Schedule Clashes (with merged categories)
    print("VARIABLE 1: Class Schedule Clashes with Mess Timing")
    print("-" * 70)
    clash_dist = df[clash_col].value_counts()
    clash_pct = (clash_dist / len(df) * 100).round(2)
    for category, count in clash_dist.items():
        print(f"  {category:<25} {count:>3} responses ({clash_pct[category]:>5.1f}%)")

    # Variable 2: Meal Skipping Frequency (with merged categories)
    print("\nVARIABLE 2: How Often Students Skip Meals")
    print("-" * 70)
    skip_dist = df[skip_col].value_counts()
    skip_pct = (skip_dist / len(df) * 100).round(2)
    for category, count in skip_dist.items():
        print(f"  {category:<25} {count:>3} responses ({skip_pct[category]:>5.1f}%)")

    # 3. Create the Contingency Table
    contingency_table = pd.crosstab(df[clash_col], df[skip_col])
    
    print("\nCONTINGENCY TABLE (Observed Frequencies)")
    print("-" * 70)
    print(contingency_table.to_string())
    
    # Contingency Table with Percentages
    print("\nCONTINGENCY TABLE (Row Percentages)")
    print("-" * 70)
    contingency_pct = contingency_table.div(contingency_table.sum(axis=1), axis=0) * 100
    print(contingency_pct.round(1).to_string())

    # 4. Perform the Chi-Square Test
    chi2, p_value, dof, expected = chi2_contingency(contingency_table)

    def print_results(label=""):
        print("\n" + "=" * 70)
        print(f"STATISTICAL TEST RESULTS{(' - ' + label) if label else ''}")
        print("=" * 70)
        print(f"  Chi-Square Statistic: {chi2:.4f}")
        print(f"  P-value:              {p_value:.6f}")
        print(f"  Degrees of Freedom:   {dof}")
        print(f"  Significance Level:   α = 0.05")

    print_results()


    # 5. Interpret the Results
    alpha = 0.05
    print("\n" + "=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    
    if p_value < alpha:
        print(f"\nP-value ({p_value:.4f}) < α (0.05)")
        print("  → REJECT the null hypothesis")
        print("\nHYPOTHESIS SUPPORTED!")
        print("  There IS a statistically significant relationship between")
        print("  class timing clashes and meal-skipping frequency.")
    else:
        print(f"\nP-value ({p_value:.4f}) ≥ α (0.05)")
        print("  → FAIL TO REJECT the null hypothesis")
        print("\nHYPOTHESIS NOT SUPPORTED")
        print("  There is NO statistically significant evidence of a relationship")
        print("  between class timing clashes and meal-skipping frequency.")

    # 6. Check Assumption Warning
    def check_and_report(expected_vals):
        low = (expected_vals < 5).sum()
        total = expected_vals.size
        perc = (low / total) * 100
        return perc

    perc_low = check_and_report(expected)
    if perc_low > 20:
        print("\nWARNING: Chi-Square Test Reliability")
        print(f"  {perc_low:.1f}% of expected cell counts < 5")
        print("  Results may not be highly reliable.")

        # attempt stronger grouping if still problematic
        if perc_low > 20:
            print("\nAttempting broader category collapse to improve reliability...")
            broader_map = {
                "Never": "Never/Rarely/Sometimes",
                "Rarely": "Never/Rarely/Sometimes",
                "Sometimes": "Never/Rarely/Sometimes",
                "Often/Very often": "Often/Very often"
            }
            df[clash_col] = df[clash_col].replace(broader_map)
            df[skip_col] = df[skip_col].replace(broader_map)

            contingency_table = pd.crosstab(df[clash_col], df[skip_col])
            print("\nNEW CONTINGENCY TABLE (after broad collapse)")
            print("-" * 70)
            print(contingency_table.to_string())

            chi2, p_value, dof, expected = chi2_contingency(contingency_table)
            print_results(label="(after broad collapse)")

            perc_low = check_and_report(expected)
            if perc_low > 20:
                print("\nWARNING: Even after broad collapse, >20% cells <5.")
                print("  Consider collecting more data or simplifying variables further.")
            else:
                print("\nAssumption satisfied after broad collapse.")
    else:
        print("\nTest assumptions are satisfied (>80% of cells have count ≥ 5)")
    
    print("\n" + "=" * 70 + "\n")


# ==========================================
# HOW TO RUN THE SCRIPT
# ==========================================
# 1. Download your Google Forms responses as a CSV file.
# 2. Save it in the same folder as this Python script.
# 3. Rename it to 'responses.csv' (or change the name below).
# 4. Run the script!

if __name__ == "__main__":
    # Replace 'responses.csv' with your actual downloaded file name
    file_name = "Student Meal Habits and Class Schedule Survey.csv" 
    
    # Uncomment the line below when you are ready to test your real data
    test_hypothesis_1(file_name)