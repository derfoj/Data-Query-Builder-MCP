# Guide de Connexion: Gemini CLI + MCP Data Query Builder

## Vue d'ensemble

Ce guide explique comment connecter Gemini CLI à votre serveur MCP Data Query Builder pour permettre à Gemini d'accéder et d'analyser vos données SQL.

## Architecture

```
Gemini CLI
    ↓
MCP Client Connection
    ↓
MCP Data Query Builder Server (server.py)
    ↓
SQLite Database + Tool Manager
```

## Configuration de Gemini CLI

### 1. Localisez le fichier de configuration de Gemini CLI

Le fichier de configuration se trouve généralement à:

**Windows (PowerShell):**
```
$env:USERPROFILE\.gemini\config.json
```

**macOS/Linux:**
```
~/.gemini/config.json
```

### 2. Créez ou modifiez `config.json`

Ajoutez la configuration pour le serveur MCP:

```json
{
  "mcpServers": {
    "data-query-builder": {
      "command": "python",
      "args": [
        "C:\\Users\\andyl\\OneDrive\\Desktop\\MCP_Server\\data-query-builder\\run_server.py"
      ],
      "cwd": "C:\\Users\\andyl\\OneDrive\\Desktop\\MCP_Server\\data-query-builder",
      "env": {
        "PYTHONPATH": "C:\\Users\\andyl\\OneDrive\\Desktop\\MCP_Server\\data-query-builder"
      }
    }
  }
}
```

**Adaptez les chemins** à votre environnement!

### 3. Remarques importantes

- ✓ Utilisez les chemins complets
- ✓ Utilisez des barres obliques `/` ou doubles barres obliques `\\` sur Windows
- ✓ Assurez-vous que Python est accessibles depuis le PATH
- ✓ Le répertoire `cwd` doit contenir `server.py`

## Démarrage du serveur MCP manuellement

Pour tester avant de configurer Gemini CLI:

```bash
# Naviguez au répertoire du serveur
cd C:\Users\andyl\OneDrive\Desktop\MCP_Server\data-query-builder

# Lancez le serveur
python run_server.py
```

Le serveur s'exécutera en mode stdio et attendrà les connexions.

## Test avec Gemini CLI

Une fois configuré:

```bash
# Démarrer Gemini CLI
gemini

# Dans Gemini CLI, vous devriez voir:
# "Connected to data-query-builder server"
```

## Cas d'usage - Exemple

Avec Gemini CLI connecté, vous pouvez:

```
gemini> Charge le fichier employees.csv dans ma base de données

→ Gemini utilise le tool "load_csv" de votre serveur MCP
→ Données chargées dans SQLite

gemini> Montre-moi les employés par département avec leur salaire moyen

→ Gemini:
   1. Utilise "describe_schema" pour connaître la structure
   2. Utilise "run_query" pour exécuter une requête GROUP BY
   3. Affiche les résultats
```

## Outils disponibles dans Gemini CLI

Une fois connecté, Gemini CLI aura accès à:

| Outil | Description |
|-------|-------------|
| `load_csv` | Charger un fichier CSV dans la base de données |
| `describe_schema` | Voir la structure des tables |
| `run_query` | Exécuter une requête SELECT SQL |
| `get_statistics` | Obtenir des statistiques sur une colonne |
| `list_tables` | Lister toutes les tables chargées |

## Dépannage

### Erreur: "command not found: python"

**Solution:**
- Vérifiez que Python est dans le PATH
- Utilisez le chemin complet vers Python:
  ```json
  "command": "C:\\Users\\andyl\\AppData\\Local\\Programs\\Python\\Python311\\python.exe"
  ```

### Erreur: "No module named 'mcp'"

**Solution:**
```bash
pip install mcp
```

### Erreur: "ImportError in server.py"

**Solution:**
```bash
# Assurez-vous que vous êtes dans le bon répertoire
cd C:\Users\andyl\OneDrive\Desktop\MCP_Server\data-query-builder

# Testez l'import
python -c "from tools import ToolManager; print('OK')"
```

### Le serveur démarre mais Gemini ne se connecte pas

**Vérifications:**
1. ✓ Vérifiez que le serveur affiche "Waiting for connections"
2. ✓ Vérifiez que `config.json` est syntaxiquement valide (JSON valide)
3. ✓ Vérifiez les chemins dans la configuration
4. ✓ Redémarrez Gemini CLI après les changements

## Développement et débogage

### Mode verbose

Pour déboguer la connexion:

```bash
# Lancez le serveur en mode verbose
python run_server.py --verbose
```

### Test local sans Gemini CLI

```bash
# Testez directement les outils
python test_server.py
```

Cela devrait afficher un rapport complet du fonctionnement.

## Structure des ressources

Le serveur expose également des ressources:

- `db://schema` - Schéma de la base de données en JSON
- `db://query-history` - Historique des requêtes exécutées

Gemini CLI peut accéder à ces ressources via la connexion MCP.

## Performance et limitations

### Limites actuelles

- Max 50 lignes par défaut (configurable en paramètre)
- Requêtes SELECT uniquement (sécurité)
- Base de données en mémoire (données perdues à chaque redémarrage)

### Optimisations possibles

Pour persister les données:
1. Modifier `sqlite_helper.py` pour utiliser un fichier SQLite
2. Charger le fichier au démarrage du serveur
3. Les changements persisteront entre les sessions

## Prochaines étapes

1. ✓ Testez avec `python test_server.py`
2. ✓ Configurez Gemini CLI avec votre `config.json`
3. ✓ Lancez `gemini` et connectez-vous
4. ✓ Chargez des données CSV et interrogez

## Ressources

- [MCP Documentation](https://modelcontextprotocol.io/)
- [Gemini CLI Documentation](https://ai.google.dev/gemini-api/docs)
- [FastMCP Documentation](https://github.com/jlouis/fastmcp)

## Support

Pour des problèmes:

1. Consultez [ARCHITECTURE.md](ARCHITECTURE.md) pour les détails techniques
2. Consultez [tools/README.md](tools/README.md) pour les outils individuels
3. Exécutez `python test_server.py` pour vérifier le fonctionnement
