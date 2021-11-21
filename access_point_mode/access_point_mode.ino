#include <ESP8266WiFi.h>

char ssid[] = "Network-1";          //  your network SSID (name) 

IPAddress IP = {10, 10, 1, 1};
IPAddress gateway = {10, 10, 1, 1};
IPAddress NMask = {255, 255, 255, 0};

WiFiServer server(80);

void setup ()
{
  Serial.begin(9600);

  WiFi.mode(WIFI_AP);  
  WiFi.softAP(ssid);
  delay(1000);
  
  Serial.print("AP IP address: ");
  Serial.println(WiFi.softAPIP()); 
  
  WiFi.softAPConfig(IP, IP, NMask);

  delay(1000);
  
  Serial.print("AP IP address: ");
  Serial.println(WiFi.softAPIP());  

  server.begin();
}

void loop ()
{ }
