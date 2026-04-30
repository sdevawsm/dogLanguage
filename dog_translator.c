#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

typedef struct {
    const char *dog;
    const char *c_equiv;
} TokenMap;

TokenMap keywords[] = {
    {"chamar_matilha", "#include"},
    {"funcao", ""},
    {"canil", "int main"},
    {"AU", "{"},
    {"UAU", "}"},
    {"latir", "printf"},
    {"farejar", "scanf"},
    {"dar_a_pata", "if"},
    {"ou_fingir_de_morto", "else"},
    {"focar_no_esquilo", "while"},
    {"trazer_bolinha", "return"},
    {"matilha", "struct"},
    {"novo", ""},
    {"pinscher", "int"},
    {"vira_lata", "int"},
    {"inteiro", "int"},
    {"real", "float"},
    {"texto", "char*"},
    {"booleano", "int"},
    {"instinto", ""},
    {"this", "self"},
    {NULL, NULL}
};

typedef struct {
    char name[256];
    char type[256];
} Variable;

Variable vars[1024];
int var_count = 0;

void register_variable(const char *name, const char *type) {
    if (var_count < 1024) {
        strcpy(vars[var_count].name, name);
        strcpy(vars[var_count].type, type);
        var_count++;
    }
}

const char *translate_type(const char *type) {
    if (strcmp(type, "inteiro") == 0) return "int";
    if (strcmp(type, "real") == 0) return "float";
    if (strcmp(type, "texto") == 0) return "char*";
    if (strcmp(type, "booleano") == 0) return "int";
    return type;
}

const char *translate_keyword(const char *word) {
    for (int i = 0; keywords[i].dog != NULL; i++) {
        if (strcmp(word, keywords[i].dog) == 0) {
            return keywords[i].c_equiv;
        }
    }
    return word;
}

void traduzir(FILE *in, FILE *out) {
    char buffer[16384];
    int pos = 0;
    int ch;
    
    while ((ch = fgetc(in)) != EOF) {
        if (pos < (int)sizeof(buffer) - 1) {
            buffer[pos++] = (char)ch;
        }
    }
    buffer[pos] = '\0';
    
    int i = 0;
    int in_include = 0;
    int in_class = 0;
    int brace_depth = 0;
    
    while (i < pos) {
        if (isspace(buffer[i])) {
            fputc(buffer[i], out);
            i++;
            continue;
        }
        
        if (buffer[i] == '"') {
            fprintf(out, "\"");
            i++;
            while (i < pos && buffer[i] != '"') {
                if (buffer[i] == '\\') {
                    fputc(buffer[i], out);
                    i++;
                    if (i < pos) {
                        fputc(buffer[i], out);
                        i++;
                    }
                } else {
                    fputc(buffer[i], out);
                    i++;
                }
            }
            if (i < pos) {
                fputc(buffer[i], out);
                i++;
            }
            in_include = 0;
            continue;
        }
        
        if ((buffer[i] >= 'a' && buffer[i] <= 'z') || (buffer[i] >= 'A' && buffer[i] <= 'Z') || buffer[i] == '_') {
            char word[256];
            int wpos = 0;
            int start_i = i;
            while (i < pos && ((buffer[i] >= 'a' && buffer[i] <= 'z') || (buffer[i] >= 'A' && buffer[i] <= 'Z') || (buffer[i] >= '0' && buffer[i] <= '9') || buffer[i] == '_')) {
                word[wpos++] = buffer[i++];
            }
            word[wpos] = '\0';
            
            if (strcmp(word, "AU") == 0) {
                fprintf(out, "{");
                brace_depth++;
            } else if (strcmp(word, "UAU") == 0) {
                fprintf(out, "}");
                brace_depth--;
            } else if (strcmp(word, "trazer_bolinha") == 0) {
                fprintf(out, "return");
            } else if (strcmp(word, "chamar_matilha") == 0) {
                fprintf(out, "#include");
                in_include = 1;
            } else if (strcmp(word, "matilha") == 0) {
                fprintf(out, "typedef struct ");
                while (i < pos && isspace(buffer[i])) {
                    fputc(buffer[i], out);
                    i++;
                }
                wpos = 0;
                while (i < pos && ((buffer[i] >= 'a' && buffer[i] <= 'z') || (buffer[i] >= 'A' && buffer[i] <= 'Z') || (buffer[i] >= '0' && buffer[i] <= '9') || buffer[i] == '_')) {
                    word[wpos++] = buffer[i++];
                }
                word[wpos] = '\0';
                fprintf(out, "%s %s;\nstruct %s", word, word, word);
                in_class = 1;
            } else if (strcmp(word, "funcao") == 0) {
                fprintf(out, "");
            } else if (strcmp(word, "pinscher") == 0) {
                fprintf(out, "int");
            } else if (strcmp(word, "vira_lata") == 0) {
                fprintf(out, "int");
            } else if (strcmp(word, "instinto") == 0) {
                fprintf(out, "");
            } else if (strcmp(word, "novo") == 0) {
                while (i < pos && isspace(buffer[i])) i++;
                wpos = 0;
                while (i < pos && ((buffer[i] >= 'a' && buffer[i] <= 'z') || (buffer[i] >= 'A' && buffer[i] <= 'Z') || (buffer[i] >= '0' && buffer[i] <= '9') || buffer[i] == '_')) {
                    word[wpos++] = buffer[i++];
                }
                word[wpos] = '\0';
                fprintf(out, "(struct %s *)malloc(sizeof(struct %s))", word, word);
            } else if (strcmp(word, "latir") == 0) {
                fprintf(out, "printf");
            } else if (strcmp(word, "dar_a_pata") == 0) {
                fprintf(out, "if");
            } else if (strcmp(word, "ou_fingir_de_morto") == 0) {
                fprintf(out, "else");
            } else if (strcmp(word, "focar_no_esquilo") == 0) {
                fprintf(out, "while");
            } else {
                fprintf(out, "%s", word);
            }
            continue;
        }
        
        fputc(buffer[i], out);
        i++;
    }
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Uso: %s arquivo.dog\n", argv[0]);
        return 1;
    }

    FILE *in = fopen(argv[1], "r");
    if (!in) {
        perror("Erro ao abrir arquivo .dog");
        return 1;
    }

    FILE *out = fopen("traduzido.c", "w");
    if (!out) {
        fclose(in);
        return 1;
    }

    traduzir(in, out);

    fclose(in);
    fclose(out);

    printf("Sucesso! Arquivo 'traduzido.c' gerado.\n");
    printf("Compile com: gcc traduzido.c -o programa\n");

    return 0;
}