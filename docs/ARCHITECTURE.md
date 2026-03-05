# Architecture Modulaire - Data Query Builder

## Vue d'ensemble

Le serveur MCP Data Query Builder utilise une **architecture modulaire** où chaque outil est encapsulé dans sa propre classe avec son propre system prompt dédié.

## Structure du projet

```
data-query-builder/
├── server.py                          # Serveur MCP principal
├── sqlite_helper.py                   # Utilitaires SQLite
├── sample_employees.csv               # Données d'exemple
│
├── tools/                             # Répertoire modulaire des outils
│   ├── __init__.py                    # ToolManager - gestionnaire centralisé
│   ├── tool_base.py                   # Classe de base abstraite
│   ├── prompt_loader.py               # Chargeur de prompts depuis markdown
│   │
│   ├── load_csv_tool.py               # Outil: charger CSV
│   ├── describe_schema_tool.py         # Outil: décrire le schéma
│   ├── run_query_tool.py              # Outil: exécuter requêtes
│   ├── get_statistics_tool.py         # Outil: statistiques colonnes
│   ├── list_tables_tool.py            # Outil: lister les tables
│   │
│   ├── tool_load_csv.md               # System prompt: load_csv
│   ├── tool_describe_schema.md        # System prompt: describe_schema
│   ├── tool_run_query.md              # System prompt: run_query
│   ├── tool_get_statistics.md         # System prompt: get_statistics
│   ├── tool_list_tables.md            # System prompt: list_tables
│   └── README.md                      # Index et navigation
│
└── TOOL_PROMPTS.md                    # Vue d'ensemble (référence)
```

## Architecture en couches

```
┌─────────────────────────────────────────┐
│          server.py (FastMCP)            │
│  Registration des outils MCP            │
└──────────────────┬──────────────────────┘
                   │ Utilise
┌──────────────────▼──────────────────────┐
│         ToolManager (__init__.py)       │
│  Gestionnaire centralisé des outils     │
│  - Initialisation des outils            │
│  - Gestion de l'historique              │
└──────────┬─────────────────┬────────────┘
           │                 │
    ┌──────▼─────┐    ┌─────▼──────┐
    │ Tool (base)│    │  Tools Multiples
    └──────┬─────┘    │
           │          ├─ LoadCSVTool
   ┌───────┴────────┐ ├─ DescribeSchemaTool
   │                │ ├─ RunQueryTool
   ├─ execute()     │ ├─ GetStatisticsTool
   ├─ __call__()    │ └─ ListTablesTool
   └────────────────┘

┌──────────────────────────────────────────┐
│      prompt_loader.py                    │
│  Chargement des system prompts            │
│  depuis les fichiers markdown (.md)      │
└──────────────────────────────────────────┘
```

## Avantages de cette architecture

### 1. **Modularité**
- Chaque outil est une classe indépendante
- Facile à ajouter/retirer des outils
- Pas de dépendances circulaires

### 2. **Maintenabilité**
- Logique par outil isolée dans son fichier
- System prompts séparés dans des markdown
- Modifications faciles sans affecter les autres outils

### 3. **Extensibilité**
- Ajouter un nouvel outil:
  1. Créer `new_tool.py` hérité de `Tool`
  2. Créer `tool_new_tool.md` avec le system prompt
  3. Ajouter dans `ToolManager.__init__()`
  4. Enregistrer dans `server.py`

### 4. **Réutilisabilité**
- Classes `Tool` utilisables ailleurs
- `ToolManager` transférable à d'autres projets
- `prompt_loader` générique

### 5. **Testabilité**
- Chaque outil peut être testé indépendamment
- Système de prompts découplé de la logique
- Mock faciles pour les tests

## Flux de chargement des System Prompts

### 1. Initialization
```python
# Dans server.py
manager = get_tool_manager()  # Crée ToolManager
```

### 2. ToolManager crée les outils
```python
# Dans __init__.py
self.load_csv = LoadCSVTool(self.db)  # Chaque outil
```

### 3. Tool charge son prompt au init
```python
# Dans tool_base.py
def __init__(self, name: str):
    self.system_prompt = load_system_prompt(name)
```

### 4. prompt_loader lit le markdown
```python
# Dans prompt_loader.py
# Lit: tools/tool_load_csv.md
# Extrait: section "## System Prompt"
```

### 5. Prompt disponible pour les LLM
```python
# Via MCP
tool_instance.get_system_prompt()  # Retourne le system prompt complet
```

## Utilisation dans le code

### Utiliser un outil

```python
manager = get_tool_manager()

# Méthode 1: accès direct
result = manager.load_csv("file.csv", "table")

# Méthode 2: accès par nom
tool = manager.get_tool("load_csv")
result = tool("file.csv", "table")

# Méthode 3: tous les outils
tools = manager.get_all_tools()
for name, tool in tools.items():
    print(f"{name}: {tool.get_system_prompt()}")
```

### Ajouter un nouvel outil

1. **Créer la classe** (`tools/my_tool.py`):
```python
from tool_base import Tool

class MyTool(Tool):
    def __init__(self, db_connection):
        super().__init__("my_tool")
        self.db = db_connection
    
    def execute(self, param1: str) -> str:
        # Logique de l'outil
        return "result"
    
    def __call__(self, param1: str) -> str:
        return self.execute(param1=param1)
```

2. **Créer le system prompt** (`tools/tool_my_tool.md`):
```markdown
# Tool: my_tool

## Purpose
Description...

## System Prompt
Instructions pour le LLM...

## Parameters
...
```

3. **Enregistrer dans ToolManager** (`tools/__init__.py`):
```python
from my_tool import MyTool

class ToolManager:
    def __init__(self, db_connection):
        self.my_tool = MyTool(db_connection)
```

4. **Enregistrer dans server.py**:
```python
@mcp.tool()
def my_tool(param1: str) -> str:
    manager = get_tool_manager()
    return manager.my_tool(param1)
```

## Communication avec les LLM

### Le LLM reçoit:

1. **Définition de l'outil** (from `@mcp.tool()`)
   ```
   Name: load_csv
   Description: "Load a CSV file..."
   Parameters: file_path, table_name
   ```

2. **System Prompt** (from markdown)
   ```
   "You have the ability to load CSV files..."
   ```

3. **Best Practices** (from markdown)
   ```
   "Verify file exists..."
   ```

### Flux LLM → Outil
```
LLM lit System Prompt (via Tool.get_system_prompt())
    ↓
LLM comprend quand utiliser l'outil
    ↓
LLM appelle avec les paramètres appropriés
    ↓
Tool.execute() reçoit l'appel
    ↓
Résultat retourné au LLM
```

## Gestion de la base de données

### Connexion partagée
```python
db = get_db()  # Singleton
manager = ToolManager(db)  # Tous les outils utilisent le même db
```

### Historique des requêtes
```python
manager.query_history  # Liste partagée
# Alimentée par: RunQueryTool
# Accessible via: db://query-history resource
```

## Bonnes pratiques

### Pour les outils
- ✓ Hériter de `Tool`
- ✓ Implémenter `execute(**kwargs)`
- ✓ Implémenter `__call__(**kwargs)`
- ✓ Charger prompts dans `__init__`
- ✓ Documenter dans markdown

### Pour les prompts
- ✓ Fichiers séparés: `tool_<name>.md`
- ✓ Sections: Purpose, System Prompt, Parameters, Best Practices
- ✓ Exemples concrets
- ✓ Cas d'usage clairs (When to Use / When NOT to Use)

### Pour le serveur
- ✓ Utiliser `ToolManager` pour accès centralisé
- ✓ Une fonction wrapper par outil
- ✓ Documentation complète dans docstrings

## Performance

- **Lazy loading**: ToolManager créé à la première utilisation
- **Cached prompts**: Chargés une fois à l'init
- **Single DB connection**: Partagée et réutilisée
- **Memory efficient**: Pas de duplication

## Migration depuis l'ancien code

### Avant (monolithique)
```python
@mcp.tool()
def load_csv(...):
    # Logique mélangée
    # Prompt dans docstring
```

### Après (modulaire)
```python
@mcp.tool()
def load_csv(...):
    manager = get_tool_manager()
    return manager.load_csv(...)
    # Logique dans LoadCSVTool
    # Prompt dans tool_load_csv.md
```

## Debugging

### Vérifier un tool
```python
manager = get_tool_manager()
tool = manager.load_csv
print(tool.get_system_prompt())
```

### Lister tous les outils
```python
manager = get_tool_manager()
for name, tool in manager.get_all_tools().items():
    print(f"{name}: {tool.description}")
```

### Vérifier les prompts chargés
```python
from tools.prompt_loader import load_system_prompt
prompt = load_system_prompt("load_csv")
print(prompt)
```

## Résumé

✅ **Architecture modulaire**: Chaque outil dans son propre fichier  
✅ **System prompts séparés**: Dans des fichiers markdown dédiés  
✅ **Gestionnaire centralisé**: `ToolManager` pour cohésion  
✅ **Extensible**: Ajouter des outils facilement  
✅ **Maintenable**: Séparation des préoccupations claire  
✅ **Testable**: Chaque composant indépendant  
✅ **Performant**: Lazy loading et caching  
