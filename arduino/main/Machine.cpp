#include "Machine.h"
#include "Movement.h"

Machine::Machine()
{

}

void Machine::Update()
{
    meriCode.movement.Move();
    delay(10);
}

void Machine::ExecuteMeriCode(char* command)
{
    meriCode.executeMeriCode(command);
}


