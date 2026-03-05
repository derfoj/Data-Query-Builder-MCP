# Sécurité - Data Query Builder MCP

## Vue d'ensemble

Le serveur MCP Data Query Builder implémente plusieurs couches de sécurité pour protéger contre les attaques communes :

- **Validation des entrées** : Tous les paramètres utilisateur sont validés
- **Protection contre l'injection SQL** : Requêtes paramétrées et validation des mots-clés
- **Contrôle d'accès aux fichiers** : Validation des chemins et extensions autorisées
- **Limites de taux** : Prévention des abus par limitation des requêtes
- **Assainissement des erreurs** : Suppression des informations sensibles
- **Journalisation** : Traçabilité de toutes les opérations

## Architecture de sécurité

```
┌─────────────────────────────────────────┐
│         SecurityManager                  │
│  Gestionnaire centralisé de sécurité     │
├─────────────────────────────────────────┤
│  • validate_file_path()                  │
│  • validate_sql_query()                  │
│  • check_rate_limit()                    │
│  • sanitize_error_message()              │
│  • execute_query_safely()                │
└──────────────────┬──────────────────────┘
                   │ Utilisé par
┌──────────────────▼──────────────────────┘
│         Tous les outils                    │
│  Validation avant exécution               │
└───────────────────────────────────────────┘
```

## Protections implémentées

### 1. Validation des fichiers (load_csv)

**Objectif** : Prévenir l'accès à des fichiers non autorisés ou dangereux.

**Protections** :
- ✅ Vérification de l'existence du fichier
- ✅ Validation des extensions autorisées (`.csv`, `.txt`, `.tsv`)
- ✅ Limitation de la taille maximale (10MB)
- ✅ Vérification des permissions de lecture
- ✅ Résolution des chemins absolus pour éviter les traversées

**Exemple de rejet** :
```
Erreur de sécurité: Extension non autorisée: .exe. Extensions permises: .csv, .txt, .tsv
```

### 2. Validation SQL (run_query)

**Objectif** : Prévenir l'injection SQL et les opérations dangereuses.

**Protections** :
- ✅ Interdiction des mots-clés dangereux (`DROP`, `DELETE`, `INSERT`, etc.)
- ✅ Détection des patterns d'injection (`; DROP`, `UNION SELECT`, etc.)
- ✅ Limitation de la longueur des requêtes (10,000 caractères)
- ✅ Forçage du mode read-only (SELECT uniquement)
- ✅ Validation du paramètre `limit` (1-10,000)

**Exemple de rejet** :
```
Erreur de sécurité: Opération interdite détectée: DELETE
```

### 3. Validation des noms (tables/colonnes)

**Objectif** : Prévenir l'injection via les noms d'objets.

**Protections** :
- ✅ Caractères autorisés uniquement (lettres, chiffres, underscore)
- ✅ Longueur maximale (128 caractères)
- ✅ Éviter les mots réservés SQL
- ✅ Vérification de l'existence des tables/colonnes

**Exemple de rejet** :
```
Erreur de sécurité: Nom de table invalide. Utilisez uniquement lettres, chiffres et underscore
```

### 4. Limites de taux (Rate Limiting)

**Objectif** : Prévenir les abus et attaques par déni de service.

**Protections** :
- ✅ Maximum 60 requêtes par minute par client
- ✅ Fenêtre glissante de 60 secondes
- ✅ Nettoyage automatique des anciennes entrées

**Exemple de rejet** :
```
Erreur de sécurité: Trop de requêtes. Limite: 60 par minute
```

### 5. Assainissement des erreurs

**Objectif** : Éviter les fuites d'informations sensibles.

**Protections** :
- ✅ Suppression des chemins absolus
- ✅ Masquage des détails techniques
- ✅ Limitation de la longueur des messages
- ✅ Suppression des informations de débogage

**Avant** :
```
Error: [Errno 2] No such file or directory: 'C:\\Users\\andyl\\secret\\file.csv'
```

**Après** :
```
Error loading CSV: [Errno 2] No such file or directory: [CHEMIN_PROTEGE]
```

### 6. Exécution sécurisée des requêtes

**Objectif** : Protection contre les timeouts et erreurs inattendues.

**Protections** :
- ✅ Timeout configuré (30 secondes)
- ✅ Gestion gracieuse des erreurs SQLite
- ✅ Journalisation des opérations réussies
- ✅ Utilisation de requêtes paramétrées quand possible

## Configuration de sécurité

```python
# Dans security.py
class SecurityManager:
    # Limites configurables
    max_requests_per_minute = 60
    max_file_size = 10 * 1024 * 1024  # 10MB
    query_timeout = 30.0  # secondes
    max_query_length = 10000  # caractères

    # Extensions autorisées
    allowed_file_extensions = {'.csv', '.txt', '.tsv'}

    # Mots-clés interdits
    dangerous_sql_keywords = [
        "DROP", "DELETE", "ALTER", "INSERT", "UPDATE",
        "CREATE", "TRUNCATE", "EXEC", "EXECUTE", "MERGE",
        "BULK", "BACKUP", "RESTORE", "SHUTDOWN", "PRAGMA",
        "ATTACH", "DETACH"
    ]
```

## Journalisation

Toutes les opérations de sécurité sont journalisées :

```
2026-03-05 15:51:02,850 - mcp_security - INFO - Requête exécutée: SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'
2026-03-05 15:51:02,852 - mcp_security - INFO - Accès autorisé au fichier: test_data.csv
2026-03-05 15:51:02,855 - mcp_security - INFO - CSV chargé: test_data.csv -> table 'employees' (3 lignes)
```

## Tests de sécurité

Le système inclut des tests automatisés pour valider les protections :

```python
# Exemples de tests
def test_sql_injection_protection():
    # Devrait rejeter les tentatives d'injection
    assert "DELETE" in run_query("SELECT * FROM users; DELETE FROM users")
    assert "DROP" in run_query("SELECT * FROM users; DROP TABLE users")

def test_file_path_validation():
    # Devrait rejeter les chemins dangereux
    assert "non autorisée" in load_csv("/etc/passwd")
    assert "trop volumineux" in load_csv("huge_file.csv")  # >10MB

def test_rate_limiting():
    # Devrait limiter les requêtes fréquentes
    for i in range(70):  # Plus que la limite
        if i > 60:
            assert "Trop de requêtes" in some_operation()
```

## Recommandations d'utilisation

### Pour les développeurs
1. **Toujours utiliser les outils** plutôt que l'accès direct à la DB
2. **Valider les entrées** avant de les passer aux outils
3. **Gérer les erreurs** retournées par les outils
4. **Monitorer les logs** pour détecter les tentatives d'attaque

### Pour les administrateurs
1. **Ajuster les limites** selon l'usage prévu
2. **Monitorer les logs** régulièrement
3. **Mettre à jour** les listes de mots-clés dangereux
4. **Sauvegarder** les logs de sécurité

### Pour les utilisateurs
1. **Utiliser des noms simples** pour tables et colonnes
2. **Éviter les caractères spéciaux** dans les noms
3. **Respecter les limites** de taille de fichier
4. **Ne pas abuser** du système avec trop de requêtes

## Évolutions futures

- **Authentification** : Ajout d'un système d'authentification utilisateur
- **Autorisation** : Contrôle d'accès basé sur les rôles
- **Chiffrement** : Protection des données sensibles
- **Audit avancé** : Journalisation plus détaillée des opérations
- **Machine Learning** : Détection d'anomalies basée sur l'IA