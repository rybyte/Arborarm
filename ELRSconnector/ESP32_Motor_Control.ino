#include <Arduino.h>
#include <ESP32Servo.h>
#include <CrsfSerial.h>

// === Motor A Pins (CH2) ===
#define IN1 18
#define IN2 19
#define ENA 21

// === Motor B Pins (CH3) ===
#define IN3 5
#define IN4 15
#define ENB 22

// === Servo (CH6) ===
#define SERVO_PIN 23  // Signal pin
Servo myServo;

// === PWM Config ===
#define MOTOR_PWM_FREQ 1000
#define MOTOR_PWM_RES 8
#define SPEED 255

// === CRSF Serial Setup ===
CrsfSerial crsf(Serial2, CRSF_BAUDRATE);  // GPIO16 as RX

void setup() {
  Serial.begin(115200);

  // === Motor A setup ===
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  ledcAttach(ENA, MOTOR_PWM_FREQ, MOTOR_PWM_RES);

  // === Motor B setup ===
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  ledcAttach(ENB, MOTOR_PWM_FREQ, MOTOR_PWM_RES);

  // === Servo setup ===
  myServo.setPeriodHertz(50);  // 50Hz standard
  myServo.attach(SERVO_PIN, 500, 2400);  // 0.5ms to 2.4ms range (MG996R safe)
  myServo.write(90);  // Initial center position

  // === Start CRSF ===
  Serial2.begin(CRSF_BAUDRATE, SERIAL_8N1, 16, -1);  // RX on GPIO16
  crsf.begin();

  Serial.println("🚀 Dual DC Motors + MG996R Servo via ELRS (CH2, CH3, CH6)");
}

void loop() {
  crsf.loop();  // Update CRSF data

  // === Channel Inputs ===
  uint16_t ch2 = crsf.getChannel(2);  // Motor A
  uint16_t ch3 = crsf.getChannel(3);  // Motor B
  uint16_t ch6 = crsf.getChannel(6);  // Servo (CH6 = index 5)

  // === Motor A (CH2) ===
  if (ch2 > 1510) {
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    ledcWrite(ENA, SPEED);
  } else if (ch2 < 1497) {
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    ledcWrite(ENA, SPEED);
  } else {
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, HIGH);
    ledcWrite(ENA, 0);
  }

  // === Motor B (CH3) ===
  if (ch3 > 1510) {
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
    ledcWrite(ENB, SPEED);
  } else if (ch3 < 1497) {
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
    ledcWrite(ENB, SPEED);
  } else {
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, HIGH);
    ledcWrite(ENB, 0);
  }

  // === Servo (CH6) ===
  int angle = map(ch6, 172, 1875, 0, 180);
  angle = constrain(angle, 0, 180);
  myServo.write(angle);

  // === Debug Monitor ===
  Serial.print("CH2: "); Serial.print(ch2);
  Serial.print(" | CH3: "); Serial.print(ch3);
  Serial.print(" | CH6: "); Serial.print(ch6);
  Serial.print(" → Servo Angle: "); Serial.println(angle);

  delay(50);
}
