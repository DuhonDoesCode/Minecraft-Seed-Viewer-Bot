#include "finders.h"
#include "generator.h"
#include <stdio.h>
#include <stdlib.h>

int test(uint64_t seed, int version, int structure, char *structureName){
    printf("Exe'd");
    Generator g;
    setupGenerator(&g, version, 0);   
    applySeed(&g, DIM_OVERWORLD, seed); 
    Pos p;
    if(getStructurePos(structure, version, seed, 0, 0, &p)){
        printf("Found");
        if(isViableStructurePos(structure, &g, p.x, p.z, 0)){
            printf("Valid");
            FILE *fptr;
            fptr = fopen(".\\tmp.txt","w");
            fprintf(fptr, "Seed: %" PRId64 " has the closest %s at: (%d, %d)\n", (int64_t) seed, structureName, p.x, p.z);
            fclose(fptr);
            return 0;
        }
    }
    FILE *fptr;
    fptr = fopen(".\\tmp.txt","w");
    fprintf(fptr, "Not found.");
    fclose(fptr);
    return 0;
}

int main(int argc, char** argv) {
    printf("Exe'd");
    char *end = NULL;
    uint64_t arg1 = strtoull(argv[1], &end, 10);
    int arg2 = atoi(argv[2]);
    int arg3 = atoi(argv[3]);
    test(arg1, arg2, arg3, argv[4]);
    return 0;
}