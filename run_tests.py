#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lanceur pour les tests du serveur MCP Data Query Builder.
Configure le PYTHONPATH pour inclure le dossier src/.
"""

import sys
import os
from pathlib import Path

# Ajouter le dossier src au PYTHONPATH
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

# Importer et lancer les tests
from tests.test_server import test_workflow

if __name__ == "__main__":
    test_workflow()