Je suis enseignant en collège / lycée en France, et l'équipe pédagogique utilise l'outil EcoleDirecte pour les notes / appréciations / messages etc (https://www.ecoledirecte.com/)

[Problem Statement]

La préparation d'un conseil de classe est extrêmement chronophage pour un professeur principal. Les bulletins de chaque élève doivent être téléchargés en navigant dans les profils élèves. Et le professeur doit préparer trois choses :
1. Une appréciation générale du trimestre pour chaque élève, basée sur les appréciations des professeurs de chaque matière et des notes observées
2. Une note de synthèse rapide qui résume les points forts / points d'amélioration de l'élève / alertes (beaucoup de retards / de travaux non rendus etc)
3. une suggestion de récompense (Blanc, encouragement, tableau d'honneur etc)
Tout cela est extrêmement long et manuel pour un professeur principal qui doit potentiellement faire cela pour plusieurs classes

[Solution envisagée]

Je cherche à développer une application web puisse se connecter à EcoleDirecte avec les identifiants du professeur, afficher les classes des enseignants, et centraliser tous les bulletins PDF de chaque élève de la classe (par trimestre) dans une seule et même fenêtre. Ces bulletins seront ensuite convertis et réogarnisés en format texte, interprété par un LLM qui générera, pour chaque élève, un résumé des 3 points mentionnés ci-dessus.

L'application devra à terme être capable de récupérer des informations supplémentaire à propos de l'élève, disponibles à d'autres "endroits" dans EcoleDirecte : retards réguliers / abscences / mots dans le carnet et communication avec les parents (carnet de correspondance), nombre de devoirs non faits ou non rendus (dans le carnet de notes)

[Persona]

Tu es CTO expert en code et infrastructure tech : tu aiguilles sur les technologies à utiliser pour créer des MVPs de produits tech. Tout en ayant en tête que l'infrastructure doit être scalable.

[Tâche]
J'implémenterai la plateforme en codant avec Claude mais avant ça, je veux être clair sur l'architecture à mettre en place. Explique moi à quoi doit ressembler cette infrastructure : elle doit être relativement minimaliste au départ, mais suffisamenet robuste pour que je puisse capitaliser dessus ensuite.
Je voudrais : 
- un schéma et la liste (et le pourquoi) des choix technologiques
- un plan de déploiement 

[Contraintes / Volume] 
- Chaque professeur a en moyenne 4 classes
- Chaque classe a environ 25 élèves.
- Hébergement : France
- Sécurité : les professeurs fournissent leurs identifiants EcoleDirecte : ces identifiants devront être chiffrés.

[Idées de fonctionnalités de l'application] 
- Authentification de l'enseignant
- Récupération de la liste des classes et des élèves
- Téléchargement des bulletins PDF (par trimestre)
- Extraction texte + structuration (matière, appréciation, note/moyenne, absences/retards si présents)
- Génération LLM des 3 sorties par élève
- UI : vue classe avec tous les élèves + export (CSV/Doc/PDF) des résultats
- Lorsque le LLM restituera l'information des bulletins dans un format csv, il n'y aura aucune interprétation du LLM, les sorties ne seront que factuelles et exactement équivalentes au contenu du bulletin. 
- Pour générer les résumés de bulletin etc, le professeur disposera d'une interface où il verra le prompt par défaut, et il / elle pourra le configurer pour changer le ton, la longueur, le vocabulaire etc.


[Limites / à creuser]
- EcoleDirecte ne dispose pas d'API officielle, elle peut être reverse engineered, mais une autre option peut être de scapper les données (ils changent très rarement de design sur leur site web)
- Plusieurs développeurs ont essayé de reverse cette api, mais je ne sais pas si leur code est toujours valide (le plus commun : https://github.com/EduWireApps/ecoledirecte-api-docs. Un moins commun : https://github.com/louislegrain/api-ecoledirecte/)



