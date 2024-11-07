import cv2
import mediapipe as mp
import pyautogui
import serial
import hand_tracking_mouse_controller as hand_controller
import drawing as drawing_handler

ser = serial.Serial('COM3', 9600)  # Serial communication setup
hand_detector = mp.solutions.hands.Hands()
screen_w, screen_h = pyautogui.size()  # Get screen dimensions

class HardwareController:    
    def __init__(self):
        self.video = cv2.VideoCapture(1)

    def __del__(self):
        self.video.release()

    def signal(self):       
        _, frame = self.video.read()
        frame = cv2.flip(frame, 1)
        frame_h, frame_w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = hand_detector.process(rgb_frame)
        hands = output.multi_hand_landmarks

        if hands:
            try: 
                data_to_send = '0'  # Serial communication for hand detection
                ser.write(data_to_send.encode())
            except KeyboardInterrupt:
                print("Exiting...")
                ser.close()
        else:
            try: 
                data_to_send = '1'  # Serial communication for no hand detection
                ser.write(data_to_send.encode())
            except KeyboardInterrupt:
                print("Exiting...")
                ser.close()

        _, jpg = cv2.imencode('.jpg', frame)
        return jpg.tobytes()

class HandMouseController:
    def virtual_mouse():
        hand_controller.main()  # Calls the hand tracking module's main function

class DrawingController:
    def get_drawing_frame():
        return drawing_handler.get_frame()