# Simple Security System Application
# Written by Will Lattimore in conjunction with chatGPT-4o (OpenAI)
# Dec 21 2024
# Designed and tested on Macbook Air M2 2022, Sonoma 14.5

import cv2
import logging
import json
from datetime import datetime
import time

# Main Application Code
class Logger:
    def __init__(self, log_file='app.log', log_level=logging.DEBUG):
        """Initializes the logger and sets up file and console handlers."""
        self.logger = logging.getLogger('SSA_logger')
        self.logger.setLevel(log_level)

        # File handler (appends to log file)
        file_handler = logging.FileHandler(log_file, mode='a')

        # Console handler (outputs to terminal)
        console_handler = logging.StreamHandler()

        # Log format (timestamp - name - level type - message)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Set formatter for both handlers
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        # Optionally, set console log level to INFO
        console_handler.setLevel(logging.INFO)

        # Log that initialization was successful
        self.logger.info("Loggers successfully initialized.")

    def log_info(self, info):
        """Logs an info message."""
        try:
            self.logger.info(info)
        except Exception as e:
            print(f"Failed to log info message: {info}. Error: {e}")

    def log_error(self, info):
        """Logs an error message."""
        try:
            self.logger.error(info)
        except Exception as e:
            print(f"Failed to log error message: {info}. Error: {e}")

def log_to_json(log_message, log_type, file_path="SSA_Events.json"):
    """
    Logs a message to a JSON file with the fields: timestamp, info, and type.
    
    Parameters:
        log_message (str): The log message to store.
        log_type (str): The type of log (e.g., 'info', 'error', 'warning').
        file_path (str): The path to the JSON file (default is 'custom_log.json').
    """
    # Create the log entry
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "info": log_message,
        "type": log_type
    }
    
    try:
        # Read existing logs if the file exists
        try:
            with open(file_path, "r") as file:
                logs = json.load(file)
        except FileNotFoundError:
            logs = []  # Initialize an empty list if the file doesn't exist
        
        # Append the new log entry
        logs.append(log_entry)
        
        # Write updated logs back to the file
        with open(file_path, "w") as file:
            json.dump(logs, file, indent=4)
            
        print(f"Log added successfully: {log_entry}")
    
    except Exception as e:
        print(f"Error writing to log file: {e}")

def generate_filename():
    """Generates a unique filename with a readable date and time."""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        return f"security_camera_{timestamp}.jpg"
    except Exception as e:
        logger.log_error(f"ERROR: Could not generate image filename: {e}.")
        raise

def take_photo(output_filename, camera_index=0):
    """Captures a photo using the built-in camera."""
    try:
        # Create camera object
        camera = cv2.VideoCapture(camera_index, cv2.CAP_AVFOUNDATION)
        if not camera.isOpened():
            raise Exception(f"Error: Camera {camera_index} is not opened.")
        
         # Allow the camera to adjust white balance and exposure
        warmup_frames = 10
        for i in range(warmup_frames):
            ret, frame = camera.read()
            if not ret:
                raise Exception("Error: Failed to capture frame during warmup.")
            time.sleep(0.1)  # 100 ms delay between frames

        # Capture image frame from camera, if ret (bool) is true, capture was succesful
        ret, frame = camera.read()
        if not ret:
            raise Exception("Error: Failed to capture frame.")

        # Save the image captured (frame) to a destination (output_filename)
        cv2.imwrite(output_filename, frame)
        logger.log_info(f"Photo taken from camera {camera_index} and saved as {output_filename}.")
        log_to_json(f"Photo taken from camera {camera_index} and saved as {output_filename}.", "Image Capture: Successful")

        return True
    except Exception as e:
        logger.log_error(f"ERROR: Could not take photo from camera {camera_index} : {e}.")
        log_to_json(f"ERROR: Could not take photo from camera {camera_index} : {e}.", "Image Capture: Failed")

        return False
    finally:
        # Release the camera video feed from this application if the resource is currently open
        if 'camera' in locals() and camera.isOpened():
            camera.release()
        cv2.destroyAllWindows()
# Main Normal Mode
def normal_mode():
    print("Normal Mode...")
    logger.log_info(f"User entered Normal Mode.")

    while True:
        key = input("Press 'w' to simulate security event.\nPress 'q' to quit: ").strip().lower()

        if key == 'w':
            filename = generate_filename()
            take_photo(filename)
            
        elif key == 'q':
            print("Exiting...")
            logger.log_info(f"User exited normal mode.")

            break
        else:
            print("Invalid input.")

# Test Mode
def test_mode():
    print("Test Mode...")
    logger.log_info(f"User entered Test Mode.")

    while True:
        print("[q] Test Filename Generation")
        print("[w] Test Camera Feed (camera: 0)")
        print("[e] Test Photo Capture (camera: 0)")
        print("[r] Close Camera Feed (camera: 0)")
        print("[t] Exit Test Mode")

        # Obtain key value for following logic
        key = input("Enter your choice: ").strip().lower()

        # Test filename generation
        if key == 'q':
            filename = generate_filename()
            logger.log_info(f"Succesfully generated image filename: {filename}")
        
        # Test camera feed
        elif key == 'w':
            try:
                camera = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
                if not camera.isOpened():
                    raise Exception(f"Error: Camera {0} is not opened.")
                logger.log_info(f"Succesfully opened camera 0 feed.")

                ret, frame = camera.read()
                if not ret:
                    raise Exception("Error: Failed to capture frame.")
                
                cv2.imshow("Camera Feed", frame)
                logger.log_info(f"Succesfully opened camera 0 feed.")

            except Exception as e:
                logger.log_error(f"ERROR: Could not open camera feed : {e}.")
        # Test image capture
        elif key == 'e':
            try:
                cv2.imwrite(filename, frame)
                logger.log_info(f"Photo taken from camera {0} and saved as {filename}.")
            except Exception as e:
                logger.log_error(f"ERROR: Could not take photo from camera {0} : {e}.")
        # Test closing camera feed
        elif key == 'r':
            try:
                if 'camera' in locals() and camera.isOpened():
                    camera.release()
                cv2.destroyAllWindows()
                logger.log_info(f"Camera feed closed")
            except Exception as e:
                logger.log_error(f"ERROR: Could not close camera feed: {e}")
        # Exits Test mode
        elif key == 't':
            print("Exiting Test Mode.")
            break
        else:
            print("Invalid choice. Try again.")

 # Initialize the Logger class globally
logger = Logger()

if __name__ == "__main__":
    # Prompt user for mode selection
    mode = input("Enter 'n' for Normal Mode or 't' for Test Mode: ").strip().lower()
    if mode == 'n':
       normal_mode()
    elif mode == 't':
        test_mode()
    else:
        print("Invalid mode. Exiting.")
    