import streamlit as st
import os

# Import components
from components import gcs_explorer
from components import ondemand_eval
from components import batch_eval
from components import hitl_review

st.set_page_config(
    page_title="Medical Imaging PoV",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "Home", 
    "GCS Explorer", 
    "On-Demand Evaluation", 
    "Batch Evaluation",
    "HITL Review"
])

def show_home():
    st.title("Medical Imaging Path Foundation Model PoV")
    st.markdown("""
    Welcome to the Medical Imaging Proof of Value application. 
    This tool allows you to:
    - Explore Rat and CRC WSI datasets stored in Google Cloud Storage.
    - Evaluate images on-demand or in batch mode using Google's pretrained Path Foundation models (Medgemma/MedSigLip).
    - Review tile embeddings and mask generation visually.
    - Pathologist HITL (Human-in-the-loop) review to ascertain biological accuracy.
    - Generate IOU measurement reports.
    """)

if page == "Home":
    show_home()
elif page == "GCS Explorer":
    gcs_explorer.render()
elif page == "On-Demand Evaluation":
    ondemand_eval.render()
elif page == "Batch Evaluation":
    batch_eval.render()
elif page == "HITL Review":
    hitl_review.render()

