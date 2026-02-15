# Attention : nombre imaginaire c'est 1j (ou 2j etc)


# Représentation graphique des nombres complexes

import numpy as np
import matplotlib.pyplot as plt

z1 = 1 + 2j
z2 = -2 + 1j

points = [z1, z2, z1 + z2, z1 * z2, np.conj(z1)]
labels = ['z1', 'z2', 'z1 + z2', 'z1 * z2', 'conj(z1)']
colors = ['blue', 'orange', 'green', 'red', 'purple']

plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)

for z, label, c in zip(points, labels, colors):
    plt.scatter(z.real, z.imag, color=c)
    plt.text(z.real + 0.1, z.imag, label, fontsize=10)

plt.xlabel("Partie réelle")
plt.ylabel("Partie imaginaire")
plt.grid()
plt.axis('equal')
plt.title("Opérations de base sur les complexes")
plt.show()

# Racines n-ièmes de l'unité


n_cote = input("nombre_cotes :")
coord_exp = []

for k in range(int(n_cote)):
    coord_exp.append(np.exp(2*np.pi*1j*k/int(n_cote)))

print(coord_exp)

coord_cart = [(z.real, z.imag) for z in coord_exp]
print(coord_cart)

- Puis extraire les coordonées et les mettre dans la création du polygone 
- 