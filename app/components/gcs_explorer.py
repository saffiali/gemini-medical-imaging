import streamlit as st
import os
from utils.gcs_helper import list_blobs, download_blob
from PIL import Image

def render():
    st.title("GCS Image Explorer")
    st.markdown("Browse and view Whole Slide Images (WSI) or patches stored in Google Cloud Storage.")

    # Get bucket name from env or default for local testing
    bucket_name = os.environ.get("WSI_BUCKET", "gsk-cmc-hackathon-med-imaging-pov-wsi-images")

    st.sidebar.subheader("GCS Settings")
    selected_bucket = st.sidebar.text_input("Bucket Name", value=bucket_name)
    prefix = st.sidebar.text_input("Folder Prefix", value="")

    if st.sidebar.button("List Images"):
        with st.spinner("Fetching list from GCS..."):
            blobs = list_blobs(selected_bucket, prefix=prefix if prefix else None)
            # Filter for common image formats for preview
            image_blobs = [b for b in blobs if b.lower().endswith(('.png', '.jpg', '.jpeg', '.tif', '.tiff'))]
            st.session_state['image_blobs'] = image_blobs
            if not image_blobs:
                st.warning("No images found in the specified bucket/prefix.")

    if 'image_blobs' in st.session_state and st.session_state['image_blobs']:
        st.write(f"Found **{len(st.session_state['image_blobs'])}** images.")
        
        selected_image = st.selectbox("Select an image to preview", st.session_state['image_blobs'])
        
        if st.button("Preview Image"):
            with st.spinner("Downloading image..."):
                local_path = os.path.join("/tmp", os.path.basename(selected_image))
                success = download_blob(selected_bucket, selected_image, local_path)
                
                if success:
                    try:
                        # Display using PIL (Note: large WSIs like .svs or .ndpi might need openslide)
                        image = Image.open(local_path)
                        # Downsize for quick preview
                        image.thumbnail((800, 800))
                        st.image(image, caption=selected_image, use_column_width=True)
                    except Exception as e:
                        st.error(f"Error previewing image: {e}")
                else:
                    st.error("Failed to download image from GCS.")
