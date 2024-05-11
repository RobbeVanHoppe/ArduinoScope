#include <Arduino.h>

// Variable declaration
unsigned char inputPin = A9;    // Analog input pin
uint16_t readings[100];         // Array to store readings
unsigned char readingPtr;       // Pointer to the current reading
int timeBase;                   // Size of delay between readings
bool timeoutStatus;             // Timeout status for UART
String serialRead;              // String to store serial input

void setup()
{
    Serial.begin(115200);
    Serial.setTimeout(20);
    pinMode(inputPin, INPUT);
    timeBase = 100;
}

void loop()
{
    for (readingPtr = 0; readingPtr < 100; readingPtr++)
    {
        readings[readingPtr] = analogRead(inputPin);
        delayMicroseconds(timeBase);
    }

    timeoutStatus = true;

    while (timeoutStatus)
    {
        Serial.println("R?");
        serialRead = Serial.readString();
        if (serialRead == "K")
        {
            timeoutStatus = false;
        }

        for (readingPtr = 0; readingPtr < 100; readingPtr++)
        {
            Serial.write(highByte(readings[readingPtr] << 6));
        }
    }
}