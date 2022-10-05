#ifndef MicroGcode_h
#define MicroGcode_h

#include "Arduino.h"

class MicroGcode
{
  public:
    MicroGcode();
    void executeMiniGcode(char* microGcodeCharacters);

  private:
    void receivedInvalidCode();
    void executeDcode(char* dCharacters);
};

#endif