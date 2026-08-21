import streamlit as st
import requests
import time
import os
import pandas as pd
from a_platform.d_skills.d_data_engineering.profiler import DataProfilerSkill

st.set_page_config(page_title="Analytics AI Factory v1.0", layout="wide")

API_BASE = "http://127.0.0.1:8000/api/v1"
RAW_DATA_DIR = "a_platform/d_input/a_datasets/a_raw"
os.makedirs(RAW_DATA_DIR, exist_ok=True)

st.title("🏭 Analytics AI Factory (Real Execution)")

if "job_id" not in st.session_state:
    st.session_state.job_id = None
if "current_status" not in st.session_state:
    st.session_state.current_status = "IDLE"
if "project_plan" not in st.session_state:
    st.session_state.project_plan = None
if "discovery_questions" not in st.session_state:
    st.session_state.discovery_questions = None
if "profiling_data" not in st.session_state:
    st.session_state.profiling_data = {}
if "idea" not in st.session_state:
    st.session_state.idea = ""

tab1, tab2, tab3, tab4, tab5 = st.tabs(["💡 Nova Ideia", "📊 Profiling", "🕸️ Grafo", "🏗️ Planejamento", "🏭 Fábrica & Certificação"])

with tab1:
    if st.session_state.discovery_questions is None and not st.session_state.job_id:
        st.markdown("### Passo 1: O que você deseja construir hoje?")
        prompt = st.text_area("Descreva seu projeto de dados, ETL, pipeline ou dashboard:")
        
        st.markdown("### Upload de Dataset Real (Opcional)")
        uploaded_file = st.file_uploader("Envie seu CSV, JSON ou Parquet", type=["csv", "json", "parquet"])
        
        if st.button("🔍 Analisar Ideia"):
            if prompt:
                st.session_state.idea = prompt
                if uploaded_file:
                    file_path = os.path.join(RAW_DATA_DIR, uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    st.info(f"Arquivo salvo em {file_path}. Profiling em andamento...")
                    profiler = DataProfilerSkill()
                    st.session_state.profiling_data = profiler.profile_dataset(file_path)
                
                # Fetch questions
                res = requests.post(f"{API_BASE}/project/discover", json={"idea": prompt})
                if res.status_code == 200:
                    st.session_state.discovery_questions = res.json().get("questions", [])
                    st.rerun()
                else:
                    st.error("Erro ao gerar questionário de discovery.")
            else:
                st.warning("Por favor, digite um prompt.")
                
    elif st.session_state.discovery_questions is not None and not st.session_state.job_id:
        st.markdown("### Passo 2: Questionário de Refinamento (Discovery)")
        st.info("Responda às perguntas abaixo para guiar a Arquitetura da Fábrica.")
        
        answers = {}
        for q in st.session_state.discovery_questions:
            answers[q] = st.text_input(q)
            
        if st.button("🚀 Iniciar Fábrica v1.0"):
            payload = {
                "prompt": st.session_state.idea,
                "answers": answers,
                "profiling_data": st.session_state.profiling_data
            }
            res = requests.post(f"{API_BASE}/project/submit", json=payload)
            if res.status_code == 200:
                data = res.json()
                st.session_state.job_id = data["job_id"]
                st.session_state.current_status = "STARTED"
                st.success(f"Job Submetido! ID: {st.session_state.job_id}")
                st.rerun()
            else:
                st.error("Falha ao submeter projeto.")

if st.session_state.job_id:
    placeholder = st.empty()
    
    with placeholder.container():
        res = requests.get(f"{API_BASE}/project/{st.session_state.job_id}/status")
        if res.status_code == 200:
            status_data = res.json()
            st.session_state.current_status = status_data.get("status")
            st.session_state.project_plan = status_data.get("plan")
            
    with tab2:
        if st.session_state.profiling_data:
            st.markdown("### Profiling Data Result")
            st.json(st.session_state.profiling_data)
        else:
            if st.session_state.project_plan:
                st.markdown("### Profiling Data")
                st.info("Nenhum dataset anexado. Profiling estatístico padrão assumido.")
            else:
                st.info("Aguardando Profiler...")
            
    with tab3:
        if st.session_state.project_plan:
            st.markdown("### Grafo de Arquitetura")
            st.markdown("```mermaid\ngraph TD;\n    A[Source] --> B[ETL];\n    B --> C[(Database)];\n    C --> D[API];\n    D --> E[Dashboard];\n```")
        else:
            st.info("Aguardando Brain Graph Builder...")

    with tab4:
        if st.session_state.project_plan:
            st.markdown("### Arquitetura Desenhada")
            st.json(st.session_state.project_plan)
        else:
            st.info("Aguardando o Agente de Arquitetura desenhar o plano...")
            
    with tab5:
        from a_platform.l_interfaces.ui.components import render_logs
        render_logs(st.session_state.current_status)
        
        if "COMPLETED" in st.session_state.current_status:
            cert_res = requests.get(f"{API_BASE}/project/{st.session_state.job_id}/certificate")
            if cert_res.status_code == 200:
                cert = cert_res.json()
                if "project_id" in cert:
                    st.markdown("### Certificado de Qualidade Final")
                    st.json(cert)
