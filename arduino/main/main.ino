#include "Arduino.h"
#include "microGcode.h"

const byte numChars = 32;
char receivedChars[numChars];

boolean newData = false;

MicroGcode microGcode;

void setup() {
    Serial.begin(115200);
}

void loop() {
    checkSerial();
    checkData();
}

void checkSerial() {
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
            }
        }

        else if (data == startMarker) {
            receiving = true;
        }
    }
}

void checkData() {
    if (newData == true) {
        executeCommand(receivedChars);
        newData = false;
    }
}

void executeCommand(char* receivedChars) 
{
    microGcode.executeMiniGcode(receivedChars);
}
