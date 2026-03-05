#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lanceur pour le guide de bienvenue.
Configure le PYTHONPATH pour inclure le répertoire du projet.
"""

import sys
import os
from pathlib import Path

# Forcer UTF-8 pour les sorties
if sys.stdout.encoding != 'utf-8':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Ajouter le dossier projet au PYTHONPATH
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Importer et lancer le welcome
from scripts.welcome import main

if __name__ == "__main__":
    main()