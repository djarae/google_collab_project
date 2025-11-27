import pandas as pd
import numpy as np
import os
import glob
import matplotlib.pyplot as plt
import seaborn as sns

# Define paths
DATA_DIR = 'resources/03_BI'
OUTPUT_FILE = 'analysis_results.txt'

def load_data():
    print("Loading data...")
    all_files = glob.glob(os.path.join(DATA_DIR, "NAC_*.csv"))
    df_list = []
    
    for filename in all_files:
        try:
            # Try reading with latin1 first as it's common for these files
            df = pd.read_csv(filename, sep=';', encoding='latin1')
            df_list.append(df)
            print(f"Loaded {os.path.basename(filename)}: {df.shape}")
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            
    if not df_list:
        print("No data loaded.")
        return None
        
    full_df = pd.concat(df_list, ignore_index=True)
    print(f"Total records: {full_df.shape}")
    return full_df

def clean_data(df):
    print("Cleaning data...")
    # Standardize column names if necessary (convert to upper case)
    df.columns = [c.upper() for c in df.columns]
    
    # Ensure numeric columns are numeric
    numeric_cols = ['PESO', 'TALLA', 'EDAD_P', 'EDAD_M', 'MES_NAC', 'DIA_NAC', 'ANO_NAC']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    return df

def analyze_freq_month(df):
    print("\n--- 2. Most Frequent Month ---")
    if 'MES_NAC' in df.columns:
        freq_month = df['MES_NAC'].mode()[0]
        print(f"Most frequent month: {freq_month}")
        print(df['MES_NAC'].value_counts().head())
    else:
        print("MES_NAC column not found.")

def analyze_freq_day(df):
    print("\n--- 3. Most Frequent Day of Year ---")
    if 'MES_NAC' in df.columns and 'DIA_NAC' in df.columns:
        # Create a temporary date column (ignoring year for day-of-year)
        # We use a leap year (e.g., 2000) to include Feb 29
        try:
            # Filter invalid dates
            valid_dates = df[(df['MES_NAC'].between(1, 12)) & (df['DIA_NAC'].between(1, 31))].copy()
            # Construct string 'MM-DD'
            valid_dates['MD'] = valid_dates['MES_NAC'].astype(int).astype(str).str.zfill(2) + '-' + \
                                valid_dates['DIA_NAC'].astype(int).astype(str).str.zfill(2)
            
            freq_day = valid_dates['MD'].mode()[0]
            print(f"Most frequent day (MM-DD): {freq_day}")
            print(valid_dates['MD'].value_counts().head())
        except Exception as e:
            print(f"Error in day analysis: {e}")

def analyze_cov_corr_peso_talla(df):
    print("\n--- 4. Covariance/Correlation Peso vs Talla ---")
    if 'PESO' in df.columns and 'TALLA' in df.columns:
        # Filter valid data (e.g., weight > 0, height > 0)
        valid = df[(df['PESO'] > 0) & (df['PESO'] < 9999) & (df['TALLA'] > 0) & (df['TALLA'] < 99)]
        
        cov = valid['PESO'].cov(valid['TALLA'])
        corr = valid['PESO'].corr(valid['TALLA'])
        print(f"Global Covariance: {cov}")
        print(f"Global Correlation: {corr}")
        
        print("By Year:")
        if 'ANO_NAC' in df.columns:
            years = valid['ANO_NAC'].unique()
            years.sort()
            for year in years:
                subset = valid[valid['ANO_NAC'] == year]
                if len(subset) > 1:
                    c = subset['PESO'].corr(subset['TALLA'])
                    print(f"Year {year}: {c}")

def analyze_cov_corr_parents_age(df):
    print("\n--- 5. Covariance/Correlation Parent Ages ---")
    if 'EDAD_P' in df.columns and 'EDAD_M' in df.columns:
        # Filter valid ages (e.g., 10-100)
        valid = df[(df['EDAD_P'] > 10) & (df['EDAD_P'] < 100) & (df['EDAD_M'] > 10) & (df['EDAD_M'] < 100)]
        
        cov = valid['EDAD_P'].cov(valid['EDAD_M'])
        corr = valid['EDAD_P'].corr(valid['EDAD_M'])
        print(f"Global Covariance: {cov}")
        print(f"Global Correlation: {corr}")
        
        print("By Year:")
        if 'ANO_NAC' in df.columns:
            years = valid['ANO_NAC'].unique()
            years.sort()
            for year in years:
                subset = valid[valid['ANO_NAC'] == year]
                if len(subset) > 1:
                    c = subset['EDAD_P'].corr(subset['EDAD_M'])
                    print(f"Year {year}: {c}")

def analyze_premature(df):
    print("\n--- 6. Premature Analysis ---")
    # Conditions: Premature (<37 weeks), Term (37-41), Post-term (>41)
    # Assuming 'SEMANAS' column exists
    if 'SEMANAS' in df.columns:
        df['SEMANAS'] = pd.to_numeric(df['SEMANAS'], errors='coerce')
        valid = df[(df['SEMANAS'] > 20) & (df['SEMANAS'] < 45)]
        
        def categorize(weeks):
            if weeks < 37: return 'Prematuro'
            elif weeks <= 41: return 'A termino'
            else: return 'Postermino'
            
        valid['Category'] = valid['SEMANAS'].apply(categorize)
        
        print(valid['Category'].value_counts())
        
        # Boxplots would be generated here in the notebook
        print("Boxplot data prepared.")

def analyze_ambulance_indicator(df):
    print("\n--- 7. Ambulance/Transit Indicator ---")
    # Logic: 1 if Ambulance, 2 if Transit (since 1996)
    # Placeholder logic: We don't have the exact codes. 
    # We will create the column but populate it with 0 (Unknown) for now, 
    # or try to infer if possible.
    
    df['indicador'] = 0
    
    # Attempt to find codes if they existed (Hypothetical)
    # if 'LOCAL_PART' in df.columns:
    #     df.loc[df['LOCAL_PART'] == 999, 'indicador'] = 1 # Example
    
    print("Indicator column created (initialized to 0 due to missing code info).")
    
    # Outlier analysis logic (IQR)
    # For rows where indicator is 1 or 2
    subset = df[df['indicador'].isin([1, 2])]
    if not subset.empty:
        print("Analyzing outliers for Ambulance/Transit cases...")
    else:
        print("No Ambulance/Transit cases identified to analyze outliers.")

def main():
    df = load_data()
    if df is not None:
        df = clean_data(df)
        analyze_freq_month(df)
        analyze_freq_day(df)
        analyze_cov_corr_peso_talla(df)
        analyze_cov_corr_parents_age(df)
        analyze_premature(df)
        analyze_ambulance_indicator(df)

if __name__ == "__main__":
    main()
