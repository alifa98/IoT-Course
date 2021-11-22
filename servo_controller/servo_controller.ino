/*********
  Rui Santos
  Complete project details at https://randomnerdtutorials.com/esp8266-nodemcu-access-point-ap-web-server/
  
  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files.
  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.
*********/

// Import required libraries
#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <Hash.h>

#include <ESPAsyncWebServer.h>
#include <ESPAsyncTCP.h>
#include <SPI.h>
#include <MFRC522.h>
#include <Servo.h> 
const char* ssid     = "Pashmak";
const char* password = "alialiali";

// Create AsyncWebServer object on port 80
AsyncWebServer server(80);



const int servoPin = D4; 
Servo Servo1; 

const char index_html[] PROGMEM = R"rawliteral(
<!DOCTYPE HTML><html>
  <head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>
<body>
<div id="target">
<div class="value" id="value">0</div>
<input type="range" min="0" max="180" step="1" value="0" >
</div>
    <style>
body {
  font-family: "Dosis", Helvetica, Arial, sans-serif;
  background: #ecf0f1;
  color: #34495e;
  padding-top: 40px;
  text-shadow: white 1px 1px 1px;
}
.value {
  border-bottom: 4px dashed #bdc3c7;
  text-align: center;
  font-weight: bold;
  font-size: 10em;
  width: 300px;
  height: 100px;
  line-height: 60px;
  margin: 40px auto;
  letter-spacing: -.07em;
  text-shadow: white 2px 2px 2px;
}
input[type="range"] {
  display: block;
  -webkit-appearance: none;
  background-color: #bdc3c7;
  width: 300px;
  height: 5px;
  border-radius: 5px;
  margin: 0 auto;
  outline: 0;
}
input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  background-color: #e74c3c;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  border: 2px solid white;
  cursor: pointer;
  transition: .3s ease-in-out;
}​
  input[type="range"]::-webkit-slider-thumb:hover {
    background-color: white;
    border: 2px solid #e74c3c;
  }
  input[type="range"]::-webkit-slider-thumb:active {
    transform: scale(1.6);
  }
    </style>
    <script>
    var elem = document.querySelector('input[type="range"]');
  var rangeValue = function(){
    var newValue = elem.value;
    var target = document.querySelector('.value');
    target.innerHTML = newValue;
    
  }
  elem.addEventListener("input", rangeValue);
    </script>
  </body>
  
<script>
//document.getElementById("target").onclick = 
last = 0;
setInterval(function ( ) {
 // var xhttp = new XMLHttpRequest();
 // xhttp.open("GET", "/"+document.getElementById("value").innerHTML, true);
//  xhttp.send(document.getElementById("value").innerHTML);
var val = document.getElementById("value").innerHTML;
if(last == val)
  return;
var http = new XMLHttpRequest();
//params =  'orem=ipsum&name=binny';
http.open('POST', "/data", true);
http.onreadystatechange = function() {//Call a function when the state changes.
    if(http.readyState == 4 && http.status == 200) {
        alert(http.responseText);
    }
}
//alert(params);
last = val;
var params = `orem=${val}&name=binny`;
http.send(params);
}, 200 ) ;
</script>
</html>)rawliteral";
void handleBody(AsyncWebServerRequest *request, uint8_t *data, size_t len, size_t index, size_t total){
  if(!index){
    Serial.printf("BodyStart: %u B\n", total);
  }
  for(size_t i=0; i<len; i++){
    Serial.write(data[i]);
  }
  if(index + len == total){
    Serial.printf("BodyEnd: %u B\n", total);
  }
}
void setup(){
  // Serial port for debugging purposes
  Serial.begin(115200);

  
  Serial.print("Setting AP (Access Point)…");
  // Remove the password parameter, if you want the AP (Access Point) to be open
  WiFi.softAP(ssid, password);

  IPAddress IP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(IP);

  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(200, "text/html", index_html);
  });
  
  server.on("/data", HTTP_POST, [](AsyncWebServerRequest *request){
if(request->hasParam("orem", true)){
  AsyncWebParameter* p = request->getParam("orem", true);
  Serial.println(p->value().c_str());
  Servo1.write(p->value().toInt());
}
  });
server.onRequestBody(handleBody);


  // Start server
  server.begin();

  Servo1.attach(servoPin); 
  Servo1.write(0); 
}


void loop(){ 
  delay(500);
}
