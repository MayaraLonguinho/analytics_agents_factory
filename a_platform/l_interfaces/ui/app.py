import streamlit as st
import requests
import time

st.set_page_config(page_title="Analytics AI Factory", layout="wide")

API_BASE = "http://127.0.0.1:8000/api/v1"

st.title("🏭 Analytics AI Factory")

# Session state initialization
if "job_id" not in st.session_state:
    st.session_state.job_id = None
if "current_status" not in st.session_state:
    st.session_state.current_status = "IDLE"
if "project_plan" not in st.session_state:
    st.session_state.project_plan = None

tab1, tab2, tab3, tab4, tab5 = st.tabs(["💡 Nova Ideia", "📊 Profiling", "🕸️ Grafo", "🏗️ Planejamento", "🏭 Fábrica & Certificação"])

with tab1:
    st.markdown("### O que você deseja construir hoje?")
    prompt = st.text_area("Descreva seu projeto de dados, ETL, pipeline ou dashboard:")
    if st.button("🚀 Iniciar Fábrica"):
        if prompt:
            response = requests.post(f"{API_BASE}/project/submit", json={"prompt": prompt})
            if response.status_code == 200:
                data = response.json()
                st.session_state.job_id = data["job_id"]
                st.session_state.current_status = "STARTED"
                st.success(f"Job Submetido! ID: {st.session_state.job_id}")
            else:
                st.error("Falha ao submeter projeto.")
        else:
            st.warning("Por favor, digite um prompt.")

if st.session_state.job_id:
    # Auto-refresh loop using empty container
    placeholder = st.empty()
    
    with placeholder.container():
        res = requests.get(f"{API_BASE}/project/{st.session_state.job_id}/status")
        if res.status_code == 200:
            status_data = res.json()
            st.session_state.current_status = status_data.get("status")
            st.session_state.project_plan = status_data.get("plan")
            
    with tab2:
        if st.session_state.project_plan:
            st.markdown("### Profiling Data")
            # We simulate that the profiling chart would come in the plan metadata or state
            st.info("Gráficos de profiling estatístico do pipeline seriam exibidos aqui.")
            # For demonstration, we could call an endpoint or render a base64 string
        else:
            st.info("Aguardando Profiler...")
            
    with tab3:
        if st.session_state.project_plan:
            st.markdown("### Grafo de Arquitetura")
            # Mermaid native rendering in Streamlit
            st.markdown("```mermaid\\ngraph TD;\\n    A[Source] --> B[ETL];\\n    B --> C[(Database)];\\n    C --> D[API];\\n    D --> E[Dashboard];\\n```")
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
                    st.markdown("### Certificado de Qualidade")
                    st.json(cert)
