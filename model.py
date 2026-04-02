import time
import random

class CropVisionModel:
    """
    Mock class representing a compiled TensorFlow/PyTorch model.
    In a real scenario, this loads a .h5 or .onnx file.
    """
    def __init__(self):
        self.classes = ["Healthy", "Rust Fungi", "Blight Fungi"]
        self.is_loaded = True

    def predict(self, image_bytes):
        # Simulate inference latency
        time.sleep(random.uniform(0.05, 0.15)) 
        
        # Mock prediction logic based on byte size (just for deterministic testing)
        file_size = len(image_bytes)
        prediction = self.classes[file_size % 3]
        confidence = round(random.uniform(0.85, 0.99), 4)
        
        return {"diagnosis": prediction, "confidence": confidence}
