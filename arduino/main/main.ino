#include "Arduino.h"
#include "Machine.h"
#include "Config.h"

const byte numChars = 32;
char receivedChars[numChars];

boolean newData = false;

Machine machine;

void setup() 
{
    Serial.begin(921600);
}

void loop() 
{
    checkSerial();
    checkData();
    machine.Update();
}

void checkSerial() 
{
    static boolean receiving = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char data;
    while (Serial.available() > 0 && newData == false) {
        data = Serial.read();
        if (receiving == true) {
            if (data != endMarker) {
                receivedChars[ndx] = data;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0';
                receiving = false;
                ndx = 0;
                newData = true;
                addData(receivedChars);
            }
        }

        else if (data == startMarker) {
            receiving = true;
        }
    }
}

void addData(char* data)
{
    machine.AddMeriCodeToBuffer(data);
}

void checkData() 
{
    if (newData == true) {
        
        newData = false;
    }
}
