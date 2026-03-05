# -*- coding: utf-8 -*-
"""Outil pour exécuter des requêtes SQL SELECT."""
import sqlite3
from typing import List
import sys
from pathlib import Path
from .tool_base import Tool


class RunQueryTool(Tool):
    """Outil pour exécuter des requêtes SELECT read-only."""
    
    def __init__(self, db_connection: sqlite3.Connection, query_history: List[str] = None):
        """Initialise l'outil.
        
        Args:
            db_connection: Connexion SQLite à la base de données
            query_history: Liste pour stocker l'historique des requêtes
        """
        super().__init__("run_query")
        self.db = db_connection
        self.query_history = query_history if query_history is not None else []
        
        # Importer le gestionnaire de sécurité
        parent_dir = str(Path(__file__).parent.parent)
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)
        from security import security_manager
        self.security = security_manager
    
    def execute(self, sql: str, limit: int = 50) -> str:
        """Exécute une requête SELECT read-only.
        
        Args:
            sql: Requête SQL SELECT
            limit: Nombre maximum de lignes à retourner
        
        Returns:
            Résultats de la requête ou message d'erreur
        """
        try:
            # Validation de sécurité: vérifier la requête SQL
            is_valid, error_msg = self.security.validate_sql_query(sql)
            if not is_valid:
                return f"Erreur de sécurité: {error_msg}"
            
            # Vérifier les limites de taux
            is_allowed, error_msg = self.security.check_rate_limit("run_query")
            if not is_allowed:
                return f"Erreur de sécurité: {error_msg}"
            
            # Valider le paramètre limit
            if not isinstance(limit, int) or limit < 1 or limit > 10000:
                return "Erreur de sécurité: limit doit être un entier entre 1 et 10000"
            
            # Ajouter LIMIT si absent
            sql_upper = sql.upper().strip()
            if "LIMIT" not in sql_upper:
                sql = f"{sql} LIMIT {limit}"
            
            # Exécuter la requête de manière sécurisée
            success, error_msg, rows = self.security.execute_query_safely(self.db, sql)
            if not success:
                return error_msg
            
            # Formater les résultats
            if not rows:
                result = "Aucune ligne trouvée."
            else:
                # Obtenir les noms des colonnes
                cursor = self.db.execute(sql)
                column_names = [desc[0] for desc in cursor.description]
                
                # Formater en tableau
                result_lines = []
                result_lines.append(", ".join(column_names))
                
                for row in rows:
                    formatted_row = []
                    for value in row:
                        if value is None:
                            formatted_row.append("NULL")
                        else:
                            formatted_row.append(str(value))
                    result_lines.append(", ".join(formatted_row))
                
                result = "\n".join(result_lines)
            
            # Ajouter à l'historique
            self.query_history.append(sql)
            
            return result
            
        except Exception as e:
            error_msg = self.security.sanitize_error_message(str(e))
            return f"Error executing query: {error_msg}"
    
    def __call__(self, sql: str, limit: int = 50) -> str:
        """Rend l'outil appelable directement."""
        return self.execute(sql=sql, limit=limit)
