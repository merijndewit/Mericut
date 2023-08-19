#include "Arduino.h"
#include "Movement.h"
#include "MeriCode.h"

MeriCode::MeriCode()
{
}

void MeriCode::Run()
{
    if (moving)
    {
        movement.Update();
        if (movement.IsMovingToTarget() == false)
        {
            moving = false;
            completedMericodeInBuffer();
        }
    }
}

void MeriCode::receivedInvalidCode()
{
    Serial.println("<E0>");
}

void MeriCode::addMeriCode(char* meriCodeCharacters)
{
    askedForMeriCode = false;
    ringBuffer.put(meriCodeCharacters);
    itemsInBuffer++;
    executeNextCommand();
    if (itemsInBuffer < 10)
    {
        askedForMeriCode = true;
        Serial.println("<C1>");
    }
}

void MeriCode::completedMericodeInBuffer()
{
    if (!askedForMeriCode)
    {
        askedForMeriCode = true;
        Serial.println("<C1>");
    }
    executeNextCommand();
}

void MeriCode::executeNextCommand()
{
    if (itemsInBuffer != 0 && moving == false)
    {
        char* nextCommand = ringBuffer.get();
        itemsInBuffer--;
        bool isCompleted = executeMeriCode(nextCommand);
        delete nextCommand;
        if (isCompleted)
        {
            completedMericodeInBuffer();
        }
    }
}

// returns true if mericode could be completed in one call
// returns false if mericode coudn't be completed in a single call like setting the next target position
// invalid mericode returns true
bool MeriCode::executeMeriCode(char* meriCodeCharacters)
{
    bool couldComplete = true;
    switch (meriCodeCharacters[0]) //get first character of mericode
    {
        case 'D':
        {
            char* substr = meriCodeCharacters + 1;
            couldComplete = executeDcode(substr++);
        }
            break;
        case 'M':
        {
            char* substr = meriCodeCharacters + 1;
            couldComplete = executeMcode(substr++);
        }
            break;
        case 'S':
        {
            char* substr = meriCodeCharacters + 1;
            couldComplete = executeScode(substr++);
        }
            break;
        default:
            receivedInvalidCode();
            break;
    }
    return couldComplete;
}

bool MeriCode::executeDcode(char* dCharacters)
{
    switch (dCharacters[0])
    {
        case '0':
            Serial.println("<C0>");
            return true;
        
        default:
            receivedInvalidCode();
            return true;
    }
}

bool MeriCode::executeMcode(char* mCharacters)
{
    char* substr = mCharacters + 1;
    switch (mCharacters[0])
    {
        case '0':
            movement.SetNormalSpeed();
            M0(substr++);
            return false;

        case '1':
            movement.SetTravelSpeed();
            M0(substr++);
            return false;
        
        default:
            receivedInvalidCode();
            return true;
    }
}
bool MeriCode::executeScode(char* sCharacters)
{
    char* substr = sCharacters + 1;
    switch (sCharacters[0])
    {
        case '0':
            S0(substr++);
            return true;
        
        default:
            receivedInvalidCode();
            return true;
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
    moving = true;
    float x = NAN;
    float y = NAN;
    float z = NAN;
    float t = NAN;
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
        if (characters[i] == 'T')
        {
            t = GetNumberAfterCharacter(substr + i);
            continue;
        }
    } 
    movement.SetTargetPosition(x, y, z, t);
}

void MeriCode::S0(char* characters)
{
    float xy = NAN;
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
            xy = GetNumberAfterCharacter(substr + i);
            movement.SetSpeedXY(xy);
            continue;
        }
        if (characters[i] == 'Z')
        {
            z = GetNumberAfterCharacter(substr + i);
            movement.SetSpeedZ(z);

            continue;
        }
    } 
}