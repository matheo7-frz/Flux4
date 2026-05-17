# Flux4 - Lanceur PS4

Un lanceur desktop et frontend pour l'émulateur PS4 [shadPS4](https://github.com/shadps4-emu/shadPS4), construit avec Python et PySide6.

## Fonctionnalités

- **Gestion du Firmware** : Importer et valider les fichiers firmware PS4 (PS4UPDATE.PUP)
- **Bibliothèque de jeux** : Parcourir, organiser et lancer votre collection de jeux PS4 avec jaquettes
- **Intégration shadPS4** : Détection automatique ou configuration manuelle de shadPS4, lancement direct des jeux
- **Interface style PS4** : Thème bleu foncé inspiré de l'interface PlayStation 4
- **Panneau de paramètres** : Configurer le moteur GPU, la résolution, le mode plein écran, etc.
- **Firmware obligatoire** : Impossible de lancer un jeu sans avoir installé le firmware PS4
- **Multi-plateforme** : Fonctionne sur Windows, Linux et macOS

## Captures d'écran

Le lanceur propose un thème sombre inspiré de la PS4 avec :
- Tableau de bord avec vue d'ensemble
- Import et validation du firmware
- Grille de jeux avec jaquettes
- Panneau de paramètres complet

## Installation

### Prérequis

- Python 3.10 ou supérieur
- pip (gestionnaire de paquets Python)

### Installer depuis les sources

```bash
# Cloner le dépôt
git clone https://github.com/matheo7-frz/Flux4.git
cd Flux4

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python main.py
```

### Installer comme paquet

```bash
pip install .
ps4-emu-launcher
```

## Guide de configuration

### 1. Installer shadPS4

Le lanceur nécessite [shadPS4](https://github.com/shadps4-emu/shadPS4/releases) installé sur votre système.

- Téléchargez la dernière version depuis GitHub
- Extrayez-le dans un emplacement connu
- Le lanceur essaiera de le détecter automatiquement, ou vous pouvez définir le chemin manuellement dans les Paramètres

### 2. Importer le Firmware PS4

Le firmware PS4 est **obligatoire** pour lancer les jeux :

1. Allez dans l'onglet **Firmware**
2. Cliquez sur **Importer le Firmware (.PUP)**
3. Sélectionnez votre fichier `PS4UPDATE.PUP`
4. Le lanceur le valide et l'installe automatiquement

### 3. Ajouter des jeux

Ajoutez vos dumps de jeux PS4 à la bibliothèque :

1. Allez dans l'onglet **Bibliothèque**
2. Cliquez sur **Ajouter un jeu** pour ajouter des jeux individuellement
3. Ou cliquez sur **Scanner un dossier** pour trouver tous les jeux dans un répertoire
4. Double-cliquez sur un jeu pour le lancer

### Structure d'un dossier de jeu

Un dump de jeu PS4 valide doit contenir :
```
DossierJeu/
  eboot.bin          (exécutable principal)
  sce_sys/
    param.sfo        (métadonnées du jeu)
    icon0.png        (icône/jaquette du jeu)
```

## Configuration

Les paramètres sont stockés dans `~/.ps4-emu-launcher/config.json` et incluent :

| Paramètre | Description | Défaut |
|-----------|-------------|--------|
| Moteur GPU | Vulkan ou OpenGL | Vulkan |
| Résolution | Résolution de rendu | 1920x1080 |
| Plein écran | Lancer en plein écran | Désactivé |
| Niveau de log | Verbosité des logs de l'émulateur | Info |

## Structure du projet

```
Flux4/
├── main.py                    # Point d'entrée
├── requirements.txt           # Dépendances Python
├── setup.py                   # Installation du paquet
├── src/
│   ├── __init__.py
│   ├── main_window.py         # Fenêtre principale avec barre latérale
│   ├── styles.py              # Feuilles de style thème PS4
│   ├── core/
│   │   ├── config.py          # Gestion de la configuration
│   │   ├── firmware_manager.py # Validation et import du firmware
│   │   ├── emulator_manager.py # Intégration shadPS4
│   │   └── game_library.py    # Scan et catalogue de jeux
│   └── pages/
│       ├── home.py            # Page tableau de bord
│       ├── firmware.py        # Page gestion du firmware
│       ├── library.py         # Page bibliothèque de jeux
│       └── settings.py        # Page paramètres
```

## Licence

Licence MIT
