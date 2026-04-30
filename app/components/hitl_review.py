import streamlit as st

def render():
    st.title("Pathologist HITL Review")
    st.markdown("Human-In-The-Loop review mechanism to ascertain biological accuracy of the Path Foundation Model.")

    if 'latest_predictions' not in st.session_state or not st.session_state['latest_predictions']:
        st.info("No recent predictions found. Please run On-Demand Evaluation first to review tiles.")
        return
        
    predictions = st.session_state['latest_predictions']
    st.write(f"**{len(predictions)}** tiles available for review.")
    
    # Select a specific tile for review
    selected_index = st.number_input("Select Tile Index to Review", min_value=0, max_value=len(predictions)-1, value=0)
    
    tile_data = predictions[selected_index]
    
    st.subheader(f"Tile Data (Index {selected_index})")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Model Prediction:**")
        st.write(f"Class: `{tile_data['class']}`")
        st.write(f"Coordinates: `{tile_data['coords']}`")
        st.write("Embedding Vector Snippet (Truncated):")
        st.json(tile_data['embedding'][:4]) # Show first 4
        
    with col2:
        st.write("**Biological Accuracy Assessment:**")
        st.write("Please determine the accuracy of this tile embedding against ground truth.")
        
        accuracy_label = st.radio(
            "Select Label:",
            ["True Positive (TP)", "False Positive (FP)", "True Negative (TN)", "False Negative (FN)"]
        )
        
        if st.button("Submit Assessment"):
            # In a real app, this would save to BigQuery or GCS to fine-tune the model
            st.success(f"Assessment `{accuracy_label}` recorded for Tile {selected_index}.")
