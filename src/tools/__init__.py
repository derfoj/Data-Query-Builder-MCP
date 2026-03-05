"""Initialisation du module tools - architecture modulaire."""
import sqlite3
from typing import Dict, List
from .load_csv_tool import LoadCSVTool
from .describe_schema_tool import DescribeSchemaTool
from .run_query_tool import RunQueryTool
from .get_statistics_tool import GetStatisticsTool
from .list_tables_tool import ListTablesTool


class ToolManager:
    """Gestionnaire centralisé de tous les outils."""
    
    def __init__(self, db_connection: sqlite3.Connection):
        """Initialise tous les outils avec la même connexion DB.
        
        Args:
            db_connection: Connexion SQLite partagée
        """
        self.db = db_connection
        self.query_history: List[str] = []
        
        # Initialiser tous les outils
        self.load_csv = LoadCSVTool(self.db)
        self.describe_schema = DescribeSchemaTool(self.db)
        self.run_query = RunQueryTool(self.db, self.query_history)
        self.get_statistics = GetStatisticsTool(self.db)
        self.list_tables = ListTablesTool(self.db)
    
    def get_all_tools(self) -> Dict:
        """Retourne tous les outils en tant que dictionnaire.
        
        Returns:
            Dictionnaire {nom: outil}
        """
        return {
            "load_csv": self.load_csv,
            "describe_schema": self.describe_schema,
            "run_query": self.run_query,
            "get_statistics": self.get_statistics,
            "list_tables": self.list_tables,
        }
    
    def get_tool(self, name: str):
        """Récupère un outil spécifique par nom.
        
        Args:
            name: Nom de l'outil
        
        Returns:
            L'outil demandé ou None
        """
        tools = self.get_all_tools()
        return tools.get(name)
    
    def get_query_history(self) -> List[str]:
        """Retourne l'historique des requêtes exécutées.
        
        Returns:
            Liste des requêtes
        """
        return self.query_history


__all__ = [
    "ToolManager",
    "LoadCSVTool",
    "DescribeSchemaTool",
    "RunQueryTool",
    "GetStatisticsTool",
    "ListTablesTool",
]
