# -*- coding: utf-8 -*-
"""Outil pour charger des fichiers CSV dans la base de données."""
import sqlite3
import os
import sys
from pathlib import Path
from .tool_base import Tool


class LoadCSVTool(Tool):
    """Outil pour charger un fichier CSV dans une table SQLite."""
    
    def __init__(self, db_connection: sqlite3.Connection):
        """Initialise l'outil.
        
        Args:
            db_connection: Connexion SQLite à la base de données
        """
        super().__init__("load_csv")
        self.db = db_connection
        
        # Importer le gestionnaire de sécurité
        parent_dir = str(Path(__file__).parent.parent)
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)
        from security import security_manager
        self.security = security_manager
    
    def execute(self, file_path: str, table_name: str) -> str:
        """Charge un fichier CSV dans une nouvelle table.
        
        Args:
            file_path: Chemin vers le fichier CSV
            table_name: Nom de la table à créer
        
        Returns:
            Message de succès ou d'erreur
        """
        try:
            # Validation de sécurité: vérifier le chemin du fichier
            is_valid, error_msg = self.security.validate_file_path(file_path)
            if not is_valid:
                return f"Erreur de sécurité: {error_msg}"
            
            # Validation de sécurité: vérifier le nom de la table
            is_valid, error_msg = self.security.validate_table_name(table_name)
            if not is_valid:
                return f"Erreur de sécurité: {error_msg}"
            
            # Vérifier les limites de taux
            is_allowed, error_msg = self.security.check_rate_limit("load_csv")
            if not is_allowed:
                return f"Erreur de sécurité: {error_msg}"
            
            from ..sqlite_helper import load_csv_to_table
            result = load_csv_to_table(self.db, file_path, table_name)
            columns = ', '.join(c[0] for c in result['columns'])
            
            # Journaliser l'opération réussie
            self.security.logger.info(f"CSV chargé: {file_path} -> table '{table_name}' ({result['row_count']} lignes)")
            
            return f"✓ Loaded {result['row_count']} rows into table '{table_name}' with columns: {columns}"
        except Exception as e:
            error_msg = self.security.sanitize_error_message(str(e))
            return f"Error loading CSV: {error_msg}"
    
    def __call__(self, file_path: str, table_name: str) -> str:
        """Rend l'outil appelable directement."""
        return self.execute(file_path=file_path, table_name=table_name)
