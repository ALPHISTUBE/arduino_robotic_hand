#include <Servo.h>

Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;

#define f1 11
#define f2 10
#define f3 9
#define f4 5
#define f5 6

void setup() {
  Serial.begin(9600);  // Initialize serial communication
  // Attach each servo to a different pin
  servo1.attach(f1, 600, 2300);
  servo2.attach(f2, 600, 2300);
  servo3.attach(f3, 600, 2300);
  servo4.attach(f4, 600, 2300);
  servo5.attach(f5, 600, 2300);
}

void loop() {
  if (Serial.available() > 0) {
    // Read the incoming data
    int angles[5];
    for (int i = 0; i < 5; i++) {
      angles[i] = Serial.parseInt();
    }
    // Array of servo objects for easy looping
    Servo servos[5] = {servo1, servo2, servo3, servo4, servo5};

    // Loop through each servo and move to its target angle
    for (int i = 0; i < 5; i++) {
      servos[i].write(angles[i]);  // Move servo to target angle
      delay(500);  // Delay for 1 second before moving to the next finger
    }
  }
}