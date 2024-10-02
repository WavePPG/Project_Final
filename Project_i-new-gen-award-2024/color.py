import cv2
import numpy as np

def rgb_to_cmyk(r, g, b):
    """Converts RGB color to CMYK values."""
    r /= 255
    g /= 255
    b /= 255

    k = 1 - max(r, g, b)
    if k == 1:
        return 0, 0, 0, 1, 0  # Black (CMY = 0, K = 1, W = 0)

    c = (1 - r - k) / (1 - k)
    m = (1 - g - k) / (1 - k)
    y_cmyk = (1 - b - k) / (1 - k)

    # Calculate white based on the amount of black (k)
    w = 1 - k

    # Ensure CMYK values are in the 0-1 range
    c = np.clip(c, 0, 1)
    m = np.clip(m, 0, 1)
    y_cmyk = np.clip(y_cmyk, 0, 1)
    k = np.clip(k, 0, 1)
    w = np.clip(w, 0, 1)

    return c, m, y_cmyk, k, w  # CMYK + W values

# Global variables to store the current point and calculation trigger
current_point = (0, 0)
clicked = False

def mouse_callback(event, x, y_coord, flags, param):
    """Mouse callback function to update the current point on click."""
    global current_point, clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        current_point = (x, y_coord)
        clicked = True  # Set the clicked flag to true

# Open the default camera (source 0)
cap = cv2.VideoCapture(0)

# Initialize variables for RGB, CMYK, and White values
r, g, b = 0, 0, 0
c, m, y_cmyk, k, w = 0, 0, 0, 0, 0

# Initialize variables for color ratios
c_ratio, m_ratio, y_ratio, k_ratio, w_ratio = 0, 0, 0, 0, 0

# Set up the mouse callback
cv2.namedWindow('Color Detection - Press Q to Exit')
cv2.setMouseCallback('Color Detection - Press Q to Exit', mouse_callback)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Check if the frame was captured properly
    if not ret:
        print("Failed to grab frame")
        break

    # If the user clicked, perform color calculations
    if clicked:
        # Get the dimensions of the frame
        height, width, _ = frame.shape

        # Get the RGB values at the current point
        x, y_coord = current_point
        if 0 <= x < width and 0 <= y_coord < height:
            center_rgb = frame[y_coord, x]

            # Convert BGR (from OpenCV) to RGB
            b, g, r = center_rgb
            r, g, b = int(r), int(g), int(b)

            # Convert RGB to CMYK + W
            c, m, y_cmyk, k, w = rgb_to_cmyk(r, g, b)

            # Calculate ratios for 20 ml total
            total_volume = 20
            c_ratio = c * total_volume
            m_ratio = m * total_volume
            y_ratio = y_cmyk * total_volume
            k_ratio = k * total_volume
            w_ratio = w * total_volume

        # Reset the clicked flag so that it doesn't recalculate until next click
        clicked = False

    # Draw a small circle at the center point to show the sampling point
    x, y_coord = current_point
    cv2.circle(frame, (x, y_coord), 5, (255, 255, 255), -1)

    # Add a border around the text to improve readability
    font_scale = 0.45
    text_color = (255, 255, 255)
    border_color = (0, 0, 0)
    thickness = 1

    # Print RGB values
    text_rgb = f"RGB: ({r}, {g}, {b})"
    cv2.putText(frame, text_rgb, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, font_scale, border_color, thickness + 2)
    cv2.putText(frame, text_rgb, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, thickness)

    # Print CMYK values including White
    text_cmykw = f"C: ({c:.2f}, M: {m:.2f}, Y: {y_cmyk:.2f}, K: {k:.2f}, W: {w:.2f})"
    cv2.putText(frame, text_cmykw, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, font_scale, border_color, thickness + 2)
    cv2.putText(frame, text_cmykw, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, thickness)

    # Print mix ratios for 20 ml including white
    text_ratios = f"Mix Ratios for 20ml: C: {c_ratio:.2f}ml, M: {m_ratio:.2f}ml, Y: {y_ratio:.2f}ml, K: {k_ratio:.2f}ml, W: {w_ratio:.2f}ml"
    cv2.putText(frame, text_ratios, (10, 90), cv2.FONT_HERSHEY_SIMPLEX, font_scale, border_color, thickness + 2)
    cv2.putText(frame, text_ratios, (10, 90), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, thickness)

    # Display the resulting frame with color info
    cv2.imshow('Color Detection - Press Q to Exit', frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
