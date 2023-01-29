#include "finders.h"
#include "generator.h"
#include <stdio.h>
#include <stdlib.h>

int test(uint64_t seed, int version, int structure, char *structureName){
    Generator g;
    setupGenerator(&g, version, 0);   
    applySeed(&g, DIM_OVERWORLD, seed); 
    StructureConfig sconf;
    if (!getStructureConfig(structure, version, &sconf))
        return 0;
    double blocksPerRegion = sconf.regionSize * 16.0;
    int r = 1000;
    int x0 = -r;
    int z0 = -r;
    int x1 = r;
    int z1 = r;
    int rx0 = (int) floor(x0 / blocksPerRegion);
    int rz0 = (int) floor(z0 / blocksPerRegion);
    int rx1 = (int) ceil(x1 / blocksPerRegion);
    int rz1 = (int) ceil(z1 / blocksPerRegion);
    int i, j;

    for (j = rz0; j <= rz1; j++)
    {
        for (i = rx0; i <= rx1; i++)
        {   // check the structure generation attempt in region (i, j)
            Pos pos;
            if (!getStructurePos(structure, version, seed, i, j, &pos))
                continue; // this region is not suitable
            if (pos.x < x0 || pos.x > x1 || pos.z < z0 || pos.z > z1)
                continue; // structure is outside the specified area
            if (!isViableStructurePos(structure, &g, pos.x, pos.z, 0))
                continue; // biomes are not viable
            else if (version >= MC_1_18)
            {   // some structures in 1.18+ depend on the terrain
                if (!isViableStructureTerrain(structure, &g, pos.x, pos.z))
                    continue;
            }
            FILE *fptr;
            fptr = fopen(".\\tmp.txt","w");
            fprintf(fptr, "Seed: %" PRId64 " has the closest %s at: (%d, %d)\n", (int64_t) seed, structureName, pos.x, pos.z);
            fclose(fptr);
            return 0;
        }
    }
}

int main(int argc, char** argv) {
    char *end = NULL;
    uint64_t arg1 = strtoull(argv[1], &end, 10);
    int arg2 = atoi(argv[2]);
    int arg3 = atoi(argv[3]);
    test(arg1, arg2, arg3, argv[4]);
    return 0;
}