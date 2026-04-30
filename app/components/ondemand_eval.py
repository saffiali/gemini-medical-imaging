import streamlit as st
import os
import time
from utils.gcs_helper import list_blobs, download_blob
from utils.image_processing import extract_tiles, generate_mask, overlay_mask
from utils.vertex_client import call_med_foundation_model
from PIL import Image

def render():
    st.title("On-Demand Image Evaluation")
    st.markdown("Select a WSI or Tissue Patch from GCS to process immediately through the Path Foundation Model.")

    bucket_name = os.environ.get("WSI_BUCKET", "gsk-cmc-hackathon-med-imaging-pov-wsi-images")
    endpoint_id = os.environ.get("MEDGEMMA_ENDPOINT", "mock")

    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Selection")
        prefix = st.text_input("GCS Folder Prefix", value="")
        
        if st.button("Refresh List"):
            blobs = list_blobs(bucket_name, prefix=prefix if prefix else None)
            image_blobs = [b for b in blobs if b.lower().endswith(('.png', '.jpg', '.jpeg', '.tif'))]
            st.session_state['eval_image_blobs'] = image_blobs
            
        if 'eval_image_blobs' in st.session_state and st.session_state['eval_image_blobs']:
            selected_image = st.selectbox("Select Image", st.session_state['eval_image_blobs'])
            
            if st.button("Run Evaluation"):
                st.session_state['eval_running'] = True
                st.session_state['eval_selected_image'] = selected_image

    if st.session_state.get('eval_running'):
        with col2:
            st.subheader("Results")
            selected_image = st.session_state['eval_selected_image']
            local_path = os.path.join("/tmp", os.path.basename(selected_image))
            
            with st.spinner("Downloading image from GCS..."):
                success = download_blob(bucket_name, selected_image, local_path)
            
            if success:
                st.image(local_path, caption="Original Image", width=400)
                
                with st.spinner("Extracting tiles and running inference..."):
                    tiles, img_size = extract_tiles(local_path)
                    st.write(f"Extracted {len(tiles)} tiles. Running inference via Vertex AI...")
                    
                    predictions = []
                    progress_bar = st.progress(0)
                    for i, tile_data in enumerate(tiles):
                        # Save tile to temporary file for inference
                        tile_path = f"/tmp/tile_{i}.png"
                        tile_data["tile"].save(tile_path)
                        
                        # Call foundation model
                        result = call_med_foundation_model(endpoint_id, tile_path)
                        if result:
                            predictions.append({
                                "coords": tile_data["coords"],
                                "class": result["prediction"]["class"],
                                "embedding": result["prediction"]["embedding"]
                            })
                            
                        # Clean up tile
                        if os.path.exists(tile_path):
                            os.remove(tile_path)
                            
                        progress_bar.progress((i + 1) / len(tiles))
                        
                    st.success("Inference complete.")
                    
                    with st.spinner("Generating overlay mask..."):
                        mask = generate_mask(predictions, img_size)
                        overlay = overlay_mask(local_path, mask)
                        
                        st.image(overlay, caption="Mask Overlay (Red=Tumor/CRC, Green=Normal)", width=400)
                        
                        # Store predictions in session state for HITL / Batch export
                        st.session_state['latest_predictions'] = predictions
            else:
                st.error("Failed to download image.")
                
            st.session_state['eval_running'] = False
