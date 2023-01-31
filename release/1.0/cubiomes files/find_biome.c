#include "generator.h"
#include <stdio.h>
#include <stdlib.h>

int find(int biome, char *biomeName, int version, int start){
    // Set up a biome generator that reflects the biome generation of
    // Minecraft 1.18.
    Generator g;
    setupGenerator(&g, version, 0);

    // Seeds are internally represented as unsigned 64-bit integers.
    uint64_t seed;
    for (seed = start + 1; ; seed++)
    {
        // Apply the seed to the generator for the Overworld dimension.
        applySeed(&g, DIM_OVERWORLD, seed);

        // To get the biome at a single block position, we can use getBiomeAt().
        int scale = 1; // scale=1: block coordinates, scale=4: biome coordinates
        int x = 0, y = 63, z = 0;
        int biomeID = getBiomeAt(&g, scale, x, y, z);
        
        //printf("%" PRId64 "\n", seed);
        if (biomeID == biome)
        {
            FILE *fptr;
            fptr = fopen(".\\tmp.txt","w");
            fprintf(fptr, "Seed %" PRId64 " has a %s biome at "
                "block position (%d, %d).\n", (int64_t) seed, biomeName, x, z);
            fclose(fptr);
            break;
        }
    }

    return 0;
}

int main(int argc, char** argv) {
    int arg1 = atoi(argv[1]);
    int arg3 = atoi(argv[3]);
    int arg4 = atoi(argv[4]);
    find(arg1, argv[2], arg3, arg4);
    return 0;
}