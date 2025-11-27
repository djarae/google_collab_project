import pandas as pd

try:
    df = pd.read_csv('resources/03_BI/NAC_2017.csv', sep=';')
    print("Columns:", df.columns.tolist())
    
    potential_cols = [c for c in df.columns if 'LUGAR' in c or 'LOCAL' in c or 'ESTAB' in c]
    print("Potential Place Columns:", potential_cols)
    
    for col in potential_cols:
        print(f"\nValue Counts for {col}:")
        print(df[col].value_counts().head(10))
        
except Exception as e:
    print(e)
