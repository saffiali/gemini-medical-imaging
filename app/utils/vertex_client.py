import os
import json
import base64
from google.cloud import aiplatform

def get_vertex_client():
    project = os.environ.get("PROJECT_ID", "gsk-cmc-hackathon")
    region = os.environ.get("REGION", "us-central1")
    aiplatform.init(project=project, location=region)
    return aiplatform

def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def call_med_foundation_model(endpoint_id, image_path, prompt="Quantify tiles and identify tissue types."):
    """
    Calls a Vertex AI Endpoint hosting Medgemma or MedSigLip.
    Uses mock response for the PoV if endpoint isn't fully active.
    """
    client = get_vertex_client()
    
    # In a real scenario, this would call endpoint.predict()
    # For PoV without real endpoint active, we mock the embedding/classification response
    if not endpoint_id or endpoint_id == "mock":
        # Return mocked structured data (embedding array + class)
        return {
            "prediction": {
                "class": "tumor" if "CRC" in image_path else "normal",
                "embedding": [0.1, 0.2, -0.1, 0.5], # Truncated mock embedding
                "confidence": 0.95
            }
        }
    
    try:
        endpoint = aiplatform.Endpoint(endpoint_id)
        image_b64 = encode_image(image_path)
        
        # The payload structure depends on the specific model's serving container
        instance = {
            "image_bytes": image_b64,
            "prompt": prompt
        }
        
        response = endpoint.predict(instances=[instance])
        return response.predictions[0]
    except Exception as e:
        print(f"Error calling Vertex AI: {e}")
        return None
