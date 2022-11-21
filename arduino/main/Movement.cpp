#include "Arduino.h"
#include "Movement.h"

bool compareFloats(float A, float B, float tolerance = 0.05f)
{
    return (fabs(A - B) < tolerance);
}

Movement::Movement()
{
    xStepper.setAcceleration(STEPPERACCELERATION);
    yStepper.setAcceleration(STEPPERACCELERATION);
    yyStepper.setAcceleration(STEPPERACCELERATION);
    zStepper.setAcceleration(STEPPERACCELERATION);
    tStepper.setAcceleration(STEPPERACCELERATION);
    SetNormalSpeed();
}

void Movement::SetNormalSpeed()
{
    xStepper.setMaxSpeed(XYMAXSPEED);
    yStepper.setMaxSpeed(XYMAXSPEED);
    yyStepper.setMaxSpeed(XYMAXSPEED);
    zStepper.setMaxSpeed(ZMAXSPEED);
    tStepper.setMaxSpeed(TMAXSPEED);
}

void Movement::SetTravelSpeed()
{
    xStepper.setMaxSpeed(XYMAXTRAVELSPEED);
    yStepper.setMaxSpeed(XYMAXTRAVELSPEED);
    yyStepper.setMaxSpeed(XYMAXTRAVELSPEED);
    zStepper.setMaxSpeed(ZMAXTRAVELSPEED);
    tStepper.setMaxSpeed(TMAXTRAVELSPEED);
}

void Movement::SetTargetPosition(float x, float y, float z, float t)
{
    xMoving = false;
    yMoving = false;
    zMoving = false;
    tMoving = false;

    isMovingToTarget = true;

    if (!isnan(x))
    {
        targetPosition[0] = (long)(x * XSTEPPERMM * MICROSTEPPING);
        xMoving = true;
        xStepper.moveTo((long)(x * XSTEPPERMM * MICROSTEPPING));
    }
    if (!isnan(y))
    {
        targetPosition[1] = (long)(y * YSTEPPERMM * MICROSTEPPING);
        yMoving = true;
        yStepper.moveTo((long)(y * YSTEPPERMM * MICROSTEPPING));
        yyStepper.moveTo((long)(y * YSTEPPERMM * MICROSTEPPING));
    }    
    MoveXY();
    if (!isnan(z))
    {
        zStepper.moveTo(z * MICROSTEPPING);
        //targetPosition[2] = z;
        zMoving = true;
    }
    if (!isnan(t))
    {
        tStepper.moveTo((t * TSTEPPERDEG) * MICROSTEPPING);
        //targetPosition[3] = t;
        tMoving = true;
    }
}

void Movement::MoveXY()
{
    long distance[2] = {};
    distance[0] = abs(targetPosition[0] - xStepper.currentPosition());
    distance[1] = abs(targetPosition[1] - yStepper.currentPosition());

    if(distance[0] >= distance[1]){
        xStepper.setMaxSpeed(XYMAXSPEED);    
        xStepper.setAcceleration(XYMAXSPEED);
        if (distance[1] == 0)
        {
            return;
        }
        yStepper.setMaxSpeed((float)(ceil(XYMAXSPEED * distance[1]/distance[0])));    
        yStepper.setAcceleration((float)(ceil(XYMAXSPEED * distance[1]/distance[0])));    
        yyStepper.setMaxSpeed((float)(ceil(XYMAXSPEED * distance[1]/distance[0])));    
        yyStepper.setAcceleration((float)(ceil(XYMAXSPEED * distance[1]/distance[0])));   
    }
    else{
        yStepper.setMaxSpeed(XYMAXSPEED);    
        yStepper.setAcceleration(XYMAXSPEED);    
        yyStepper.setMaxSpeed(XYMAXSPEED);    
        yyStepper.setAcceleration(XYMAXSPEED); 
        if (distance[0] == 0)
        {
            return;
        }
        xStepper.setMaxSpeed((float)(ceil(XYMAXSPEED * distance[0]/distance[1])));    
        xStepper.setAcceleration((float)(ceil(XYMAXSPEED * distance[0]/distance[1])));    
    }
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
        yyStepper.run();
        yMoving = yStepper.run();
        moved++;
    }

    if(zMoving)
    {
        zMoving = zStepper.run();
        moved++;
    }
    if(tMoving)
    {
        tMoving = tStepper.run();
        moved++;
    }

    if (moved == 0)
    {
        isMovingToTarget = false;
    }
    else
    {
        isMovingToTarget = true;
    }
}
