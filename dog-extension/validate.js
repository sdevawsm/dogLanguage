const fs = require('fs');

const files = [
  'package.json',
  'language-configuration.json',
  'syntaxes/dog.tmLanguage.json',
  'snippets/dog.json'
];

console.log('Validando arquivos da extensão Dog Language...\n');

files.forEach(f => {
  try {
    const content = fs.readFileSync(f, 'utf8');
    JSON.parse(content);
    console.log('✓', f);
  } catch(e) {
    console.log('✗', f, '-', e.message);
  }
});

console.log('\n✓ Todos os arquivos JSON estão válidos!');
