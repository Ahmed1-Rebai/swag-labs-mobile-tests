# Guide : Créer 3 AVD pour Tests Responsive

## Objectif
Créer 3 Android Virtual Devices (AVD) avec résolutions différentes pour tester l'app sur :
1. **Petit téléphone** (4.7") → 720x1280
2. **Téléphone moyen** (6.4") → 1080x1920
3. **Grande tablette** (10") → 2560x1600

---

## Prérequis
- Android Studio installé
- SDK Android >= 11 (recommandé : SDK 30+)
- Au moins 20 GB d'espace disque libre (3 AVD × ~6GB chacun)

---

## Étape 1 : Ouvrir Android Studio AVD Manager

1. Ouvrir **Android Studio**
2. Menu → **Tools** → **Device Manager** (ou **AVD Manager** selon version)
3. Cliquer sur **Create Virtual Device** (bouton bleu "+")

---

## Étape 2 : Créer les 3 AVD

### AVD 1 : Petit Téléphone (4.7" - 720x1280)

**Étape 2.1 - Sélectionner le modèle de device**
1. Catégorie : **Phone**
2. Choisir : **Pixel 5** (4.6", 1080x2340) OU **Pixel 4a** (5.8", 1080x2300)
   - (Alternative : tout téléphone standard ~4.7")
3. Cliquer **Next**

**Étape 2.2 - Sélectionner l'image système**
1. Release Name : **Android 13** (API 33) ou **Android 14** (API 34)
2. ABI : **x86_64** (recommandé pour vitesse)
3. Cliquer **Next**

**Étape 2.3 - Configurer l'AVD**
1. AVD Name : `Pixel_4_7_Small` (ou nom de votre choix)
2. Cocher **Use Host GPU** (si disponible) pour plus de vitesse
3. Cliquer **Show Advanced Settings**
4. **Memory and Storage** :
   - RAM : 4 GB (min 2 GB)
   - VM heap : 512 MB
   - Internal Storage : 1024 MB (1 GB)
5. **Display** :
   - LCD DPI : 420 (standard)
6. Cliquer **Finish**

---

### AVD 2 : Téléphone Moyen (6.4" - 1080x1920)

**Étape 3.1 - Sélectionner le modèle**
1. Catégorie : **Phone**
2. Choisir : **Pixel 5** (5.0", 1080x2340) OU **Pixel 6** (6.1", 1440x3120)
3. Cliquer **Next**

**Étape 3.2 - Sélectionner l'image système**
1. Android 13 ou 14 (même version que AVD 1 recommandé)
2. ABI : **x86_64**
3. Cliquer **Next**

**Étape 3.3 - Configurer**
1. AVD Name : `Pixel_6_4_Medium`
2. RAM : 4 GB
3. Internal Storage : 1024 MB
4. Cliquer **Finish**

---

### AVD 3 : Grande Tablette (10" - 2560x1600)

**Étape 4.1 - Sélectionner le modèle**
1. Catégorie : **Tablet**
2. Choisir : **Pixel Tablet** (10.1", 2560x1600)
   - (Alternative : **iPad** emulation si disponible)
3. Cliquer **Next**

**Étape 4.2 - Sélectionner l'image système**
1. Android 13 ou 14
2. ABI : **x86_64**
3. Cliquer **Next**

**Étape 4.3 - Configurer**
1. AVD Name : `Pixel_Tablet_10`
2. RAM : 4 GB (voire 6 GB si disponible)
3. Internal Storage : 2048 MB (2 GB)
4. Cliquer **Finish**

---

## Étape 5 : Vérifier les AVD créés

Dans **Device Manager**, vous devriez voir :
```
✓ Pixel_4_7_Small    (4.7", 720x1280)
✓ Pixel_6_4_Medium   (6.4", 1080x1920)
✓ Pixel_Tablet_10    (10", 2560x1600)
```

---

## Étape 6 : Lancer les AVD (une seule à la fois)

### Méthode 1 : Depuis Android Studio
1. Device Manager → Cliquer le bouton **Play** (▶) à côté de l'AVD

### Méthode 2 : Depuis terminal
```powershell
# Lister les AVD disponibles
emulator -list-avds

# Lancer un AVD spécifique
emulator -avd Pixel_4_7_Small
emulator -avd Pixel_6_4_Medium
emulator -avd Pixel_Tablet_10
```

**Note** : Un seul émulateur à la fois (limitation matérielle typique).

---

## Étape 7 : Exécuter les tests responsive

Une fois l'AVD lancé et l'app installée :

```powershell
# Sur AVD 1 (petit téléphone)
pytest tests/test_responsive.py -v -k "resp01" --html=report_small.html

# Sur AVD 2 (téléphone moyen)
pytest tests/test_responsive.py -v -k "resp02" --html=report_medium.html

# Sur AVD 3 (tablette)
pytest tests/test_responsive.py -v -k "resp03" --html=report_large.html
```

---

## Étape 8 : Automatiser (optionnel)

Créer un script PowerShell `run_responsive_tests.ps1` :

```powershell
# Script pour exécuter les 3 tests sur les 3 AVD

$avds = @(
    @{name="Pixel_4_7_Small"; report="report_small.html"; desc="4.7\" Small"},
    @{name="Pixel_6_4_Medium"; report="report_medium.html"; desc="6.4\" Medium"},
    @{name="Pixel_Tablet_10"; report="report_large.html"; desc="10\" Tablet"}
)

foreach ($avd in $avds) {
    Write-Host "================================"
    Write-Host "Testing on $($avd.desc) ($($avd.name))"
    Write-Host "================================"
    
    # Lancer l'AVD
    Write-Host "Launching AVD: $($avd.name)"
    Start-Process -NoNewWindow emulator -ArgumentList "-avd $($avd.name)"
    
    # Attendre que l'émulateur soit prêt (~30-60 secondes)
    Start-Sleep -Seconds 45
    
    # Exécuter les tests
    Write-Host "Running responsive tests..."
    pytest tests/test_responsive.py -v --html=$($avd.report)
    
    # Arrêter l'émulateur
    Write-Host "Stopping emulator..."
    adb emu kill
    Start-Sleep -Seconds 5
}

Write-Host "All responsive tests completed!"
```

Exécuter :
```powershell
.\run_responsive_tests.ps1
```

---

## Conseils de performance

- **Allouer assez de RAM** : Au moins 4 GB par AVD (8 GB total recommandé)
- **Utiliser x86_64** : Plus rapide que ARM sur PC
- **Cocher GPU Hardware** : Améliore la fluidité
- **SSD obligatoire** : Sinon très lent (~30-60s de boot)
- **Un seul AVD à la fois** : Moins de consommation système

---

## Dépannage

| Problème | Solution |
|----------|----------|
| Émulateur très lent | Allouer plus de RAM, vérifier GPU hardware coché |
| Erreur "GPU not supported" | Cocher "Use Host GPU" (VM setting), ou décocher |
| Erreur "No space left" | Allouer disque interne plus petit (~1 GB) ou vérifier SSD |
| adb not found | Ajouter Android SDK tools au PATH |
| App ne s'installe pas | Vérifier AVD lancé avec `adb devices` |

---

## Fichiers générés

- `report_small.html` — Résultats test petit téléphone (4.7")
- `report_medium.html` — Résultats test téléphone moyen (6.4")
- `report_large.html` — Résultats test tablette large (10")

Chaque rapport contient :
- ✓ RESP01 : Login display
- ✓ RESP02 : Products visibility
- ✓ RESP03 : Button clickability

---

## Prochaines étapes

Après création des AVD :
1. Lancer chaque AVD manuellement dans Android Studio
2. Installer l'APK Swag Labs
3. Exécuter les tests responsive
4. Analyser les résultats dans les rapports HTML

---

*Guide créé pour : Tests Responsive (ISTQB) — Année 2025-2026*
