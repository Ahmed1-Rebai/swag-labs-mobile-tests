# Bug Report Template

## Informations générales
- ID : [BUG-XXXX]
- Titre : [Court et descriptif]
- Priorité : [Low/Medium/High/Critical]
- Sévérité : [Minor/Major/Critical]
- Statut : [Open/In Progress/Resolved/Closed]
- Assigné à : [Dev]
- Date découverte : [YYYY-MM-DD]

## Environnement
- URL : https://www.exampleshop.demo
- OS : Windows 10
- Navigateur : Chrome 120 / Firefox 116 / Edge 120
- Version de l'application : v1.2.3
- Version du test : branch `main`, commit `abcdef`

## Description
[Description courte du comportement observé]

## Étapes pour reproduire (Step-by-step)
1. Aller sur la page d'accueil `https://...`
2. Se connecter en tant que `standard_user` / `secret_sauce`
3. Vérifier que le panier est vide
4. Ouvrir le panier et cliquer sur `CHECKOUT`
5. Remplir le formulaire utilisateur (nom, prénom, code postal)
6. Cliquer sur `CONTINUE`
7. Observer que le bouton `FINISH` est affiché et permet de compléter le checkout malgré un panier vide

## Résultat attendu
La procédure de checkout devrait bloquer et afficher une erreur indiquant que le panier est vide. Le serveur doit empêcher la création d'une commande sans items.

## Résultat observé
Le bouton `FINISH` est accessible et la commande peut se terminer. (capture: `reports/screenshots/XXXXX.png`)

## Logs et captures d'écran
- Capture d'écran : `reports/screenshots/<nom_fichier>.png`
- Logs Appium / console : `logs/appium_YYYYMMDD.log`

## Priorisation & Remarques
- Priorité recommandée : High (blocage métier)
- Suggestion corrective : ajouter validation côté serveur au moment de la création de commande; ajouter test serveur qui refuse commande vide.

---

## Exemple de ticket (Jira)
- Project: EXSHOP
- Issue Type: Bug
- Summary: "Checkout completed with empty cart"
- Description: copier la section "Étapes pour reproduire" + logs + capture
- Labels: `checkout`, `critical`, `automated-test`


*Fin du rapport de bug*