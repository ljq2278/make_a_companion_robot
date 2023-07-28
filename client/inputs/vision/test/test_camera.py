import cv2

# Open the USB camera
camera_index = 1
cap = cv2.VideoCapture(camera_index)

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Error: Could not open the camera")
    exit()

# Capture and display images in a loop
while True:
    # Capture a frame
    ret, frame = cap.read()

    # Check if the frame was read correctly
    if not ret:
        print("Error: Could not read a frame from the camera")
        break

    # Display the captured frame
    cv2.imshow('USB Camera', frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the display window
cap.release()
cv2.destroyAllWindows()