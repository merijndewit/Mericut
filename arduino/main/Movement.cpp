#include "Arduino.h"
#include "Movement.h"

bool compareFloats(float A, float B, float tolerance = 0.05f)
{
    return (fabs(A - B) < tolerance);
}

Movement::Movement()
{
    steppers.addStepper(xStepper);
    steppers.addStepper(yStepper);
    steppers.addStepper(yyStepper);
    SetDefaultSpeed();
}

void Movement::SetDefaultSpeed()
{
    xStepper.setMaxSpeed(2000);
    yStepper.setMaxSpeed(2000);
    yyStepper.setMaxSpeed(2000);
    zStepper.setMaxSpeed(MAXSTEPPERSPEED);
    xStepper.setAcceleration(STEPPERACCELERATION);
    yStepper.setAcceleration(STEPPERACCELERATION);
    yyStepper.setAcceleration(STEPPERACCELERATION);
    zStepper.setAcceleration(STEPPERACCELERATION);
}


void Movement::SetTargetPosition(float x, float y, float z)
{
    xMoving = false;
    yMoving = false;
    zMoving = false;

    long xyPositions[3] = {long(targetPosition[0]), long(targetPosition[1]), long(targetPosition[1])};


    //SyncMovementXY(x, y);

    if (isMovingToTarget)
    {
        return;
    }
    if (!isnan(x))
    {
        targetPosition[0] = (x * XSTEPPERMM) * MICROSTEPPING;
        xyPositions[0] = long((x * XSTEPPERMM) * MICROSTEPPING);
        //xStepper.moveTo((x * XSTEPPERMM) * MICROSTEPPING);
        xMoving = true;
    }
    if (!isnan(y))
    {
        //yStepper.moveTo((y * YSTEPPERMM) * MICROSTEPPING);
        //yyStepper.moveTo((y * YSTEPPERMM) * MICROSTEPPING);
        xyPositions[1] = long((y * YSTEPPERMM) * MICROSTEPPING);
        xyPositions[2] = long((y * YSTEPPERMM) * MICROSTEPPING);

        targetPosition[1] = (y * YSTEPPERMM) * MICROSTEPPING;
        yMoving = true;
    }    
    if (!isnan(z))
    {
        zStepper.moveTo(z * MICROSTEPPING);
        targetPosition[2] = z;
        zMoving = true;
    }
    steppers.moveTo(xyPositions);
    isMovingToTarget = true;
}

void Movement::Move()
{
    int moved = 0;

    if(xMoving)
    {
        xMoving = steppers.run();
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
