# 📚 Documentation Complète - Data Query Builder MCP + Gemini CLI

## 🎯 Commencez ici

**Nouveau venu?** Lisez dans cet ordre:
1. 👈 [README_SUMMARY.md](README_SUMMARY.md) - **Vue d'ensemble (2 min)**
2. 🚀 [QUICKSTART_GEMINI.md](QUICKSTART_GEMINI.md) - **Guide de démarrage (5 min)**
3. 🏗️ [ARCHITECTURE.md](ARCHITECTURE.md) - **Détails techniques (10 min)**
4. 🔧 [GEMINI_SETUP.md](GEMINI_SETUP.md) - **Configuration avancée (si besoin)**

---

## 📁 Structure complète du projet

```
data-query-builder/
│
├── 📄 Documentation principale
│   ├── README_SUMMARY.md          ← COMMENCEZ ICI
│   ├── QUICKSTART_GEMINI.md       ← Configuration rapide
│   ├── ARCHITECTURE.md             ← Détails techniques
│   ├── SECURITY.md                 ← 🔒 SÉCURITÉ (NOUVEAU!)
│   ├── GEMINI_SETUP.md             ← Configuration avancée
│   ├── TOOL_PROMPTS.md             ← Tous les prompts en 1 fichier
│   └── INDEX.md                    ← Navigation (ce fichier)
│
├── 🐍 Code source (src/)
│   ├── server.py                   ← Serveur MCP FastMCP (5 outils)
│   ├── security.py                 ← Gestionnaire de sécurité
│   ├── sqlite_helper.py            ← Utilitaires SQLite
│   └── tools/                      ← Architecture modulaire des outils
│       ├── __init__.py             ← ToolManager (orchestrateur)
│       ├── tool_base.py            ← Classe abstraite Tool
│       ├── prompt_loader.py        ← Chargeur de prompts markdown
│       ├── load_csv_tool.py        ← Charger CSV
│       ├── describe_schema_tool.py ← Voir le schéma
│       ├── run_query_tool.py       ← Exécuter requêtes
│       ├── get_statistics_tool.py  ← Statistiques colonnes
│       ├── list_tables_tool.py     ← Lister tables
│       └── tool_*.md               ← System prompts
│
├── ⚙️ Configuration (config/)
│   ├── mcp_config.json             ← Configuration MCP
│   └── .env                        ← Variables d'environnement
│
├── 📊 Données (data/)
│   ├── sample_employees(in).csv    ← Données d'exemple
│   └── test_data.csv               ← Données de test (généré)
│
├── 🧪 Tests (tests/)
│   └── test_server.py              ← Suite de tests complète ✓ VÉRIFIÉ
│
├── 🔧 Scripts (scripts/)
│   └── welcome.py                  ← Guide de bienvenue
│
├── 🚀 Lanceurs principaux
│   ├── run_mcp_server.py          ← Lancer le serveur MCP
│   ├── run_tests.py                ← Exécuter les tests
│   ├── welcome.py                  ← Guide de bienvenue
│   └── README.md                   ← Documentation principale
│
└── 🔒 .gitignore                   ← Fichiers à ignorer
```
    │
    ├── 📚 System prompts (en markdown)
    │   ├── tool_load_csv.md         ← Prompt: load_csv
    │   ├── tool_describe_schema.md  ← Prompt: describe_schema
    │   ├── tool_run_query.md        ← Prompt: run_query
    │   ├── tool_get_statistics.md   ← Prompt: get_statistics
    │   ├── tool_list_tables.md      ← Prompt: list_tables
    │   └── README.md                ← Navigation des outils
    │
    └── __pycache__/                 ← Cache Python
```

---

## 🎯 Cas d'usage

### Cas 1: Je veux juste tester rapidement
```powershell
python test_server.py
# ✓ Vérification complète du serveur en 5 secondes
```

### Cas 2: Je veux configurer Gemini CLI
1. Lire [QUICKSTART_GEMINI.md](QUICKSTART_GEMINI.md)
2. `pip install mcp`
3. Éditer `~/.gemini/config.json`
4. Lancer `gemini`

### Cas 3: Je veux comprendre l'architecture
Lire [ARCHITECTURE.md](ARCHITECTURE.md) pour:
- Vue d'ensemble en couches
- Flux de chargement des prompts
- Comment ajouter un nouvel outil
- Communication avec les LLM

### Cas 4: Je veux dépanner une erreur
1. Vérifier [QUICKSTART_GEMINI.md](QUICKSTART_GEMINI.md) section "Dépannage"
2. Vérifier [GEMINI_SETUP.md](GEMINI_SETUP.md) section "Dépannage"
3. Exécuter `python test_server.py` pour diagnostic

---

## 📊 Outils disponibles

| Outil | Fichier | Prompt | Status | Cas d'usage |
|-------|---------|--------|--------|------------|
| `load_csv` | [load_csv_tool.py](tools/load_csv_tool.py) | [tool_load_csv.md](tools/tool_load_csv.md) | ✓ | Importer des CSV |
| `describe_schema` | [describe_schema_tool.py](tools/describe_schema_tool.py) | [tool_describe_schema.md](tools/tool_describe_schema.md) | ✓ | Voir la structure |
| `run_query` | [run_query_tool.py](tools/run_query_tool.py) | [tool_run_query.md](tools/tool_run_query.md) | ✓ | Interroger données |
| `get_statistics` | [get_statistics_tool.py](tools/get_statistics_tool.py) | [tool_get_statistics.md](tools/tool_get_statistics.md) | ✓ | Statistiques colonnes |
| `list_tables` | [list_tables_tool.py](tools/list_tables_tool.py) | [tool_list_tables.md](tools/tool_list_tables.md) | ✓ | Voir tables chargées |

---

## 🔗 Navigation rapide

### Pour les utilisateurs
- 📖 Comment ça marche? → [README_SUMMARY.md](README_SUMMARY.md)
- 🚀 Démarrer avec Gemini? → [QUICKSTART_GEMINI.md](QUICKSTART_GEMINI.md)
- 🔧 Configurer? → [GEMINI_SETUP.md](GEMINI_SETUP.md)
- ❓ Quoi faire si ça bug? → [QUICKSTART_GEMINI.md](QUICKSTART_GEMINI.md#-dépannage)

### Pour les développeurs
- 🏗️ Architecture modular? → [ARCHITECTURE.md](ARCHITECTURE.md)
- ➕ Ajouter un nouvel outil? → [ARCHITECTURE.md](ARCHITECTURE.md#pour-les-outils)
- 📝 Écrire un prompt? → [tools/README.md](tools/README.md)
- 🧪 Tester? → Exécuter `python test_server.py`

### Pour chaque outil (documentation complète)
- load_csv: [tool_load_csv.md](tools/tool_load_csv.md)
- describe_schema: [tool_describe_schema.md](tools/tool_describe_schema.md)
- run_query: [tool_run_query.md](tools/tool_run_query.md)
- get_statistics: [tool_get_statistics.md](tools/tool_get_statistics.md)
- list_tables: [tool_list_tables.md](tools/tool_list_tables.md)

---

## ✅ Checklist de mise en place

### Setup initial
- [ ] Cloner/télécharger le projet
- [ ] Activer l'environnement venv: `.\.venv\Scripts\Activate.ps1`
- [ ] Tester: `python test_server.py` (voir ✓ TOUS LES TESTS RÉUSSIS)

### Configurer Gemini CLI
- [ ] Installer MCP: `pip install mcp`
- [ ] Créer `~/.gemini/config.json` (voir [QUICKSTART_GEMINI.md](QUICKSTART_GEMINI.md))
- [ ] Valider JSON (utiliser [jsonlint.com](https://jsonlint.com/))
- [ ] Redémarrer Gemini CLI

### Vérifier la connexion
- [ ] Lancer `gemini`
- [ ] Taper: `@data-query-builder list_tables`
- [ ] Voir: "No tables loaded yet." (ou des tables si déjà chargées)

### Utiliser
- [ ] Charger un CSV: `@data-query-builder load_csv "file.csv" "name"`
- [ ] Voir le schéma: `@data-query-builder describe_schema`
- [ ] Interroger: `@data-query-builder run_query "SELECT ..."`
- [ ] Statistiques: `@data-query-builder get_statistics "table" "column"`

---

## 🎓 Architecture modulaire expliquée

### Principe fondamental
**"Un outil = Une classe + Un fichier markdown + Un prompt système"**

```python
# Chaque outil:
class MyTool(Tool):                          # ← classe isolée
    def __init__(self, db):
        super().__init__("my_tool")          # ← charge auto le prompt
        # Auto-chargé depuis: tools/tool_my_tool.md
    
    def execute(self, **params):
        # Logique de l'outil
        pass
```

### Avantages
✓ Modularité - Facile à ajouter/modifier  
✓ Testabilité - Chaque outil testé isolément  
✓ Maintenabilité - Changement limité à 1 outil  
✓ Réutilisabilité - Classes portables  
✓ Documentation - Prompts ≠ code  

---

## 🚀 Workflow typique

```
1. Utilisateur → Gemini CLI
   "Charge employees.csv"
   
2. Gemini utilise @data-query-builder load_csv
   
3. MCP appelle run_server.py
   
4. run_server.py → ToolManager.load_csv()
   
5. ToolManager → LoadCSVTool.execute()
   
6. LoadCSVTool → sqlite_helper.load_csv_to_table()
   
7. Retour: "✓ Loaded 150 rows..."
   
8. Gemini reçoit le résultat
```

---

## 📞 Support et ressources

| Question | Réponse |
|----------|---------|
| Ça marche? | Exécutez `python test_server.py` |
| Comment configurer Gemini? | Lire [QUICKSTART_GEMINI.md](QUICKSTART_GEMINI.md) |
| Comment ajouter un outil? | Lire [ARCHITECTURE.md](ARCHITECTURE.md) |
| Qu'est ce qui s'est passé? | Lire [README_SUMMARY.md](README_SUMMARY.md) |
| Erreur lors du setup? | Lire [GEMINI_SETUP.md#dépannage](GEMINI_SETUP.md) |
| Je comprends rien | Commencez par [README_SUMMARY.md](README_SUMMARY.md) |

---

## 📈 Prochaines évolutions possibles

- [ ] Persistence des données (fichier SQLite)
- [ ] Support des transactions
- [ ] Authentification/autorisations
- [ ] Webhooks pour notifications
- [ ] Export en CSV/Excel
- [ ] Visualisation graphique des données
- [ ] Analyse prédictive (ML)
- [ ] Cache des requêtes
- [ ] Logs et audit trail

---

## 📜 Fichiers de configuration

### `.venv/` - Environnement virtuel Python
```
.venv/
├── Scripts/
│   ├── python.exe
│   ├── pip.exe
│   └── activate.ps1
└── Lib/site-packages/  ← Packages installés
```

### `mcp_config.json` - Configuration MCP
Exemple de configuration pour MCP Server.

### `.env` - Variables d'environnement
Fichier optionnel pour config environment.

---

## 🎯 Résumé rapide

| Élément | Location | Status |
|---------|----------|--------|
| Code serveur | `server.py` | ✓ Prêt |
| Outils modulaires | `tools/` | ✓ 5 outils |
| Tests | `test_server.py` | ✓ Vérifié |
| Documentation | `*.md` | ✓ Complète |
| Configuration Gemini | `~/.gemini/config.json` | ⚠️ À faire |
| Installation MCP | `pip install mcp` | ⚠️ À faire |

---

## 🎪 Démarrage ultra-rapide

```powershell
# 1. Vérifier que ça fonctionne
python test_server.py
# → Voir "✓ TOUS LES TESTS RÉUSSIS"

# 2. Installer MCP
pip install mcp

# 3. Configurer Gemini (voir QUICKSTART_GEMINI.md)
# Créer ~/.gemini/config.json

# 4. Utiliser
gemini
@data-query-builder list_tables
```

---

## 🔗 Tous les liens

**Documentation:**
- [README_SUMMARY.md](README_SUMMARY.md) - Vue d'ensemble
- [QUICKSTART_GEMINI.md](QUICKSTART_GEMINI.md) - Guide rapide
- [ARCHITECTURE.md](ARCHITECTURE.md) - Architecture détaillée
- [GEMINI_SETUP.md](GEMINI_SETUP.md) - Configuration avancée
- [TOOL_PROMPTS.md](TOOL_PROMPTS.md) - Tous les prompts

**Outils:**
- [tools/README.md](tools/README.md) - Index des outils
- [tools/tool_load_csv.md](tools/tool_load_csv.md)
- [tools/tool_describe_schema.md](tools/tool_describe_schema.md)
- [tools/tool_run_query.md](tools/tool_run_query.md)
- [tools/tool_get_statistics.md](tools/tool_get_statistics.md)
- [tools/tool_list_tables.md](tools/tool_list_tables.md)

**Code:**
- [server.py](server.py) - Serveur MCP
- [run_server.py](run_server.py) - Lanceur
- [test_server.py](test_server.py) - Tests
- [sqlite_helper.py](sqlite_helper.py) - Utilitaires DB

---

**Dernière mise à jour:** 2026-03-05

**Status:** ✅ Complètement fonctionnel et documenté
