#include "Machine.h"
#include "Movement.h"

Machine::Machine()
{

}

void Machine::Update()
{
    if (meriCode.movement.IsMovingToTarget())
    {
        stoppedMoving = false;
        meriCode.movement.Move();
        return;
    }
    if (stoppedMoving == false)
    {
        meriCode.completedMericodeInBuffer();
        stoppedMoving = true;
    }
}

void Machine::AddMeriCodeToBuffer(char* command)
{
    meriCode.addMeriCode(command);
}


