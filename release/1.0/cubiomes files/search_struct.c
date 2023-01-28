#include "finders.h"
#include <stdio.h>
#include <stdlib.h>

int find(uint64_t seed, int version, int structure, char *structureName){
    int mc = version;
    Pos p;
    Generator g;
    setupGenerator(&g, mc, 0);    
    int flag = 0;
    for(int x = 0; x<=16000; x+=80){
        for(int z = 0; z<=16000; z+=80){
            getStructurePos(structure, mc, seed, x, z, &p);
            if(isViableStructurePos(structure, &g, p.x, p.z, 0)){
                FILE *fptr;
                fptr = fopen(".\\tmp.txt","w");
                fprintf(fptr, "Seed %" PRId64 " has the closest %s at (%d, %d).\n",
                    (int64_t) seed, structureName, p.x, p.z);
                fclose(fptr);
                flag = 1;
                return 0;
            }
        }
    }
    if(!flag){
        FILE *fptr;
        fptr = fopen(".\\tmp.txt","w");
        fprintf(fptr, "Didn't find anything within 1000 chunks!");
        fclose(fptr);
        return 0;
    }
}

int main(int argc, char** argv) {
    char *end = NULL;
    uint64_t arg1 = strtoull(argv[1], &end, 10);
    int arg2 = atoi(argv[2]);
    int arg3 = atoi(argv[3]);
    find(arg1, arg2, arg3, argv[4]);
    return 0;
}