import cv2
import pytesseract

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

    # Iterate through the contours and draw a bounding box around the largest one
    largest_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest_contour)
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green bounding box

    return frame

# Define the region of interest (ROI) coordinates
roi_x, roi_y, roi_w, roi_h = 100, 100, 400, 400
  
# open the webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Cannot open camera")
    exit()
    
# create a window
cv2.namedWindow("Camera Feed", cv2.WINDOW_NORMAL)

while True:
  ret, frame = cap.read()
  
  if not ret:
    print("Error: Cannot read frame")
    break
  
  # Extract the ROI from the frame
  roi = frame[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]
    
  # Check image sharpness with the increased threshold
  is_blurry = is_image_blurry(roi)

  # Display the result text
  status_text = "Blurry" if is_blurry else "Clear"
  status_color = (0, 0, 255) if is_blurry else (0, 255, 0)
  cv2.putText(frame, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, status_color, 2)

  # Display a colored rectangle as an indicator
  rect_color = (0, 0, 255) if is_blurry else (0, 255, 0)
  cv2.rectangle(frame, (10, 10), (200, 50), rect_color, -1)
    
  ingredients_text = ""
  
  if not is_blurry:
    # Detect and draw bounding box around the white box
    frame = detect_and_draw_bounding_box(frame)
    
    # Convert the ROI to grayscale for better OCR results
    roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
    # Use pytesseract to perform OCR on the grayscale ROI
    ingredients_text = pytesseract.image_to_string(roi_gray, config='--psm 6')

  # Display the extracted text
  print("Ingredients List:")
  print(ingredients_text)
  
  cv2.imshow("Camera Feed", frame)
  
  if is_image_blurry(frame):
    print("Image is blurry")
  else:
    print("Image is clear")
    
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break
  
cap.release()
cv2.destroyAllWindows()
  