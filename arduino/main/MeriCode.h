#ifndef MeriCode_h
#define MeriCode_h

#include "Arduino.h"
#include "Movement.h"

class MeriCode
{
  public:
    MeriCode();
    void addMeriCode(char* meriCodeCharacters);
    void executeMeriCode(char* meriCodeCharacters);
    void completedMericodeInBuffer();
    Movement movement;

  private:
    void startListeningToFile();
    void receivedInvalidCode();
    void executeDcode(char* dCharacters);
    void executeMcode(char* dCharacters);
    void executeScode(char* dCharacters);
    void M0(char* characters);
    float GetNumberAfterCharacter(char* characterNumbers);
    int maxItemsInBuffer = 5;
    char* meriCodeBuffer[5];
    int itemsInBuffer = 0;
    bool listeningToFile = false;
    bool executingMeriCode = false;
};

#endif