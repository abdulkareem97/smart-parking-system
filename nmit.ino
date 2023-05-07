#include <Servo.h>
#include <ESP8266WiFi.h>
#include <TaskScheduler.h>

const char* ssid = "POCO X2";
const char* password = "0987654321";
WiFiServer server(80);
// Create a servo object
Servo myservo;
int ledPin = 12;    //d6
int inputPin = 13;  //d7
int inputPin2 = 2;  //d4
// int g1 = 15;
// int r1 = 14;
// int g2 = 4;
// int r2 = 5;
int ledPins[] = { 15, 14, 4, 5 };  // d8 d5 D2 D1
int numLeds = 4;
int prevLeds[] = { 0, 0, 0, 0 };
int offTime = 0;
int offLed = -1;
unsigned long bookingStart;

// int POWER = 5;



Scheduler scheduler;

// Declare the function to be scheduled
void yourFunction();

// Declare the task
Task taskName(5000, TASK_ONCE, &yourFunction, &scheduler, true);

void setup() {
  // Attach the servo to pin 9
  Serial.begin(9600);
  myservo.attach(16);
  pinMode(inputPin, INPUT);
  pinMode(inputPin2, INPUT);
  pinMode(ledPin, OUTPUT);


  // pinMode(ledPin, OUTPUT);
  for (int i = 0; i < numLeds; i++) {
    pinMode(ledPins[i], OUTPUT);
  }
  // myservo.attach(2);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  digitalWrite(ledPin, HIGH);

  // start the server
  server.begin();
  myservo.write(90);
}

void loop() {
  // Rotate the servo to 180 degrees
  WiFiClient client = server.available();

  if (!client) {
    return;
  }

  // read the message from the client
  while (client.connected()) {

      // Serial.println("+");
        if (offLed!=-1 && (offTime>0) && (millis() - bookingStart >= offTime)) {
     // Update the previous timestamp
            digitalWrite(ledPins[offLed], 1);
        digitalWrite(ledPins[offLed-1], 0);

    // Perform an action here
    // Serial.println("Hello, world!");
  }
      // scheduler.execute();
    if (Serial.available() > 0) {  // Check if there is any incoming data
      char input = Serial.read();  // Read the incoming data
      Serial.println(input);

      if (input == '1') {  // Check if the input is '1'
        // Do something
        // // Serial.println("You entered 1");  // Print a message to the Serial Monitor
        //     scheduler.addTask(taskName);
        //   taskName.enable();
        digitalWrite(ledPins[0], 1);
        digitalWrite(ledPins[1], 0);
         offLed = 1;
         offTime = -1;
      } else if (input == '2') {  // Check if the input is '1'
                                  // Do something
                                  // Serial.println("You entered 1");  // Print a message to the Serial Monitor
        digitalWrite(ledPins[2], 1);
        digitalWrite(ledPins[3], 0);
         offLed = 3;
         offTime = -1;
      } else if (input == '3') {  // Check if the input is '1'
                                  // Do something
                                  // Serial.println("You entered 1");  // Print a message to the Serial Monitor
        digitalWrite(ledPins[0], 0);
        digitalWrite(ledPins[1], 1);
         offLed = -1;
      } else if (input == '4') {  // Check if the input is '1'
                                  // Do something
                                  // Serial.println("You entered 1");  // Print a message to the Serial Monitor
        digitalWrite(ledPins[2], 0);
        digitalWrite(ledPins[3], 1);
         offLed = -1;
      } else if(input > '4') {
        offTime = (input-48)*1000;
        Serial.println(offTime);
        bookingStart = millis();

       
      }
    }



    // Serial.println("here");
    int val = digitalRead(inputPin);    // read input value
    int val2 = digitalRead(inputPin2);  // read input value
    if (ledPins[0] == 1 && ledPins[2] == 1) {
      Serial.println("Parking slot is full");
    } else if ((!val || !val2)) {  // check if the input is HIGH
                                   // Serial.println("true");           // turn LED OFF
      myservo.write(180);
      delay(2500);
      myservo.write(90);

      digitalWrite(ledPin, HIGH);
    } else {
      // Serial.println("False");  // turn LED ON
      digitalWrite(ledPin, LOW);
    }
    if (client.available()) {
      String message = client.readStringUntil('\r');
      message = message.substring(message.length() - 1);
      // int val = parseInt(message)
      Serial.println(message);
      if (message.equals("1")) {
        // digitalWrite(POWER, LOW);
        for (int i = 0; i < numLeds; i++) {
          if (prevLeds[i] == 1) {
            digitalWrite(ledPins[i], HIGH);
          }
        }

      } else if (message.equals("0")) {
        for (int i = 0; i < numLeds; i++) {
          prevLeds[i] = digitalRead(ledPins[i]);
          digitalWrite(ledPins[i], 0);
        }
        // digitalWrite(POWER, HIGH);
      }
    }
  }
  // close the connection
  client.stop();
}

void yourFunction() {
  // Code for your function
  Serial.println("Running yourFunction()!");
}
