/// install ArduinoJson
/// install StreamUtils
///

#include <SoftwareSerial.h>
#include <ArduinoJson.h>
#include <StreamUtils.h>

const uint8_t RX = 7;
const uint8_t TX = 6;
const uint8_t BLUEPIN = 3;
bool blue_pin_up = false;
bool builtin_pin_up = false;
const uint16_t default_update_time = 1000;
unsigned long previousMillis_1 = 0;
unsigned long previousMillis_2 = 0;

const uint16_t default_red_color = 127;
const uint16_t default_green_color = 127;
const uint16_t default_blue_color = 127;

uint16_t new_red_color = NULL;
uint16_t new_green_color = NULL;
uint16_t new_blue_color = NULL;

SoftwareSerial SerialBLE(RX, TX); // RX, TX on arduino board

StaticJsonDocument<200> doc_in;
ReadLoggingStream loggingStream(SerialBLE, Serial);

void setup() {
  pinMode(BLUEPIN, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);         // UART speed
  SerialBLE.begin(9600);
}

void loop() {

  ListenBlt();

  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis_1 >= default_update_time) {
    previousMillis_1 = currentMillis;

    PingPong();

    BuiltinPinOnOff();
  }

  if (currentMillis - previousMillis_2 >= 20) {
    previousMillis_2 = currentMillis;

    SetColor();
  }
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
  if (builtin_pin_up) {
    digitalWrite(LED_BUILTIN, LOW);
    builtin_pin_up = false;

  } else {
    digitalWrite(LED_BUILTIN, HIGH);
    builtin_pin_up = true;
  }
}

void SetColor() {

  if (!doc_in.isNull()) {

    if (new_red_color == NULL) {
      new_red_color = doc_in.getMember("red");
    }
    if (new_green_color == NULL) {
      new_green_color = doc_in.getMember("green");
    }
    if (new_blue_color == NULL) {
      new_blue_color = doc_in.getMember("blue");
    }

    Serial.println(
      "input; new_red_color: " + String(new_red_color) +
      "; new_green_color: " + String(new_green_color) +
      "; new_blue_color: " + String(new_blue_color)
    );

    if (new_red_color != NULL && new_green_color != NULL && new_blue_color != NULL) {
      Serial.println("new_red_color: " + String(new_red_color));
      Serial.println("new_green_color: " + String(new_green_color));
      Serial.println("new_blue_color: " + String(new_blue_color));

      StaticJsonDocument<200> doc_out;
      doc_out["color_set"] = true;
      serializeJson(doc_out, SerialBLE);

      doc_in = {};
      new_red_color = NULL;
      new_green_color = NULL;
      new_blue_color = NULL;
      Serial.println(
        "set NULL; new_red_color: " + String(new_red_color) +
        "; new_green_color: " + String(new_green_color) +
        "; new_blue_color: " + String(new_blue_color)
      );

    }
  }
}
