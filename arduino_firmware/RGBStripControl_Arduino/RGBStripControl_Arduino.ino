#include "functions.h"
#include "music.h"

const uint16_t default_update_time = 1000;
unsigned long previousMillis_1 = 0;
unsigned long previousMillis_2 = 0;
unsigned long previousMillis_3 = 0;

uint16_t pirTimer = 30000;    // 30 sec

void setup() {

  // declare digital pins
  pinMode(ptr->relayPin, OUTPUT);
  digitalWrite(ptr->relayPin , ptr->relayStatus); // turn OFF relay !!!
  // it depends on connection to relay - green led mast be OFF
  // in that case relay is OFF -> no power consuming
  pinMode(ptr->pirInputPin, INPUT);   // declare rip-sensor as input
  digitalWrite(ptr->pirInputPin , ptr->pirStatus);
  pinMode(ptr->REDPIN, OUTPUT);
  pinMode(ptr->GREENPIN, OUTPUT);
  pinMode(ptr->BLUEPIN, OUTPUT);
  pinMode(ptr->BlueLedPin, OUTPUT);   // Blue Led
  digitalWrite(ptr->BlueLedPin, 1);
  pinMode(ptr->pinBuzzer, OUTPUT);
  pinMode(ptr->pinPhoto, INPUT);

  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);         // UART speed
  SerialBLE.begin(9600);

  Buzzer();
}

void loop() {

  ListenBlt();

  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis_1 >= default_update_time) {
    previousMillis_1 = currentMillis;

    PingPong();

    BuiltinPinOnOff();

    PinStatus();      // update sensors status

    if (ptr->light_always) {
      RGBStrip(ptr->default_red_color, ptr->default_green_color, ptr->default_blue_color);
    } else if (!ptr->light_always) {
      PIR(ptr->pirStatus);      // else - update PIR sensor status
    }

    // if no motion detected in last 30s -> turn LED OFF
    if (currentMillis - previousMillis_3 >= pirTimer) { // timer = 30sec
      previousMillis_3 = currentMillis;
      if (!ptr->light_always) {
        if (ptr->pirStatus == 0) {
          RGBStrip(0, 0, 0);    // rgb off
          digitalWrite(ptr->relayPin, 1);  // turn LED OFF
        }
      }
    }
  }

  if (currentMillis - previousMillis_2 >= 20) {
    previousMillis_2 = currentMillis;

    SetColor();
  }

}
