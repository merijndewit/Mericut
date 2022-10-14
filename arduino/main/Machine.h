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
        void AddMeriCodeToBuffer(char* command);
        // Movement movement;  
    private:
        MeriCode meriCode;
        bool stoppedMoving = false;

};

#endif