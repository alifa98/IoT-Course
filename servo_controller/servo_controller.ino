#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <Servo.h>

//Wi-Fi networks user and pass
const char* ssid     = "Pashmak";
const char* password = "alialiali";

// Set web server port number to 80
ESP8266WebServer server(80);

// function prototypes for HTTP handlers
void handleRoot();
void handleServo();
void handleNotFound();

Servo camera_servo;  // create servo object to control a servo
const int SERVO_PIN = D2;

void setup() {
  Serial.begin(115200);
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
  server.on("/servo", HTTP_POST, handleServo);
  server.onNotFound(handleNotFound);           // When a client requests an unknown URI (i.e. something other than "/"), call function "handleNotFound"

  server.begin();

  camera_servo.attach(SERVO_PIN);  // attaches the servo on pin 9 to the servo object
}

void loop(void){
  server.handleClient();                     // Listen for HTTP requests from clients
}

void handleRoot() {
  server.send(200, "text/html", "<!DOCTYPE html> <html> <body> <input type=\"range\" min=\"0\" max=\"180\" value=\"50\" id=\"myRange\"> <br> <span id=\"labelShow\"></span> <script> let handlerFunc = function () { let value = document.getElementById(\"myRange\").value; document.getElementById(\"labelShow\").innerHTML = value; const xhttp = new XMLHttpRequest(); xhttp.open(\"POST\", \"/servo\"); xhttp.setRequestHeader(\"Content-type\", \"application/x-www-form-urlencoded\"); xhttp.send(\"value=\" + value); }; document.getElementById(\"myRange\").addEventListener(\"change\", handlerFunc); </script> </body> </html>");
}
void handleServo() { 
  String value = server.arg("value");
  if (value != NULL){
    server.send(200, "text/html", "OK");
    camera_servo.write(value.toInt());              // tell servo to go to the position.
  }else{
    server.send(200, "text/html", "NOK");
  }
  Serial.println(value.toInt());
}

void handleNotFound(){
  server.send(404, "text/plain", "404: Not found");
}
