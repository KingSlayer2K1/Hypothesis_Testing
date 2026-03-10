import math
import sys

import numpy as np
import pandas as pd

try:
    from scipy.stats import chi2_contingency as scipy_chi2_contingency
    from scipy.stats import fisher_exact as scipy_fisher_exact
except ModuleNotFoundError:
    scipy_chi2_contingency = None
    scipy_fisher_exact = None


def _regularized_gamma_q(a, x):
    """Regularized upper incomplete gamma Q(a, x)."""
    if a <= 0:
        raise ValueError("Parameter 'a' must be positive.")
    if x < 0:
        raise ValueError("Parameter 'x' must be non-negative.")
    if x == 0:
        return 1.0

    eps = 1e-12
    max_iter = 1000
    tiny = 1e-300
    gln = math.lgamma(a)

    if x < a + 1.0:
        ap = a
        delta = 1.0 / a
        series_sum = delta
        for _ in range(max_iter):
            ap += 1.0
            delta *= x / ap
            series_sum += delta
            if abs(delta) < abs(series_sum) * eps:
                break
        p = series_sum * math.exp(-x + a * math.log(x) - gln)
        return max(0.0, min(1.0, 1.0 - p))

    b = x + 1.0 - a
    c = 1.0 / tiny
    d = 1.0 / max(b, tiny)
    h = d
    for i in range(1, max_iter + 1):
        an = -i * (i - a)
        b += 2.0
        d = an * d + b
        if abs(d) < tiny:
            d = tiny
        c = b + an / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < eps:
            break

    q = math.exp(-x + a * math.log(x) - gln) * h
    return max(0.0, min(1.0, q))


def _chi2_contingency_fallback(observed, correction=True):
    observed = np.asarray(observed, dtype=float)
    if observed.ndim != 2:
        raise ValueError("Observed frequencies must be a 2D table.")
    if (observed < 0).any():
        raise ValueError("Observed frequencies must be non-negative.")
    total = observed.sum()
    if total <= 0:
        raise ValueError("Observed table must contain at least one count.")

    row_sums = observed.sum(axis=1, keepdims=True)
    col_sums = observed.sum(axis=0, keepdims=True)
    expected = (row_sums @ col_sums) / total
    if (expected == 0).any():
        raise ValueError("Expected frequencies contain zero; chi-square undefined.")

    dof = (observed.shape[0] - 1) * (observed.shape[1] - 1)
    if dof == 0:
        return 0.0, 1.0, dof, expected

    if correction and dof == 1:
        adjusted = np.maximum(np.abs(observed - expected) - 0.5, 0.0)
        chi2 = float(((adjusted ** 2) / expected).sum())
    else:
        chi2 = float((((observed - expected) ** 2) / expected).sum())

    p_value = _regularized_gamma_q(dof / 2.0, chi2 / 2.0)
    return chi2, p_value, dof, expected


def chi2_contingency(observed, correction=True):
    if scipy_chi2_contingency is not None:
        return scipy_chi2_contingency(observed, correction=correction)
    return _chi2_contingency_fallback(observed, correction=correction)


def _fisher_exact_2x2_fallback(observed):
    observed = np.asarray(observed, dtype=int)
    if observed.shape != (2, 2):
        raise ValueError("Fisher's exact test requires a 2x2 table.")
    if (observed < 0).any():
        raise ValueError("Observed frequencies must be non-negative.")

    a, b = int(observed[0, 0]), int(observed[0, 1])
    c, d = int(observed[1, 0]), int(observed[1, 1])
    row1 = a + b
    row2 = c + d
    col1 = a + c
    col2 = b + d
    n = row1 + row2
    denom = math.comb(n, row1)

    def hypergeom_p(x):
        return (math.comb(col1, x) * math.comb(col2, row1 - x)) / denom

    x_min = max(0, row1 - col2)
    x_max = min(row1, col1)

    p_obs = hypergeom_p(a)
    p_two_sided = 0.0
    for x in range(x_min, x_max + 1):
        p = hypergeom_p(x)
        if p <= p_obs + 1e-15:
            p_two_sided += p

    return max(0.0, min(1.0, p_two_sided))


def fisher_exact_2x2(observed):
    if scipy_fisher_exact is not None:
        _, p_value = scipy_fisher_exact(observed, alternative="two-sided")
        return float(p_value)
    return _fisher_exact_2x2_fallback(observed)


def _find_column(columns, required_terms, label):
    for col in columns:
        col_lower = col.lower()
        if all(term in col_lower for term in required_terms):
            return col
    raise ValueError(
        f"Could not find a column for '{label}'. Required terms: {required_terms}"
    )


def _normalize_frequency(value):
    if not isinstance(value, str):
        return value
    cleaned = " ".join(value.strip().lower().split())
    if cleaned.startswith("very often"):
        return "Very often"
    if cleaned.startswith("often"):
        return "Often"
    if cleaned.startswith("sometimes"):
        return "Sometimes"
    if cleaned.startswith("rarely"):
        return "Rarely"
    if cleaned.startswith("never"):
        return "Never"
    return value.strip()


def _read_csv_with_fallback(csv_file_path):
    encodings = ["utf-8", "utf-8-sig", "cp1252", "latin1"]
    last_error = None
    for encoding in encodings:
        try:
            return pd.read_csv(csv_file_path, encoding=encoding)
        except UnicodeDecodeError as exc:
            last_error = exc
    raise last_error


def _print_section_header(title):
    print(f"\n{title}")
    print("-" * len(title))


def test_hypothesis_1(csv_file_path, alpha=0.05):
    try:
        df = _read_csv_with_fallback(csv_file_path)
    except FileNotFoundError:
        print(f"Error: Could not find '{csv_file_path}'.")
        return
    except UnicodeDecodeError:
        print(f"Error: Could not decode '{csv_file_path}' with supported encodings.")
        return

    try:
        clash_col = _find_column(df.columns, ["clash", "mess"], "clash frequency")
        skip_col = _find_column(df.columns, ["skip", "meal"], "meal skipping frequency")
    except ValueError as exc:
        print(f"Column mapping error: {exc}")
        return

    base = df[[clash_col, skip_col]].copy()
    base[clash_col] = base[clash_col].map(_normalize_frequency)
    base[skip_col] = base[skip_col].map(_normalize_frequency)
    base = base.dropna()

    print(f"File: {csv_file_path}")
    print(f"Total usable responses: {len(base)}")
    print(f"alpha = {alpha:.2f}")

    # 5x5 raw analysis (before collapsing)
    raw_levels = ["Never", "Rarely", "Sometimes", "Often", "Very often"]
    raw_table = pd.crosstab(base[clash_col], base[skip_col]).reindex(
        index=raw_levels, columns=raw_levels, fill_value=0
    )
    raw_test_table = raw_table.loc[
        raw_table.sum(axis=1) > 0, raw_table.sum(axis=0) > 0
    ]
    if raw_test_table.shape[0] < 2 or raw_test_table.shape[1] < 2:
        print("\nRaw 5x5 table does not have enough variation for chi-square.")
        return

    raw_chi2, raw_p, raw_dof, raw_expected = chi2_contingency(
        raw_test_table, correction=False
    )
    raw_low_cells = int((raw_expected < 5).sum())
    raw_total_cells = raw_expected.size
    raw_low_pct = (raw_low_cells / raw_total_cells) * 100 if raw_total_cells else 0.0

    raw_out = raw_table.rename(
        index={"Very often": "VeryOften"},
        columns={"Very often": "VeryOften"},
    )
    raw_out.index.name = "Class clash"
    raw_out.columns.name = "Meal skipping"

    _print_section_header("5x5 Matrix (Raw Categories)")
    print(raw_out.to_string())
    print(
        f"Chi-square: statistic = {raw_chi2:.4f}, dof = {raw_dof}, p-value = {raw_p:.6f}"
    )
    print(
        f"Expected counts < 5: {raw_low_cells}/{raw_total_cells} ({raw_low_pct:.1f}%)"
    )
    if raw_low_pct > 20:
        print("Warning: >20% expected counts are <5 (chi-square assumption limitation).")
        print("Action: collapse to 2x2 and retest.")
    else:
        print("Assumption check: acceptable expected counts for chi-square.")

    # 2x2 collapsed analysis
    collapsed = base.copy()
    combine_map = {
        "Never": "Never/Rarely/Sometimes",
        "Rarely": "Never/Rarely/Sometimes",
        "Sometimes": "Never/Rarely/Sometimes",
        "Often": "Often/Very often",
        "Very often": "Often/Very often",
    }
    collapsed[clash_col] = collapsed[clash_col].replace(combine_map)
    collapsed[skip_col] = collapsed[skip_col].replace(combine_map)
    labels = ["Never/Rarely/Sometimes", "Often/Very often"]
    contingency_table = pd.crosstab(collapsed[clash_col], collapsed[skip_col]).reindex(
        index=labels, columns=labels, fill_value=0
    )
    if (contingency_table.sum(axis=1) == 0).any() or (
        contingency_table.sum(axis=0) == 0
    ).any():
        print("\nCollapsed 2x2 table does not have enough variation for testing.")
        print(contingency_table.to_string())
        return

    chi2, chi2_p, dof, expected = chi2_contingency(contingency_table, correction=True)
    fisher_p = fisher_exact_2x2(contingency_table.values)
    expected_df = pd.DataFrame(
        expected, index=contingency_table.index, columns=contingency_table.columns
    )
    short_labels = {
        "Never/Rarely/Sometimes": "Low",
        "Often/Very often": "High",
    }
    observed_out = contingency_table.rename(index=short_labels, columns=short_labels)
    observed_out.index.name = "Class clash"
    observed_out.columns.name = "Meal skipping"
    expected_out = expected_df.rename(index=short_labels, columns=short_labels).round(3)
    expected_out.index.name = "Class clash"
    expected_out.columns.name = "Meal skipping"
    low_cells = int((expected < 5).sum())
    total_cells = expected.size
    perc_low = (low_cells / total_cells) * 100 if total_cells else 0.0

    _print_section_header("2x2 Matrix (Collapsed) + Final Tests")
    print(observed_out.to_string())
    print("\nExpected matrix:")
    print(expected_out.to_string())
    print(
        f"Chi-square (Yates): statistic = {chi2:.4f}, dof = {dof}, p-value = {chi2_p:.6f}"
    )
    print(f"Fisher exact (two-sided): p-value = {fisher_p:.6f}")
    print(f"Expected counts < 5: {low_cells}/{total_cells} ({perc_low:.1f}%)")
    print(
        "Decision (Chi-square): "
        + ("Reject H0" if chi2_p < alpha else "Fail to reject H0")
    )
    print(
        "Decision (Fisher): "
        + ("Reject H0" if fisher_p < alpha else "Fail to reject H0")
    )
    if chi2_p >= alpha and fisher_p >= alpha:
        print(
            "\nFinal conclusion: There is no statistically significant evidence that students skip meals due to class schedule clashes."
        )
    else:
        print(
            "\nFinal conclusion: There is statistically significant evidence that class schedule clashes are related to students skipping meals."
        )


if __name__ == "__main__":
    file_name = sys.argv[1] if len(sys.argv) > 1 else "responses.csv"
    test_hypothesis_1(file_name)
