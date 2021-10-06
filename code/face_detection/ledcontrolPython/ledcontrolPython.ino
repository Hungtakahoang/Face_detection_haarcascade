#include <cvzone.h>
#include <Servo.h>

SerialData data(1, 1);
int led = 13;
int ValRec[1];

void setup() {
    pinMode(led, OUTPUT);
    data.begin();
    Serial.begin(9600);    
}

void loop() {
    data.Get(ValRec);
    Serial.print("we have received 1 value already!!!");
    digitalWrite(led, ValRec[0]);
}
