import cv2
import mediapipe as mp
import pyautogui

# Controller class
class Controller:
    prev_hand = None
    right_clicked = False
    left_clicked = False
    double_clicked = False
    dragging = False
    hand_Landmarks = None
    little_finger_down = None
    little_finger_up = None
    index_finger_down = None
    index_finger_up = None
    middle_finger_down = None
    middle_finger_up = None
    ring_finger_down = None
    ring_finger_up = None
    Thump_finger_down = None 
    Thump_finger_up = None
    all_fingers_down = None
    all_fingers_up = None
    index_finger_within_Thumb_finger = None
    middle_finger_within_Thumb_finger = None
    little_finger_within_Thumb_finger = None
    ring_finger_within_Thumb_finger = None
    screen_width, screen_height = pyautogui.size()

    @staticmethod
    def update_fingers_status():
        Controller.little_finger_down = Controller.hand_Landmarks.landmark[20].y > Controller.hand_Landmarks.landmark[17].y
        Controller.little_finger_up = Controller.hand_Landmarks.landmark[20].y < Controller.hand_Landmarks.landmark[17].y
        Controller.index_finger_down = Controller.hand_Landmarks.landmark[8].y > Controller.hand_Landmarks.landmark[5].y
        Controller.index_finger_up = Controller.hand_Landmarks.landmark[8].y < Controller.hand_Landmarks.landmark[5].y
        Controller.middle_finger_down = Controller.hand_Landmarks.landmark[12].y > Controller.hand_Landmarks.landmark[9].y
        Controller.middle_finger_up = Controller.hand_Landmarks.landmark[12].y < Controller.hand_Landmarks.landmark[9].y
        Controller.ring_finger_down = Controller.hand_Landmarks.landmark[16].y > Controller.hand_Landmarks.landmark[13].y
        Controller.ring_finger_up = Controller.hand_Landmarks.landmark[16].y < Controller.hand_Landmarks.landmark[13].y
        Controller.Thump_finger_down = Controller.hand_Landmarks.landmark[4].y > Controller.hand_Landmarks.landmark[13].y
        Controller.Thump_finger_up = Controller.hand_Landmarks.landmark[4].y < Controller.hand_Landmarks.landmark[13].y
        Controller.all_fingers_down = Controller.index_finger_down and Controller.middle_finger_down and Controller.ring_finger_down and Controller.little_finger_down
        Controller.all_fingers_up = Controller.index_finger_up and Controller.middle_finger_up and Controller.ring_finger_up and Controller.little_finger_up
        Controller.index_finger_within_Thumb_finger = Controller.hand_Landmarks.landmark[8].y > Controller.hand_Landmarks.landmark[4].y and Controller.hand_Landmarks.landmark[8].y < Controller.hand_Landmarks.landmark[2].y
        Controller.middle_finger_within_Thumb_finger = Controller.hand_Landmarks.landmark[12].y > Controller.hand_Landmarks.landmark[4].y and Controller.hand_Landmarks.landmark[12].y < Controller.hand_Landmarks.landmark[2].y
        Controller.little_finger_within_Thumb_finger = Controller.hand_Landmarks.landmark[20].y > Controller.hand_Landmarks.landmark[4].y and Controller.hand_Landmarks.landmark[20].y < Controller.hand_Landmarks.landmark[2].y
        Controller.ring_finger_within_Thumb_finger = Controller.hand_Landmarks.landmark[16].y > Controller.hand_Landmarks.landmark[4].y and Controller.hand_Landmarks.landmark[16].y < Controller.hand_Landmarks.landmark[2].y
    
    @staticmethod
    def get_position(hand_x_position, hand_y_position):
        old_x, old_y = pyautogui.position()
        current_x = int(hand_x_position * Controller.screen_width)
        current_y = int(hand_y_position * Controller.screen_height)

        ratio = 1
        Controller.prev_hand = (current_x, current_y) if Controller.prev_hand is None else Controller.prev_hand
        delta_x = current_x - Controller.prev_hand[0]
        delta_y = current_y - Controller.prev_hand[1]
        
        Controller.prev_hand = [current_x, current_y]
        current_x , current_y = old_x + delta_x * ratio , old_y + delta_y * ratio

        threshold = 5
        if current_x < threshold:
            current_x = threshold
        elif current_x > Controller.screen_width - threshold:
            current_x = Controller.screen_width - threshold
        if current_y < threshold:
            current_y = threshold
        elif current_y > Controller.screen_height - threshold:
            current_y = Controller.screen_height - threshold

        return (current_x, current_y)
        
    @staticmethod
    def cursor_moving():
        point = 9
        current_x, current_y = Controller.hand_Landmarks.landmark[point].x , Controller.hand_Landmarks.landmark[point].y
        x, y = Controller.get_position(current_x, current_y)
        cursor_freezed = Controller.all_fingers_up and Controller.Thump_finger_down
        if not cursor_freezed:
            pyautogui.moveTo(x, y, duration = 0)
    
    @staticmethod
    def detect_scrolling():
        scrolling_up =  Controller.little_finger_up and Controller.index_finger_down and Controller.middle_finger_down and Controller.ring_finger_down
        if scrolling_up:
            pyautogui.scroll(120)
            print("Scrolling UP")

        scrolling_down = Controller.index_finger_up and Controller.middle_finger_down and Controller.ring_finger_down and Controller.little_finger_down
        if scrolling_down:
            pyautogui.scroll(-120)
            print("Scrolling DOWN")
    
    @staticmethod
    def detect_zoomming():
        zoomming = Controller.index_finger_up and Controller.middle_finger_up and Controller.ring_finger_down and Controller.little_finger_down
        window = .05
        index_touches_middle = abs(Controller.hand_Landmarks.landmark[8].x - Controller.hand_Landmarks.landmark[12].x) <= window
        zoomming_out = zoomming and index_touches_middle
        zoomming_in = zoomming and not index_touches_middle
        
        if zoomming_out:
            pyautogui.keyDown('ctrl')
            pyautogui.scroll(-50)
            pyautogui.keyUp('ctrl')
            print("Zooming Out")

        if zoomming_in:
            pyautogui.keyDown('ctrl')
            pyautogui.scroll(50)
            pyautogui.keyUp('ctrl')
            print("Zooming In")

    @staticmethod
    def detect_clicking():
        left_click_condition = Controller.index_finger_within_Thumb_finger and Controller.middle_finger_up and Controller.ring_finger_up and Controller.little_finger_up and not Controller.middle_finger_within_Thumb_finger and not Controller.ring_finger_within_Thumb_finger and not Controller.little_finger_within_Thumb_finger
        if not Controller.left_clicked and left_click_condition:
            pyautogui.click()
            Controller.left_clicked = True
            print("Left Clicking")
        elif not Controller.index_finger_within_Thumb_finger:
            Controller.left_clicked = False

        right_click_condition = Controller.middle_finger_within_Thumb_finger and Controller.index_finger_up and Controller.ring_finger_up and Controller.little_finger_up and not Controller.index_finger_within_Thumb_finger and not Controller.ring_finger_within_Thumb_finger and not Controller.little_finger_within_Thumb_finger
        if not Controller.right_clicked and right_click_condition:
            pyautogui.rightClick()
            Controller.right_clicked = True
            print("Right Clicking")
        elif not Controller.middle_finger_within_Thumb_finger:
            Controller.right_clicked = False

        double_click_condition = Controller.ring_finger_within_Thumb_finger and Controller.index_finger_up and Controller.middle_finger_up and Controller.little_finger_up and not Controller.index_finger_within_Thumb_finger and not Controller.middle_finger_within_Thumb_finger and not Controller.little_finger_within_Thumb_finger
        if not Controller.double_clicked and  double_click_condition:
            pyautogui.doubleClick()
            Controller.double_clicked = True
            print("Double Clicking")
        elif not Controller.ring_finger_within_Thumb_finger:
            Controller.double_clicked = False
    
    @staticmethod
    def detect_dragging():
        if not Controller.dragging and Controller.all_fingers_down:
            pyautogui.mouseDown(button = "left")
            Controller.dragging = True
            print("Dragging")
        elif not Controller.all_fingers_down:
            pyautogui.mouseUp(button = "left")
            Controller.dragging = False


# Initialize video capture
cap = cv2.VideoCapture(0)

# Initialize Mediapipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # Convert image to RGB for Mediapipe processing
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            Controller.hand_Landmarks = hand_landmarks
            mp_draw.draw_landmarks(img, Controller.hand_Landmarks, mp_hands.HAND_CONNECTIONS)

            # Update finger statuses
            Controller.update_fingers_status()

            # Execute actions
            Controller.cursor_moving()
            Controller.detect_scrolling()
            Controller.detect_zoomming()
            Controller.detect_clicking()
            Controller.detect_dragging()
    # Display the frame
    cv2.imshow('Hand Gesture Controller', img)

    # Break the loop on pressing "ESC"
    if cv2.waitKey(5) & 0xFF == 27:
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
