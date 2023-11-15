import cv2
import cv2.aruco as aruco

def detect_aruco_from_camera(camera_id=0):
    # Initialize the video capture
    cap = cv2.VideoCapture(camera_id)

    # Initialize the ArUco dictionary and parameters
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters = aruco.DetectorParameters_create()

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            break

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect ArUco markers
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

        # Check if any ArUco markers were detected
        if len(corners) > 0:
            # Draw detected markers
            aruco.drawDetectedMarkers(frame, corners, ids)

        # Display the frame
        cv2.imshow('Frame', frame)

        # Break the loop with 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    cap.release()
    cv2.destroyAllWindows()

# Example usage
detect_aruco_from_camera()
