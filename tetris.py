import pygame
import random

pygame.init()

TAILLE = 30
COLONNES = 10
LIGNES = 20
LARGEUR = COLONNES * TAILLE
HAUTEUR = LIGNES * TAILLE

ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Tetris")

horloge = pygame.time.Clock()
police = pygame.font.SysFont("Arial", 24)

pieces = [
    ([[1, 1, 1, 1]], (0, 240, 240)),
    ([[1, 1], [1, 1]], (240, 240, 0)),
    ([[0, 1, 0], [1, 1, 1]], (180, 0, 240)),
    ([[1, 0, 0], [1, 1, 1]], (0, 80, 240)),
    ([[0, 0, 1], [1, 1, 1]], (240, 140, 0)),
    ([[1, 1, 0], [0, 1, 1]], (0, 220, 0)),
    ([[0, 1, 1], [1, 1, 0]], (240, 0, 0))
]

grille = [[None for _ in range(COLONNES)]
          for _ in range(LIGNES)]

def nouvelle_piece():
    forme, couleur = random.choice(pieces)
    return {
        "forme": [ligne[:] for ligne in forme],
        "couleur": couleur,
        "x": COLONNES // 2 - len(forme[0]) // 2,
        "y": 0
    }

def valide(piece, dx=0, dy=0, forme=None):
    forme = forme or piece["forme"]

    for y, ligne in enumerate(forme):
        for x, case in enumerate(ligne):
            if not case:
                continue

            nx = piece["x"] + x + dx
            ny = piece["y"] + y + dy

            if nx < 0 or nx >= COLONNES or ny >= LIGNES:
                return False

            if ny >= 0 and grille[ny][nx] is not None:
                return False

    return True

def fixer(piece):
    for y, ligne in enumerate(piece["forme"]):
        for x, case in enumerate(ligne):
            if case:
                nx = piece["x"] + x
                ny = piece["y"] + y

                if ny < 0:
                    return False

                grille[ny][nx] = piece["couleur"]

    return True

def effacer_lignes():
    global grille

    restantes = [
        ligne for ligne in grille
        if any(case is None for case in ligne)
    ]

    nombre = LIGNES - len(restantes)

    grille = [
        [None for _ in range(COLONNES)]
        for _ in range(nombre)
    ] + restantes

    return nombre

def dessiner_case(x, y, couleur):
    rect = pygame.Rect(
        x * TAILLE, y * TAILLE, TAILLE, TAILLE
    )
    pygame.draw.rect(ecran, couleur, rect)
    pygame.draw.rect(ecran, (35, 35, 50), rect, 1)

def dessiner(piece, score):
    ecran.fill((12, 12, 25))

    for y in range(LIGNES):
        for x in range(COLONNES):
            couleur = grille[y][x]

            if couleur:
                dessiner_case(x, y, couleur)

    for y, ligne in enumerate(piece["forme"]):
        for x, case in enumerate(ligne):
            if case:
                dessiner_case(
                    piece["x"] + x,
                    piece["y"] + y,
                    piece["couleur"]
                )

    texte = police.render(
        f"Score : {points}", True, (255, 255, 255)
    )
    ecran.blit(texte, (5, 5))

    pygame.display.flip()

piece = nouvelle_piece()
score = 0
temps_chute = 0
termine = False
jouer = True

while jouer:
    dt = horloge.tick(60)
    temps_chute += dt

    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            jouer = False

        if evenement.type == pygame.KEYDOWN and not termine:
            if evenement.key == pygame.K_LEFT:
                if valide(piece, dx=-1):
                    piece["x"] -= 1

            elif evenement.key == pygame.K_RIGHT:
                if valide(piece, dx=1):
                    piece["x"] += 1

            elif evenement.key == pygame.K_DOWN:
                if valide(piece, dy=1):
                    piece["y"] += 1

            elif evenement.key == pygame.K_UP:
                rotation = [
                    list(ligne)
                    for ligne in zip(*piece["forme"][::-1])
                ]

                if valide(piece, forme=rotation):
                    piece["forme"] = rotation

            elif evenement.key == pygame.K_SPACE:
                while valide(piece, dy=1):
                    piece["y"] += 1

                temps_chute = 1000

    if not termine and temps_chute >= 500:
        temps_chute = 0

        if valide(piece, dy=1):
            piece["y"] += 1
        else:
            if not fixer(piece):
                termine = True
            else:
                lignes_effacees = effacer_lignes()
                score += [0, 100, 300, 500, 800][lignes_effacees]
                piece = nouvelle_piece()

                if not valide(piece):
                    termine = True

    dessiner(piece, score)

    if termine:
        texte = police.render(
            "Perdu", True, (255, 80, 80)
        )
        ecran.blit(
            texte,
            (LARGEUR // 2 - texte.get_width() // 2,
             HAUTEUR // 2)
        )
        pygame.display.flip()

pygame.quit()