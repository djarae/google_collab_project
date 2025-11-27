import pandas as pd

def inspect_year(year):
    try:
        filename = f'resources/03_BI/NAC_{year}.csv'
        df = pd.read_csv(filename, sep=';', nrows=10000) # Read more rows to see rare values
        print(f"\n--- {year} ---")
        print("Columns:", df.columns.tolist())
        
        potential_cols = [c for c in df.columns if 'LUGAR' in c or 'LOCAL' in c or 'ESTAB' in c]
        for col in potential_cols:
            print(f"Value Counts for {col}:")
            print(df[col].value_counts())
            
    except Exception as e:
        print(f"Error reading {year}: {e}")

inspect_year(1995)
inspect_year(1996)
