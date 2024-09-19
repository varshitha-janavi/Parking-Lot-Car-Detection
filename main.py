import cv2  # Import OpenCV for video and image processing
from util import get_parking_spots_bboxes  # Import a utility function to get parking spot bounding boxes
from util import empty_or_not  # Import a utility function to determine if a parking spot is empty

# Path to the mask image (a binary image showing where parking spots are located)
mask = r"C:\Users\varsh\OneDrive\Desktop\Computer Vision Projects\Parking Lot\mask_1920_1080.png"

# Path to the video file of the parking lot
video_path = r"C:\Users\varsh\OneDrive\Desktop\Computer Vision Projects\Parking Lot\data\parking_1920_1080_loop.mp4"

# Load the mask as a grayscale image (0 means load as grayscale)
mask = cv2.imread(mask, 0)

# Capture the video from the provided path
cap = cv2.VideoCapture(video_path)

# Use connected components analysis to identify the different parking spots from the mask
connected_components = cv2.connectedComponentsWithStats(mask, 4, cv2.CV_32S)

# Get the bounding boxes of all parking spots identified by the mask
spots = get_parking_spots_bboxes(connected_components)

# Initialize a list to store the status (empty/occupied) of each parking spot
spots_status = [None for j in spots]

# Initialize the frame counter
frame_number = 0

# Define the total number of parking spots
total_spots = len(spots)

# Read frames from the video in a loop
ret = True  # ret is a flag indicating whether the frame was successfully read
time_step = 1  # How often to check the status of the parking spots (in terms of frames)

while ret:
    ret, frame = cap.read()  # Read the next frame from the video

    # Check the parking spots at intervals defined by time_step
    if frame_number % time_step == 0:
        occupied_spots = 0  # Initialize counter for occupied spots

        # Loop through all parking spots to check if they are empty or not
        for spot_index, spot in enumerate(spots):
            x1, y1, w, h = spot  # Get the bounding box of the spot (x, y, width, height)
            spot_crop = frame[y1:y1+h, x1:x1+w, :]  # Crop the frame to the spot's region
            spot_status = empty_or_not(spot_crop)  # Check if the parking spot is empty
            spots_status[spot_index] = spot_status  # Store the status (True = empty, False = occupied)

            if not spot_status:  # If the spot is occupied
                occupied_spots += 1

        # Draw rectangles around each parking spot, color-coded based on its status
        for spot_index, spot in enumerate(spots):
            spot_status = spots_status[spot_index]  # Get the current status of the spot
            x1, y1, w, h = spots[spot_index]  # Get the coordinates and size of the spot

            # If the spot is empty, draw a green rectangle
            if spot_status:
                frame = cv2.rectangle(frame, (x1, y1), (x1+w, y1+h), (0, 255, 0), 2)
            # If the spot is occupied, draw a red rectangle
            else:
                frame = cv2.rectangle(frame, (x1, y1), (x1+w, y1+h), (0, 0, 255), 2)

        # Add a text label showing the number of occupied spots and total spots
        label = f"Occupied Spots: {occupied_spots} / {total_spots}"
        cv2.putText(frame, label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Create a resizable window and display the current frame with the parking spot status
    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    cv2.imshow('frame', frame)

    # If the 'q' key is pressed, break the loop and stop the video
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

    # Increment the frame counter
    frame_number += 1

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

