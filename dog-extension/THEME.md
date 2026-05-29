# Dog Language Theme Colors
This file documents the color scheme used by the Dog Language extension.

## Scopes and Colors

### Keywords (Control Flow)
- `keyword.control.conditional.dog` - dar_a_pata, se_tiver_petisco, ou_rosnar (if/else)
- `keyword.control.loop.dog` - focar_no_esquilo, perseguir (while)
- `keyword.control.return.dog` - trazer_bolinha (return)
- `keyword.control.import.dog` - chamar_matilha (import)
- `keyword.control.class.dog` - classe, matilha, instinto (class)
- `keyword.control.function.dog` - funcao, latido, novo, this, eu_mesmo (function/new/self)
- `keyword.control.exception.dog` - tentar_pegar, fugiu_o_gato (try/catch)

### Types
- `storage.type.primitive.dog` - pedigree, pelo, carne, raça, pinscher, vira_lata
- `storage.type.numeric.dog` - inteiro, real
- `storage.type.string.dog` - texto
- `storage.type.boolean.dog` - booleano

### Functions
- `entity.name.function.builtin.dog` - canil, latir, farejar, etc

### Constants
- `constant.numeric.integer.dog` - Inteiros (123)
- `constant.numeric.float.dog` - Floats (123.45)
- `constant.language.dog` - bom_garoto, mal_educado (true/false)

### Comments and Strings
- `comment.line.double-slash.dog` - //
- `comment.block.dog` - /* */
- `string.quoted.double.dog` - "texto"
- `constant.character.escape.dog` - \\n, \\t, etc

### Operators
- `keyword.operator.comparison.dog` - ==, !=, <, >, <=, >=
- `keyword.operator.arithmetic.dog` - +, -, *, /, %
- `keyword.operator.assignment.dog` - =
- `keyword.operator.logical.dog` - &&, ||, !

## Custom Theme Example

To create a custom theme for Dog Language, add these entries to your theme:

```json
{
  "name": "Dog Language Theme",
  "tokenColors": [
    {
      "scope": "keyword.control.conditional.dog",
      "settings": {
        "foreground": "#FF6B6B",
        "fontStyle": "bold"
      }
    },
    {
      "scope": "storage.type.primitive.dog",
      "settings": {
        "foreground": "#4ECDC4"
      }
    },
    {
      "scope": "entity.name.function.builtin.dog",
      "settings": {
        "foreground": "#FFE66D"
      }
    }
  ]
}
```
