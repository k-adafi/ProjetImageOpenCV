import cv2
import os
import numpy as np
import _tkinter

input_filename = 'Image/lenna.png'
image = cv2.imread(input_filename)

def etiquetage_composants_connexes(image):
    # Convertir l'image en niveaux de gris si elle est en couleur
    if len(image.shape) > 2:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    # Initialiser une image pour stocker les étiquettes
    etiquettes = np.zeros_like(gray, dtype=np.uint8)
    etiquette = 1  # numéro d'étiquette initial

    # Fonction récursive DFS pour étiqueter les composants connexes
    def dfs(x, y, etiquette):
        stack = [(x, y)]

        while stack:
            cx, cy = stack.pop()

            if cx < 0 or cy < 0 or cx >= gray.shape[0] or cy >= gray.shape[1]:
                continue
            if gray[cx, cy] == 0 or etiquettes[cx, cy] > 0:
                continue

            # Étiqueter le pixel actuel
            etiquettes[cx, cy] = etiquette

            # Ajouter les voisins 4-connectés à la pile
            stack.append((cx + 1, cy))
            stack.append((cx - 1, cy))
            stack.append((cx, cy + 1))
            stack.append((cx, cy - 1))

    # Parcourir tous les pixels de l'image pour l'étiquetage
    for i in range(gray.shape[0]):
        for j in range(gray.shape[1]):
            if gray[i, j] > 0 and etiquettes[i, j] == 0:
                dfs(i, j, etiquette)
                etiquette += 1  # incrémenter l'étiquette pour le prochain composant

    return etiquettes


def sauvegarderImage():
    # Vérifier si l'image a été correctement chargée
    if image is None:
        print(f"Erreur : Impossible de charger l'image {input_filename}")
    else:
        # Afficher l'image chargée (optionnel)
        cv2.imshow('Image', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Étiquetage des composants connexes
        etiquettes = etiquetage_composants_connexes(image)

        # Définir le chemin du répertoire de sauvegarde
        image_sauvegarder = 'C:/Users/KADAFI Ben/PycharmProjects/MIAprojectOpenCV/DossierDeSauvegarde'

        # Créer le répertoire de sauvegarde s'il n'existe pas
        if not os.path.exists(image_sauvegarder):
            os.makedirs(image_sauvegarder)

        # Définir les noms des fichiers de sortie avec le chemin complet
        output_image_filename = os.path.join(image_sauvegarder, 'lennaEnregistrer.png')
        output_numpy_filename = os.path.join(image_sauvegarder, 'lennaEnregistrer.npy')

        # Sauvegarder l'image au format .png
        cv2.imwrite(output_image_filename, image)

        # Sauvegarder l'image des étiquettes pour visualisation
        cv2.imwrite(os.path.join(image_sauvegarder, 'lennaEtiquettes.png'), etiquettes)

        # Sauvegarder l'image au format numpy .npy
        np.save(output_numpy_filename, etiquettes)

        print(f"L'image a été sauvegardée sous le nom de {output_image_filename}")
        print(f"Le tableau numpy a été sauvegardé sous le nom de {output_numpy_filename}")
        print(f"Les étiquettes des composants ont été sauvegardées sous le nom de 'lennaEtiquettes.png'")

sauvegarderImage()
