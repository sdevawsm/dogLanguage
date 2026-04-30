#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

void traduzir(FILE *in, FILE *out) {
    // Injeção de cabeçalhos necessária para as funções de sistema
    fprintf(out, "#include <stdio.h>\n#include <stdlib.h>\n#include <string.h>\n\n");

    char buffer[32768];
    int pos = fread(buffer, 1, sizeof(buffer) - 1, in);
    buffer[pos] = '\0';

    int i = 0;
    int em_matilha = 0;
    char nome_matilha[256] = "";

    while (i < pos) {
        // Ignorar espaços e comentários
        if (isspace(buffer[i])) {
            fputc(buffer[i++], out);
            continue;
        }

        // Processar strings
        if (buffer[i] == '"') {
            fputc(buffer[i++], out);
            while (i < pos && buffer[i] != '"') fputc(buffer[i++], out);
            if (i < pos) fputc(buffer[i++], out);
            continue;
        }

        // Processar Identificadores
        if (isalpha(buffer[i]) || buffer[i] == '_') {
            char word[256];
            int wpos = 0;
            while (i < pos && (isalnum(buffer[i]) || buffer[i] == '_')) {
                word[wpos++] = buffer[i++];
            }
            word[wpos] = '\0';

            // Lógica de Classes (Matilha)
            if (strcmp(word, "matilha") == 0) {
                while (isspace(buffer[i])) i++;
                int npos = 0;
                while (isalnum(buffer[i])) nome_matilha[npos++] = buffer[i++];
                nome_matilha[npos] = '\0';
                fprintf(out, "typedef struct %s %s;\nstruct %s", nome_matilha, nome_matilha, nome_matilha);
                em_matilha = 1;
            } 
            else if (strcmp(word, "instinto") == 0) {
                // Construtor: void init_NomeDaClasse
                fprintf(out, "void init_%s", nome_matilha);
            }
            else if (strcmp(word, "funcao") == 0) {
                // Se estiver dentro de uma matilha, é um método
                fprintf(out, "void"); 
            }
            else if (strcmp(word, "AU") == 0) {
                fprintf(out, "{");
            }
            else if (strcmp(word, "UAU") == 0) {
                if (em_matilha && buffer[i] != ' ' && buffer[i] != '\n') { // heurística simples
                    fprintf(out, "}"); // fechando método
                } else if (em_matilha) {
                    fprintf(out, "};"); // fechando a struct da matilha
                    em_matilha = 0;
                } else {
                    fprintf(out, "}");
                }
            }
            // Palavras Divertidas
            else if (strcmp(word, "chamar_matilha") == 0) fprintf(out, "#include");
            else if (strcmp(word, "canil") == 0) fprintf(out, "int main");
            else if (strcmp(word, "latir") == 0) fprintf(out, "printf");
            else if (strcmp(word, "farejar") == 0) fprintf(out, "scanf");
            else if (strcmp(word, "pinscher") == 0) fprintf(out, "int");
            else if (strcmp(word, "vira_lata") == 0) fprintf(out, "int");
            else if (strcmp(word, "dar_a_pata") == 0) fprintf(out, "if");
            else if (strcmp(word, "ou_fingir_de_morto") == 0) fprintf(out, "else");
            else if (strcmp(word, "focar_no_esquilo") == 0) fprintf(out, "while");
            else if (strcmp(word, "trazer_bolinha") == 0) fprintf(out, "return");
            else if (strcmp(word, "novo") == 0) {
                 while (isspace(buffer[i])) i++;
                 char tipo[256]; int tpos = 0;
                 while (isalnum(buffer[i])) tipo[tpos++] = buffer[i++];
                 tipo[tpos] = '\0';
                 fprintf(out, "(%s*)malloc(sizeof(%s))", tipo, tipo);
            }
            else fprintf(out, "%s", word);
            
            continue;
        }

        fputc(buffer[i++], out);
    }
}

int main(int argc, char *argv[]) {
    if (argc < 2) { return printf("Uso: %s arquivo.dog\n", argv[0]), 1; }
    FILE *in = fopen(argv[1], "r");
    FILE *out = fopen("traduzido.c", "w");
    if (!in || !out) return 1;
    traduzir(in, out);
    fclose(in); fclose(out);
    printf("🐕 Tradução concluída com sucesso!\n");
    return 0;
}