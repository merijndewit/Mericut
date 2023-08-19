#ifndef Stepperi_h
#define Stepperi_h

#include <Arduino.h>

class Stepperi
{
    public:
        Stepperi(int stepPin, int directionPin);
        void runSpeed();
        bool run();
        void setTargetPosition(int position)
        {
            this->targetStepPosition = position;
        };
        void setSpeed(float speed)
        {
            this->speed = speed;
        };
        int getStepPosition()
        {
            return this->stepPosition;
        };
        int getStepsToGo();
        float getPosition();
        void setRunSpeed(float speed);
    private:
        void step(); 
        void setDirection(bool reverse);

        int stepPin;
        int directionPin;

        float speed;
        int stepPosition;
        int targetStepPosition;

        unsigned long timeLastStepped;
        bool backwards;
};

#endif