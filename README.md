# security_system_application
 Python file that simulates a simple security camera image capture

Written by Will Lattimore in conjunction with chatGPT-4o (OpenAI)
Dec 21 2024
Designed and tested on Macbook Air M2 2022, Sonoma 14.5

Assuming the application can be tested on OSX with camera such as Macbook.
Assuming use of the default built in camera as substitution for a real-life security camera via HTTP request.

How to use: 
    1. Run the script. ex /path/to/security_system_application/main.py , python3 main.py
    2. Press 'n' to enter normal application mode or press 't' for unit testing mode.
    3. Normal mode: Press 'w' to run a 'security event' capturing an image from the camera, press 'q' to exit.
    4. Unit testing mode:   Press 'q' to test image filename generation, 
                            Press 'w' to open camera feed,
                            Press 'e' to capture image from camera,
                            Press 'r' to close camera feed,
                            Press 't' to exit.
                            
Use of generative AI:

AI code generation assistance was used in the development of this application.

    1. To provide information on key functions and thier dependancies that would be useful in development of the application.

        Example prompt: "What python dependancies (python 3) and their functions are used for access and control of the camera in a macbook air M2 sonoma 14.5"

        Response: "1. OpenCV (cv2)
                •	Purpose: Provides tools for accessing and processing video from the camera.
                •	Functions:
                •	cv2.VideoCapture(index): Opens the camera, where index is usually 0 for the default camera.
                •	capture.read(): Captures frames from the camera.
                •	cv2.imshow(): Displays the captured video frames in a window.
                •	cv2.imwrite(): Saves captured frames as image files.
                •	Installation: pip install opencv-python"

    2. To condense (optimize for efficiency, clean and tidy code) developer made code to improve the overall quality and readability of the code.

        Example prompt: "Optimize this function for efficiency and readability: def take_photo(output_filename, camera_index=0):
                            
                            # Initialize the camera
                            camera = cv2.VideoCapture(camera_index)

                            # Take a photo
                            ret, frame = camera.read()
                            if ret:
                                try:
                                    cv2.imwrite(output_filename, frame)
                                    print(f"Photo saved as {output_filename}")
                                    # Logging information
                                    logger.log_info("Photo taken successfully.")
                                except Exception as e:
                                    print("Error saving photo:", e)
                                    logger.log_error(f"Error saving photo: {e}")
                                    return False
                            else:
                                print("Failed to capture image. Please try again.")
                                logger.log_error("Failed to capture image.")
                                return False

                            # Turn off camera
                            try:
                                camera.release()
                            except Exception as e:
                                print("Error releasing camera:", e)

                            # Clean up
                            try:
                                cv2.destroyAllWindows()
                            except Exception as e:
                                print("Error destroying windows:", e)

                            return True "

        Response:   "def take_photo(output_filename, camera_index=0):
                        """Captures a photo using the built-in camera."""
                        try:
                            # Create camera object
                            camera = cv2.VideoCapture(camera_index, cv2.CAP_AVFOUNDATION)
                            if not camera.isOpened():
                                raise Exception(f"Error: Camera {camera_index} is not opened.")
                            
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
                            cv2.destroyAllWindows()"

        3.	To review developer-completed code blocks such as functions and classes for syntax, logical errors, and functionality, mainly in areas with complex nested logic.
