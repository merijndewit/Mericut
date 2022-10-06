#include "Arduino.h"
#include "MeriCode.h"

MeriCode::MeriCode()
{

}

void MeriCode::receivedInvalidCode()
{
    Serial.println("<E0>");
}

void MeriCode::executeMeriCode(char* meriCodeCharacters)
{
    switch (meriCodeCharacters[0]) //get first character of mericode
    {
        case 'D':
        {
            char* substr = meriCodeCharacters + 1;
            executeDcode(substr++);
        }
            break;
        default:
            receivedInvalidCode();
            break;
    }
}

void MeriCode::executeDcode(char* dCharacters)
{
    switch (dCharacters[0])
    {
        case '0':
            Serial.println("<C0>");
            break;
        
        default:
            receivedInvalidCode();
            break;
    }
}
