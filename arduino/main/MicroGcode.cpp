#include "Arduino.h"
#include "MicroGcode.h"

MicroGcode::MicroGcode()
{

}

void MicroGcode::executeMiniGcode(char* microGcodeCharacters)
{
  
  switch (microGcodeCharacters[0]) //get first character of micro g-code
  {
    case 'D':
        Serial.println("Received D instruction");
        break;
    
    default:
        break;
  }
}
