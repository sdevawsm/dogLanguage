// Dog Language Extension
// Extensão VS Code para DogLanguage

const vscode = require('vscode');

/**
 * Ativa a extensão
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
    console.log('🐕 Dog Language Extension ativada!');
}

/**
 * Desativa a extensão
 */
function deactivate() {
    console.log('🐕 Dog Language Extension desativada');
}

module.exports = {
    activate,
    deactivate
};
