#include "Arduino.h"
#include "MicroGcode.h"

MicroGcode::MicroGcode()
{

}

void MicroGcode::receivedInvalidCode()
{
    Serial.println("<E0>");
}

void MicroGcode::executeMiniGcode(char* microGcodeCharacters)
{
    switch (microGcodeCharacters[0]) //get first character of micro g-code
    {
        case 'D':
        {
            char* substr = microGcodeCharacters + 1;
            executeDcode(substr++);
        }
            break;
        default:
            receivedInvalidCode();
            break;
    }
}

void MicroGcode::executeDcode(char* dCharacters)
{
    switch (dCharacters[0]) //get first character of micro g-code
    {
        case '0':
            Serial.println("<C0>");
            break;
        
        default:
            receivedInvalidCode();
            break;
    }
}
