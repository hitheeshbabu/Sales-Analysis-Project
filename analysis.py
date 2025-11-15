# analysis.py
# Basic sales data analysis for Sales_Analysis_Project
# Requires: pandas, matplotlib, seaborn

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# -- Settings
DATAFILE = "sales_data.csv"
OUT_DIR = "."  # saves plots to project folder

def load_data(path):
    df = pd.read_csv(path)
    # try to parse Date column
    try:
        df['Date'] = pd.to_datetime(df['Date'])
    except Exception:
        # if parse fails, try common format
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=False, errors='coerce')
    return df

def ensure_total_sales(df):
    if 'Total Sales' not in df.columns:
        df['Total Sales'] = df['Quantity'] * df['Price']
    return df

def summary(df):
    print("\n--- DATA HEAD ---")
    print(df.head().to_string(index=False))
    print("\n--- DTYPE & MISSING ---")
    print(df.dtypes)
    print("\nMissing values per column:")
    print(df.isnull().sum())

def analyze_category(df):
    cat = df.groupby('Category', dropna=False)['Total Sales'].sum().reset_index()
    cat = cat.sort_values('Total Sales', ascending=False)
    print("\n--- Total Sales by Category ---")
    print(cat.to_string(index=False))
    return cat

def analyze_region(df):
    reg = df.groupby('Region', dropna=False)['Total Sales'].sum().reset_index()
    reg = reg.sort_values('Total Sales', ascending=False)
    print("\n--- Total Sales by Region ---")
    print(reg.to_string(index=False))
    return reg

def analyze_monthly(df):
    # create Month column
    df['Month'] = df['Date'].dt.to_period('M').astype(str)
    mon = df.groupby('Month')['Total Sales'].sum().reset_index()
    print("\n--- Monthly Total Sales ---")
    print(mon.to_string(index=False))
    return mon

def plot_category(cat_df):
    plt.figure(figsize=(7,5))
    sns.barplot(data=cat_df, x='Category', y='Total Sales')
    plt.title('Total Sales by Category')
    plt.tight_layout()
    fname = os.path.join(OUT_DIR, 'category_sales.png')
    plt.savefig(fname)
    plt.close()
    print(f"Saved plot: {fname}")

def plot_monthly(mon_df):
    plt.figure(figsize=(8,4))
    sns.lineplot(data=mon_df, x='Month', y='Total Sales', marker='o')
    plt.title('Monthly Total Sales')
    plt.xticks(rotation=45)
    plt.tight_layout()
    fname = os.path.join(OUT_DIR, 'monthly_trend.png')
    plt.savefig(fname)
    plt.close()
    print(f"Saved plot: {fname}")

def main():
    if not os.path.exists(DATAFILE):
        print(f"Data file not found: {DATAFILE}")
        return

    df = load_data(DATAFILE)
    df = ensure_total_sales(df)
    summary(df)

    cat = analyze_category(df)
    reg = analyze_region(df)
    mon = analyze_monthly(df)

    plot_category(cat)
    plot_monthly(mon)

    # quick insights (simple)
    top_cat = cat.iloc[0]
    top_reg = reg.iloc[0]
    print("\n--- Quick Insights ---")
    print(f"Top category by sales: {top_cat['Category']} (₹{int(top_cat['Total Sales'])})")
    print(f"Top region by sales: {top_reg['Region']} (₹{int(top_reg['Total Sales'])})")
    print("Monthly trend plot and category plot saved to project folder.")

if __name__ == "__main__":
    main()
