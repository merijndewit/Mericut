#include "Stepperi.h"

Stepperi::Stepperi(int stepPin, int directionPin)
{
    this->stepPin = stepPin;
    this->directionPin = directionPin;
    this->backwards = true;
    this->timeLastStepped = micros();
    this->targetStepPosition = 0;
    this->stepPosition = 0;

    pinMode(stepPin, OUTPUT);
    pinMode(directionPin, OUTPUT);
}

void Stepperi::runSpeed()
{
    if (1000000 / this->speed <= micros() - this->timeLastStepped)
    { 
        step();
        this->timeLastStepped = micros();
    }
}

bool Stepperi::run()
{
    if (this->targetStepPosition > this->stepPosition)
    {
        //stepping "forwards"
        this->setRunSpeed(speed);
        runSpeed();
        if(this->stepPosition >= this->targetStepPosition)
        {
            return false;
        }
    }
    else
    {
        //stepping "backwards"
        this->setRunSpeed(-speed);
        runSpeed();
        if(this->stepPosition <= this->targetStepPosition)
        {
            return false;
        }
    }
    
    return true;
}

void Stepperi::step()
{
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(1);
    digitalWrite(stepPin, LOW);
    if(this->backwards)
    {
        stepPosition--;
    }
    else
    {
        stepPosition++;
    }
}

void Stepperi::setRunSpeed(float speed)
{
    if (speed < 0)
    {
        setDirection(true);
        this->speed = abs(speed);
        return;
    }
    setDirection(false);
    this->speed = speed;
}

void Stepperi::setDirection(bool backwards)
{
    if (backwards && !this->backwards)
    {
        digitalWrite(directionPin, LOW);
        this->backwards = true;
        return;
    }
    if (!backwards && this->backwards)
    {
        digitalWrite(directionPin, HIGH);
        this->backwards = false;
        return;
    }
}

int Stepperi::getStepsToGo()
{
    return abs(this->stepPosition - this->targetStepPosition);
}