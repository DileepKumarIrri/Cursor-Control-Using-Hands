import cv2
import mediapipe as mp
import pyautogui

hand_detector=mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
screen_w, screen_h= pyautogui.size()
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
class vm():    
    def __init__(self):
        self.video=cv2.VideoCapture(0)
    def __del__(self):
        self.video.release()
    def virtual_mouse(self):       
        _, frame = self.video.read()
        frame = cv2.flip(frame, 1)
        frame_h , frame_w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        output = hand_detector.process(rgb_frame)
        hands = output.multi_hand_landmarks
        index_y = 0
        if hands:
            for hand in hands:               
                drawing_utils.draw_landmarks(frame, hand)
                landmarks = hand.landmark
                for id, landmark in enumerate(landmarks):
                    x = int(landmark.x*frame_w)
                    y = int(landmark.y*frame_h)
                    print(x, y)
                    if id == 8:
                        cv2.circle(img=frame, center=(x,y), radius=10, color=(0,255,255))                      
                        index_x = screen_w/frame_w*x
                        index_y = screen_h/frame_h*y
                        pyautogui.moveTo(index_x,index_y)
                    if id == 4:
                        cv2.circle(img=frame, center=(x,y), radius=10, color=(0,255,255))
                        thumb_x = screen_w/frame_w*x
                        thumb_y = screen_h/frame_h*y
                        print('outside ',abs(index_y - thumb_y))
                        if abs(index_y - thumb_y)<20:
                            pyautogui.click(clicks=2)
                            pyautogui.sleep(1)
                    if id == 12:
                        cv2.circle(img=frame, center=(x,y), radius=10, color=(0,255,255))
                        mid_x = screen_w/frame_w*x
                        mid_y = screen_h/frame_h*y
                        print('outside ',abs(index_y - mid_y))
                        if abs(index_y - mid_y)<20:
                            pyautogui.click(clicks=2)
                            pyautogui.sleep(1)
                        
        _,jpg=cv2.imencode('.jpg',frame)
        return jpg.tobytes()

class vm2():
    def __init__(self):
        self.video=cv2.VideoCapture(0)
    def __del__(self):
        self.video.release()
    def virtual_mouse2(self):       
        _, frame2 = self.video.read()
        frame2 = cv2.flip(frame2, 1)
        rgb_frame = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
        output2 = face_mesh.process(rgb_frame)
        landmark_points = output2.multi_face_landmarks
        frame_h2, frame_w2, _ = frame2.shape
        if landmark_points:
            landmarks = landmark_points[0].landmark
            for id, landmark in enumerate(landmarks[474:478]):
                x = int(landmark.x * frame_w2)
                y = int(landmark.y * frame_h2)
                cv2.circle(frame2, (x, y), 3, (0, 255, 0))
                if id == 1:
                    screen_x = screen_w * landmark.x
                    screen_y = screen_h * landmark.y
                    pyautogui.moveTo(screen_x, screen_y)
            left = [landmarks[145], landmarks[159]]
            for landmark in left:
                x = int(landmark.x * frame_w2)
                y = int(landmark.y * frame_h2)
                cv2.circle(frame2, (x, y), 3, (0, 255, 255))
            if (left[0].y - left[1].y) < 0.004:
                pyautogui.click(clicks=2)
                pyautogui.sleep(1)
        _,jpg2=cv2.imencode('.jpg',frame2)
        return jpg2.tobytes()
    













  
    