# -*- coding: utf-8 -*-
"""Outil pour obtenir des statistiques sur une colonne."""
import sqlite3
import sys
from pathlib import Path
from .tool_base import Tool


class GetStatisticsTool(Tool):
    """Outil pour calculer des statistiques résumées d'une colonne."""
    
    def __init__(self, db_connection: sqlite3.Connection):
        """Initialise l'outil.
        
        Args:
            db_connection: Connexion SQLite à la base de données
        """
        super().__init__("get_statistics")
        self.db = db_connection
        
        # Importer le gestionnaire de sécurité
        parent_dir = str(Path(__file__).parent.parent)
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)
        from security import security_manager
        self.security = security_manager
    
    def execute(self, table_name: str, column: str) -> str:
        """Calcule les statistiques d'une colonne.
        
        Args:
            table_name: Nom de la table
            column: Nom de la colonne
        
        Returns:
            Statistiques formatées ou message d'erreur
        """
        try:
            # Validation de sécurité: vérifier le nom de la table
            is_valid, error_msg = self.security.validate_table_name(table_name)
            if not is_valid:
                return f"Erreur de sécurité: {error_msg}"
            
            # Validation de sécurité: vérifier le nom de la colonne
            is_valid, error_msg = self.security.validate_column_name(column)
            if not is_valid:
                return f"Erreur de sécurité: {error_msg}"
            
            # Vérifier les limites de taux
            is_allowed, error_msg = self.security.check_rate_limit("get_statistics")
            if not is_allowed:
                return f"Erreur de sécurité: {error_msg}"
            
            # Vérifier que la table existe
            cursor = self.db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
            if not cursor.fetchone():
                return f"Erreur de sécurité: Table '{table_name}' n'existe pas"
            
            # Vérifier que la colonne existe dans la table
            cursor = self.db.execute(f"PRAGMA table_info({table_name})")
            columns_info = cursor.fetchall()
            column_names = [col[1] for col in columns_info]
            
            if column not in column_names:
                return f"Erreur de sécurité: Colonne '{column}' n'existe pas dans la table '{table_name}'"
            
            # Utiliser des requêtes paramétrées pour éviter l'injection SQL
            query = """
            SELECT
                COUNT(*) as total,
                COUNT(?) as non_null,
                COUNT(*) - COUNT(?) as nulls,
                MIN(?) as min_val,
                MAX(?) as max_val,
                AVG(CAST(? AS REAL)) as mean_val
            FROM ?
            """
            
            # Exécuter la requête de manière sécurisée
            success, error_msg, rows = self.security.execute_query_safely(
                self.db, 
                f"SELECT COUNT(*) as total, COUNT(`{column}`) as non_null, COUNT(*) - COUNT(`{column}`) as nulls, MIN(`{column}`) as min_val, MAX(`{column}`) as max_val, AVG(CAST(`{column}` AS REAL)) as mean_val FROM `{table_name}`"
            )
            
            if not success:
                return error_msg
            
            if not rows:
                return "Aucune donnée trouvée."
            
            row = rows[0]
            total, non_null, nulls, min_val, max_val, mean_val = row
            mean_display = f"{mean_val:.2f}" if mean_val is not None else "N/A"
            
            stats = f"""Statistics for {table_name}.{column}:
  Total rows: {total}
  Non-null: {non_null}
  Nulls: {nulls}
  Min: {min_val}
  Max: {max_val}
  Mean: {mean_display}"""
            
            return stats
        except Exception as e:
            error_msg = self.security.sanitize_error_message(str(e))
            return f"Error computing statistics: {error_msg}"
    
    def __call__(self, table_name: str, column: str) -> str:
        """Rend l'outil appelable directement."""
        return self.execute(table_name=table_name, column=column)
