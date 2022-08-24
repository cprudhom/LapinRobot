# Projet SIM-Rabbit et Lapin automate

## Projet visant à développer un automate simulant les fonctions vitales d'un lapin

Le projet Sim Rabbit vise à développer, pour les travaux pratiques de physiologie expérimentale, un automate qui simule le comportement d’un lapin vivant, en particulier les variations de sa pression artérielle, de sa diurèse*, ou encore de sa fréquence ventilatoire et cardiaque en réponse à l’injection de différentes substances ou à la stimulation nerveuse.

À terme, le but du projet est la construction d'un lapin automate, prêt à l’emploi pour les futurs travaux pratiques vétérinaires. Le lapin sera accompagné d’une interface logicielle sur laquelle les étudiants pourront injecter numériquement des doses de substance dans le lapin et observer les tracés de la réponse du lapin aux différentes injections. Le lapin automate devra avoir des réactions réalistes en fonction des injections.

Les fonctions vitales sont constituées du rythme cardiaque, de la fréquence respiratoire et d’un signal sonore répétitif représentatif de la diurèse. Ils seront glissés dans un lapin en silicone pour permettre un gonflement des poumons et les vibrations du cœur. L’électronique permettant le pilotage sera déplacée et cachée pour avoir un final plus réaliste.


# Contenu du GitHub 

Le Github est composé de 5 dossiers : 

- Le dossier "Code Arduino" comprends le code "AutoConst_Rabbit" qui doit être compilier et transverser dans la carte Arduino avec le logiciel Arduino

- Toute l'application en Python se trouve dans le dossier "LapinRobot", nous avons utilisez le logiciel PyCharm pour le developper.
Pour accéder au codes et effectuer des modifications ou exécuter ouvrir le projet complet dans PyCharm et lancer le fichier "app"
Un fichier requirements détail les versions des logiciels et librairie utilisés pour assuré la portabilité du projet

- Dans le dossier "Documents diverses" vous trouverez la thèse de Marie Chevalier et le rapport de stage de Cassandra Barbey ainsi que des rapports d'ancien étudiants ingénieur ayant travaillé sur le projet. 

- Vous pouvez trouver les TP de physiologie dans lesquelles le projet s'insère.

- Un fichier type contenant les données d'un spécimen de type cardio_respi

Une vidéo d'une première démonstration du projet ainsi qu'une vidéo récente montrant les derniers avancements


# Lapin automate

## Fichiers de données
On considère deux types donnée: cardio-respiratoire et cardio-rénale.
Les tracés issus d'un séance de travaux pratiques sont classés par année puis par *nom* de la séance.
Par exemple: `Data_2016/BlancheNeige`.

Une séance de TP est découpée en plusieurs fichiers de texte, un par séquence.
Chaque fichier porte le nom de la séquence et est compressé au format lzma.
Le séparateur est la tabulation (`\t`).
Une séquence correspond à un état de l'animal et reporte l'évolution de différentes constantes au cours du temps.
Les constantes observées différent d'un type de TP à l'autre.
Par exemple, un fichier nommé `Sansinjection.txt.lzma` est un fichier compressé décrivant
différentes constantes alors que l'animal n'a encore subit aucune injection.
A l'inverse, `Adrenaline.txt.lzma` reporte l'évolution, avec le temps, des différentes constantes enregistrées suite à l'injection d'adrenalyne.

### Cardio réspiratoire
Les fichiers se trouvent dans `./public/data/Cardio_Respi/` et sont classés en sous-dossiers.

Les fichiers de ce dossier ont le format suivant et doivent être mise en forme pour être utilisé dans le logiciel :

```txt
Time        PA          SP  PA moy.     FC          FR
1350,05     1280,039    0   1169,866    154,7285    20,66807
1350,051    1280,039    0   1169,866    154,7285    20,66807
1350,052    1280,039    0   1169,866    154,7285    20,66807
...
```
L'en-tête doit être présente mais est ignoré lors du chargement du fichier.
Les colonnes sont les suivantes:
- `Time` : horodatage de la ligne (il y a une ligne toutes les 5ms).
- `PA` : Pression Artérielle
- `SP` : Spirometrie
- `PA moy.` : PA moyenne
- `FC` : Fréquence Cardiaque 
- `FR` : Fréquence Respiratoire


### Cardio rénale
Les fichiers se trouvent dans `./public/data/Cardio_Respi/` et sont classés en sous-dossiers.

Par convention, les fichiers de ce dossier ont le format suivant:

```txt
Diurese	Blood Pressure	Heart Rate
1108.89	86.1572	166.667
1083.37	86.145	166.667
1100.83	86.1572	166.667
1065.8	86.1694	166.667
...
```


## Conditions pour ajouter un fichier dans le dossier `data` 

### Cardio_Respi
#### Pré-requis

1. Le fichier doit être nommé selon la séquence qu'il reporte suivi de l'extension `.txt`. 
*p-ex:* `Adrenaline.txt`

2. Son contenu doit respecter le format suivant:
    + 4 colonnes, dans l'ordre: 
        - CH1 spirométrie (amplitude ventilation) 
        - CH2 PA
        - CH40 Fréquence ventilatoire
        - CH41 Fréquence cardiaque 
    + les intitulés importent peu, ils seront ignorés, la lecture se basant sur l'ordre
    + chaque élement d'une ligne est séparé du suivant par une tabulation (`\t`) 
    + chaque ligne se termine par un retour chariot (`\n`)  

3. Le fichier texte est compréssé au format lzma: 
```bash 
$> lzma fichier.txt`
```
Ou pour convertir plusieurs fichiers en une commande:
```bash
for f in `find . -name "*.txt"`; do lzma $f; done
```

**Attention:**
il arrive parfois qu'un fichier ait été édité sous Windows et comporte des caractères `^M` en fin de ligne.
Pour éviter que certains éditeurs affichent ces valeurs, il convient de les supprimer:
```bash
cat fichier.txt | tr -d '\r' > fichier.txt
```




##### Exemple de contenu
```txt
CH1	CH2	CH40	CH41
-0.0167847	62.4634	19.0779	142.857
0.00152588	62.2559	19.0779	142.857
0.00915527	62.1216	19.0779	142.857
0.00305176	62.0972	19.0779	142.857
...
```    

### Cardio_Renale

Mise en forme de la même manière que Cardio_Respi 

Son contenu doit respecter le format suivant:
    + 3 colonnes, dans l'ordre: 
        - Diurese (volume des urines émises) 
        - Blood Pressure (Pression sanguine)
        - Heart Rate (rythme cardiaque)
    + les intitulés importent peu, ils seront ignorés, la lecture se basant sur l'ordre
    + chaque élement d'une ligne est séparé du suivant par une tabulation (`\t`) 
    + chaque ligne se termine par un retour chariot (`\n`)  
    
    
##### Exemple de contenu
```txt
Diurese	Blood Pressure	Heart Rate
89.7217	30.896	169.014
83.8623	30.8838	169.014
89.8438	30.835	169.014
83.8623	30.7495	169.014
...
```      



#### Dépôt

1. Créer si nécessaire le sous-dossier correspondant à l'année du TP suivi de son nom. 
*p-ex:* `Data_2016/BlancheNeige`
2. Déposer le fichier dans le dossier, et l'ajouter à `git`




