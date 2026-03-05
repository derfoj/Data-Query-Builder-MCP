#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Affichage du guide de bienvenue et de l'état du projet.

Usage:
    python welcome.py
"""

def print_banner():
    """Affiche la bannière de bienvenue."""
    banner = """
╔═════════════════════════════════════════════════════════════════════════════╗
║                                                                             ║
║           🎉 BIENVENUE - Data Query Builder MCP + Gemini CLI 🎉            ║
║                                                                             ║
║           Serveur MCP modulaire avec architecture complète                 ║
║           Connectez Gemini CLI pour analyser vos données SQL               ║
║           develop by NZ Systems                                             ║
║                                                                             ║
╚═════════════════════════════════════════════════════════════════════════════╝
"""
    print(banner)


def print_status():
    """Affiche l'état du projet."""
    status = """
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ✅ STATUS DU PROJET                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ✓ Architecture modulaire          → Chaque outil dans sa classe           │
│  ✓ System prompts séparés          → Fichiers markdown dédiés             │
│  ✓ 5 outils disponibles            → load_csv, run_query, etc.           │
│  ✓ Documentation complète          → 7 fichiers markdown                  │
│  ✓ Tests fonctionnels              → ✓ VÉRIFIÉS                          │
│  ✓ Prêt pour Gemini CLI            → En attente de configuration         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
"""
    print(status)


def print_quick_start():
    """Affiche le guide de démarrage rapide."""
    guide = """
┌─────────────────────────────────────────────────────────────────────────────┐
│                        🚀 DÉMARRAGE RAPIDE                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ÉTAPE 1: Vérifier que ça fonctionne (30 secondes)                         │
│  ─────────────────────────────────────────────────────                     │
│    $ python test_server.py                                                 │
│    → Voir: ✓ TOUS LES TESTS RÉUSSIS                                       │
│                                                                             │
│  ÉTAPE 2: Installer MCP (1 minute)                                         │
│  ───────────────────────────────────                                       │
│    $ pip install mcp                                                       │
│                                                                             │
│  ÉTAPE 3: Configurer Gemini CLI (5 minutes)                                │
│  ────────────────────────────────────────                                  │
│    → Lire: QUICKSTART_GEMINI.md                                            │
│    → Créer: ~/.gemini/config.json                                          │
│    → Voir le guide pour les chemins complets                               │
│                                                                             │
│  ÉTAPE 4: Utiliser Gemini CLI (en direct)                                  │
│  ──────────────────────────────────────                                    │
│    $ gemini                                                                │
│    > @data-query-builder list_tables                                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
"""
    print(guide)


def print_files():
    """Affiche la structure des fichiers."""
    files = """
┌─────────────────────────────────────────────────────────────────────────────┐
│                        📁 STRUCTURE DU PROJET                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  📚 DOCUMENTATION (Lisez dans cet ordre)                                    │
│  ├─ README_SUMMARY.md     ← COMMENCEZ ICI (2 min)                         │
│  ├─ QUICKSTART_GEMINI.md  ← Guide de config rapide (5 min)               │
│  ├─ ARCHITECTURE.md       ← Vue d'ensemble technique (10 min)            │
│  ├─ GEMINI_SETUP.md       ← Configuration avancée (si besoin)            │
│  ├─ INDEX.md              ← Cet index de navigation                       │
│  └─ TOOL_PROMPTS.md       ← Tous les prompts (référence)                 │
│                                                                             │
│  🐍 CODE                                                                    │
│  ├─ server.py             ← Serveur MCP FastMCP (5 outils)               │
│  ├─ run_server.py         ← Lanceur du serveur                           │
│  ├─ sqlite_helper.py      ← Utilitaires SQLite                           │
│  └─ mcp_config.json       ← Configuration MCP                            │
│                                                                             │
│  🧪 TESTS                                                                   │
│  ├─ test_server.py        ← Tests complets ✓ VÉRIFIÉ                     │
│  ├─ test_data.csv         ← Données de test                              │
│  └─ sample_employees.csv  ← Exemple de données                           │
│                                                                             │
│  🛠️ OUTILS (tools/)                                                        │
│  ├─ tool_base.py          ← Classe abstraite                             │
│  ├─ prompt_loader.py      ← Chargeur de prompts markdown                │
│  ├─ __init__.py           ← ToolManager (orchestrateur)                 │
│  │                                                                          │
│  ├─ load_csv_tool.py      }                                              │
│  ├─ describe_schema_tool.py}  5 outils modulaires                        │
│  ├─ run_query_tool.py      }  avec prompts séparés                       │
│  ├─ get_statistics_tool.py }                                             │
│  ├─ list_tables_tool.py    }                                             │
│  │                                                                          │
│  ├─ tool_load_csv.md       }                                             │
│  ├─ tool_describe_schema.md}  System prompts                             │
│  ├─ tool_run_query.md      }  (markdown)                                 │
│  ├─ tool_get_statistics.md }                                             │
│  ├─ tool_list_tables.md    }                                             │
│  │                                                                          │
│  └─ README.md              ← Navigation des outils                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
"""
    print(files)


def print_tools():
    """Affiche les outils disponibles."""
    tools = """
┌─────────────────────────────────────────────────────────────────────────────┐
│                        🔧 OUTILS DISPONIBLES                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1️⃣  load_csv                                                              │
│      → Charger un fichier CSV dans la base de données                     │
│      → Usage: @data-query-builder load_csv "file.csv" "table_name"       │
│      → Résultat: ✓ Loaded X rows into table 'name'                       │
│                                                                             │
│  2️⃣  describe_schema                                                       │
│      → Afficher la structure de toutes les tables                         │
│      → Usage: @data-query-builder describe_schema                        │
│      → Résultat: Table: xxx, Columns: col1 (TYPE), col2 (TYPE)...       │
│                                                                             │
│  3️⃣  run_query                                                             │
│      → Exécuter une requête SQL SELECT                                   │
│      → Usage: @data-query-builder run_query "SELECT * FROM table"        │
│      → Résultat: Données formatées en colonnes                           │
│                                                                             │
│  4️⃣  get_statistics                                                        │
│      → Obtenir des statistiques sur une colonne                          │
│      → Usage: @data-query-builder get_statistics "table" "column"        │
│      → Résultat: Count, Min, Max, Mean, Nulls                           │
│                                                                             │
│  5️⃣  list_tables                                                           │
│      → Lister toutes les tables avec leurs nombres de lignes             │
│      → Usage: @data-query-builder list_tables                            │
│      → Résultat: Tables: table1 (X rows), table2 (Y rows)...            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
"""
    print(tools)


def print_next_steps():
    """Affiche les prochaines étapes."""
    steps = """
┌─────────────────────────────────────────────────────────────────────────────┐
│                        📋 PROCHAINES ÉTAPES                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ✅ MAINTENANT:                                                             │
│     $ python test_server.py                                                │
│     → Confirm que tout fonctionne                                          │
│                                                                             │
│  ⏭️  ENSUITE:                                                               │
│     1. pip install mcp                                                     │
│     2. Lire QUICKSTART_GEMINI.md                                          │
│     3. Créer ~/.gemini/config.json                                        │
│     4. gemini                                                              │
│        @data-query-builder list_tables                                    │
│                                                                             │
│  📚 POUR EN SAVOIR PLUS:                                                    │
│     • Structure détaillée → ARCHITECTURE.md                                │
│     • Documentation outils → tools/README.md                               │
│     • Chaque outil → tools/tool_*.md                                      │
│     • Navigation → INDEX.md                                                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
"""
    print(steps)


def print_tips():
    """Affiche les conseils d'utilisation."""
    tips = """
┌─────────────────────────────────────────────────────────────────────────────┐
│                        💡 CONSEILS ET ASTUCES                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  🔍 Déboguer:                                                               │
│     • test_server.py affiche un diagnostic complet                        │
│     • Voir QUICKSTART_GEMINI.md section "Dépannage"                      │
│                                                                             │
│  📊 Utiliser les données:                                                   │
│     1. load_csv() pour importer                                           │
│     2. describe_schema() pour voir la structure                           │
│     3. list_tables() pour vérifier                                        │
│     4. run_query() pour interroger                                        │
│     5. get_statistics() pour analyser                                    │
│                                                                             │
│  🔐 Sécurité:                                                               │
│     • Requêtes SELECT uniquement (read-only)                             │
│     • Pas de modifiation de données                                      │
│     • Données en mémoire (isolation)                                      │
│                                                                             │
│  ⚡ Performance:                                                            │
│     • Max 50 lignes par défaut (ajustable)                               │
│     • Utilisez WHERE pour filtrer gros datasets                          │
│     • Index automatiques (SQLite)                                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
"""
    print(tips)


def print_support():
    """Affiche les ressources de support."""
    support = """
┌─────────────────────────────────────────────────────────────────────────────┐
│                        🎯 SUPPORT ET RESSOURCES                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Si vous avez des questions:                                              │
│                                                                             │
│  ❓ "Comment ça marche?"                                                    │
│     → Lire: README_SUMMARY.md                                             │
│                                                                             │
│  🚀 "Comment configurer Gemini?"                                            │
│     → Lire: QUICKSTART_GEMINI.md                                          │
│                                                                             │
│  🏗️ "Comment ajouter un outil?"                                            │
│     → Lire: ARCHITECTURE.md                                               │
│                                                                             │
│  ❌ "Ça ne marche pas!"                                                     │
│     → Exécuter: python test_server.py                                     │
│     → Lire: QUICKSTART_GEMINI.md (section Dépannage)                     │
│                                                                             │
│  📞 Pour aide avancée:                                                      │
│     → GEMINI_SETUP.md (configuration détaillée)                           │
│     → ARCHITECTURE.md (détails techniques)                                │
│     → tools/README.md (documentation outils)                              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
"""
    print(support)


def main():
    """Affiche tout le guide de bienvenue."""
    print_banner()
    print_status()
    print_quick_start()
    print_files()
    print_tools()
    print_next_steps()
    print_tips()
    print_support()
    
    # Footer
    footer = """
═════════════════════════════════════════════════════════════════════════════

  👉 Commencez par: python test_server.py
  
  📚 Lisez ensuite: README_SUMMARY.md
  
  🚀 Pour Gemini CLI: QUICKSTART_GEMINI.md

═════════════════════════════════════════════════════════════════════════════
"""
    print(footer)


if __name__ == "__main__":
    main()
