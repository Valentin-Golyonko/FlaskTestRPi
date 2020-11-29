#include "net.h"
#include <ArduinoJson.h>
#include <WiFiClient.h>

unsigned long updMillis = 0;
const uint8_t LED_BUILTIN = 2;
bool start = true;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);
  Serial.begin(115200);
  Serial.println("Booting");

  startWiFi();
  ota();
  ArduinoOTA.begin();
}

void sendJson() {
  int t = random(-40, 50);
  int h = random(5, 95);
  int a = random(100, 300);
  int p = random(950, 1100);

  // Use WiFiClient class to create TCP connections
  WiFiClient client;
  const int httpPort = 5001;
  if (!client.connect(host, httpPort)) {
    Serial.println("connection failed");
    return;
  }

  StaticJsonDocument<200> doc;
  // DynamicJsonDocument  doc(200);
  doc["sensor"] = "esp32";
  doc["time"] = 1351824120;
  doc["temp"] = t;
  doc["hum"] = h;
  doc["air"] = a;
  doc["pres"] = p;
  
  serializeJson(doc, Serial);
  Serial.println();
  serializeJson(doc, client);

  unsigned long timeout = millis();
  while (client.available() == 0) {
    if (millis() - timeout > 5000) {
      Serial.println("Client Timeout!");
      client.stop();
      return;
    }
  }

  // Read all the lines of the reply from server and print them to Serial
  while (client.available()) {
    String line = client.readStringUntil('\r');
    Serial.print(line);
  }

  client.print("q");

  Serial.println();
  Serial.println("closing connection");
}

void loop() {
  ArduinoOTA.handle();
  unsigned long currentMillis = millis();
  
  if (currentMillis - updMillis > 10000) {     // update sensors every 'period' = 300000 = 5 min
    updMillis = currentMillis;
    
    digitalWrite(LED_BUILTIN, HIGH);
    Serial.println("delta time 10 sec");

    sendJson();

    digitalWrite(LED_BUILTIN, LOW);
  }
  if (start) {
    sendJson();
    start = false;
  }
}
