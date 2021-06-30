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

  ListenBlt();        // if the data came from SerialBLE

  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis_1 >= default_update_time) { // period from android app
    previousMillis_1 = currentMillis;

    PingPong();

    BuiltinPinOnOff();
  }
}

void ListenBlt() {
  if (SerialBLE.available() > 0) {
    deserializeJson(doc_in, loggingStream);
  }
}

void PingPong() {
  String ping = doc_in.getMember("ping");

  if (!doc_in.isNull() && ping == "ping") {  // .isNull() ;   .containsKey("")
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
