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
        movement.Move();
        if (!movement.IsMovingToTarget())
        {
            completedMericodeInBuffer();
            moving = false;
        }
    }
}

void MeriCode::receivedInvalidCode()
{
    Serial.println("<E0>");
}

void MeriCode::addMeriCode(char* meriCodeCharacters)
{
    meriCodeBuffer[itemsInBuffer++] = meriCodeCharacters;
    executeMeriCode(meriCodeBuffer[0]);
    if (!moving)
    {
        completedMericodeInBuffer();
    }
}

void MeriCode::completedMericodeInBuffer()
{
    meriCodeBuffer + 1;
    itemsInBuffer--;
    Serial.println("<C1>"); //ask for next command
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
    this->movement.SetTargetPosition(x, y, z);
}