"""Utilitaire pour charger les prompts système depuis les fichiers markdown."""
import os
import re
from pathlib import Path


def load_system_prompt(tool_name: str) -> str:
    """Charge le system prompt d'un outil depuis son fichier markdown.
    
    Args:
        tool_name: Nom du fichier sans extension (ex: 'load_csv')
    
    Returns:
        Contenu du system prompt
    """
    tools_dir = Path(__file__).parent
    prompt_file = tools_dir / f"tool_{tool_name}.md"
    
    if not prompt_file.exists():
        return f"Tool prompt not found: {prompt_file}"
    
    with open(prompt_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extraire le System Prompt section
    match = re.search(r'## System Prompt\n(.*?)\n##', content, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    return "System prompt section not found in markdown"


def get_tool_description(tool_name: str) -> str:
    """Extrait la description d'un outil depuis son markdown.
    
    Args:
        tool_name: Nom de l'outil
    
    Returns:
        Description formatée
    """
    tools_dir = Path(__file__).parent
    prompt_file = tools_dir / f"tool_{tool_name}.md"
    
    if not prompt_file.exists():
        return ""
    
    with open(prompt_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extraire Purpose
    match = re.search(r'## Purpose\n(.*?)\n##', content, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    return ""


def get_best_practices(tool_name: str) -> str:
    """Extrait les bonnes pratiques d'un outil.
    
    Args:
        tool_name: Nom de l'outil
    
    Returns:
        Bonnes pratiques
    """
    tools_dir = Path(__file__).parent
    prompt_file = tools_dir / f"tool_{tool_name}.md"
    
    if not prompt_file.exists():
        return ""
    
    with open(prompt_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extraire Best Practices
    match = re.search(r'## Best Practices\n(.*?)(?:\n##|$)', content, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    return ""
