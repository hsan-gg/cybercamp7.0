/* Teaching example: build a buffer from a few fields, then checksum it.
   Read make_tag(), then find the same three steps in Ghidra.
   Build: gcc -O0 -fno-inline teach.c -o teach     Expected: tag = 07B7395A */
#include <stdint.h>
#include <stdio.h>

static uint32_t crc32_bytes(const uint8_t *data, size_t length)
{
    uint32_t crc = 0xFFFFFFFFu;
    for (size_t i = 0; i < length; i++) {
        crc ^= data[i];
        for (int bit = 0; bit < 8; bit++)
            crc = (crc & 1u) ? (crc >> 1) ^ 0xEDB88320u : (crc >> 1);
    }
    return crc ^ 0xFFFFFFFFu;
}

static uint32_t make_tag(uint16_t count, uint8_t value)
{
    uint8_t buffer[5];
    buffer[0] = 'C';                      /* collect */
    buffer[1] = 'C';
    buffer[2] = (uint8_t)(count);         /* serialize: count, 2 bytes little-endian */
    buffer[3] = (uint8_t)(count >> 8);
    buffer[4] = value;
    return crc32_bytes(buffer, sizeof(buffer));   /* checksum the whole buffer */
}
 
int main(void)
{
    printf("tag = %08X\n", make_tag(1000, 42));
    return 0;
}
