#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//#include <brinquedos.h>

typedef struct GoldenRetriever GoldenRetriever;
struct GoldenRetriever {
    int energia;

    void init_GoldenRetriever(int e) {
        energia = e;
    };

    void latir_alto() {
        printf("WOOF WOOF!\n");
    }
}

void int main() {
    int rex = (GoldenRetriever*)malloc(sizeof(GoldenRetriever))(10);

    if (rex.energia > 5) {
        printf("O Rex quer brincar!\n");
        while (rex.energia > 0) {
            printf("Rex correndo...\n");
            rex.energia = rex.energia - 1;
        }
    } else {
        printf("Rex está tirando um cochilo.\n");
    }

    return 0;
}