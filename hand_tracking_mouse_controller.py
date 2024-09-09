import cv2
import mediapipe as mp
import numpy as np
import pyautogui
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2

MARGIN = 10  # pixels
FONT_SIZE = 1
FONT_THICKNESS = 1
HANDEDNESS_TEXT_COLOR = (88, 205, 54) # vibrant green

cursor_radius = 10
cursor_color = (0, 255, 0)  
click_color = (0, 0, 255)  #


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

pyautogui.FAILSAFE = 'False'
cursor_positions = []

def apply_moving_average(new_position):
    cursor_positions.append(new_position)
    if len(cursor_positions) > 3: 
        cursor_positions.pop(0)
    return np.mean(cursor_positions, axis=0).astype(int)

def modified(scale_x, scale_y):
    if(scale_x>=960):
        scale_x += (0.284*(scale_x))-262.60
    else:
        scale_x -= 263.64-(0.284*(scale_x))
    
    if(scale_y>=540):
        scale_y += (0.963*scale_y)-510.1
    else:
        scale_y -= (-0.31*scale_y)+176.8
        
    return (scale_x,scale_y)


def draw_landmarks_on_image(rgb_image, detection_result):
    mp_drawing = mp.solutions.drawing_utils
    hand_landmarks_list = detection_result.multi_hand_landmarks
    annotated_image = np.copy(rgb_image)
    # Loop through the detected hands to visualize.
    for hand_landmarks in hand_landmarks_list:
        # Draw the hand landmarks.
        hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        hand_landmarks_proto.landmark.extend([
          landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks.landmark
        ])
        mp_drawing.draw_landmarks(
          annotated_image,
          hand_landmarks_proto,
          mp_hands.HAND_CONNECTIONS,
          mp_drawing.DrawingSpec(color=(255,255,255), thickness=1, circle_radius=1),
          mp_drawing.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=2)
        )
        # Get the top left corner of the detected hand's bounding box.
        height, width, _ = annotated_image.shape
        x_coordinates = [landmark.x for landmark in hand_landmarks.landmark]
        y_coordinates = [landmark.y for landmark in hand_landmarks.landmark]
        text_x = int(min(x_coordinates) * width)
        text_y = int(min(y_coordinates) * height) - MARGIN
        # Draw handedness (left or right hand) on the image.
        if detection_result.multi_handedness:
            handedness = detection_result.multi_handedness[0].classification[0].label
            cv2.putText(annotated_image, f"{handedness}",
                        (text_x, text_y), cv2.FONT_HERSHEY_DUPLEX,
                        FONT_SIZE, HANDEDNESS_TEXT_COLOR, FONT_THICKNESS, cv2.LINE_AA)
    return annotated_image





def main():
    cap = cv2.VideoCapture(0)
    screen_width, screen_height = pyautogui.size()  #
    print(screen_height) # 1080
    print(screen_width) # 1920
    while True:
        success, img = cap.read()
        if not success:
            continue

        img = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        if results.multi_hand_landmarks:
            img = draw_landmarks_on_image(img, results)
            for hand_landmarks in results.multi_hand_landmarks:
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]


                # print("thumb ",thumb_tip)
                thumb_tip_pos = np.array([thumb_tip.x, thumb_tip.y])
                index_finger_tip_pos = np.array([index_finger_tip.x, index_finger_tip.y])
                # print(thumb_tip_pos[0])
                width, height = img.shape[1], img.shape[0]
                # width =width+200 # 640
                # height=height+200 # 480
                # print("w:", width)
                # print(height)
                thumb_tip_pos_scaled = np.multiply(thumb_tip_pos, [width, height]).astype(int)
                index_finger_tip_pos_scaled = np.multiply(index_finger_tip_pos, [width, height]).astype(int)

                smoothed_position = apply_moving_average(index_finger_tip_pos_scaled)

                scaled_x = np.interp(smoothed_position[0], [0, width], [0, screen_width])
                scaled_y = np.interp(smoothed_position[1], [0, height], [0, screen_height])
                coordinates= modified(scaled_x,scaled_y)
                scaled_x = coordinates[0]
                scaled_y = coordinates[1]
                # print(scaled_x)
                # print("y ", scaled_y)
                # thumb_tip_pos_scaled = scale_with_edge_correction(thumb_tip_pos, img.shape[1], img.shape[0], screen_width, screen_height, edge_buffer=30)
                # index_finger_tip_pos_scaled = scale_with_edge_correction(index_finger_tip_pos, img.shape[1], img.shape[0], screen_width, screen_height, edge_buffer=30)
                distance = np.linalg.norm(thumb_tip_pos_scaled - index_finger_tip_pos_scaled)
                # print(thumb_tip_pos_scaled )
                # print(index_finger_tip_pos_scaled)
                print(distance)
                clicked = distance < 24

                pyautogui.moveTo(scaled_x, scaled_y) 
                if clicked:
                    pyautogui.click(clicks=1)  

        cv2.imshow("Cursor Control", img)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
