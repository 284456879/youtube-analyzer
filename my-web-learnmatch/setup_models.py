import os
import requests

# Models needed for face-api.js
MODELS = [
    "ssd_mobilenet_v1_model-weights_manifest.json",
    "ssd_mobilenet_v1_model-shard1",
    "face_landmark_68_model-weights_manifest.json",
    "face_landmark_68_model-shard1",
    "face_recognition_model-weights_manifest.json",
    "face_recognition_model-shard1",
    "face_recognition_model-shard2"
]

BASE_URL = "https://raw.githubusercontent.com/justadudewhohacks/face-api.js/master/weights"
TARGET_DIR = os.path.join("static", "models")

def download_models():
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)
        print(f"Created directory: {TARGET_DIR}")

    for model in MODELS:
        url = f"{BASE_URL}/{model}"
        path = os.path.join(TARGET_DIR, model)
        
        if os.path.exists(path):
            print(f"Skipping {model} (already exists)")
            continue
            
        print(f"Downloading {model}...")
        try:
            response = requests.get(url)
            response.raise_for_status()
            with open(path, 'wb') as f:
                f.write(response.content)
            print(f"Successfully downloaded {model}")
        except Exception as e:
            print(f"Failed to download {model}: {e}")

if __name__ == "__main__":
    download_models()
