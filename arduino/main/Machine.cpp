#include "Machine.h"
#include "Movement.h"

Machine::Machine()
{

}

void Machine::Update()
{
    meriCode.Run();
}

void Machine::AddMeriCodeToBuffer(char* command)
{
    meriCode.addMeriCode(command);
}


