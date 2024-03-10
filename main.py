import pygame
import sys
from tree import BTreeNode, display_tree
from hashing import CryptographicHash, HashTable, ExtendableHashing

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tree Visualization")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Fonts
font = pygame.font.SysFont(None, 40)
small_font = pygame.font.SysFont(None, 25)

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def choix_type():
    screen.fill(WHITE)
    draw_text("Choix du type de structure", font, BLACK, WIDTH // 2, HEIGHT // 4)

    # Draw buttons
    button_width, button_height = 200, 50
    hash_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, button_width, button_height)
    index_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, button_width, button_height)

    pygame.draw.rect(screen, BLUE, hash_button)
    pygame.draw.rect(screen, BLUE, index_button)

    draw_text("Hachage", font, WHITE, WIDTH // 2, HEIGHT // 2 - 25)
    draw_text("Indexation", font, WHITE, WIDTH // 2, HEIGHT // 2 + 75)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if hash_button.collidepoint(mouse_pos):
                    return 'hachage'
                elif index_button.collidepoint(mouse_pos):
                    return 'indexation'

def choix_arbre():
    screen.fill(WHITE)
    draw_text("Choix de l'arbre", font, BLACK, WIDTH // 2, HEIGHT // 4)

    # Draw buttons
    button_width, button_height = 200, 50
    btree_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, button_width, button_height)
    bplus_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, button_width, button_height)

    pygame.draw.rect(screen, BLUE, btree_button)
    pygame.draw.rect(screen, BLUE, bplus_button)

    draw_text("B Tree", font, WHITE, WIDTH // 2, HEIGHT // 2 - 25)
    draw_text("B+ Tree", font, WHITE, WIDTH // 2, HEIGHT // 2 + 75)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if btree_button.collidepoint(mouse_pos):
                    return 'btree'
                elif bplus_button.collidepoint(mouse_pos):
                    return 'bplus'

def hachage_level():
    screen.fill(WHITE)
    draw_text("Niveau Hachage", font, BLACK, WIDTH // 2, HEIGHT // 2)
    back_button = pygame.Rect(50, 50, 100, 50)
    pygame.draw.rect(screen, GREEN, back_button)
    draw_text("Retour", small_font, WHITE, 100, 75)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_button.collidepoint(mouse_pos):
                    return

def indexation_level():
    screen.fill(WHITE)
    draw_text("Niveau Indexation", font, BLACK, WIDTH // 2, HEIGHT // 2)

    # Choose between B-tree and B+ tree
    tree_choice = choix_arbre()

    # Display the chosen tree interface
    if tree_choice == 'btree':
        # Display interface for B-tree
        b_tree_level()
    elif tree_choice == 'bplus':
        # Display interface for B+ tree
        bplus_tree_level()

    # Add a back button
    back_button = pygame.Rect(50, 50, 100, 50)
    pygame.draw.rect(screen, GREEN, back_button)
    draw_text("Retour", small_font, WHITE, 100, 75)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_button.collidepoint(mouse_pos):
                    return
                
def b_tree_level():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Indexation")

    # Couleurs
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Variables pour les zones de texte
    input_text = ""
    input_rect = pygame.Rect(200, 50, 400, 30)

    # Variables pour les boutons
    add_button = pygame.Rect(200, 100, 100, 50)
    remove_button = pygame.Rect(350, 100, 100, 50)
    show_tree_button = pygame.Rect(500, 100, 200, 50)

    # Création de la racine de l'arbre B-tree
    root_node = BTreeNode()

    # Boucle de jeu
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle key events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Traiter les données saisies par l'utilisateur
                    data = input_text
                    print("Données saisies :", data)
                    input_text = ""
                    # Insérer la donnée dans l'arbre B-tree
                    root_node.insert(data, None)
                elif event.key == pygame.K_BACKSPACE:
                    # Gérer la suppression d'un caractère
                    input_text = input_text[:-1]
                else:
                    # Ajouter le caractère saisi à l'entrée utilisateur
                    input_text += event.unicode

            # Handle mouse events
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if add_button.collidepoint(mouse_pos):
                    # Ajouter des données à l'indexation
                    data = input_text
                    print("Ajouter des données :", data)
                    input_text = ""
                    # Insérer la donnée dans l'arbre B-tree
                    root_node.insert(data, None)
                elif remove_button.collidepoint(mouse_pos):
                    # Supprimer des données de l'indexation
                    print("Supprimer des données")
                elif show_tree_button.collidepoint(mouse_pos):
                    # Afficher l'arbre B-tree
                    print(display_tree())

        # Affichage des éléments graphiques
        screen.fill(WHITE)

        # Zones de texte et boutons
        pygame.draw.rect(screen, BLACK, input_rect, 2)
        text_surface = font.render(input_text, True, BLACK)
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

        pygame.draw.rect(screen, BLACK, add_button)
        add_text = small_font.render("Ajouter", True, WHITE)
        screen.blit(add_text, (add_button.x + 10, add_button.y + 15))

        pygame.draw.rect(screen, BLACK, remove_button)
        remove_text = small_font.render("Supprimer", True, WHITE)
        screen.blit(remove_text, (remove_button.x + 10, remove_button.y + 15))

        pygame.draw.rect(screen, BLACK, show_tree_button)
        show_tree_text = small_font.render("Afficher l'arbre", True, WHITE)
        screen.blit(show_tree_text, (show_tree_button.x + 10, show_tree_button.y + 15))

        # Affichage du message d'information
        info_text = small_font.render("Bienvenue dans l'application d'indexation !", True, BLACK)
        screen.blit(info_text, (200, 10))

        # Dessiner l'arbre centré sous les boutons
        root_node_x = (WIDTH - (len(root_node.keys) + 1) * 40) // 2
        root_node.draw(screen, root_node_x, 200, 0)

        pygame.display.flip()


                
def bplus_tree_level():
    screen.fill(WHITE)
    draw_text("Niveau B+ tree", font, BLACK, WIDTH // 2, HEIGHT // 2)
    back_button = pygame.Rect(50, 50, 100, 50)
    pygame.draw.rect(screen, GREEN, back_button)
    draw_text("Retour", small_font, WHITE, 100, 75)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_button.collidepoint(mouse_pos):
                    return

def main():
    while True:
        choice = choix_type()
        if choice == 'hachage':
            hachage_level()
        elif choice == 'indexation':
            indexation_level()

if __name__ == "__main__":
    main()
