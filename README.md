# Parking-Lot-Car-Detection
This project uses OpenCV to detect and classify parking spots in a video feed as empty or occupied. It applies a pre-defined mask to locate parking spots and updates their status in real-time, displaying green for empty spots and red for occupied ones.

main.py: This is the main script that processes the video feed. It uses OpenCV to classify parking spots as empty or occupied based on a predefined mask and displays the results.
util.py: Contains helper functions such as get_parking_spots_bboxes, which extracts bounding boxes of parking spots from the mask, and empty_or_not, which determines whether a parking spot is empty.

![output_parking_lot](https://github.com/user-attachments/assets/401e4b53-5f36-433c-83c8-68148f20ffd6)


