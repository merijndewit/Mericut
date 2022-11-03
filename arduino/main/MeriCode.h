#ifndef MeriCode_h
#define MeriCode_h

#include "Arduino.h"
#include "Movement.h"

class MeriCode
{
  public:
    MeriCode();
    void addMeriCode(char* meriCodeCharacters);
    void Run();
    Movement movement;

  private:
    void executeMeriCode(char* meriCodeCharacters);
    void completedMericodeInBuffer();
    void receivedInvalidCode();
    void executeDcode(char* dCharacters);
    void executeMcode(char* dCharacters);
    void M0(char* characters);
    float GetNumberAfterCharacter(char* characterNumbers);
    int maxItemsInBuffer = 5;
    char* meriCodeBuffer[5];
    int itemsInBuffer = 0;
    bool moving = false;
};

#endif