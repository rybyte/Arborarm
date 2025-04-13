#include <Arduino.h>
#include <CrsfSerial.h>

// Motor control pins
#define IN1 18
#define IN2 19
#define ENA 21

#define PWM_FREQ 1000
#define PWM_RES 8
#define SPEED 255

// CRSF on UART2 (GPIO16 = RX)
CrsfSerial crsf(Serial2, CRSF_BAUDRATE);

void setup() {
  Serial.begin(115200);

  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  ledcAttach(ENA, PWM_FREQ, PWM_RES);

  Serial2.begin(CRSF_BAUDRATE, SERIAL_8N1, 16, -1);  // RX only
  crsf.begin();

  Serial.println("🔧 CRSF CH2 → Motor Control with Debug");
}

void loop() {
  crsf.loop();  // Process incoming CRSF data

  uint16_t ch2 = crsf.getChannel(2);  // CH2 

  // Show raw CH2 value
  Serial.print("🔁 CH2 Value: ");
  Serial.print(ch2);
  delay(100);

  if (ch2 > 1510) {
    // ➡️ Forward
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    ledcWrite(ENA, SPEED);
    Serial.println(" → Forward");
  }
  else if (ch2 < 1497) {
    // ⬅️ Reverse
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    ledcWrite(ENA, SPEED);
    Serial.println(" → Reverse");
  }
  else {
    // 🛑 Brake
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, HIGH);
    ledcWrite(ENA, 0);
    Serial.println(" → Brake");
  }

  delay(100);  // Adjust for smoother or faster response
}
