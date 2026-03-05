# MCP Data Query Builder

Un serveur MCP (Model Context Protocol) pour l'analyse de données conversationnelle avec une architecture modulaire sécurisée.

## 🚀 Démarrage rapide

### Installation
```bash
# Installer les dépendances
pip install mcp

# Lancer le serveur
python run_mcp_server.py
```

### Tests
```bash
# Lancer les tests
python run_tests.py
```

### Guide de bienvenue
```bash
# Afficher le guide complet
python welcome.py
```

## 📁 Structure du projet

```
data-query-builder/
├── src/                    # Code source
│   ├── server.py          # Serveur MCP principal
│   ├── security.py        # Gestionnaire de sécurité
│   ├── sqlite_helper.py   # Utilitaires SQLite
│   └── tools/             # Outils modulaires
│       ├── __init__.py
│       ├── tool_base.py
│       ├── prompt_loader.py
│       └── [outils individuels]
├── docs/                  # Documentation
│   ├── README_SUMMARY.md
│   ├── ARCHITECTURE.md
│   ├── SECURITY.md
│   └── ...
├── config/                # Configuration
│   ├── mcp_config.json
│   └── .env
├── data/                  # Données exemples
│   ├── sample_employees(in).csv
│   └── test_data.csv
├── tests/                 # Tests
│   └── test_server.py
├── scripts/               # Scripts utilitaires
│   └── welcome.py
├── run_mcp_server.py     # Lanceur du serveur
├── run_tests.py          # Lanceur des tests
└── welcome.py            # Guide de bienvenue
```

## 🔧 Fonctionnalités

- **Chargement CSV intelligent** avec détection automatique des types
- **Requêtes SQL sécurisées** (SELECT uniquement)
- **Analyse statistique** avancée
- **Exploration de schéma** interactive
- **Sécurité multicouche** contre les attaques communes
- **Interface MCP standard** pour intégration avec Gemini CLI

## 🛡️ Sécurité

- Validation des chemins de fichiers
- Protection contre les injections SQL
- Limites de taux (rate limiting)
- Assainissement des messages d'erreur
- Journalisation complète des opérations

## 📚 Documentation

Voir le dossier `docs/` pour la documentation complète :
- [Guide de démarrage rapide](docs/QUICKSTART_GEMINI.md)
- [Architecture technique](docs/ARCHITECTURE.md)
- [Guide de sécurité](docs/SECURITY.md)
- [Configuration Gemini](docs/GEMINI_SETUP.md)

## 🧪 Tests

```bash
# Exécuter tous les tests
python run_tests.py
```

## 🤝 Contribution

1. Le code source est dans `src/`
2. Les tests dans `tests/`
3. La documentation dans `docs/`
4. Les données d'exemple dans `data/`

## 📄 Licence

Ce projet est fourni tel quel pour démonstration des capacités MCP.