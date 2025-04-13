#include <Arduino.h>
#include <ESP32Servo.h>  // Make sure this library is installed

Servo myServo;           // Create servo object
const int SERVO_PIN = 23; // Servo signal pin (PWM-capable)

void setup() {
  Serial.begin(115200);

  // Attach servo to GPIO23
  myServo.setPeriodHertz(50);  // Standard 50Hz for hobby servos
  myServo.attach(SERVO_PIN, 500, 2400);  // Min/max pulse width in microseconds

  Serial.println("🔧 MG996R Servo Test Started");
}

void loop() {
  // Sweep 0 → 180
  for (int pos = 0; pos <= 180; pos += 5) {
    myServo.write(pos);
    Serial.print("Angle: ");
    Serial.println(pos);
    delay(50);
  }

  // Sweep 180 → 0
  for (int pos = 180; pos >= 0; pos -= 5) {
    myServo.write(pos);
    Serial.print("Angle: ");
    Serial.println(pos);
    delay(50);
  }

  delay(1000); // Pause between sweeps
}
