import pandas as pd

try:
    df = pd.read_csv('resources/03_BI/NAC_1996.csv', sep=';', encoding='latin1') # Try latin1 just in case
    print("Columns:", df.columns.tolist())
    
    if 'ESTAB' in df.columns:
        print("\nSearching in ESTAB:")
        ambulancia = df[df['ESTAB'].astype(str).str.contains('AMBULANCIA', case=False, na=False)]
        trayecto = df[df['ESTAB'].astype(str).str.contains('TRAYECTO', case=False, na=False)]
        
        print(f"Rows with AMBULANCIA: {len(ambulancia)}")
        if not ambulancia.empty:
            print(ambulancia['ESTAB'].unique())
            
        print(f"Rows with TRAYECTO: {len(trayecto)}")
        if not trayecto.empty:
            print(trayecto['ESTAB'].unique())
            
except Exception as e:
    print(f"Error: {e}")
