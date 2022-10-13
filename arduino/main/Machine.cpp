#include "Machine.h"
#include "Movement.h"

Machine::Machine()
{

}

void Machine::Update()
{
    if (meriCode.movement.IsMovingToTarget())
    {
        meriCode.movement.Move();
    }
}

void Machine::ExecuteMeriCode(char* command)
{
    meriCode.executeMeriCode(command);
}


