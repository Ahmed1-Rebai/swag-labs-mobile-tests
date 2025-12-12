# Rapport de Structure de Projet de Test Automatisé

## Étudiant: [Votre Nom]
## Date: Décembre 2025
## Cours: Test Automatisé

## Objectif du Projet
Organisation et structuration d'une suite de tests automatisés pour une application mobile utilisant Appium et pytest, avec séparation par type de test et numérotation séquentielle TC1-TC57.

## Structure Organisée

### 📁 tests/
```
tests/
├── TestSuite1_Login.py          # Tests de connexion (TC1-TC7)
├── TestSuite2_Basic.py          # Tests basiques (TC8)
├── TestSuite3_Navigation.py      # Tests de navigation (TC9-TC13)
├── TestSuite4_Products.py        # Tests produits (TC14-TC36)
├── TestSuite5_Checkout.py        # Tests checkout (TC37-TC48)
├── TestSuite6_Responsive.py      # Tests responsive (TC49-TC52)
├── TestSuite7_Performance.py     # Tests performance (TC53-TC54)
└── TestSuite8_Stress.py          # Tests stress (TC55-TC57)
```

## Description des Test Suites

### Tests Fonctionnels (Functionality)
**TestSuite1_Login.py - Tests de Connexion (TC1-TC7)**
- TC1: Authentification utilisateurs acceptés
- TC2: Validation champs vides
- TC3: Gestion mot de passe incorrect
- TC4: Gestion nom utilisateur incorrect
- TC5: Test limite mot de passe vide
- TC6: Test limite nom utilisateur vide
- TC7: Test limite champs dépassant limite

**TestSuite2_Basic.py - Tests Basiques (TC8)**
- TC8: Lancement et vérification état initial application

**TestSuite3_Navigation.py - Tests de Navigation (TC9-TC13)**
- TC9: Ouverture menu latéral
- TC10: Navigation vers différentes sections
- TC11: Fonctionnalité bouton retour Android
- TC12: Changements orientation portrait/paysage
- TC13: Redémarrage application et état session

**TestSuite4_Products.py - Tests Produits (TC14-TC26)**
- TC14-TC16: Affichage et disponibilité éléments page produits
- TC17-TC20: Fonctions panier (ajouter, retirer, multiples, drag & drop)
- TC21-TC24: Navigation (panier, menu, détails produit, déconnexion)
- TC25-TC26: Tri et défilement produits

**TestSuite5_Checkout.py - Tests Checkout (TC37-TC48)**
- TC37-TC42: Tri produits et gestion panier
- TC43-TC44: Validation panier vide et checkout sans produits
- TC45-TC46: Processus achat complet et annulation
- TC47-TC48: Validation formulaire et tests utilisateur problème

### Tests Responsives (Responsive)
**TestSuite6_Responsive.py - Tests Multi-Appareils (TC49-TC52)**
- TC49: Affichage connexion téléphone petit (4.7")
- TC50: Visibilité produits téléphone moyen (6.4")
- TC51: Clic boutons tablette grande (10")
- TC52: Résumé tests responsive

### Tests Performance (Performance)
**TestSuite7_Performance.py - Tests de Performance (TC53-TC54)**
- TC53: Temps chargement page produits
- TC54: Performance chargement initial

### Tests Stress (Stress)
**TestSuite8_Stress.py - Tests de Stress (TC55-TC57)**
- TC55: Cycles ajouter/retirer produits (20 itérations)
- TC56: Cycles connexion/déconnexion (20 itérations)
- TC57: Test charge défilement rapide liste produits

## Métriques du Projet

| Catégorie | Nombre Suites | Nombre Tests | Couverture |
|-----------|---------------|--------------|------------|
| Fonctionnel | 5 | 38 | Authentification, Navigation, Produits, Checkout |
| Responsive | 1 | 4 | 3 tailles d'écran |
| Performance | 1 | 2 | Temps de réponse |
| Stress | 1 | 3 | Stabilité sous charge |
| **Total** | **8** | **47** | **Complète** |

## Technologies Utilisées
- **Framework**: pytest
- **Automatisation Mobile**: Appium
- **Langage**: Python 3.x
- **Reporting**: HTML reports
- **Marqueurs**: performance, stress, responsive

## Commandes d'Exécution

```bash
# Exécuter tous les tests
pytest

# Exécuter par catégorie
pytest tests/functionality/ -m functionality
pytest tests/responsive/ -m responsive
pytest tests/performance/ -m performance
pytest tests/stress/ -m stress

# Rapport HTML
pytest --html=reports/test_report.html
```

## Points Clés de l'Organisation

1. **Séparation par Type**: Tests regroupés logiquement par fonctionnalité
2. **Numérotation TC1-TC57**: Suite séquentielle pour présentation claire
3. **Élimination Doublons**: Tests similaires fusionnés (ex: fonctionnalités panier consolidées)
4. **Maintenabilité**: Structure claire facilitant ajouts/modifications
5. **Reporting**: Rapports HTML automatiques pour analyse résultats

## Conclusion

Cette structure organise efficacement les suites de tests automatisés selon les meilleures pratiques, permettant une maintenance facile et une exécution ciblée par type de test. La numérotation TC1-TC47 facilite la présentation et le suivi des cas de test individuels au sein des suites.