# -*- coding: utf-8 -*-
"""
Module de sécurité pour le serveur MCP Data Query Builder.
Implémente les protections contre les attaques communes.
"""

import os
import re
import time
import logging
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import sqlite3


class SecurityManager:
    """Gestionnaire centralisé de la sécurité."""

    def __init__(self):
        self.logger = logging.getLogger("mcp_security")
        self.logger.setLevel(logging.INFO)

        # Créer le handler si pas déjà présent
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        # Limites de taux (rate limiting)
        self.rate_limits: Dict[str, List[float]] = {}
        self.max_requests_per_minute = 60

        # Mots-clés SQL dangereux
        self.dangerous_sql_keywords = [
            "DROP", "DELETE", "ALTER", "INSERT", "UPDATE", "CREATE",
            "TRUNCATE", "EXEC", "EXECUTE", "MERGE", "BULK", "BACKUP",
            "RESTORE", "SHUTDOWN", "PRAGMA", "ATTACH", "DETACH"
        ]

        # Extensions de fichiers autorisées
        self.allowed_file_extensions = {'.csv', '.txt', '.tsv'}

        # Taille maximale des fichiers (10MB)
        self.max_file_size = 10 * 1024 * 1024

        # Délai d'expiration des requêtes (30 secondes)
        self.query_timeout = 30.0

    def validate_file_path(self, file_path: str) -> Tuple[bool, str]:
        """
        Valide un chemin de fichier pour la sécurité.

        Args:
            file_path: Chemin du fichier à valider

        Returns:
            Tuple (is_valid, error_message)
        """
        try:
            path = Path(file_path).resolve()

            # Vérifier que le fichier existe
            if not path.exists():
                return False, f"Fichier non trouvé: {file_path}"

            # Vérifier que c'est un fichier (pas un répertoire)
            if not path.is_file():
                return False, f"Chemin n'est pas un fichier: {file_path}"

            # Vérifier l'extension
            if path.suffix.lower() not in self.allowed_file_extensions:
                return False, f"Extension non autorisée: {path.suffix}. Extensions permises: {', '.join(self.allowed_file_extensions)}"

            # Vérifier la taille du fichier
            file_size = path.stat().st_size
            if file_size > self.max_file_size:
                return False, f"Fichier trop volumineux: {file_size} bytes (max: {self.max_file_size})"

            # Vérifier que le fichier est lisible
            if not os.access(path, os.R_OK):
                return False, f"Permissions insuffisantes pour lire: {file_path}"

            # Journaliser l'accès
            self.logger.info(f"Accès autorisé au fichier: {file_path}")

            return True, ""

        except Exception as e:
            return False, f"Erreur de validation du fichier: {str(e)}"

    def validate_sql_query(self, sql: str) -> Tuple[bool, str]:
        """
        Valide une requête SQL pour la sécurité.

        Args:
            sql: Requête SQL à valider

        Returns:
            Tuple (is_valid, error_message)
        """
        try:
            sql_upper = sql.upper().strip()

            # Vérifier que c'est une requête SELECT
            if not sql_upper.startswith("SELECT"):
                return False, "Seules les requêtes SELECT sont autorisées"

            # Vérifier les mots-clés dangereux
            for keyword in self.dangerous_sql_keywords:
                if keyword in sql_upper:
                    return False, f"Opération interdite détectée: {keyword}"

            # Vérifier les injections SQL communes
            suspicious_patterns = [
                r';\s*(DROP|DELETE|INSERT|UPDATE|ALTER)',  # Point-virgule suivi d'opération dangereuse
                r'/\*.*?\*/',  # Commentaires multi-lignes (potentiels pour obfuscation)
                r'--.*?(DROP|DELETE|INSERT|UPDATE|ALTER)',  # Commentaires ligne
                r'UNION\s+SELECT.*--',  # UNION attacks
                r';\s*EXEC',  # Exec commands
            ]

            for pattern in suspicious_patterns:
                if re.search(pattern, sql_upper, re.IGNORECASE):
                    return False, "Motif SQL suspect détecté"

            # Vérifier la longueur raisonnable
            if len(sql) > 10000:
                return False, "Requête trop longue (max 10000 caractères)"

            return True, ""

        except Exception as e:
            return False, f"Erreur de validation SQL: {str(e)}"

    def check_rate_limit(self, client_id: str = "default") -> Tuple[bool, str]:
        """
        Vérifie les limites de taux pour éviter les abus.

        Args:
            client_id: Identifiant du client

        Returns:
            Tuple (is_allowed, error_message)
        """
        now = time.time()

        if client_id not in self.rate_limits:
            self.rate_limits[client_id] = []

        # Nettoyer les anciennes entrées (plus de 1 minute)
        self.rate_limits[client_id] = [
            timestamp for timestamp in self.rate_limits[client_id]
            if now - timestamp < 60
        ]

        # Vérifier la limite
        if len(self.rate_limits[client_id]) >= self.max_requests_per_minute:
            return False, f"Trop de requêtes. Limite: {self.max_requests_per_minute} par minute"

        # Ajouter cette requête
        self.rate_limits[client_id].append(now)

        return True, ""

    def sanitize_error_message(self, error: str) -> str:
        """
        Assainit les messages d'erreur pour éviter les fuites d'informations.

        Args:
            error: Message d'erreur original

        Returns:
            Message d'erreur assaini
        """
        # Supprimer les chemins absolus
        error = re.sub(r'[A-Za-z]:\\[^\'"\s]*', '[CHEMIN_PROTEGE]', error)
        error = re.sub(r'/[^\'"\s]*', '[CHEMIN_PROTEGE]', error)

        # Supprimer les détails techniques sensibles
        error = re.sub(r'(sqlite3\.|sqlalchemy\.|pymysql\.)[^\s\'"]*', '[DETAIL_PROTEGE]', error)

        # Limiter la longueur
        if len(error) > 500:
            error = error[:500] + "..."

        return error

    def execute_query_safely(self, db: sqlite3.Connection, sql: str, timeout: float = None) -> Tuple[bool, str, Optional[List]]:
        """
        Exécute une requête SQL de manière sécurisée.

        Args:
            db: Connexion à la base de données
            sql: Requête SQL
            timeout: Timeout optionnel

        Returns:
            Tuple (success, error_message, results)
        """
        timeout = timeout or self.query_timeout

        try:
            # Configurer le timeout
            db.execute(f"PRAGMA busy_timeout = {int(timeout * 1000)}")

            cursor = db.execute(sql)
            results = cursor.fetchall()

            # Journaliser la requête réussie
            self.logger.info(f"Requête exécutée: {sql[:100]}{'...' if len(sql) > 100 else ''}")

            return True, "", results

        except sqlite3.OperationalError as e:
            error_msg = self.sanitize_error_message(f"Erreur opérationnelle: {str(e)}")
            self.logger.warning(f"Erreur SQL: {error_msg}")
            return False, error_msg, None

        except Exception as e:
            error_msg = self.sanitize_error_message(f"Erreur inattendue: {str(e)}")
            self.logger.error(f"Erreur critique: {error_msg}")
            return False, error_msg, None

    def validate_table_name(self, table_name: str) -> Tuple[bool, str]:
        """
        Valide un nom de table.

        Args:
            table_name: Nom de la table à valider

        Returns:
            Tuple (is_valid, error_message)
        """
        # Vérifier les caractères autorisés (lettres, chiffres, underscore)
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', table_name):
            return False, "Nom de table invalide. Utilisez uniquement lettres, chiffres et underscore"

        # Vérifier la longueur
        if len(table_name) > 128:
            return False, "Nom de table trop long (max 128 caractères)"

        # Éviter les mots réservés SQL
        reserved_words = ["SELECT", "FROM", "WHERE", "INSERT", "UPDATE", "DELETE", "DROP", "CREATE", "ALTER", "TABLE"]
        if table_name.upper() in reserved_words:
            return False, f"Nom de table réservé: {table_name}"

        return True, ""

    def validate_column_name(self, column_name: str) -> Tuple[bool, str]:
        """
        Valide un nom de colonne.

        Args:
            column_name: Nom de la colonne à valider

        Returns:
            Tuple (is_valid, error_message)
        """
        # Même règles que pour les tables
        return self.validate_table_name(column_name)


# Instance globale du gestionnaire de sécurité
security_manager = SecurityManager()