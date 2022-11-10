#ifndef MeriCode_h
#define MeriCode_h

#include "Arduino.h"
#include "Movement.h"
#include "RingBuffer.h"

class MeriCode
{
  public:
    MeriCode();
    void addMeriCode(char* meriCodeCharacters);
    void Run();
    Movement movement;

  private:
    bool executeMeriCode(char* meriCodeCharacters);
    void completedMericodeInBuffer();
    void executeNextCommand();
    void receivedInvalidCode();
    bool executeDcode(char* dCharacters);
    bool executeMcode(char* dCharacters);
    void M0(char* characters);
    float GetNumberAfterCharacter(char* characterNumbers);
    RingBuffer ringBuffer;
    bool moving = false;
    bool askedForMeriCode = false;
    int itemsInBuffer = 0;
};

#endif