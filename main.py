import serial
import time
import cv2
import mediapipe as mp
import math

# Initialize serial communication
arduino = serial.Serial('COM4', 9600)
time.sleep(2)  # Wait for the connection to be established

# Function to send a list of angles to the Arduino
def send_angles(angles):
    command = ' '.join(map(str, angles)) + '\n'
    arduino.write(command.encode())

# Function to calculate the percentage of a value within a range
def calculate_percentage(min_value, max_value, value):
    if min_value == max_value:
        return 0
    return (value - min_value) / (max_value - min_value) * 100

# Initialize Mediapipe Hand model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Example usage
cap = cv2.VideoCapture(0)  # Open webcam
while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    # Convert the image to RGB and process it with Mediapipe
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get the coordinates of the wrist and finger points
            wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
            finger_points = [hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP],
                             hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP],
                             hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP],
                             hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP],
                             hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]]

            # Calculate the distance between the wrist and each finger point
            distances = [math.dist([wrist.x, wrist.y], [finger.x, finger.y]) for finger in finger_points]

            selectedAngles = [0, 90, 180]  # Define the angle values for each finger based on the distance ranges
            # Define the angle values for each finger based on the distance ranges
            # Modify the ranges variable for each finger
            ranges = [
                [0.20523228396301077, 0.5720734268133739],  # Range for INDEX finger
                [0.17056102933969877, 0.5965675984232481],  # Range for MIDDLE finger
                [0.14162196121660425, 0.5539264929940794],  # Range for RING finger
                [0.1388035388548916, 0.43033979044479204],  # Range for PINKY finger
                [0.2974687380462259, 0.3124047333345117]   # Range for THUMB finger
            ]

            # Determine the angle for each finger based on the distance range
            angles = []
            for distance, finger_range in zip(distances, ranges):
                percentage = calculate_percentage(finger_range[0], finger_range[1], distance)
                if percentage < 10:
                    angles.append(selectedAngles[0])
                elif percentage < 50:
                    angles.append(selectedAngles[1])
                else:
                    angles.append(selectedAngles[2])

            # Send the angles to the Arduino
            send_angles(angles)

            # Draw lines on the image to visualize hand tracking
            mp_drawing = mp.solutions.drawing_utils
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow('Hand Tracking', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

# Close the serial connection
arduino.close()
cap.release()
cv2.destroyAllWindows()
