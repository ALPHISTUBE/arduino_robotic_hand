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

send_angles([0, 0, 0, 0, 0])  # Send initial angles to the Arduino

# Example usage
cap = cv2.VideoCapture(0)  # Open webcam
while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    # Convert the image to RGB and process it with Mediapipe
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)
    previousDistances = [0, 0, 0, 0, 0]
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get the coordinates of the wrist and finger points
            wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
            finger_points = [hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP],
                             hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP],
                             hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP],
                             hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP],
                             hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]]

            # Calculate the distance between the wrist and each finger point
            distances = [math.dist([wrist.x, wrist.y], [finger.x, finger.y]) for finger in finger_points]
            if previousDistances:
                updatedDistances = []
                for i in range(len(distances)):
                    if abs(distances[i] - previousDistances[i]) > 0.03:  # Adjust the threshold as needed
                        updatedDistances.append(distances[i])
                    else:
                        updatedDistances.append(previousDistances[i])
                distances = updatedDistances
            previousDistances = distances
            selectedAngles = [0, 180]  # Define the angle values for each finger based on the distance ranges

            ranges = [
                [0.2504687380462259, 0.3124047333345117],   # Range for THUMB finger
                [0.20523228396301077, 0.5720734268133739],  # Range for INDEX finger
                [0.17056102933969877, 0.5965675984232481],  # Range for MIDDLE finger
                [0.14162196121660425, 0.5539264929940794],  # Range for RING finger
                [0.1388035388548916, 0.43033979044479204]  # Range for PINKY finger
            ]

            angles = []

            cv2.putText(image, f"Thumb: {distances[0]:.3f}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.putText(image, f"Index: {distances[1]:.3f}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.putText(image, f"Middle: {distances[2]:.3f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.putText(image, f"Ring: {distances[3]:.3f}", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.putText(image, f"Pinky: {distances[4]:.3f}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
            for distance, finger_range in zip(distances, ranges):
                percentage = calculate_percentage(finger_range[0], finger_range[1], distance)
                if percentage < 50:
                    angles.append(selectedAngles[0])
                else:
                    angles.append(selectedAngles[1])

            send_angles(angles)

            mp_drawing = mp.solutions.drawing_utils
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow('Hand Tracking', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

arduino.close()
cap.release()
cv2.destroyAllWindows()
