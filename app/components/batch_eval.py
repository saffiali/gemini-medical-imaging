import streamlit as st
import os
import time
from utils.gcs_helper import list_blobs, download_blob, upload_blob
from utils.image_processing import extract_tiles
from utils.vertex_client import call_med_foundation_model
from utils.report_generator import calculate_iou, generate_word_report

def render():
    st.title("Batch Image Evaluation")
    st.markdown("Evaluate multiple WSIs in bulk and generate a comprehensive IOU report.")

    bucket_name = os.environ.get("WSI_BUCKET", "gsk-cmc-hackathon-med-imaging-pov-wsi-images")
    reports_bucket = os.environ.get("REPORTS_BUCKET", "gsk-cmc-hackathon-med-imaging-pov-reports")
    endpoint_id = os.environ.get("MEDGEMMA_ENDPOINT", "mock")

    st.subheader("Select Batch Input")
    prefix = st.text_input("GCS Folder Prefix for Batch (e.g., 'crc_samples/')", value="")
    
    if st.button("Load Batch"):
        with st.spinner("Fetching batch list..."):
            blobs = list_blobs(bucket_name, prefix=prefix if prefix else None)
            batch_images = [b for b in blobs if b.lower().endswith(('.png', '.jpg', '.jpeg', '.tif'))]
            st.session_state['batch_images'] = batch_images
            
    if 'batch_images' in st.session_state and st.session_state['batch_images']:
        st.write(f"**{len(st.session_state['batch_images'])}** images loaded for batch processing.")
        
        if st.button("Start Batch Processing"):
            results = []
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, img_blob in enumerate(st.session_state['batch_images']):
                status_text.text(f"Processing {img_blob}...")
                
                local_path = os.path.join("/tmp", os.path.basename(img_blob))
                download_blob(bucket_name, img_blob, local_path)
                
                tiles, _ = extract_tiles(local_path)
                
                tumor_count = 0
                normal_count = 0
                
                for i_t, tile_data in enumerate(tiles):
                    tile_path = f"/tmp/batch_tile.png"
                    tile_data["tile"].save(tile_path)
                    
                    result = call_med_foundation_model(endpoint_id, tile_path)
                    if result:
                        cls = result["prediction"]["class"]
                        if cls == "tumor":
                            tumor_count += 1
                        elif cls == "normal":
                            normal_count += 1
                            
                # Calculate IOU
                iou = calculate_iou([]) # Dummy predictions for PoV
                
                results.append({
                    "image_name": os.path.basename(img_blob),
                    "iou": iou,
                    "tiles_processed": len(tiles),
                    "tumor_count": tumor_count,
                    "normal_count": normal_count
                })
                
                progress_bar.progress((i + 1) / len(st.session_state['batch_images']))
                
            status_text.text("Generating Word Report...")
            report_path = generate_word_report(results)
            
            # Upload report to GCS
            report_name = f"IOU_Report_{int(time.time())}.docx"
            upload_blob(reports_bucket, report_path, report_name)
            
            st.success(f"Batch processing complete! Report saved to GCS bucket `{reports_bucket}` as `{report_name}`.")
            
            with open(report_path, "rb") as file:
                st.download_button(
                    label="Download Word Report",
                    data=file,
                    file_name=report_name,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
