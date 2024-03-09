import pygame

# Initialisation de Pygame
pygame.init()

# Création de la fenêtre
screen = pygame.display.set_mode((800, 600))

# Titre de la fenêtre
pygame.display.set_caption("Indexation")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Police de caractères
font = pygame.font.Font(None, 24)

# Variables pour les zones de texte
input_text = ""
input_rect = pygame.Rect(200, 50, 400, 30)

# Variables pour les boutons
add_button = pygame.Rect(200, 100, 100, 50)
remove_button = pygame.Rect(350, 100, 100, 50)
show_tree_button = pygame.Rect(500, 100, 200, 50)

# Arbre B-tree
class BTreeNode:
    def __init__(self, keys=None, values=None, children=None):
        if keys is None:
            keys = []
        if values is None:
            values = []
        if children is None:
            children = []
        self.keys = keys
        self.values = values
        self.children = children

    def insert(self, key, value):
        if not self.keys:  # Si le nœud est vide
            self.keys.append(key)
            self.values.append(value)
        else:
            index = 0
            while index < len(self.keys) and key > self.keys[index]:
                index += 1

            if index < len(self.children):  # Si le nœud a des enfants
                self.children[index].insert(key, value)
            else:
                self.keys.insert(index, key)
                self.values.insert(index, value)

            if len(self.keys) > 3:  # Si le nœud dépasse le nombre maximum de clés
                # Diviser le nœud en deux et promouvoir la clé médiane
                middle_index = len(self.keys) // 2
                new_node = BTreeNode()
                new_node.keys = self.keys[middle_index + 1:]
                new_node.values = self.values[middle_index + 1:]
                new_node.children = self.children[middle_index + 1:]

                del self.keys[middle_index:]
                del self.values[middle_index:]
                del self.children[middle_index + 1:]

                if not self.children:  # Si le nœud est une feuille
                    self.children = [new_node]
                else:
                    self.children.insert(index + 1, new_node)

    def draw(self, surface, x, y, level):
        if level == 0:  # Si c'est la racine, on centre
            x -= sum(len(child.keys) + 1 for child in self.children) * 20 // 2

        # Dessiner les clés du nœud actuel
        for i, key in enumerate(self.keys):
            pygame.draw.circle(surface, BLACK, (x + i * 40, y), 15 + len(str(key)) * 2)
            text_surface = font.render(str(key), True, WHITE)
            surface.blit(text_surface, (x + i * 40 - len(str(key)) * 4, y - 10))

        # Dessiner les liens vers les enfants
        for i, child in enumerate(self.children):
            child_x = x + i * 40 + 20
            child_y = y + 100
            pygame.draw.line(surface, BLACK, (x + i * 40 + 20, y + 20), (child_x, child_y), 2)
            child.draw(surface, child_x - len(child.keys) * 20, child_y, level + 1)


# Création de la racine de l'arbre B-tree
root_node = BTreeNode()

# Fonction pour afficher l'arbre
def display_tree():
    global root_node
    tree_text = "Arbre B-tree : " + str(root_node.keys)
    return tree_text

# Boucle de jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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
    add_text = font.render("Ajouter", True, WHITE)
    screen.blit(add_text, (add_button.x + 10, add_button.y + 15))

    pygame.draw.rect(screen, BLACK, remove_button)
    remove_text = font.render("Supprimer", True, WHITE)
    screen.blit(remove_text, (remove_button.x + 10, remove_button.y + 15))

    pygame.draw.rect(screen, BLACK, show_tree_button)
    show_tree_text = font.render("Afficher l'arbre", True, WHITE)
    screen.blit(show_tree_text, (show_tree_button.x + 10, show_tree_button.y + 15))

    # Affichage du message d'information
    info_text = font.render("Bienvenue dans l'application d'indexation !", True, BLACK)
    screen.blit(info_text, (200, 10))

    # Dessiner l'arbre
    root_node.draw(screen, 200, 200, 0)

    pygame.display.flip()

# Fermeture de Pygame
pygame.quit()
