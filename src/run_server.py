#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lanceur du serveur MCP Data Query Builder.

Lance le serveur MCP en mode stdio pour communication avec les clients.
Usage:
    python run_server.py
"""
import sys
import os

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(__file__))

# Importer et lancer le serveur MCP
if __name__ == "__main__":
    try:
        from server import mcp
        
        # Le serveur FastMCP gère automatiquement la communication stdio
        # quand on appelle run() sans arguments
        mcp.run()
    except ImportError as e:
        print(f"Erreur d'importation: {e}", file=sys.stderr)
        print("Assurez-vous que tous les modules sont disponibles.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Erreur du serveur: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
