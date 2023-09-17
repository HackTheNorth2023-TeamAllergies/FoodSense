import cv2

import pytesseract

import numpy as np

import time



# Function to calculate image sharpness

def is_image_blurry(image, threshold=150):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    variance = cv2.Laplacian(gray, cv2.CV_64F).var()

    return variance < threshold



# Function to detect and draw a bounding box around the white box

def detect_and_draw_bounding_box(frame):

    # Convert the frame to grayscale

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)



    # Apply thresholding to isolate the white box (you may need to adjust the threshold value)

    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)



    # Find contours in the thresholded image

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)



    # Initialize variables for the largest valid quadrilateral

    largest_quad = None

    largest_quad_area = 0



    for contour in contours:

        # Approximate the contour as a quadrilateral

        epsilon = 0.04 * cv2.arcLength(contour, True)

        approx = cv2.approxPolyDP(contour, epsilon, True)



        # Filter quadrilaterals based on the number of vertices (4)

        if len(approx) == 4:

            # Calculate the area of the quadrilateral

            area = cv2.contourArea(approx)



            # Update the largest quadrilateral if a larger one is found

            if area > largest_quad_area:

                largest_quad = approx

                largest_quad_area = area



    # Draw the largest valid quadrilateral as the bounding quadrilateral

    if largest_quad is not None:

        cv2.drawContours(frame, [largest_quad], -1, (0, 255, 0), 2)  # Green bounding box



    return frame, largest_quad



# Open the webcam

cap = cv2.VideoCapture(0)



if not cap.isOpened():

    print("Error: Cannot open camera")

    exit()



# Create a window

cv2.namedWindow("Camera Feed", cv2.WINDOW_NORMAL)



# Initialize variables

wait_time = 5  # Wait time in seconds

start_time = time.time()

ingredients_text = ""



while True:

    ret, frame = cap.read()



    if not ret:

        print("Error: Cannot read frame")

        break



    # Check image sharpness with the increased threshold

    is_blurry = is_image_blurry(frame)



    # Display the result text

    status_text = "Blurry" if is_blurry else "Clear"

    status_color = (0, 0, 255) if is_blurry else (0, 255, 0)

    cv2.putText(frame, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, status_color, 2)



    # Display a colored rectangle as an indicator

    rect_color = (0, 0, 255) if is_blurry else (0, 255, 0)

    cv2.rectangle(frame, (10, 10), (200, 50), rect_color, -1)



    if not is_blurry:

        # Detect and draw bounding box around the white box

        frame, largest_quad = detect_and_draw_bounding_box(frame)



        # Get the current time

        current_time = time.time()



        if current_time - start_time >= wait_time and not ingredients_text and largest_quad is not None:

            # Extract the coordinates of the largest quadrilateral

            x, y, w, h = cv2.boundingRect(largest_quad)



            # Extract the region of interest (ROI) within the bounding box

            roi = frame[y:y+h, x:x+w]



            # Convert the ROI to grayscale for OCR

            gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)



            # Use pytesseract to perform OCR on the grayscale ROI

            ingredients_text = pytesseract.image_to_string(gray_roi, config='--psm 6')



            # Print the ingredients list

            print("Ingredients List:")

            print(ingredients_text)



    cv2.imshow("Camera Feed", frame)



    if cv2.waitKey(1) & 0xFF == ord('q'):

        break



cap.release()

cv2.destroyAllWindows()