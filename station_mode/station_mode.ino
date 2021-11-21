#include <ESP8266WiFi.h>

const String wifiApSSID = "Pashmak";
const String wifiApPassword = "alialiali";

void setup() {
  Serial.begin(9600);
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
}

void loop() {
  
  if(WiFi.status() == WL_CONNECTED){
    Serial.print("The device is connected to Wi-Fi with IP address of ");
    Serial.println(WiFi.localIP());
    delay(5000);
    return;
  }

  //Scan wifi networks and print them
  int numberOfNetworks = WiFi.scanNetworks();
  if (numberOfNetworks == 0) {
      Serial.println("There is not any WIFI networks");
  } else {
    for (int index = 0; index < numberOfNetworks; ++index) {
      Serial.println(WiFi.SSID(index));
      delay(100);
    }
  }

  //Connect to our WiFi
  WiFi.begin(wifiApSSID, wifiApPassword);
  Serial.print("Connecting to WiFi ...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
  
  Serial.print("Connected to: ");
  Serial.println(wifiApSSID);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  
  delay(10000);
}
