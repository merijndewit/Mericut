#ifndef MeriCode_h
#define MeriCode_h

#include "Arduino.h"

class MeriCode
{
  public:
    MeriCode();
    void executeMeriCode(char* meriCodeCharacters);

  private:
    void receivedInvalidCode();
    void executeDcode(char* dCharacters);
};

#endif