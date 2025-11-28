import pandas as pd
import sys

try:
    with open('inspection_1996.txt', 'w', encoding='utf-8') as f:
        df = pd.read_csv('resources/03_BI/NAC_1996.csv', sep=';', encoding='latin1')
        f.write(f"Columns: {df.columns.tolist()}\n\n")
        
        for col in df.columns:
            f.write(f"--- {col} ---\n")
            f.write(str(df[col].value_counts().head(20)) + "\n\n")
            
    print("Inspection complete. Check inspection_1996.txt")
            
except Exception as e:
    print(f"Error: {e}")
