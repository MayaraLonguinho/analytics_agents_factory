import streamlit as st

def render_logs(status: str):
    st.subheader("Factory Logs")
    if "INITIALIZED" in status or "STARTED" in status:
        st.info("Initializing Agent Factory...")
    elif "DISCOVERY" in status:
        st.warning("Discovery Agent is profiling requirements...")
    elif "PLANNING" in status:
        st.warning("Architecture & Planning Agent are building the schema...")
    elif "FACTORY" in status:
        st.warning("Specialist Agents are materializing code...")
    elif "RUNTIME" in status:
        st.warning("Runtime Engine is executing the stack...")
    elif "CERTIFICATION" in status:
        st.warning("Validation and Quality Gates are running...")
    elif "COMPLETED_SUCCESS" in status:
        st.success("Pipeline Completed Successfully!")
    elif "FAILED" in status or "REJECTED" in status:
        st.error(f"Pipeline Failed: {status}")
