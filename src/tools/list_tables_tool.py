# -*- coding: utf-8 -*-
"""Outil pour lister toutes les tables avec leurs conte de lignes."""
import sqlite3
import sys
from pathlib import Path
from .tool_base import Tool


class ListTablesTool(Tool):
    """Outil pour lister toutes les tables et leurs nombres de lignes."""
    
    def __init__(self, db_connection: sqlite3.Connection):
        """Initialise l'outil.
        
        Args:
            db_connection: Connexion SQLite à la base de données
        """
        super().__init__("list_tables")
        self.db = db_connection
        
        # Importer le gestionnaire de sécurité
        parent_dir = str(Path(__file__).parent.parent)
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)
        from security import security_manager
        self.security = security_manager
    
    def execute(self) -> str:
        """Liste toutes les tables avec leurs comptes de lignes.
        
        Returns:
            Liste des tables ou message d'erreur
        """
        try:
            # Vérifier les limites de taux
            is_allowed, error_msg = self.security.check_rate_limit("list_tables")
            if not is_allowed:
                return f"Erreur de sécurité: {error_msg}"
            
            # Utiliser une requête sécurisée pour lister les tables
            success, error_msg, rows = self.security.execute_query_safely(
                self.db, 
                "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
            )
            
            if not success:
                return error_msg
            
            tables = [row[0] for row in rows]
            
            if not tables:
                return "Aucune table chargée pour le moment."
            
            result = ["Tables:"]
            for table in tables:
                # Validation de sécurité du nom de table avant de compter
                is_valid, error_msg = self.security.validate_table_name(table)
                if not is_valid:
                    result.append(f"  - {table} (nom de table invalide)")
                    continue
                
                # Compter les lignes de manière sécurisée
                success, error_msg, count_rows = self.security.execute_query_safely(
                    self.db, 
                    f"SELECT COUNT(*) FROM `{table}`"
                )
                
                if success and count_rows:
                    count = count_rows[0][0]
                    result.append(f"  - {table} ({count} lignes)")
                else:
                    result.append(f"  - {table} (erreur de comptage)")
            
            return "\n".join(result)
        except Exception as e:
            error_msg = self.security.sanitize_error_message(str(e))
            return f"Error listing tables: {error_msg}"
    
    def __call__(self) -> str:
        """Rend l'outil appelable directement."""
        return self.execute()
