# RSAtatoskr

## Description

Ce programme contient, via les dossier enc/ et dec/, le moyen de chiffrer ses fichiers pour les protéger lors d'un transfert. 
Exemple, en cas de vol d'une clé USB, le voleur ne pourra pas avoir accès à l'information.

## Informations

### config.json

Les deux dossiers enc/ et dec/ possèdent tous deux un fichier config.json

#### global

Les parties "global" de ces deux fichiers doivent être identique à l'exeption de "size block in" et "size block out" qui sont inversés.
Ils désignent la taille des blocs utilisé lors du chiffrement / déchiffrement.

"name" désigne le nom du programme, il est utilisé pour changer les noms des fichiers.

"step" désigne le pas entre chaque blocs à chiffrer, autrement dit, plus "step" est grand plus le programme ira vite mais moins l'information sera caché (2 est un bon compromis sauf pour les fichiers txt qui gardent uen partie de l'information en clair).

#### enc et dec

La partie "dec" contient a et b, ces nombres doivent être premier.

Leur produit donne le n de la partie "enc", ce dernier doit être compris entre 256 puissance "size block in" et 256 puissance "size block out".

Pour vous aider à les générer, il y a le programme generate_a_b_n dans le dossier other_tools/.

### Mise en place

Il faut commencer par remplir les fichiers config.json comme indiqué dans la partie précédente.

Il faut ensuite déplacer le fichier enc/ vers l'ordianteur à l'origine du déplacement des fichiers, et dec/ sur celui qui les reçoit.

Attention : Je conseil d'utiliser des configurations différentes de (a, b, n) entre le transfert de &alpha; vers &beta; et de &beta; vers &alpha;. 

### Utilisation

Les fichiers à chiffrer doivent être mis dans le dossier enc/INPUT/, leur version chiffrées seront disponible dans le dossier enc/OUTPUT/ avec un fichier info.txt, ce dernier contient l'identifiant permettant le déchiffrement, il contient aussi la clé publique (utile en cas de problème avec la génération de l'aléatoire pour pouvoir déchiffrer malgré tout).

Pour déchiffrer les fichiers, il faut suivre la même logique mais dans le dossier dec/.

### Attention nombres premiers

Mon programme se base sur l'algorithme de primalité de Rabin-Miller pour obtenir ses nombres permiers, il y a donc un risque, extrêmement faible mais pas inexistant, que mon programme se base sur un nombre qui n'est pas permier, auquel cas il se peut que l'algorithme de déchiffrement ne fonctionne pas.

## Disclaimer

Je ne saurais être tenu responsable de tout mauvais usage d'une partie ou de la totalité de mon programme.

Je ne saurais être tenu responsable d'un quelconque problème résultant de l'utilisation totale ou partielle de mon programme.