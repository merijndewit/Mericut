#include "Arduino.h"
#include "Movement.h"

bool compareFloats(float A, float B, float tolerance = 0.05f)
{
    return (fabs(A - B) < tolerance);
}

Movement::Movement()
{
    xStepper.setMaxSpeed(1000);
    xStepper.setAcceleration(200);
}

void Movement::SetTargetPosition(float x, float y, float z)
{
    if (isMovingToTarget)
    {
        return;
    }
    if (x != NAN)
    {
        targetPosition[0] = x;
        xStepper.moveTo(x * MICROSTEPPING);
    }
    if (y != NAN)
    {
        targetPosition[1] = y;
    }    
    if (z != NAN)
    {
        targetPosition[2] = z;
    }
    isMovingToTarget = true;
}

void Movement::Move()
{
    if(!xStepper.run())
    {
        isMovingToTarget = false;
    }
}
