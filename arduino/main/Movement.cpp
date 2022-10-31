#include "Arduino.h"
#include "Movement.h"

bool compareFloats(float A, float B, float tolerance = 0.05f)
{
    return (fabs(A - B) < tolerance);
}

Movement::Movement()
{
    xStepper.setMaxSpeed(8000);
    yStepper.setMaxSpeed(8000);
    yyStepper.setMaxSpeed(8000);
    xStepper.setAcceleration(12000);
    yStepper.setAcceleration(12000);
    yyStepper.setAcceleration(12000);
    zStepper.setMaxSpeed(8000);
    zStepper.setAcceleration(12000);
    steppers.addStepper(xStepper);
    steppers.addStepper(yStepper);
    steppers.addStepper(yyStepper);
    steppers.addStepper(zStepper);
}

void Movement::SetTargetPosition(float x, float y, float z)
{
    xMoving = false;
    yMoving = false;
    zMoving = false;
    if (isMovingToTarget)
    {
        return;
    }
    if (!isnan(x))
    {
        targetPosition[0] = x;
        xStepper.moveTo(x * MICROSTEPPING);
        xMoving = true;
    }
    if (!isnan(y))
    {
        yStepper.moveTo(y * MICROSTEPPING);
        yyStepper.moveTo(y * MICROSTEPPING);
        targetPosition[1] = y;
        yMoving = true;
    }    
    if (!isnan(z))
    {
        zStepper.moveTo(z * MICROSTEPPING);
        targetPosition[2] = z;
        zMoving = true;
    }
    Serial.println(zMoving);

    isMovingToTarget = true;
}

void Movement::Move()
{
    int moved = 0;
    if(xMoving)
    {
        xMoving = xStepper.run();
        moved++;
    }

    if(yMoving)
    {
        yMoving = yStepper.run();
        yyStepper.run();
        moved++;
    }

    if(zMoving)
    {
        zMoving = zStepper.run();
        moved++;
    }

    if (moved == 0)
    {
        isMovingToTarget = false;
    }
}
