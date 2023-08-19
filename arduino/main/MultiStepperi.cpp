#include "MultiStepperi.h"

MultiStepperi::MultiStepperi()
{
    this->stepperCount = 0;
    this->maxSpeed = 100; 
}

void MultiStepperi::addStepper(Stepperi& stepper)
{
    if(this->stepperCount >= MAXSTEPPERS)
    {
        return;
    }
    this->steppers[this->stepperCount++] = &stepper;
}

void MultiStepperi::setTargetPosition(int stepperPosition, int stepperIndex)
{
    if(stepperIndex >= MAXSTEPPERS)
    {
        return;
    }
    this->steppers[stepperIndex]->setTargetPosition(stepperPosition);
    calculateSpeed();
}

void MultiStepperi::calculateSpeed()
{
    int longestDistanceIndex = -1;
    float longestDistance = 0;
    for (int i = 0; i < this->stepperCount; i++)
    {
        if (longestDistance < this->steppers[i]->getStepsToGo())
        {
            longestDistance = this->steppers[i]->getStepsToGo();
            longestDistanceIndex = i;
        }
    }

    for (int i = 0; i < this->stepperCount; i++)
    {
        this->steppers[i]->setSpeed(this->maxSpeed * (this->steppers[i]->getStepsToGo() / longestDistance));
        this->steppersMaxSpeed[i] = this->maxSpeed * (this->steppers[i]->getStepsToGo() / longestDistance);
    }    
}

bool MultiStepperi::run() //return true when still running
{
    bool running = false;
    for (int i = 0; i < this->stepperCount; i++)
    {
        if(this->steppers[i]->getStepsToGo() == 0)
        {
            continue;
        }
        if(this->steppers[i]->run())
        {
            running = true;
        }
    }   

    return running;
}

void MultiStepperi::setMaxSpeed(float maxSpeed)
{
    this->maxSpeed = maxSpeed;
}