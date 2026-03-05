# -*- coding: utf-8 -*-
"""Classe de base pour tous les outils du serveur MCP."""
from abc import ABC, abstractmethod
from typing import Any, Dict
from .prompt_loader import load_system_prompt, get_tool_description


class Tool(ABC):
    """Classe de base abstraite pour tous les outils."""
    
    def __init__(self, name: str):
        """Initialise un outil.
        
        Args:
            name: Nom de l'outil (ex: 'load_csv', 'run_query')
        """
        self.name = name
        self.system_prompt = load_system_prompt(name)
        self.description = get_tool_description(name)
    
    @abstractmethod
    def execute(self, **kwargs) -> str:
        """Exécute l'outil avec les paramètres donnés.
        
        Args:
            **kwargs: Paramètres spécifiques à l'outil
        
        Returns:
            Résultat en tant que chaîne de caractères
        """
        pass
    
    def get_system_prompt(self) -> str:
        """Retourne le system prompt de l'outil."""
        return self.system_prompt
    
    def get_description(self) -> str:
        """Retourne la description de l'outil."""
        return self.description
