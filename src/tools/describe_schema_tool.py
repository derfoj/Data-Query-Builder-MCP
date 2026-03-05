# -*- coding: utf-8 -*-
"""Outil pour afficher le schéma de la base de données."""
import sqlite3
import sys
from pathlib import Path
from .tool_base import Tool


class DescribeSchemaTool(Tool):
    """Outil pour afficher toutes les tables et colonnes avec leurs types."""
    
    def __init__(self, db_connection: sqlite3.Connection):
        """Initialise l'outil.
        
        Args:
            db_connection: Connexion SQLite à la base de données
        """
        super().__init__("describe_schema")
        self.db = db_connection
        
        # Importer le gestionnaire de sécurité
        parent_dir = str(Path(__file__).parent.parent)
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)
        from security import security_manager
        self.security = security_manager
    
    def execute(self) -> str:
        """Affiche le schéma complet de la base de données.
        
        Returns:
            Description du schéma ou message d'erreur
        """
        try:
            # Vérifier les limites de taux
            is_allowed, error_msg = self.security.check_rate_limit("describe_schema")
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
            
            schema = []
            for table in tables:
                # Validation de sécurité du nom de table
                is_valid, error_msg = self.security.validate_table_name(table)
                if not is_valid:
                    schema.append(f"\nTable: {table} (nom invalide)")
                    continue
                
                # Obtenir les informations de colonnes de manière sécurisée
                success, error_msg, columns_info = self.security.execute_query_safely(
                    self.db, 
                    f"PRAGMA table_info(`{table}`)"
                )
                
                if not success:
                    schema.append(f"\nTable: {table} (erreur: {error_msg})")
                    continue
                
                schema.append(f"\nTable: {table}")
                for col_info in columns_info:
                    col_id, col_name, col_type, notnull, default, pk = col_info
                    nullable = "NOT NULL" if notnull else "NULL"
                    pk_marker = " PRIMARY KEY" if pk else ""
                    schema.append(f"  - {col_name} ({col_type}) {nullable}{pk_marker}")
            
            return "\n".join(schema)
        except Exception as e:
            error_msg = self.security.sanitize_error_message(str(e))
            return f"Error describing schema: {error_msg}"
    
    def __call__(self) -> str:
        """Rend l'outil appelable directement."""
        return self.execute()
