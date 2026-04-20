import tensorflow as tf

def convert_h5_to_tflite(h5_path, tflite_path):
    print(f"Loading model from {h5_path}...")
    model = tf.keras.models.load_model(h5_path)
    
    print("Converting to TFLite...")
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    # Optional: Optimization
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    tflite_model = converter.convert()
    
    print(f"Saving TFLite model to {tflite_path}...")
    with open(tflite_path, 'wb') as f:
        f.write(tflite_model)
    print("Conversion complete!")

if __name__ == "__main__":
    import os
    base_dir = r"c:\Users\dhruv\OneDrive\Desktop\SR_BE_Project"
    h5_model = os.path.join(base_dir, "model1.h5")
    tflite_model = os.path.join(base_dir, "model1.tflite")
    
    if os.path.exists(h5_model):
        convert_h5_to_tflite(h5_model, tflite_model)
    else:
        print(f"Model not found at {h5_model}")
