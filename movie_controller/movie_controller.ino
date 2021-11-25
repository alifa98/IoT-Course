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
void handleNameBtn();
void handleVolumeUpBtn();
void handleVolumeDownBtn();
void handlePlayBtn();
void handlePauseBtn();
void handleNotFound();

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
  server.on("/volumeUp", HTTP_GET, handleVolumeUpBtn);
  server.on("/volumeDown", HTTP_GET, handleVolumeDownBtn);
  server.on("/play", HTTP_GET, handlePlayBtn);
  server.on("/pause", HTTP_GET, handlePauseBtn);
  server.on("/printName", HTTP_GET, handleNameBtn);  
  server.onNotFound(handleNotFound);           // When a client requests an unknown URI (i.e. something other than "/"), call function "handleNotFound"

  server.begin();

}

void loop(void){
  server.handleClient();                     // Listen for HTTP requests from clients
}

void handleRoot() {
  server.send(200, "text/html", "<!DOCTYPE html> <html> <head> <link rel=\"stylesheet\" href=\"https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.css\" /> <script src=\"https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.js\"></script> </head> <body> <div style=\"text-align: center;\"> <button onclick=\"sendRequest(\'printName\')\" class=\"ui green button\"> <i class=\"user icon\"></i> Name </button> <br> <br> <div class=\"ui icon buttons\"> <button onclick=\"sendRequest(\'volumeUp\')\" class=\"ui button\"><i class=\"volume up icon\"></i></button> <button onclick=\"sendRequest(\'volumeDown\')\" class=\"ui button\"><i class=\"volume down icon\"></i></button> <button onclick=\"sendRequest(\'play\')\" class=\"ui button\"><i class=\"play icon\"></i></button> <button onclick=\"sendRequest(\'pause\')\" class=\"ui button\"><i class=\"pause icon\"></i></button> </div> </div> <script> function sendRequest(request) { const xhttp = new XMLHttpRequest(); xhttp.open(\"GET\", `/${request}`); xhttp.send(); }; </script> </body> </html>");
}

void handleRequest(String requestString) { 
  if (requestString != NULL){
    Serial.println(requestString);
  }else{
    server.send(403, "text/html", "Bad Request");
  }
}

void handleNameBtn() { handleRequest("printName"); }
void handleVolumeUpBtn() { handleRequest("volumeUp"); }
void handleVolumeDownBtn() { handleRequest("volumeDown"); }
void handlePlayBtn() { handleRequest("play"); }
void handlePauseBtn() { handleRequest("pause"); }

void handleNotFound(){
  server.send(404, "text/plain", "404: Not found");
}
