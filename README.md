# photo-palourde

##COMMENT IMPORTER UN NOUVEL ALBUM ?

* **Etape 1** : vider le dossier input du dossier photopalourde sur l'ordinateur

* **Etape 2** exporter les photos de l'album en qualité maximale raisonnable dans le dossier input (1 à 3 Mo).

* **Etape 2bis** : *FACULTATIF* Pour avoir un ordre spécial des photos dans l'album, les renommer dans l'ordre alphabétique souhaité.

* **Etape 3** : ouvrir le terminal (Applications -> Terminal).
On doit se trouver dans le dossier Laura. Entrer alors la commande *cd rob_work/catadioptre* (cd = commande ; ls = liste).

* **Etape 4** : maintenant qu'on se trouve dans le même dossier que le fichier import_album.py, on peut entrer la commande *python3 import_album.py* 

Plusieurs questions vont être posées : 
- bien mettre le nom de l'album tel qu'il apparaîtra sur le site
- choisir le numéro correspondand à la photo de couverture de l'album
- et entrer la date au format MM/AAAA exemple (02/2019)

* **Etape 5** : une fois l'importation terminée, aller dans le dossier output et double cliquer sur le fichier index.html. Cela va ouvrir le site dans Firefox. Se balader sur le site pour vérifier que tout est ok avec le nouvel album.

* **Etape 6** : si tout est ok, alors on peut publier le site sur le serveur à l'aide de la commande : *scp -r ./output/* photo-palourde@carlosdisarli.all2all.org:./public/*
Un mot de passe sera demandé pour exécuter la commande. Attention il faut être connecté à internet pour pouvoir copier le site sur le serveur.


> Serveur d'hébergement :  carlosdisarli.all2all.org
> Nom d'utilisateur :      photo-palourde
> Mot de passe :           **************
> Adresse statistiques :   http://www.photo-palourde.com/stats
> URL interface gestion :  https://carlosdisarli.all2all.org:10000/


##COMMENT MODIFIER UN ALBUM ?

* **Etape 1** : si jamais il y a eu un problème avec l'importation et qu'on veut recommencer, alors supprimer le dossier du nouvel album dans le dossier output/albums. 

* **Etape 2** : dans le dossier photoparloude de l'ordinateur, ouvrir le fichier albums.csv (avec Sublime ou Textedit) et supprimer la ligne de l'album qu'on souhaite modifier. Prendre garde à bien laisser une ligne vide à la fin. 
Si malgré cela, le site est toujours cassé, alors copier le contenu de output/backup dans le dossier output, pour revenir au site tel qu'il était au début de la manip.

* **Etape 3** : recommencer tout le process d'upload d'un nouvel album.

	
##COMMENT MODIFIER LE À PROPOS ?

* Ouvrir le fichier output/a_propos.html dans sublime, et faire les modifs.
* Ouvrir le fichier templates_html/a_propos.html et faire les mêmes modifs.
# photo-palourde
