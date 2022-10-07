#include "Arduino.h"
#include "Movement.h"
#include "Config.h"

float position[3] = {0, 0, 0};
float targetPosition[3] = {0, 0, 0};

bool compareFloats(float A, float B, float tolerance = 0.05f)
{
    return (fabs(A - B) < tolerance);
}

Movement::Movement()
{
    
}

void Movement::SetTargetPosition(float x, float y, float z)
{
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
}

void Movement::Move()
{
    if (compareFloats(position[0], targetPosition[0]))
    {
        digitalWrite(XRIGHTPIN, LOW);
        digitalWrite(XLEFTPIN, LOW);
    }
    else if (position[0] < targetPosition[0])
    {
        digitalWrite(XLEFTPIN, HIGH);
        digitalWrite(XRIGHTPIN, LOW);
        position[0] += 0.1f;

    }
    else if (position[0] > targetPosition[0])
    {
        digitalWrite(XRIGHTPIN, HIGH);
        digitalWrite(XLEFTPIN, LOW);
        position[0] -= 0.1f;
    }

    if (compareFloats(position[1], targetPosition[1]))
    {
        digitalWrite(YRIGHTPIN, LOW);
        digitalWrite(YLEFTPIN, LOW);
    }
    else if (position[1] < targetPosition[1])
    {
        digitalWrite(YLEFTPIN, HIGH);
        digitalWrite(YRIGHTPIN, LOW);
        position[1] += 0.1f;

    }
    else if (position[1] > targetPosition[1])
    {
        digitalWrite(YRIGHTPIN, HIGH);
        digitalWrite(YLEFTPIN, LOW);
        position[1] -= 0.1f;
    }

    if (compareFloats(position[2], targetPosition[2]))
    {
        digitalWrite(ZRIGHTPIN, LOW);
        digitalWrite(ZLEFTPIN, LOW);
    }
    else if (position[2] < targetPosition[2])
    {
        digitalWrite(ZLEFTPIN, HIGH);
        digitalWrite(ZRIGHTPIN, LOW);
        position[2] += 0.1f;

    }
    else if (position[2] > targetPosition[2])
    {
        digitalWrite(ZRIGHTPIN, HIGH);
        digitalWrite(ZLEFTPIN, LOW);
        position[2] -= 0.1f;
    }
}
