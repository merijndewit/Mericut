#ifndef Machine_h
#define Machine_h

#include "Arduino.h"
#include "MeriCode.h"
#include "Movement.h"

class Machine
{
    public:
        Machine();
        void Update();
        void ExecuteMeriCode(char* command);
        void test();
        MeriCode meriCode;
        // Movement movement;  
    protected:

};

#endif