#include "finders.h"
#include <stdio.h>
#include <stdlib.h>

int find(uint64_t seed, int version){
    int mc = version;

    // Only the first stronghold has a position which can be estimated
    // (+/-112 blocks) without biome check.
    StrongholdIter sh;
    Pos pos = initFirstStronghold(&sh, mc, seed);
    FILE *fptr;
    fptr = fopen(".\\tmp.txt","w");
    fprintf(fptr, "Seed: %" PRId64 "// Estimated position of first stronghold: (%d, %d)\n", (int64_t) seed, pos.x, pos.z);
    fclose(fptr);
    return 0;

    // Generator g;
    // setupGenerator(&g, mc, 0);
    // applySeed(&g, DIM_OVERWORLD, seed);

    // pos = getSpawn(&g);
    // printf("Spawn: (%d, %d)\n", pos.x, pos.z);

    // int i, N = 12;
    // for (i = 1; i <= N; i++)
    // {
    //     if (nextStronghold(&sh, &g) <= 0)
    //         break;
    //     printf("Stronghold #%-3d: (%6d, %6d)\n", i, sh.pos.x, sh.pos.z);
    // }

}

int main(int argc, char** argv) {
    char *end = NULL;
    uint64_t arg1 = strtoull(argv[1], &end, 10);
    int arg3 = atoi(argv[2]);
    find(arg1, arg3);
    return 0;
}