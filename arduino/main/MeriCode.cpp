#include "Arduino.h"
#include "Movement.h"
#include "MeriCode.h"

MeriCode::MeriCode()
{

}

void MeriCode::receivedInvalidCode()
{
    Serial.println("<E0>");
}

void MeriCode::startListeningToFile()
{
    listeningToFile = true;
        Serial.println("<C1>");
}

void MeriCode::addMeriCode(char* meriCodeCharacters)
{
    if (!listeningToFile)
    {
        executeMeriCode(meriCodeCharacters);
        return;
    }
    meriCodeBuffer[itemsInBuffer++] = meriCodeCharacters;
    if (!executingMeriCode)
    {
        executeMeriCode(meriCodeBuffer[0]);
        executingMeriCode = true;
    }
}

void MeriCode::completedMericodeInBuffer()
{

    if (listeningToFile)
    {
        executingMeriCode = false;
        meriCodeBuffer + 1;
        itemsInBuffer--;
        Serial.println("<C1>"); //ask for next command
    }

    if (itemsInBuffer != 0 && !executingMeriCode)
    {
        executeMeriCode(meriCodeBuffer[0]);
        executingMeriCode = true;
    }

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
        case 'M':
        {
            char* substr = meriCodeCharacters + 1;
            executeMcode(substr++);
        }
            break;
        case 'S':
        {
            char* substr = meriCodeCharacters + 1;
            executeScode(substr++);
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

void MeriCode::executeMcode(char* mCharacters)
{
    char* substr = mCharacters + 1;
    switch (mCharacters[0])
    {
        case '0':
            M0(substr++);
            break;
        
        default:
            receivedInvalidCode();
            break;
    }
}

void MeriCode::executeScode(char* mCharacters)
{
    char* substr = mCharacters + 1;
    switch (mCharacters[0])
    {
        case '0':
            completedMericodeInBuffer();
            listeningToFile = false;
            executingMeriCode = false;
            itemsInBuffer = 0;
            break;

        case '1':
            startListeningToFile();
            break;
        
        default:
            receivedInvalidCode();
            break;
    }
}

float MeriCode::GetNumberAfterCharacter(char* characterNumbers)
{
    char number[32] = {};
    
    for (size_t i = 0; i < 32; i++)
    {
        if(characterNumbers[i] == ' ')
        {
            break;
        }
        number[i] = characterNumbers[i];
    }
    return atof(number);
    
}

void MeriCode::M0(char* characters)
{
    float x = NAN;
    float y = NAN;
    float z = NAN;
    char* substr = characters + 1;
    
    for (size_t i = 0; i < 32; i++)
    {
        if(characters[i] == '\x00') 
        {
            break;
        }
        if (characters[i] == 'X')
        {
            x = GetNumberAfterCharacter(substr + i);
            continue;
        }
        if (characters[i] == 'Y')
        {
            
            y = GetNumberAfterCharacter(substr + i);
            continue;
        }        
        if (characters[i] == 'Z')
        {
            z = GetNumberAfterCharacter(substr + i);
            continue;
        }
    } 
    Serial.print(x);
    Serial.print(y);
    Serial.print(z);

    this->movement.SetTargetPosition(x, y, z);
}
