# CSV to ICS/ICAL
## 1. Télécharger Python 
ATTENTION : la version de python doit être supérieur ou égale à 3.0  
 voir site internet : [Lien vers le site de téléchargement](https://www.python.org/downloads/windows/ "Python pour Windows")
  
    
     
### a. Téléchargement 
> Vérifier que la case Add Python to PATH  (Ajouter Python au PATH) est coché (c’est pour la suite)
![select add to path](https://datatofish.com/wp-content/uploads/2018/10/0001_add_Python_to_Path.png)
  	￼
  
### b. Téléchargement des modules :
pour lancer le programmes, il faut télécharger 2 modules complémentaires :   Pytz, qui va nous aider à gérer les fuseaux horaires, et ics qui va nous aider à transformer le calendrier dans le bon format.  
* Pour se faire, sur Windows : 
	- lancer le Powershell et entrer :
		* `pip install pytz`
		* `pip install ics`
		* `pip install tzlocal`
* sur Linux / Macos : 
	- ouvrir un terminal et entrer :
		* `python3 -m pip install pytz`
		* `python3 -m pip install ics`
		* `python3 -m pip install tzlocal`
 
   
## 2. Lancer le programme :
Pour lancer le programme, il suffit : 
* Dans le Powershell :   
taper : 
	* `cd adresseDuFichierICaler.py` (pour trouver l’adresse, cliquer sur le fichier depuis l’explorateur de fichiers + propriétés)   
puis taper :
	* `py.exe icaler.py`
* Dans l’explorateur de fichiers :
	cliquer sur le fichier `icaler.py` ou sélectionner lancer avec python, via un clique droit
	
## 3. Utilisation du programme : 
Pour utiliser le programme : 
* lancer une fois le programme tel quel :
	* Celui-ci va créer le dossier dans lequel vous devez déposer les fichiers que vous voulez transformer.
* un fois le programme lancé, placez vos fichiers à transformer, vous pouvez en mettre autant que vous voulez. Veuillez à suivre le format disponible dans le dossier Template, les fichiers doivent tout de même ètre mis au format CSV pour fonctionner.  
> Si vous mettez plusieurs fichiers comportant les mêmes personnes, pas de soucis, le fichier final de cette personne contiendra tous les créneaux de cette personne 
* récuperez les fichiers dans le dossier de sortie, puis envoyez les aux personnes concernées. celles-ci n'auront qu'à cliquer dessus pour les ajouter à leur calendrier.


