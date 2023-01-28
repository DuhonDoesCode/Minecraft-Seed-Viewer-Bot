#include "finders.h"
#include "generator.h"
#include <stdio.h>
#include <stdlib.h>

int test(uint64_t seed, int version, int structure, char *structureName){
    printf("bro\n");
    Generator g;
    setupGenerator(&g, version, 0);   
    applySeed(&g, DIM_OVERWORLD, seed); 
    printf("bro3\n");
    int flag = 0;
    int listX[8000];
    int listZ[8000];
    printf("bro4\n");
    for(int x = -800; x<=800; x+=16){
        for(int z = -800; z<=800; z+=16){
            Pos p;
            if(!getStructurePos(structure, version, seed, x, z, &p)){
                continue;
            }
            if(!(abs(p.x - x) >= 16 || abs(p.z - z) >= 16)){
                continue;
            }
            if(isViableStructurePos(structure, &g, p.x, p.z, 0)){
                listX[abs(p.x)] = 1;
                listZ[abs(p.z)] = 1;
                flag = 1;
            }
        }
    }
    printf("%d\n", flag);
    for(int i = 0; i <= 1600; i++){
        for(int j = 0; j <= 1600; j++){
            if(listX[i] && listZ[j]){
                FILE *fptr;
                fptr = fopen(".\\tmp.txt","w");
                fprintf(fptr, "Seed: %" PRId64 " has the closest %s at: (%d, %d)\n", (int64_t) seed, structureName, i, j);
                fclose(fptr);
                return 0;
            }
        }
    }
    if(!flag){
        printf("Well damn\n");
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
    test(arg1, arg2, arg3, argv[4]);
    printf("bro2\n"); // Doesn't execute? What?
    return 0;
}