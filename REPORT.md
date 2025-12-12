**Faculté des Sciences de Sfax**  
**Enseignant :** Taher Labidi  
**Département :** Informatique — Test logiciel (Certification ISTQB)  
**Audience :** 1ère Année Ingénieur  
**Année universitaire :** 2025-2026  

# Projet : Automatisation de tests Selenium + Python

## 1. Résumé exécutif
Ce projet présente la conception, l'implémentation et l'exécution d'un ensemble de tests automatisés pour une application Web choisie (ex : site e-commerce de démonstration). L'objectif est de couvrir au moins 20 cas de tests (positifs et négatifs), de fournir 4 suites de tests (performance, cross-browser, responsive, stress) et d'appliquer des techniques avancées de test (tests aux limites, tests d'état, tests de configuration, mesures de temps de réponse). Le rapport suit les exigences du module « Test logiciel (ISTQB) ».  

Ce rapport contient : description de l'application testée, architecture du projet, stratégie de test, spécification détaillée des 20 cas de test (avec étapes et résultats), exécutions et statuts, exemples de bugs (avec modèle de ticket), résultats des suites (performance, cross-browser, responsive, stress), et annexes (commande d'exécution, setup environnemental, conversion PDF).

---

## 2. Application testée
- Nom : ExempleShop (site de démonstration e-commerce)  
- URL : https://www.exampleshop.demo  (ou URL locale fournie)  
- Fonctionnalités ciblées : page d'accueil, recherche de produit, fiche produit, ajout au panier, panier, checkout (formulaire), connexion / déconnexion, filtres et tri, responsive layout.

### 2.1 Environnement de test
- Système d'exploitation : Windows 10/11 (tests exécutés depuis VM ou poste local)  
- Langage : Python 3.10  
- Framework d'automatisation : Selenium WebDriver (Python)  
- Gestion des dépendances : `requirements.txt` (ex. selenium, pytest, pytest-html, webdriver-manager, locust)
- CI (optionnel) : GitHub Actions / GitLab CI (exécution programmée)
- Navigateurs : Chrome (stable), Firefox (ESR), Edge (stable)

### 2.2 Répertoire du projet (extrait)
- `tests/` : cas de test pytest
- `pages/` : Page Object Model (POM)
- `conftest.py` : fixtures (WebDriver, configuration, hooks pytest-html)
- `reports/` : rapports HTML et captures
- `scripts/` : scripts d'exécution et helpers

---

## 3. Stratégie de test
Objectifs : vérifier la conformité fonctionnelle, la robustesse aux entrées limites, le comportement multi-navigateurs, l'affichage responsive, et mesurer les performances basiques.

Principes appliqués :
- Page Object Model (POM) pour séparer logique de tests et éléments UI.
- Tests automatisés exécutés via `pytest` et regroupés en suites via marqueurs `@pytest.mark.performance`, `@pytest.mark.cross_browser`, `@pytest.mark.responsive`, `@pytest.mark.stress`.
- Captures d'écran et logs en cas d'échec (intégration `pytest-html`).
- Mesures simples de temps de réponse via `time.perf_counter()` autour d'actions critiques.

---

## 4. Techniques de test utilisées
- Tests basés sur les limites : saisies de champs (vitesse, longueur max/min, caractères spéciaux).  
- Tests d'état : transitions panier vide → article ajouté → checkout abandonné → retour.  
- Tests de configuration : exécution sur différents navigateurs et tailles d'écran.  
- Tests de charge basique : répétition de scénarios pour mesurer temps de réponse moyen/médian et taux d'échec.

---

## 5. Suites de tests (description et commande d'exécution)

### 5.1 Suite fonctionnelle (smoke + régression)
- Objectif : couverture des fonctions critiques (login, recherche, panier, checkout).  
- Commande : `pytest tests/test_functional.py -m "smoke or regression" --html=report.html`

### 5.2 Tests de performance (mesures simples)
- Objectif : mesurer temps de réponse des actions critiques (temps de chargement fiche produit, temps d'ajout au panier, temps de soumission du checkout).  
- Outils : pytest avec `time.perf_counter()` ou `locust` pour charges plus importantes.  
- Commande simple : `pytest tests/test_performance.py -m performance -q --html=report.html`

### 5.3 Tests cross-browser
- Objectif : vérifier compatibilité sur Chrome, Firefox, Edge.  
- Méthode : parametrisation des fixtures `browser` dans `conftest.py`.  
- Commande :
```powershell
pytest tests/test_cross_browser.py -m cross_browser -q --html=report.html
```
(ou utiliser Selenium Grid / Remote WebDriver pour paralléliser)

### 5.4 Tests responsive
- Objectif : vérifier l'affichage et les éléments clés pour différentes résolutions (desktop/tablet/mobile).  
- Résolutions exemples : 1366x768, 1024x768, 768x1024, 375x812 (iPhone X).  
- Commande :
```powershell
pytest tests/test_responsive.py -m responsive -q --html=report.html
```

### 5.5 Stress test (prototype)
- Objectif : envoyer de nombreuses actions simultanées (surtout via API ou headless) pour observer comportements.  
- Outil recommandé : `locust` pour curseur de charge, ou exécution répétée via `pytest-xdist` (par ex. `pytest -n 10` pour 10 workers).  
- Exemple avec locust : `locust -f scripts/locustfile.py --host https://www.exampleshop.demo`

---

## 6. Cas de test (20 cas de test détaillés)
Tableau résumé (ID, Title, Type, Technique, Priorité, Statut) — les cas détaillés suivent.

| ID | Titre | Type | Technique | Priorité | Statut |
|----|-------|------|----------|----------|--------|
| TC01 | Login valide | Fonctionnel (positif) | Test d'état | High | Passed |
| TC02 | Login invalide (mot de passe) | Fonctionnel (négatif) | Boundary/input | High | Passed |
| TC03 | Login champ vide | Fonctionnel (négatif) | Boundary | Medium | Passed |
| TC04 | Recherche produit existant | Fonctionnel | Transition | Medium | Passed |
| TC05 | Recherche produit non-existant | Fonctionnel (négatif) | Boundary | Low | Passed |
| TC06 | Fiche produit affichée correctement | UI/acceptance | Responsive | Medium | Passed |
| TC07 | Ajouter 1 produit au panier | Fonctionnel | Transition | High | Passed |
| TC08 | Ajouter multiples produits (quantity) | Fonctionnel | Boundary (quantité) | High | Passed |
| TC09 | Supprimer produit du panier | Fonctionnel | State | Medium | Passed |
| TC10 | Checkout sans remplir formulaire | Négatif | Boundary | High | Passed |
| TC11 | Checkout avec champs aux limites | Boundary | Boundary | High | Passed |
| TC12 | Paiement simulé (Success) | End-to-end | State | High | Passed |
| TC13 | Gestion d'erreur paiement | Négatif | State | High | Failed |
| TC14 | Tri par prix (asc) | Fonctionnel | Regression | Medium | Passed |
| TC15 | Filtre par catégorie | Fonctionnel | Regression | Medium | Passed |
| TC16 | Cross-browser: page d'accueil Chrome | Compatibilité | Config | High | Passed |
| TC17 | Cross-browser: page d'accueil Firefox | Compatibilité | Config | High | Passed |
| TC18 | Responsive mobile: header/menu visible | UI | Responsive | Medium | Passed |
| TC19 | Performance: chargement fiche produit (<2s) | Performance | Mesure temps | High | Passed |
| TC20 | Stress: 50 utilisateurs simulés - checkout | Stress | Charge | High | Failed |

> Remarque : les statuts ci-dessus sont des exemples. Lors de votre exécution, remplacez-les par les statuts réels obtenus.

### 6.1 Détail d'un cas de test (exemple TC01)
- ID : TC01  
- Titre : Login valide  
- Pré-conditions : utilisateur enregistré existant (user: `standard_user`, pwd: `secret_sauce`).  
- Étapes :
  1. Ouvrir la page d'accueil.  
  2. Cliquer sur "Login".  
  3. Saisir `standard_user` dans le champ username.  
  4. Saisir `secret_sauce` dans le champ password.  
  5. Cliquer sur "Sign in".  
- Résultat attendu : redirection vers la page produit; message de bienvenue affiché; élément "Logout" présent.  
- Résultat observé : (à remplir après exécution).  
- Statut : Passed/Failed.

(Répéter format pour chaque TC — inclure capture d'écran et logs pour chaque échec dans les annexes)

---

## 7. Exécution des tests et état (extrait d'exécution)
- Commande d'exécution complète :
```powershell
pytest -q --html=report.html --self-contained-html
```
- Exemple de sortie (résumé):
  - Total tests : 20
  - Passed : 16
  - Failed : 2
  - Skipped : 2

Ajoutez ici la table complète d'exécution par test case (ID, Start time, Duration, Statut, Screenshot path si échec).

---

## 8. Analyse des bugs / défauts trouvés
Liste des bugs critiques (exemples) :
- BUG-001 : Checkout réussi avec panier vide (voir `BUG_REPORT.md` pour ticket complet).  
- BUG-002 : Échec de paiement pour certaines cartes test (erreur 500).  

Pour chaque bug : priorité, sévérité, pas à pas pour reproduire, logs, capture d'écran, statut du ticket.

---

## 9. Recommandations & actions correctives
- Corriger la validation côté serveur du panier durant la procédure de checkout.  
- Ajouter contrôles serveur pour éviter paiement sans items.  
- Ajouter limites et validation côté client pour champs critiques (numéros, CVV).  
- Ajouter tests automatiques dans CI (exécuter smoke suite à chaque push).

---

## 10. Conclusion
Le projet montre la capacité d'automatiser des scénarios fonctionnels, de compatibilité et de performance à un niveau basique-intermédiaire. Les tests identifient des régressions et des bugs critiques ; l'intégration des rapports et captures facilite la remontée vers l'équipe de développement.

---

## Annexes
### A. Installation & Setup rapide
1. Créer un environnement virtuel :
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
2. Requirements suggérés (`requirements.txt`) :
```
selenium
pytest
pytest-html
webdriver-manager
locust
pytest-xdist
```

### B. Commandes utiles
- Lancer une suite spécifique : `pytest tests/test_functional.py -q -m regression --html=report.html`
- Lancer cross-browser (exemple) : `pytest tests/test_cross_browser.py -q -k chrome --html=report.html`
- Convertir `REPORT.md` en PDF (voir section suivante).

### C. Conversion Markdown -> PDF
Option 1 (pandoc + wkhtmltopdf / LaTeX):
```powershell
# installer pandoc (https://pandoc.org/installing.html) et wkhtmltopdf
pandoc REPORT.md -o REPORT.pdf --from markdown --pdf-engine=wkhtmltopdf
```
Option 2 (Visual Studio Code):
- Ouvrir `REPORT.md`, puis `Print to PDF` ou `Export` via l'extension Markdown PDF.

---

## 11. Points à présenter (10 min)
- 1 min : Contexte & objectif du projet
- 2 min : Architecture (POM, fixtures, outils)
- 3 min : Démos rapides (exécution d'un test, capture, rapport)
- 2 min : Résultats (statuts, bugs critiques)
- 1 min : Recommandations & conclusion

---

## 12. Fichiers fournis
- `REPORT.md` (ce fichier)
- `BUG_REPORT.md` (modèle + exemple)
- `tests/` (cas de test implémentés), `pages/`, `conftest.py`, `requirements.txt`


---

*Préparé pour : Faculté des Sciences de Sfax — Test logiciel (ISTQB) — Année 2025-2026*  
*Auteur : [Votre Nom]*
