#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>

//Wi-Fi networks user and pass
const char* ssid     = "Pashmak";
const char* password = "alialiali";

// Set web server port number to 80
ESP8266WebServer server(80);

// function prototypes for HTTP handlers
void handleRoot();
void handleSensorValue();
void handleNotFound();


const int trigPin = D4;
const int echoPin = D5;
const int buzzerPin = D7;
const int ledPin = D2;

long duration;
long distance;

void setup() {
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  pinMode(ledPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);
  
  Serial.begin(9600); // Starts the serial communication
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  server.on("/", HTTP_GET, handleRoot);
  server.on("/sensor", HTTP_GET, handleSensorValue);
  server.onNotFound(handleNotFound);

  server.begin();
}

void loop() {
  
  // Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  
  // Calculating the distance
  distance = duration*0.034/2;

  Serial.print("Distance: ");
  Serial.println(distance);
  
  if(distance < 8){
    tone(buzzerPin, 2000, 1000);
    digitalWrite(ledPin, HIGH);
  }else{
    noTone(buzzerPin);
    digitalWrite(ledPin, LOW);
  }

  server.handleClient();
}

void handleRoot() {
  server.send(200, "text/html", "<!DOCTYPE html> <html> <body> 0 <input type=\"range\" style=\"width: 85%;\" min=\"0\" max=\"3000\" id=\"myRange\"> 3000 <br> Distance: <span id=\"labelShow\"></span> <script> setInterval(function () { const xhttp = new XMLHttpRequest(); xhttp.onload = function () { document.getElementById(\"myRange\").value = this.responseText; document.getElementById(\"labelShow\").innerHTML = this.responseText; }; xhttp.open(\"GET\", \"/sensor\"); xhttp.send(); }, 500); </script> </body> </html>");
}

void handleSensorValue() { 
  server.send(200, "text/html", String(distance));
}

void handleNotFound(){
  server.send(404, "text/plain", "404: Not found");
}
