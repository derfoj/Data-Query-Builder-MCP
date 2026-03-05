# Guide Complet: Tester et Connecter Gemini CLI avec MCP Data Query Builder

## 📋 Plan

1. **Vérifier le fonctionnement** ✓ (test_server.py)
2. **Installer les dépendances MCP**
3. **Configurer Gemini CLI**
4. **Tester la connexion**

---

## Étape 1: Vérifier que le serveur fonctionne ✓

Le serveur fonctionne correctement! Vous pouvez le vérifier:

```powershell
# Aller au répertoire
cd C:\Users\andyl\OneDrive\Desktop\MCP_Server\data-query-builder

# Exécuter le test
python test_server.py
```

**Résultat attendu:**
```
TEST DE LA SERVEUR MCP DATA-QUERY-BUILDER
...
✓ TOUS LES TESTS RÉUSSIS
```

---

## Étape 2: Installer les dépendances MCP

Vous devez installer le package `mcp`:

```powershell
# Activer l'environnement virtuel (si pas déjà fait)
.\.venv\Scripts\Activate.ps1

# Installer mcp
pip install mcp

# Vérifier l'installation
python -c "import mcp; print('✓ MCP installé')"
```

---

## Étape 3: Configuration de Gemini CLI

### Localiser le fichier de configuration

Le fichier se trouve à:
```
%USERPROFILE%\.gemini\config.json
```

Ou via PowerShell:
```powershell
$configPath = Join-Path $env:USERPROFILE '.gemini' 'config.json'
# Créer le répertoire s'il n'existe pas
$configDir = Split-Path $configPath
if (-not (Test-Path $configDir)) { New-Item -ItemType Directory -Path $configDir -Force }
```

### Contenu du fichier `config.json`

Créez ou modifiez `~/.gemini/config.json`:

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
      },
      "disabled": false
    }
  }
}
```

### Créer le fichier avec PowerShell

```powershell
# Créer le contenu JSON
$config = @{
    mcpServers = @{
        "data-query-builder" = @{
            command = "python"
            args = @("C:\Users\andyl\OneDrive\Desktop\MCP_Server\data-query-builder\run_server.py")
            cwd = "C:\Users\andyl\OneDrive\Desktop\MCP_Server\data-query-builder"
            env = @{
                PYTHONPATH = "C:\Users\andyl\OneDrive\Desktop\MCP_Server\data-query-builder"
            }
            disabled = $false
        }
    }
}

# Convertir en JSON
$json = $config | ConvertTo-Json -Depth 10

# Créer le répertoire s'il n'existe pas
$configPath = Join-Path $env:USERPROFILE '.gemini' 'config.json'
$configDir = Split-Path $configPath
if (-not (Test-Path $configDir)) {
    New-Item -ItemType Directory -Path $configDir -Force | Out-Null
}

# Écrire le fichier
$json | Out-File -FilePath $configPath -Encoding UTF8

Write-Host "✓ Configuration créée: $configPath"
```

---

## Étape 4: Lancer Gemini CLI

### Démarrer Gemini CLI

```powershell
# Démarrer Gemini CLI
gemini
```

### Vérifier la connexion

Dans Gemini CLI, tapez:

```
@data-query-builder list_tables
```

**Résultat attendu:**
```
No tables loaded yet.
```

---

## Workflows - Exemples d'utilisation

### Workflow 1: Charger et explorer des données

```
User: Peux-tu charger employees.csv?

Gemini utilise: @data-query-builder load_csv "employees.csv" "employees"

User: Montre-moi le schéma

Gemini utilise: @data-query-builder describe_schema

User: Affiche les 5 premières lignes

Gemini utilise: @data-query-builder run_query "SELECT * FROM employees LIMIT 5"
```

### Workflow 2: Analyse statistique

```
User: Quels sont les stats des salaires?

Gemini utilise: @data-query-builder get_statistics "employees" "salary"

Résultat:
- Total rows: 150
- Non-null: 148
- Nulls: 2
- Min: 35000
- Max: 125000
- Mean: 72500.00
```

### Workflow 3: Requête complexe

```
User: Montre-moi le salaire moyen par département

Gemini utilise: @data-query-builder run_query 
"SELECT department, AVG(salary) as avg_salary, COUNT(*) as count 
 FROM employees 
 GROUP BY department 
 ORDER BY avg_salary DESC"

Résultat: Tableau avec les statistiques par département
```

---

## ✓ Checklist de configuration

- [ ] `test_server.py` exécuté avec succès
- [ ] `pip install mcp` complété
- [ ] Fichier `~/.gemini/config.json` créé
- [ ] JSON du config.json est valide (testez avec [jsonlint.com](https://jsonlint.com/))
- [ ] Chemins dans config.json utilisent `\\` ou `/` (pas mélangés)
- [ ] Répertoire `cwd` contient `run_server.py`
- [ ] Gemini CLI démarre sans erreur
- [ ] `@data-query-builder list_tables` retourne une réponse

---

## 🔧 Dépannage

### Erreur: "Module not found: mcp"

```powershell
# Vérifier l'installation
pip list | Select-String mcp

# Si absent, installer
pip install mcp
```

### Erreur: "Python not found"

Utiliser le chemin complet:
```json
"command": "C:\\Users\\andyl\\OneDrive\\Desktop\\MCP_Server\\data-query-builder\\.venv\\Scripts\\python.exe"
```

### Erreur: "Connexion impossible"

1. Vérifiez que le JSON est valide
2. Vérifiez les chemins
3. Redémarrez Gemini CLI:
```powershell
# Fermer Gemini CLI
# Ouvrir PowerShell
gemini
```

### Gemini CLI ne reconnaît pas les outils

```
@data-query-builder list_tables
# Erreur: Unknown server
```

**Solutions:**
1. Vérifiez config.json existe et est valide
2. Vérifiez les chemins
3. Redémarrez Gemini CLI
4. Vérifiez que `run_server.py` existe

### Erreur: "FileNotFoundError: sample_employees.csv"

C'est normal. `test_server.py` crée `test_data.csv`. Vous pouvez:
1. Charger votre propre fichier CSV
2. Utiliser `test_data.csv` généré par le test

---

## 📊 Prochaines étapes

1. ✓ Configurez `config.json`
2. ✓ Installez `mcp`
3. ✓ Lancez Gemini CLI
4. ✓ Testez les outils
5. ✓ Chargez vos données
6. ✓ Commencez l'analyse

---

## 📚 Ressources

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Détails techniques du serveur
- **[tools/README.md](tools/README.md)** - Documentation des outils
- **[test_server.py](test_server.py)** - Test complet du serveur
- **[MCP Protocol](https://modelcontextprotocol.io/)** - Spécification MCP

---

## 🎯 Commandes rapides

```powershell
# Aller au répertoire
cd C:\Users\andyl\OneDrive\Desktop\MCP_Server\data-query-builder

# Activer l'environnement
.\.venv\Scripts\Activate.ps1

# Installer MCP
pip install mcp

# Tester le serveur
python test_server.py

# Lancer Gemini CLI
gemini
```

---

## Support

Pour les problèmes:
1. Exécutez `python test_server.py` pour vérifier le serveur
2. Consultez `ARCHITECTURE.md` pour les détails techniques
3. Consultez `tools/README.md` pour la documentation des outils
