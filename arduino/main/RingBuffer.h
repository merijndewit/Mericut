#define BUFLEN 8

#ifndef RingBuffer_h
#define RingBuffer_h

#include "Arduino.h"

class RingBuffer
{
    public:
        void put(char* item)
        {
                buf[end] = new char[strlen(item)+1];
                strcpy(this->buf[end++], item);
                end %= BUFLEN;
        }

        char* get()
        {
                char* item = buf[start++];
                start %= BUFLEN;
                return item;
        }

    private:
        char* buf[BUFLEN];   /* array to be treated as circular buffer of BUFLEN integers */
        int end = 0;       /* write index */
        int start = 0;     /* read index */
};
#endif