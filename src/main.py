#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 14:28:57 2026

@author: data-science
"""

# src/main.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from extract import extract_dolar, extract_selic, extract_ipca
from transform import transform_dolar, transform_indicadores
from load import load_to_supabase, save_local_backup

def main():
    print("🚀 Iniciando pipeline ETL...")
    
    # 1. Extração
    print("\n📥 Extraindo dados...")
    df_dolar = extract_dolar()
    df_selic = extract_selic()
    df_ipca = extract_ipca()
    
    # 2. Transformação
    print("\n🔄 Transformando dados...")
    df_dolar_transformado = transform_dolar(df_dolar)
    df_selic_transformado = transform_indicadores(df_selic, 'Selic')
    df_ipca_transformado = transform_indicadores(df_ipca, 'IPCA_12m')
    
    # 3. Backup local
    print("\n💾 Salvando backups...")
    if not df_dolar_transformado.empty:
        save_local_backup(df_dolar_transformado, 'dolar')
    if not df_selic_transformado.empty:
        save_local_backup(df_selic_transformado, 'selic')
    if not df_ipca_transformado.empty:
        save_local_backup(df_ipca_transformado, 'ipca')
    
    # 4. Carga no Supabase
    print("\n📤 Carregando no Supabase...")
    if not df_dolar_transformado.empty:
        load_to_supabase(df_dolar_transformado, 'cambio')
    if not df_selic_transformado.empty:
        load_to_supabase(df_selic_transformado, 'indicadores')
    if not df_ipca_transformado.empty:
        load_to_supabase(df_ipca_transformado, 'indicadores')
    
    print("\n✅ Pipeline concluído com sucesso!")

if __name__ == "__main__":
    main()