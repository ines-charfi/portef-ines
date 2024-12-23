import random

# Définition des couleurs pour l'affichage dans le terminal
# Ces couleurs sont utilisées pour styliser les messages imprimés à l'écran
JAUNE = "\033[33m"
ROUGE = "\033[31m"
VERT = "\033[32m"
BLEU = "\033[34m"
ROSE = "\033[35m"
VIOLET = "\033[35m"
MAGENTA = "\033[35m"
RESET = "\033[0m"  # Pour réinitialiser la couleur

# Message de bienvenue affiché au début du jeu
print( ROUGE + " BIENVENUE AU TIC TAC TOE" + RESET)


# Variables globales pour suivre l'état du jeu
fin_jeu = False  # Indique si la partie est terminée
contre_bot = False  # Indique si on joue contre un bot
niveau_bot = ""  # Niveau du bot : "facile" ou "difficile"

# Fonction principale du jeu
def jouer():
    """
    Cette fonction gère le cycle complet du jeu :
    - Réinitialisation de la grille pour chaque nouvelle partie.
    - Choix du mode de jeu (contre un joueur ou un bot).
    - Gestion des tours et affichage du résultat.
    """
    global Grille, fin_jeu
    while True:
        Grille = ["-"] * 9  # Réinitialisation de la grille
        fin_jeu = False  # Réinitialisation de l'état du jeu
        choix_mode()  # Permet de choisir entre jouer contre un joueur ou un bot
        if contre_bot:  # Si on joue contre un bot, choisir le niveau
            choix_niveau_bot()  
        choix_joueur()  # Le joueur choisit s'il joue X ou O
        
        affichage_grille()  # Afficher la grille au début du jeu

        # Boucle principale du jeu
        while not fin_jeu:
            tour(joueur_actuel)  # Gérer le tour du joueur ou du bot
            verifier_fin_jeu()  # Vérifier si le jeu est terminé (gagnant ou nul)
            if not fin_jeu:
                joueur_suivant()  # Passer au joueur suivant si la partie continue
            # On affiche la grille seulement après un tour complet
            affichage_grille()

        # Demander si les joueurs veulent rejouer
        rejouer = input(f"{MAGENTA}Voulez-vous rejouer ? (o/n) : {RESET}").lower()
        if rejouer != "o":
            print(f"{VERT}Merci d'avoir joué ! À bientôt !{RESET}")
            break  # Quitter la boucle si les joueurs ne veulent plus jouer

# Fonction pour choisir le mode de jeu
def choix_mode():
    """
    Permet de choisir si on joue contre un autre joueur ou contre un bot.
    Modifie la variable globale `contre_bot` pour refléter le choix de l'utilisateur.
    
    """
    global contre_bot
    choix = input(f"{VIOLET}Voulez-vous jouer contre un bot ? (o/n) : {RESET}").lower()
    contre_bot = choix == "o"  # True si l'utilisateur choisit de jouer contre un bot

# Fonction pour choisir le niveau du bot
def choix_niveau_bot():
    """
    Permet de choisir le niveau de difficulté du bot : facile ou difficile.
    Modifie la variable globale 'niveau_bot' en fonction du choix de l'utilisateur.
    """
    global niveau_bot
    while True:
        niveau_bot = input(f"{BLEU}Choisissez le niveau du bot : facile ou difficile (f/d) : {RESET}").lower()
        if niveau_bot in ("f", "d"):
            niveau_bot = "facile" if niveau_bot == "f" else "difficile"
            print(f"{VERT}Vous avez choisi un bot {niveau_bot}.{RESET}")
            break
        else:
            print(f"{ROUGE}Entrée invalide. Veuillez choisir entre 'f'(facile) ou 'd'(difficile){RESET}")

# Fonction pour choisir le joueur initial
def choix_joueur():
    """
    Permet à l'utilisateur de choisir son symbole (X ou O).
    Si le joueur choisit X, l'autre joueur ou le bot prendra O, et vice-versa.
    """
    global joueur_actuel
    while True:
        joueur_actuel = input(f"{MAGENTA}Veuillez choisir votre signe, soit une croix (X), soit un rond (O) : {RESET}").upper()
        if joueur_actuel == 'X':
            print(f"{BLEU}Vous avez choisi X. L'autre joueur/bot prendra O.{RESET}")
            break
        elif joueur_actuel == 'O':
            print(f"{ROSE}Vous avez choisi O. L'autre joueur/bot prendra X.{RESET}")
            break
        else:
            print(f"{ROUGE}Entrée invalide. Veuillez choisir entre X et O.{RESET}")

# Fonction pour afficher la grille
def affichage_grille():
    """
    Affiche l'état actuel de la grille ainsi que les numéros de cases
    pour aider les joueurs à choisir leur position.
    """
    # ligne vide pour séparer l'affichage de la grille
    print("\n")
    print(f"{VERT}-------------{RESET}")

    for ligne_index in range(3):
        # initialisation d'une ligne vide pour construire chaque ligne
        ligne = ""
        for colonne_index in range(3):
            case_index = ligne_index * 3 + colonne_index

            # si case est vide ("-"), on affiche le numéro de la case (1 à 9)
            if Grille[case_index] == "-":
                ligne += f"| {case_index + 1} "  # +1 pour afficher les numéros de 1 à 9
            else:
                # si la case est occupée, on place le symbole (X ou O en couleur)
                ligne += f"| {colorier_case(Grille[case_index])} "

        # Ajout fin de ligne
        ligne += "|"
        print(ligne)

        # Affiche une ligne horizontale en vert pour délimiter la fin de la ligne
        print(f"{VERT}-------------{RESET}")  

    # Ligne vide pour séparer l'affichage de la grille
    print("\n")

# Fonction pour colorier les cases selon le symbole
def colorier_case(case):
    """
    Retourne la couleur associée à la case selon qu'elle soit X, O ou vide.
    """
    if case == "X":
        return f"{BLEU}{case}{RESET}"  # X en bleu
    elif case == "O":
        return f"{ROUGE}{case}{RESET}"  # O en rouge
    elif case == "-":
        return f"{MAGENTA}{case}{RESET}"  # Case vide en magenta
    else:
        return case

# Fonction pour gérer le tour du joueur ou du bot
def tour(joueur):
    """
    Gère le tour du joueur actuel :
    - Si c'est le bot, effectue un coup en fonction du niveau.
    - Si c'est un utilisateur, demande une position possible.
    """
    global contre_bot, niveau_bot
    if joueur == "O" and contre_bot:  # Si c'est le tour du bot
        print(f"{VERT}Le bot joue...{RESET}")
        if niveau_bot == "facile":
            bot_facile()
        elif niveau_bot == "difficile":
            bot_kenza_difficile()
    else:  # Si c'est le tour d'un utilisateur
        print(f"{VERT}C'est le tour du joueur : {colorier_case(joueur)}{RESET}")
        valide = False
        while not valide:
            try:
                # Demander une position entre 1 et 9
                position = int(input(f"{MAGENTA}Veuillez sélectionner une case vide sur la grille entre 1 et 9 : {RESET}")) - 1
                # Vérifier si la position est valide
                if position in range(9) and Grille[position] == "-":
                    Grille[position] = joueur
                    valide = True
                else:
                    print(f"{ROUGE}Case invalide ou déjà occupée. Veuillez réessayer.{RESET}")
            except ValueError:
                print(f"{ROUGE}Entrée invalide. Veuillez entrer un nombre entre 1 et 9.{RESET}")

# Fonction pour vérifier la fin du jeu

def verifier_fin_jeu():
    """
    Vérifie si le joueur actuel a gagné ou si la grille est pleine (match nul).
    Met fin à la partie si l'une de ces conditions est remplie.
    """
    global fin_jeu
    if coup_gagnant(joueur_actuel):  # Vérifie si le joueur actuel a une combinaison gagnante
        if contre_bot and joueur_actuel == "O":  # Si c'est le bot qui a gagné
            print(f"{ROUGE}Vous avez perdu, c'est le bot qui a gagné : {colorier_case(joueur_actuel)}{RESET}")
        else:
            print(f"{JAUNE}Félicitations ! Le joueur {colorier_case(joueur_actuel)}{JAUNE} a gagné !{RESET}")
        fin_jeu = True
    elif "-" not in Grille:  # Vérifie si toutes les cases sont remplies (match nul)
        print(f"{VERT}Match nul !{RESET}")
        fin_jeu = True


# Fonction pour vérifier si un joueur a une combinaison gagnante
def coup_gagnant(joueur):
    """
    Vérifie si un joueur a une combinaison gagnante parmi les lignes,
    colonnes ou diagonales.
    """
    combinaisons_gagnantes = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Lignes
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Colonnes
        [0, 4, 8], [2, 4, 6]  # Diagonales
    ]
    for combinaison in combinaisons_gagnantes:
        if Grille[combinaison[0]] == Grille[combinaison[1]] == Grille[combinaison[2]] == joueur:
            return True
    return False

# Fonction pour changer de joueur
def joueur_suivant():
    """
    Change le joueur actuel (X devient O et vice-versa).
    """
    global joueur_actuel
    joueur_actuel = "O" if joueur_actuel == "X" else "X"

# Fonction pour le bot facile (choisit une case au hasard)
def bot_facile():
    """
    Le bot facile choisit une case vide au hasard parmi celles disponibles.
    """
    case_disponible = [i for i, case in enumerate(Grille) if case == "-"]
    choix = random.choice(case_disponible)
    Grille[choix] = "O" #met à jour la grille après le coup du bot 
    print(f"{VERT}Le bot a choisi la case {choix + 1}.{RESET}")

# Fonction pour un bot difficile (espace réservé pour ajouter une logique avancée)
def bot_kenza_difficile():
    """
    Kenbot joue intelligemment :
    - Cherche à gagner si possible.
    - Bloque l'adversaire si nécessaire.
    - Sinon, joue sur une case libre aléatoire.
    """
    global Grille

    def trouver_meilleur_coup(joueur):
        """
        Vérifie les meilleures positions pour gagner ou bloquer.
        """
        # boucle pour parcourir toutes les combinaisons gagnantes possibles
        for combinaison in [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Lignes
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Colonnes
            [0, 4, 8], [2, 4, 6]              # Diagonales
        ]:
            # Extraire les valeurs dans la grille pour combiner
            valeurs = [Grille[i] for i in combinaison]

            # Vérifier si cette combinaison a exactement deux cases remplies par le joueur actuel et une case vide
            if valeurs.count(joueur) == 2 and valeurs.count("-") == 1:
                return combinaison[valeurs.index("-")]
        return None

    # Kenbot essaie de gagner
    coup = trouver_meilleur_coup("O")
    if coup is not None:
        Grille[coup] = "O"
        return

    # Kenbot essaie de bloquer l'adversaire
    coup = trouver_meilleur_coup("X")
    if coup is not None:
        Grille[coup] = "O"
        return

    # Sinon, joue sur une case libre aléatoire
    position_vide = [i for i, case in enumerate(Grille) if case == "-"]
    if position_vide:
        Grille[random.choice(position_vide)] = "O"


# Lancement du jeu
jouer()
