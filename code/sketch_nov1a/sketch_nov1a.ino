#include <Servo.h>

Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;

#define f1 11 // Thumb
#define f2 10 // Index
#define f3 9 // Middle
#define f4 6 // Ring
#define f5 5 // Pinky
int angles[5] = {0, 0, 0, 0, 0};
int preAngles[5] = {0, 0, 0, 0, 0};
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
  // if (Serial.available() > 0) {
  //   // Read the incoming data
  //   int angles[5];
  //   for (int i = 0; i < 5; i++) {
  //     angles[i] = Serial.parseInt();
  //   }
  //   servo1.write(angles[0]);
  //   servo2.write(angles[1]);
  //   servo3.write(angles[2]);
  //   servo4.write(angles[3]);
  //   servo5.write(angles[4]);
  // }

  // Test each servo individually from 0 to 180 degrees
  // for (int i = 0; i < 5; i++) {
  //   for (int angle = 0; angle <= 180; angle += 10) {
  //     if (i == 0) servo1.write(angle);
  //     if (i == 1) servo2.write(angle);
  //     if (i == 2) servo3.write(angle);
  //     if (i == 3) servo4.write(angle);
  //     if (i == 4) servo5.write(angle);
  //     delay(500);
  //   }
  //   for (int angle = 180; angle >= 0; angle -= 10) {
  //     if (i == 0) servo1.write(angle);
  //     if (i == 1) servo2.write(angle);
  //     if (i == 2) servo3.write(angle);
  //     if (i == 3) servo4.write(angle);
  //     if (i == 4) servo5.write(angle);
  //     delay(500);
  //   }
  // }

  // Test all servos together to 0 degrees
  // servo1.write(0);
  // servo2.write(0);
  // servo3.write(0);
  // servo4.write(0);
  servo5.write(0);
  delay(2000);

  // Test all servos together to 180 degrees
  // servo1.write(180);
  // servo2.write(180);
  // servo3.write(180);
  // servo4.write(180);
  servo5.write(180);
  delay(2000);
}