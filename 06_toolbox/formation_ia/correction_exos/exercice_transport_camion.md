## **Correction - Exercice 18 : Transport en camion**

### **Notion**  
La masse volumique.

### **Problème posé**  
Une entreprise possède un camion pouvant transporter une masse maximale de **26 tonnes**.  
La remorque a les dimensions suivantes :  
- **Longueur** : 13,70 m  
- **Largeur** : 2,48 m  
- **Hauteur** : 2,45 m  

On donne également les **masses volumiques des bois** dans le tableau suivant :

| **Bois**           | **Masse volumique (kg/m³)** |
|--------------------|----------------------------|
| Balsa              | 140                        |
| Chêne              | 610-980                    |
| Chêne (cœur)       | 1170                       |
| Contreplaqué       | 440-880                    |
| Ébène              | 1150                       |
| Hêtre              | 800                        |
| Pin                | 500                        |
| Sapin              | 450                        |
| Teck               | 860                        |

### **Objectif**  
Déterminer si la remorque peut être chargée au maximum avec **n'importe quel bois**.

---

### **Étape 1 : Calcul du volume utile de la remorque**  
La formule pour le volume est :  

\[
V = \text{Longueur} \times \text{Largeur} \times \text{Hauteur}
\]

Substitution des valeurs :  
\[
V = 13,70 \times 2,48 \times 2,45
\]

\[
V \approx 83,1 \, \text{m}^3
\]

Le volume utile de la remorque est **83,1 m³**.

---

### **Étape 2 : Calcul de la masse pour chaque bois**  
La masse totale d'un bois est donnée par :  

\[
\text{Masse} = \text{Masse volumique} \times \text{Volume}
\]

On a :  
\[
\text{Volume} = 83,1 \, \text{m}^3
\]

La masse maximale transportable est **26 000 kg**. On calcule les masses pour chaque bois.

| **Bois**           | **Masse calculée (kg)**       | **Conclusion**          |
|--------------------|-------------------------------|-------------------------|
| **Balsa**          | \( 140 \times 83,1 = 11 634 \) | OK                     |
| **Chêne** (max)    | \( 980 \times 83,1 = 81 438 \) | Trop lourd             |
| **Chêne (cœur)**   | \( 1170 \times 83,1 = 97 227 \) | Trop lourd             |
| **Contreplaqué**   | \( 880 \times 83,1 = 73 128 \) | Trop lourd             |
| **Ébène**          | \( 1150 \times 83,1 = 95 565 \) | Trop lourd             |
| **Hêtre**          | \( 800 \times 83,1 = 66 480 \) | Trop lourd             |
| **Pin**            | \( 500 \times 83,1 = 41 550 \) | Trop lourd             |
| **Sapin**          | \( 450 \times 83,1 = 37 395 \) | Trop lourd             |
| **Teck**           | \( 860 \times 83,1 = 71 466 \) | Trop lourd             |

---

### **Étape 3 : Conclusion**  
Seul le bois **Balsa** peut être transporté dans la remorque, car sa masse totale (**11 634 kg**) est inférieure à la limite maximale de **26 000 kg**. Tous les autres bois dépassent cette limite.

---

### **Rappel des points importants :**  
1. Calculer le **volume** pour des dimensions données.  
2. Appliquer la relation entre **masse volumique**, **volume**, et **masse**.  
3. Comparer avec la masse maximale autorisée pour tirer des conclusions.
