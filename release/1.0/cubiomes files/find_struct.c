#include "finders.h"
#include <stdio.h>
#include <stdlib.h>

int find(int structureInput, char *structureName, int version, int start) {
    int structType = structureInput;
    int mc = version;

    Generator g;
    setupGenerator(&g, mc, 0);

    uint64_t lower48;
    for (lower48 = 0; ; lower48++)
    {
        // The structure position depends only on the region coordinates and
        // the lower 48-bits of the world seed.
        Pos p;
        if (!getStructurePos(structType, mc, lower48, 0, 0, &p))
            continue;

        // Look for a seed with the structure at the origin chunk.
        if (p.x >= 16 || p.z >= 16)
            continue;

        // Look for a full 64-bit seed with viable biomes.
        uint64_t upper16;
        for (upper16 = 0; upper16 < 0x10000; upper16++)
        {
            uint64_t seed = lower48 | (upper16 << 48);
            printf("%d\n", seed);
            printf("%d\n", start);
            if(seed == start){
                printf("%d", seed);
                seed++;
            }
            applySeed(&g, DIM_OVERWORLD, seed);
            if (isViableStructurePos(structType, &g, p.x, p.z, 0))
            {
                FILE *fptr;
                fptr = fopen(".\\tmp.txt","w");
                fprintf(fptr, "Seed %" PRId64 " has your %s at (%d, %d).\n",
                    (int64_t) seed, structureName, p.x, p.z);
                fclose(fptr);
                return 0;
            }
        }
    }
}

int main(int argc, char** argv) {
    int arg1 = atoi(argv[1]);
    int arg3 = atoi(argv[3]);
    int arg4 = atoi(argv[4]);
    find(arg1, argv[2], arg3, arg4);
    return 0;
}

