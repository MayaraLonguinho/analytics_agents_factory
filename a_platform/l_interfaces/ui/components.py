import streamlit as st

def render_logs(status: str):
    st.subheader("Factory Logs Real-Time")
    if "INITIALIZED" in status or "STARTED" in status:
        st.info("Initializing Agent Factory...")
    elif "DISCOVERY" in status:
        st.warning("Discovery Agent is profiling requirements...")
    elif "PLANNING" in status:
        st.warning("Architecture & Planning Agent are building the schema...")
    elif "ATTEMPT" in status:
        st.warning(f"🛠️ Executando Ciclo na Fábrica: {status}...")
    elif "CERTIFICATION" in status:
        st.warning("Validation and Quality Gates are running...")
    elif "COMPLETED_SUCCESS" in status:
        st.success("PROJECT READY: YES! Pipeline Completed Successfully!")
    elif "FAILED" in status or "REJECTED" in status:
        st.error(f"PROJECT READY: NO! Pipeline Failed: {status}")
