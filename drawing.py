import cv2
import numpy as np
import mediapipe as mp

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

def initialize_camera():
    return cv2.VideoCapture(0)

def process_frame(frame, drawing_mode, accumulator_frame):
    fs = frame.shape
    flipped = cv2.flip(frame, 1)

    # Initialize accumulator_frame if not already
    if accumulator_frame is None:
        accumulator_frame = np.zeros_like(flipped)

    # Convert the BGR image to RGB
    img_rgb = cv2.cvtColor(flipped, cv2.COLOR_BGR2RGB)

    # Use MediaPipe to detect hands in the image
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Extract the index finger tip coordinates
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            x, y = int(index_finger_tip.x * fs[1]), int(index_finger_tip.y * fs[0])

            # Draw the cursor in green when in drawing mode
            if drawing_mode:
                cv2.circle(accumulator_frame, (x, y), 10, (0, 255, 0), -1)
            else:
                # Draw the cursor in blue when in erasing mode
                cv2.circle(accumulator_frame, (x, y), 10, (255, 0, 0), -1)

            # Draw or erase based on drawing mode
            if drawing_mode:
                # Draw a circle at the index finger tip in yellow
                cv2.circle(accumulator_frame, (x, y), 10, (0, 255, 255), -1)
            else:
                # Erase by drawing a black circle
                cv2.circle(accumulator_frame, (x, y), 20, (0, 0, 0), -1)

    return accumulator_frame

def toggle_drawing_mode(current_mode):
    return not current_mode

def main():
    cap = initialize_camera()
    accumulator_frame = None
    drawing_mode = True  # Start with drawing mode

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        accumulator_frame = process_frame(frame, drawing_mode, accumulator_frame)

        # Show the frame with drawing or erasing
        cv2.imshow('Draw', accumulator_frame)

        # Toggle drawing mode on pressing 'e'
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        elif key == ord('e'):
            drawing_mode = toggle_drawing_mode(drawing_mode)  # Toggle drawing mode

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
