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