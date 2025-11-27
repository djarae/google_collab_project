import pandas as pd

try:
    df = pd.read_csv('resources/03_BI/NAC_1996.csv', sep=';', encoding='latin1')
    
    print("Searching for 'AMBULANCIA' or 'TRAYECTO' in all columns...")
    for col in df.columns:
        if df[col].dtype == 'object':
            matches = df[df[col].astype(str).str.contains('AMBULANCIA|TRAYECTO', case=False, na=False)]
            if not matches.empty:
                print(f"Found matches in column {col}:")
                print(matches[col].unique())
                
    print("\nAll unique values in ESTAB:")
    print(df['ESTAB'].unique())
    
except Exception as e:
    print(f"Error: {e}")
