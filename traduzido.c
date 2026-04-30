#include <stdio.h>
#include <stdlib.h>

//chamar_matilha <brinquedos->h>

typedef struct GoldenRetriever GoldenRetriever;
struct GoldenRetriever  {
    int energia;

    };
void init_GoldenRetriever(GoldenRetriever* self, int e) {
        self->energia = e;
    }

    void latir_alto(GoldenRetriever* self) {
        printf("WOOF WOOF!\n");
    }
}

int main() {
    GoldenRetriever* rex = (GoldenRetriever*)malloc(sizeof(GoldenRetriever));
init_GoldenRetriever(rex, 10);;

    if (rex->energia > 5) {
        printf("O Rex quer brincar!\n");
        while (rex->energia > 0) {
            printf("Rex correndo...\n");
            rex->energia = rex->energia - 1;
        }
    } else {
        printf("Rex está tirando um cochilo.\n");
    }

    return 0;
}