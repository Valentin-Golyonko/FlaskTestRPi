#include <WiFiMulti.h>
#include <WiFiClient.h>
#include <ArduinoOTA.h>

WiFiMulti wifiMulti;

//--- wifi spots
//const char* ssid_1 = "suslik9282";        // set up your own wifi config !
//const char* password_1 = "3M0l4@09";
//const char* ssid_2 = "suslik928";
//const char* password_2 = "08022403";
//const char* ssid_3 = "suslik5.0";
//const char* password_3 = "1q2w3eZXC";
const char* ssid_4 = "suslik2.4";
const char* password_4 = "1q2w3e4rASD";

const char* host = "192.168.0.102";

void startWiFi() {      // Try to connect to some given access points. Then wait for a connection
  WiFi.mode(WIFI_STA);
  //WiFi.begin(ssid, password);
//  wifiMulti.addAP(ssid_3, password_3);
  wifiMulti.addAP(ssid_4, password_4);
//  wifiMulti.addAP(ssid_1, password_1);        // add Wi-Fi networks you want to connect to
//  wifiMulti.addAP(ssid_2, password_2);

  Serial.println("Connecting...");            // Wait for the Wi-Fi to connect
  wifiMulti.run();                            // wifiMulti.run() or WiFi.status()
  delay(10);

  if (wifiMulti.run() == WL_CONNECTED) {      // Tell us what network we're connected to
    Serial.println("\r\n");
    Serial.println("Connected to:\t" + (String) WiFi.SSID());
    Serial.print("IP address:\t");
    Serial.print(WiFi.localIP());
    Serial.println("\r\n");
  }
}

void ota() {
  // Port defaults to 3232
  // ArduinoOTA.setPort(3232);

  // Hostname defaults to esp3232-[MAC]
  // ArduinoOTA.setHostname("myesp32");

  // No authentication by default
  // ArduinoOTA.setPassword("admin");

  // Password can be set with it's md5 value as well
  // MD5(admin) = 21232f297a57a5a743894a0e4a801fc3
  // ArduinoOTA.setPasswordHash("21232f297a57a5a743894a0e4a801fc3");

  ArduinoOTA
  .onStart([]() {
    String type;
    if (ArduinoOTA.getCommand() == U_FLASH)
      type = "sketch";
    else // U_SPIFFS
      type = "filesystem";

    // NOTE: if updating SPIFFS this would be the place to unmount SPIFFS using SPIFFS.end()
    Serial.println("Start updating " + type);
  })
  .onEnd([]() {
    Serial.println("\nEnd");
  })
  .onProgress([](unsigned int progress, unsigned int total) {
    Serial.printf("Progress: %u%%\r", (progress / (total / 100)));
  })
  .onError([](ota_error_t error) {
    Serial.printf("Error[%u]: ", error);
    if (error == OTA_AUTH_ERROR) Serial.println("Auth Failed");
    else if (error == OTA_BEGIN_ERROR) Serial.println("Begin Failed");
    else if (error == OTA_CONNECT_ERROR) Serial.println("Connect Failed");
    else if (error == OTA_RECEIVE_ERROR) Serial.println("Receive Failed");
    else if (error == OTA_END_ERROR) Serial.println("End Failed");
  });

}
