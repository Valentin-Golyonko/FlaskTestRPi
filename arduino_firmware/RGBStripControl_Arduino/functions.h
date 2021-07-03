/// install ArduinoJson
/// install StreamUtils
///

#include <SoftwareSerial.h>
#include <ArduinoJson.h>
#include <StreamUtils.h>
#include <stdint.h>
#include <Wire.h>

struct input {
  const uint8_t RX = 7;           // BLT
  const uint8_t TX = 6;

  bool builtin_pin_up = false;

  const uint8_t BlueLedPin = 8;   // power indicator
  const uint8_t relayPin = 12;
  const uint8_t pirInputPin = 4;  // choose the input pin for PIR sensor
  const uint8_t pinBuzzer = 3;
  const uint8_t pinPhoto = A0;    // photo resistor

  const uint8_t REDPIN = 10;      // RGB Strip pins
  const uint8_t GREENPIN = 11;
  const uint8_t BLUEPIN = 9;

  uint16_t photo = 0;             // data from it
  bool buzzer_play = false;       // play/stop sound

  bool autoBrightness = true;     // autoBrightness on/off
  uint8_t autoB = 1;
  uint16_t period = 5000;

  bool light_always = false;

  const uint8_t default_red_color = 127;
  const uint8_t default_green_color = 127;
  const uint8_t default_blue_color = 127;

  uint8_t new_red_color = NULL;
  uint8_t new_green_color = NULL;
  uint8_t new_blue_color = NULL;

  uint8_t relayStatus = 1;    // pin status (def-t = OFF)
  uint8_t pirStatus = 0;      // we start, assuming no motion detected (def-t = OFF)
};

struct input sP;
struct input *ptr = &sP;

SoftwareSerial SerialBLE(sP.RX, sP.TX); // RX, TX on arduino board

StaticJsonDocument<200> doc_in;
ReadLoggingStream loggingStream(SerialBLE, Serial);

void RGBStrip(uint8_t r, uint8_t g, uint8_t b) {
  float multiplier = 1.0f;
  if (ptr->autoBrightness) {
    multiplier = 1.0f - (float)((sP.photo + 1.0f) / 1025.0f);   // Max outer light -> min RGBStrip brightness
  }

  analogWrite(ptr->REDPIN , r * multiplier);
  analogWrite(ptr->GREENPIN , g * multiplier);
  analogWrite(ptr->BLUEPIN , b * multiplier);
}

void Buzzer() {
  tone(ptr->pinBuzzer, 1000);   // Send 1KHz sound signal...
  delay(100);
  noTone(ptr->pinBuzzer);       // Stop sound...
}

void PIR(uint8_t val) {
  if (val == 1) {  // check if the input is 1
    digitalWrite(sP.relayPin, 0);  // turn LED ON
    RGBStrip(ptr->default_red_color, ptr->default_green_color, ptr->default_blue_color);
    if (ptr->pirStatus == 0) {
      sP.pirStatus = 1;
    }
  } else if (ptr->pirStatus == 1) {
    sP.pirStatus = 0;
  }
}

void PinStatus() {
  sP.relayStatus = digitalRead(ptr->relayPin);  // relayState
  sP.pirStatus = digitalRead(ptr->pirInputPin); // pirState
  sP.photo = analogRead(ptr->pinPhoto);         // photoResistor
}

void ListenBlt() {
  // if the data came from SerialBLE
  if (SerialBLE.available() > 0) {
    deserializeJson(doc_in, loggingStream);
  }
}

void PingPong() {
  String ping = doc_in.getMember("ping");

  if (!doc_in.isNull() && ping == "ping") {
    Serial.println("ping: " + String(ping));

    StaticJsonDocument<200> doc_out;
    doc_out["ping"] = "pong";
    serializeJson(doc_out, SerialBLE);

    doc_in = {};
  }
}

void BuiltinPinOnOff() {
  if (ptr->builtin_pin_up) {
    digitalWrite(LED_BUILTIN, LOW);
    sP.builtin_pin_up = false;

  } else {
    digitalWrite(LED_BUILTIN, HIGH);
    sP.builtin_pin_up = true;
  }
}

void SetColor() {

  if (!doc_in.isNull()) {

    if (ptr->new_red_color == NULL) {
      sP.new_red_color = doc_in.getMember("red");
    }

    if (ptr->new_green_color == NULL) {
      sP.new_green_color = doc_in.getMember("green");
    }

    if (ptr->new_blue_color == NULL) {
      sP.new_blue_color = doc_in.getMember("blue");
    }

    if (sP.new_red_color != NULL && sP.new_green_color != NULL && sP.new_blue_color != NULL) {

      StaticJsonDocument<200> doc_out;
      doc_in = {};

      if (sP.new_red_color == sP.new_green_color == sP.new_blue_color == 1) {
        Serial.println("power off");

        digitalWrite(sP.relayPin , 1);  // power off

        sP.light_always = false;

        doc_out["light_off"] = true;

      } else {
        Serial.println("power on");
        
        digitalWrite(sP.relayPin , 0);

        sP.light_always = true;

        doc_out["light_up"] = true;
      }

      RGBStrip(ptr->new_red_color, ptr->new_green_color, ptr->new_blue_color);

      serializeJson(doc_out, SerialBLE);

      Buzzer();

      doc_in = {};
      sP.new_red_color = NULL;
      sP.new_green_color = NULL;
      sP.new_blue_color = NULL;
    }
  }
}
