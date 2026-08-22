import pandas as pd
import sqlite3
import os

def run_etl(csv_path: str, db_path: str):
    # Load and clean data (desconsiderar linhas vazias)
    df = pd.read_csv(csv_path).dropna(how='all')
    
    # Calculate metrics (separar saidas, entradas)
    entradas = df[df['tipo'] == 'entrada']['valor'].sum()
    saidas = df[df['tipo'] == 'saida']['valor'].sum()
    saldo_final = entradas - saidas
    status = 'positivo' if saldo_final >= 0 else 'negativo'
    
    # Save to SQLite
    conn = sqlite3.connect(db_path)
    df.to_sql('transacoes', conn, if_exists='replace', index=False)
    
    # Save summary
    summary_df = pd.DataFrame({'entradas': [entradas], 'saidas': [saidas], 'saldo_final': [saldo_final], 'status': [status]})
    summary_df.to_sql('resumo_financeiro', conn, if_exists='replace', index=False)
    conn.close()
    
    return status, saldo_final

if __name__ == '__main__':
    run_etl('input.csv', 'finance.db')
