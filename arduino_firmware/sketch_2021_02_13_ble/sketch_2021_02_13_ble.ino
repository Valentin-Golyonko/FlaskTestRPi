#include <SoftwareSerial.h>
#include <ArduinoJson.h>
#include <StreamUtils.h>

const uint8_t RX = 7;
const uint8_t TX = 6;
const uint8_t BLUEPIN = 3;
bool blue_pin_up = false;
String some_data = "";

SoftwareSerial SerialBLE(RX, TX); // RX,TX on arduino board

unsigned long previousMillis_1 = 0;

StaticJsonDocument<200> doc_in;
ReadLoggingStream loggingStream(SerialBLE, Serial);

void ListenBlt() {
  if (SerialBLE.available() > 0) {
    deserializeJson(doc_in, loggingStream);
    //    loggingStream.read();

    send_data();
  }
}

void send_data() {
  StaticJsonDocument<200> doc_out;
  long timestamp = millis();
  int value = digitalRead(BLUEPIN);
  doc_out["timestamp"] = timestamp;
  doc_out["value"] = value;
  serializeJson(doc_out, SerialBLE);
}

void setup() {
  pinMode(BLUEPIN, OUTPUT);
  Serial.begin(9600);         // UART speed
  SerialBLE.begin(9600);
}

void loop() {
  ListenBlt();        // if the data came from SerialBLE
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis_1 >= 1000) { // period from android app
    previousMillis_1 = currentMillis;

    String hello = doc_in.getMember("hello");
    if (!doc_in.isNull()) {  // .isNull() ;   .containsKey("")
      Serial.println("hello: " + String(hello));
      doc_in = {};
    }

    if (blue_pin_up) {
      digitalWrite(BLUEPIN, LOW);
      blue_pin_up = false;
    } else {
      digitalWrite(BLUEPIN, HIGH);
      blue_pin_up = true;
    }
  }
}
