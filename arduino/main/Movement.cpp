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
    xStepper.setAcceleration(STEPPERACCELERATION);
    yStepper.setAcceleration(STEPPERACCELERATION);
    yyStepper.setAcceleration(STEPPERACCELERATION);
    zStepper.setAcceleration(STEPPERACCELERATION);
    tStepper.setAcceleration(STEPPERACCELERATION);
    SetNormalSpeed();
}

void Movement::SetNormalSpeed()
{
    topSpeed = XYMAXSPEED;
    xStepper.setMaxSpeed(XYMAXSPEED);
    yStepper.setMaxSpeed(XYMAXSPEED);
    yyStepper.setMaxSpeed(XYMAXSPEED);
    zStepper.setMaxSpeed(ZMAXSPEED);
    tStepper.setMaxSpeed(TMAXSPEED);
}

void Movement::SetTravelSpeed()
{
    topSpeed = XYMAXSPEED;
    xStepper.setMaxSpeed(XYMAXTRAVELSPEED);
    yStepper.setMaxSpeed(XYMAXTRAVELSPEED);
    yyStepper.setMaxSpeed(XYMAXTRAVELSPEED);
    zStepper.setMaxSpeed(ZMAXTRAVELSPEED);
    tStepper.setMaxSpeed(TMAXTRAVELSPEED);
}

void Movement::SetTargetPosition(float x, float y, float z, float t)
{
    xyMoving = false;
    zMoving = false;
    tMoving = false;
    moveX = false;
    moveY = false;

    long xyPositions[3] = {long(targetPosition[0]), long(targetPosition[1]), long(targetPosition[1])};

    isMovingToTarget = true;
    //SyncMovementXY(x, y);
    if (!isnan(x))
    {
        targetPosition[0] = (x * XSTEPPERMM) * MICROSTEPPING;
        xyPositions[0] = long((x * XSTEPPERMM) * MICROSTEPPING);
        //xStepper.moveTo((x * XSTEPPERMM) * MICROSTEPPING);
        xyMoving = true;
        moveX = true;
    }
    if (!isnan(y))
    {
        //yStepper.moveTo((y * YSTEPPERMM) * MICROSTEPPING);
        //yyStepper.moveTo((y * YSTEPPERMM) * MICROSTEPPING);
        xyPositions[1] = long((y * YSTEPPERMM) * MICROSTEPPING);
        xyPositions[2] = long((y * YSTEPPERMM) * MICROSTEPPING);

        targetPosition[1] = (y * YSTEPPERMM) * MICROSTEPPING;
        xyMoving = true;
        moveY = true;
    }    
    if (!isnan(z))
    {
        zStepper.moveTo(z * MICROSTEPPING);
        targetPosition[2] = z;
        zMoving = true;
    }
    if (!isnan(t))
    {
        tStepper.moveTo((t * TSTEPPERDEG) * MICROSTEPPING);
        targetPosition[3] = t;
        tMoving = true;
    }
    if (xyMoving)
    {
        steppers.moveTo(xyPositions);
    }

    angle = atan2(targetPosition[1] - position[1],targetPosition[0] - position[0]);
    cosAngle = cos(angle);
    sinAngle = sin(angle);
    currentTime = millis();
}

void Movement::MoveXY()
{
    oldTime = currentTime;
    currentTime = millis();
    float deltaTime = (currentTime - oldTime) / 1000;
    float decelDistance = pow(velocity, 2) / (2 * acceleration);
    float deltaX = targetPosition[0] - position[0];
    float deltaY = targetPosition[1] - position[1];
    float distance = sqrt(pow(deltaX, 2) + pow(deltaY, 2));
    if (distance > decelDistance)
    {
        velocity = min(velocity + acceleration * deltaTime, topSpeed);
    }
    else
    { 
        velocity = max(velocity - acceleration * deltaTime, 0.0f);
    }
    xStepper.setSpeed(velocity * cosAngle);
    yStepper.setSpeed(velocity * sinAngle);
    yyStepper.setSpeed(velocity * sinAngle);
    xStepper.runSpeed();
    yStepper.runSpeed();
    yyStepper.runSpeed();
    position[0] = float(xStepper.currentPosition());
    position[1] = float(yStepper.currentPosition());

    if (moveX && lastReachedPosition[0] < targetPosition[0])
    {
      if (position[0] >= targetPosition[0])
        {
          moveX = false;
        }
    }
    else
    {
        if (position[0] <= targetPosition[0])
        {
          moveX = false;
        }
    }
  
    if (moveY && lastReachedPosition[1] < targetPosition[1])
    {
      if (position[1] >= targetPosition[1])
        {
          moveY = false;
        }
    }
    else
    {
        if (position[1] <= targetPosition[1])
        {
            moveY = false;
        }
    }

    if (!moveX && !moveY)
    {
        lastReachedPosition[0] = position[0];
        lastReachedPosition[1] = position[1];
    }
}

void Movement::Move()
{
    int moved = 0;

    if(moveX || moveY)
    {
        MoveXY();
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
