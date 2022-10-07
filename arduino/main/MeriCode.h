#ifndef MeriCode_h
#define MeriCode_h

#include "Arduino.h"
#include "Movement.h"

class MeriCode
{
  public:
    MeriCode();
    void executeMeriCode(char* meriCodeCharacters);
    Movement movement;

  private:
    void receivedInvalidCode();
    void executeDcode(char* dCharacters);
    void executeMcode(char* dCharacters);
    void M0(char* characters);
    float GetNumberAfterCharacter(char* characterNumbers);
};

#endif