#ifndef Movement_h
#define Movement_h

#include "Arduino.h"

class Movement
{
    public:
        Movement();
        void Move();
        void SetTargetPosition(float x, float y, float z);
};

#endif