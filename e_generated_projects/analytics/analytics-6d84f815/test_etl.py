import os
import pandas as pd
import sqlite3
from etl import run_etl

def test_run_etl():
    # Setup
    csv_path = 'test_input.csv'
    db_path = 'test_finance.db'
    
    df = pd.DataFrame({
        'data': ['2023-01-01', '2023-01-02', None],
        'tipo': ['entrada', 'saida', None],
        'valor': [1000.0, 300.0, None]
    })
    df.to_csv(csv_path, index=False)
    
    # Execute
    status, saldo = run_etl(csv_path, db_path)
    
    # Assert
    assert saldo == 700.0
    assert status == 'positivo'
    
    conn = sqlite3.connect(db_path)
    resumo = pd.read_sql('SELECT * FROM resumo_financeiro', conn)
    assert resumo['entradas'][0] == 1000.0
    assert resumo['saidas'][0] == 300.0
    conn.close()
    
    # Teardown
    os.remove(csv_path)
    os.remove(db_path)
