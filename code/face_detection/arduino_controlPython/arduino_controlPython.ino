#include <cvzone.h>

SerialData data(1, 1);//(number of data to receive, number of digit in 1 data to receive)
// if we want to receive value 1 to 9 => 1 digit
// if we want to receive value 1 to 99 => 2 digit
// if we want to receive value 1 to 999 => 3 digit
// here we just want to receive 2 values are 0 and 1, so we need 1 digit 
int led = 13;
// then we need to create the array to memory data receive, we must do this because it need for activation this library
int ValRec[1]; // length of array is number of data to receive

void setup() {
    pinMode(led, OUTPUT);
    data.begin();
    Serial.begin(9600);    
}

void loop() {
    // get the value receive and put it in array
    data.Get(ValRec);
    Serial.print("we have received values already!!!");
    digitalWrite(led, ValRec[0]);
}
