#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

void traduzir(FILE *in, FILE *out) {
    fprintf(out, "#include <stdio.h>\n#include <stdlib.h>\n\n");

    char buffer[32768];
    int pos = fread(buffer, 1, sizeof(buffer) - 1, in);
    buffer[pos] = '\0';

    int i = 0;

    int em_matilha = 0;
    int em_metodo = 0;
    int struct_fechada = 0;
    int ignorar_proximo_AU = 0;

    char nome_matilha[256] = "";

    while (i < pos) {

        // =========================
        // COMENTÁRIO
        // =========================
        if (buffer[i] == '/' && buffer[i+1] == '/') {
            while (i < pos && buffer[i] != '\n') {
                fputc(buffer[i++], out);
            }
            continue;
        }

        // =========================
        // STRING
        // =========================
        if (buffer[i] == '"') {
            fputc(buffer[i++], out);
            while (i < pos && buffer[i] != '"') {
                fputc(buffer[i++], out);
            }
            if (i < pos) fputc(buffer[i++], out);
            continue;
        }

        // =========================
        // ESPAÇO
        // =========================
        if (isspace(buffer[i])) {
            fputc(buffer[i++], out);
            continue;
        }

        // =========================
        // PALAVRAS
        // =========================
        if (isalpha(buffer[i]) || buffer[i] == '_') {

            char word[256];
            int wpos = 0;

            while (i < pos && (isalnum(buffer[i]) || buffer[i] == '_')) {
                word[wpos++] = buffer[i++];
            }
            word[wpos] = '\0';

            // ===== MATILHA =====
            if (strcmp(word, "matilha") == 0) {

                while (isspace(buffer[i])) i++;

                int npos = 0;
                while (isalnum(buffer[i])) {
                    nome_matilha[npos++] = buffer[i++];
                }
                nome_matilha[npos] = '\0';

                fprintf(out,
                    "typedef struct %s %s;\nstruct %s {\n",
                    nome_matilha, nome_matilha, nome_matilha);

                em_matilha = 1;
                struct_fechada = 0;
                ignorar_proximo_AU = 1; // evita { duplicado
            }

            // ===== INSTINTO =====
            else if (strcmp(word, "instinto") == 0) {

                if (!struct_fechada) {
                    fprintf(out, "};\n");
                    struct_fechada = 1;
                }

                fprintf(out, "void init_%s(%s* self", nome_matilha, nome_matilha);

                em_metodo = 1;
                em_matilha = 0;

                while (buffer[i] != '(') i++;
                i++;

                if (buffer[i] != ')') {
                    fprintf(out, ", ");

                    while (buffer[i] != ')') {
                        if (strncmp(&buffer[i], "pinscher", 8) == 0) {
                            fprintf(out, "int");
                            i += 8;
                        } else {
                            fputc(buffer[i], out);
                            i++;
                        }
                    }
                }

                fprintf(out, ")");
                i++;
            }

            // ===== FUNÇÃO =====
            else if (strcmp(word, "funcao") == 0) {

                if (em_matilha && !struct_fechada) {
                    fprintf(out, "};\n");
                    struct_fechada = 1;
                    em_matilha = 0;
                }

                while (isspace(buffer[i])) i++;

                char func_name[256];
                int fpos = 0;

                while (isalnum(buffer[i]) || buffer[i] == '_') {
                    func_name[fpos++] = buffer[i++];
                }
                func_name[fpos] = '\0';

                // consumir ()
                while (buffer[i] != '(') i++;
                i++;
                while (buffer[i] != ')') i++;
                i++;

                if (strcmp(func_name, "canil") == 0) {
                    fprintf(out, "int main()");
                    em_metodo = 0;
                } else {
                    fprintf(out, "void %s(%s* self)", func_name, nome_matilha);
                    em_metodo = 1;
                }
            }

            // ===== OBJETO =====
            else if (strcmp(word, "vira_lata") == 0) {

                while (isspace(buffer[i])) i++;

                char var_name[256];
                int vpos = 0;

                while (isalnum(buffer[i])) {
                    var_name[vpos++] = buffer[i++];
                }
                var_name[vpos] = '\0';

                while (isspace(buffer[i]) || buffer[i] == '=') i++;

                if (strncmp(&buffer[i], "novo", 4) == 0) {
                    i += 4;

                    while (isspace(buffer[i])) i++;

                    char type[256];
                    int tpos = 0;

                    while (isalnum(buffer[i])) {
                        type[tpos++] = buffer[i++];
                    }
                    type[tpos] = '\0';

                    while (buffer[i] != '(') i++;
                    i++;

                    char args[256];
                    int apos = 0;

                    while (buffer[i] != ')') {
                        args[apos++] = buffer[i++];
                    }
                    args[apos] = '\0';
                    i++;

                    fprintf(out,
                        "%s* %s = (%s*)malloc(sizeof(%s));\n",
                        type, var_name, type, type);

                    fprintf(out,
                        "init_%s(%s, %s);\n",
                        type, var_name, args);
                }
            }

            // ===== KEYWORDS =====
            else if (strcmp(word, "AU") == 0) {
                if (ignorar_proximo_AU) {
                    ignorar_proximo_AU = 0;
                } else {
                    fprintf(out, "{");
                }
            }
            else if (strcmp(word, "UAU") == 0) fprintf(out, "}");
            else if (strcmp(word, "latir") == 0) fprintf(out, "printf");
            else if (strcmp(word, "pinscher") == 0) fprintf(out, "int");
            else if (strcmp(word, "dar_a_pata") == 0) fprintf(out, "if");
            else if (strcmp(word, "ou_fingir_de_morto") == 0) fprintf(out, "else");
            else if (strcmp(word, "focar_no_esquilo") == 0) fprintf(out, "while");
            else if (strcmp(word, "trazer_bolinha") == 0) fprintf(out, "return");

            // ===== VARIÁVEIS =====
            else {
                if (em_metodo &&
                    strcmp(word, "self") != 0 &&
                    strcmp(word, "e") != 0) {

                    fprintf(out, "self->%s", word);
                } else {
                    fprintf(out, "%s", word);
                }
            }

            continue;
        }

        // ===== OPERADOR . =====
        if (buffer[i] == '.') {
            fprintf(out, "->");
            i++;
        } else {
            fputc(buffer[i++], out);
        }
    }
}

// ===== MAIN =====
int main(int argc, char *argv[]) {

    if (argc < 2) {
        printf("Uso: ./dogc arquivo.dog\n");
        return 1;
    }

    FILE *in = fopen(argv[1], "r");
    if (!in) {
        printf("Erro ao abrir arquivo\n");
        return 1;
    }

    FILE *out = fopen("traduzido.c", "w");

    traduzir(in, out);

    fclose(in);
    fclose(out);

    printf("🐕 Código traduzido com sucesso!\n");
    return 0;
}