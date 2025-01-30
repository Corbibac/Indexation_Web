TP de Clément Mounier


#  TP2 Indexation

## 0. Liste des stopwords
https://github.com/stopwords-iso/stopwords-en/blob/master/stopwords-en.txt



## 1. Structure des Index
Ce projet génère plusieurs types d'index à partir des données extraites d'un fichier JSONL contenant des informations sur des produits. Chaque index est stocké sous forme de fichier JSON dans `TP2/indexes/`.

### **Index principaux**
1. **Index inversé**
   - `title_index.json` : Associe chaque mot du titre à une liste d'URL de produits.
   - `description_index.json` : Associe chaque mot de la description à une liste d'URL de produits.

2. **Index de position**
   - `title_pos_index.json` : Stocke les positions des mots dans les titres des produits.
   - `description_pos_index.json` : Stocke les positions des mots dans les descriptions des produits.

Avec notre implémentation. On a de la redondance antre les index et pos_index. Dans les deux cas on cherche chaque mot, on les met en lien avec une liste de doccuments (l'url dans les deux cas). Dans le cas de la position, on rajoute en plus pour chaque mot, la position dans le document associé

3. **Index des avis (reviews)**
   - `reviews_index.json` : Contient le nombre total d'avis, la note moyenne et la dernière note pour chaque produit, associée à son URL. On ne vérifie pas systématiquement, mais il semble que la note la plus récente est la dernière dans la liste des reviews. (constat fait par l'exercice, mais on ne vérifie pas à chaque fois que ce soit le cas. Ce serait possible à ajouter si on a un doute)

4. **Index des caractéristiques produit**
   Chaque fichier JSON est un index inversé mappant une valeur spécifique d'un attribut produit à une liste d'URL de produits :
   - `brand_index.json` (marque)
   - `made_in_index.json` (origine du produit)
   - `flavor_index.json` (saveur)
   - `sugar_content_index.json` (taux de sucre)
   - `material_index.json` (matériau)
   - `care_instruction_index.json` (instructions d'entretien)
   - `sizes_index.json` (tailles)
   - `design_index.json` (design)
   - `colors_index.json` (couleurs)
   - `light_index.json` (éclairage)
   - `closure_index.json` (type de fermeture)
   - `comfort_index.json` (confort)
   - `purpose_index.json` (utilisation)
   - `versatility_index.json` (polyvalence)
   - `durability_index.json` (durabilité)
   - ...
    On parcourt toutes les features possibles, elles sont rangées dans leur dossier à part indexes/features

## 2. Choix d'Implémentation

### **1. Format des Index**
- Tous les index sont stockés sous forme de fichiers JSON pour garantir l'interopérabilité et la facilité d'utilisation.
- Les index inversés utilisent des dictionnaires `{mot_clé: [liste_d'URL]}`.
- Les index de position stockent `{mot_clé: {url: [positions]}}`.
- L'index des avis stocke `{url: {total_reviews, average_score, latest_score}}`.

### **2. Prétraitement des Données**
- **Tokenisation** : Suppression de la ponctuation et conversion en minuscules.
- **Suppression des Stopwords** : Utilisation d'une liste de stopwords anglais (`TP2/stopwords-en.txt`).
- **Stockage des URLs** : Au lieu d'utiliser des IDs, les index font correspondre les mots aux URLs des produits.
- **Gestion des erreurs** : Vérification de l'existence des clés avant accès pour éviter des erreurs KeyError.

### **3. Optimisation des performances**
- Utilisation de `defaultdict(list)` pour éviter de gérer manuellement les valeurs par défaut.
- Stockage des fichiers JSON après traitement pour éviter un recalcul inutile.
- Lecture ligne par ligne du fichier JSONL pour éviter une charge mémoire excessive.

## 3. Fonctionnalités Bonus

### **1. Extraction automatique des caractéristiques produit**
- Un script `extract_unique_features.py` a été ajouté pour extraire toutes les caractéristiques disponibles sans devoir les lister manuellement.

### **2. Index des caractéristiques produit étendu**
- En plus de `brand` et `made in`, plusieurs nouvelles caractéristiques ont été indexées (toutes, on récupère les différents noms des features dans `extract_features.py` ). On load une nouvelle fois le fichier jsonl, ce n'est pas optimal et on pourrait/devrait se servir une seule fois du load.

### **3. Gestion des fichiers**
- Tous les index sont sauvegardés dans `TP2/indexes/`.
- Un mécanisme d'écrasement (`overwrite=True`) permet de recréer les fichiers sans erreur. Ou justement de ne pas les réecrire au besoin.
- Gestion des erreurs en cas de fichier existant pour éviter les pertes de données accidentelles.

## 4. Utilisation
Dans `__main__.py`, mettre en commentaire la partie code TP1 si elle ne l'était pas. Renseigner `INPUT_FILE` adresse du fichier jsonl, `OUTPUT_DIR` le dossier de sortie des différents index, `FEATURES_OUTPUT_DIR` est choisi automatiquement comme un sous dossier de `OUTPUT_DIR` mais peut être changé à la main. `INPUT_STOPWORDS` l'adresse du fichier txt des stopswords à utiliser. Pour l'instant on ne le fait qu'avec un fichier texte du type un mot par ligne.
Il ne devrait plus que lancer le main (en supposant toutes les librairies nécessaires installées)

