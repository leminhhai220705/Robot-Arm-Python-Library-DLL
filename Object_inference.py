import numpy as np
import cv2
import tensorflow as tf

# Constants
CAM_PORT = 0
MODEL_PATH = "ei-sort_defects-transfer-learning-tensorflow-lite-float32-model (5).lite"             # 160 x 160
# MODEL_PATH = "ei-sort_defects-tiny-ml-kit-transfer-learning-tensorflow-lite-float32-model.lite"   # 96 x 96


LABELS = ("circle dirty", "circle ok", "nothing", "square dirty", "square ok", "triangle dirty", "triangle ok")

def initialize_camera(port=CAM_PORT):
    """Initialize the camera."""
    return cv2.VideoCapture(port, cv2.CAP_DSHOW)

def load_tflite_model(model_path=MODEL_PATH):
    """Load the TensorFlow Lite model."""
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    return interpreter

def capture_image(camera):
    """Capture an image from the camera."""
    ret, frame = camera.read()
    if not ret:
        raise RuntimeError("Failed to capture image")
    return frame

def preprocess(frame, alpha=1, beta=50):
    """Preprocess the frame for prediction."""
    processed = cv2.convertScaleAbs(frame)
    processed = cv2.resize(processed, (160, 160))
    processed = processed / 255.0
    processed = np.expand_dims(processed, axis=0).astype(np.float32)
    return processed

def predict(interpreter, image):
    """Make a prediction using the TensorFlow Lite model."""
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    interpreter.set_tensor(input_details[0]['index'], image)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    return output_data

def main():
    camera = initialize_camera()
    model = load_tflite_model()

    while True:
        try:
            frame = capture_image(camera)
            preprocessed_frame = preprocess(frame)
            
            # Show the preprocessed frame for debugging; comment out in production
            cv2.imshow("Preprocessed Frame", frame)
            
            output = predict(model, preprocessed_frame)
            predicted_label = LABELS[np.argmax(output)]
            print("Predicted label:", predicted_label)

            if cv2.waitKey(1) & 0xFF == 27:  # ESC key
                break

        except RuntimeError as e:
            print(e)
            break

    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
