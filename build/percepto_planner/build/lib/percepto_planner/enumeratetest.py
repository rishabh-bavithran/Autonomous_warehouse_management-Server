import cv2

# Initialize the camera (0 is the default camera)
cap = cv2.VideoCapture(4)

# Get the default resolutions
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

# Print the default camera resolution
print(f"Default Resolution: {width} x {height}")

# Release the camera
cap.release()
