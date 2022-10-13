#include "Arduino.h"
#include "Movement.h"

bool compareFloats(float A, float B, float tolerance = 0.05f)
{
    return (fabs(A - B) < tolerance);
}

Movement::Movement()
{
    xStepper.setMaxSpeed(1000);
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
    bool moved = false;
    if (compareFloats(position[0], targetPosition[0]))
    {

    }
    else if (position[0] < targetPosition[0])
    {
        xStepper.setSpeed(400);
        xStepper.runSpeed();
        position[0] += 0.1f;
        moved = true;
    }
    else if (position[0] > targetPosition[0])
    {
        xStepper.setSpeed(400);
        xStepper.runSpeed();
        position[0] -= 0.1f;
        moved = true;
    }

    if (compareFloats(position[1], targetPosition[1]))
    {

    }
    else if (position[1] < targetPosition[1])
    {
        position[1] += 0.1f;
        moved = true;
    }
    else if (position[1] > targetPosition[1])
    {
        position[1] -= 0.1f;
        moved = true;
    }

    if (compareFloats(position[2], targetPosition[2]))
    {

    }
    else if (position[2] < targetPosition[2])
    {
        position[2] += 0.1f;
        moved = true;
    }
    else if (position[2] > targetPosition[2])
    {
        position[2] -= 0.1f;
        moved = true;
    }

    if (!moved)
    {
        isMovingToTarget = false;
    }
}
