import pygame
import hashlib

# Initialisation de Pygame
pygame.init()

# Création de la fenêtre (nous augmentons la taille de la fenêtre)
screen_width = 1000  # Largeur de la fenêtre
screen_height = 800  # Hauteur de la fenêtre
screen = pygame.display.set_mode((screen_width, screen_height))

# Titre de la fenêtre
pygame.display.set_caption("Illustration des Types de Hachage")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Police de caractères
font = pygame.font.Font(None, 24)


# Classe pour illustrer une fonction de hachage cryptographique
class CryptographicHash:
    def __init__(self):
        pass

    def draw(self, surface, x, y):
        text_surface = font.render("Fonction de Hachage Cryptographique", True, BLACK)
        surface.blit(text_surface, (x, y))
        text_surface = font.render("Exemple : SHA-256", True, BLACK)
        surface.blit(text_surface, (x, y + 30))
        text_surface = font.render("Utilisé pour sécuriser les données", True, BLACK)
        surface.blit(text_surface, (x, y + 60))


# Classe pour illustrer une table de hachage
class HashTable:
    def __init__(self):
        self.data = {}  # Dictionnaire pour stocker les données hachées

    def add_data(self, data):
        hashed_data = hashlib.sha256(data.encode()).hexdigest()
        self.data[hashed_data] = data

    def draw(self, surface, x, y):
        text_surface = font.render("Table de Hachage", True, BLACK)
        surface.blit(text_surface, (x, y))
        y += 30
        for i, (hashed_data, original_data) in enumerate(self.data.items()):
            text_surface = font.render(f"{i + 1}: {original_data} -> {hashed_data}", True, BLACK)
            surface.blit(text_surface, (x, y + i * 30))


# Classe pour illustrer le hachage extensible
class ExtendableHashing:
    def __init__(self):
        self.hash_table = HashTable()

    def add_data(self, data):
        self.hash_table.add_data(data)

    def draw(self, surface, x, y):
        self.hash_table.draw(surface, x, y)


# Fonction pour dessiner l'arrière-plan
def draw_background():
    screen.fill(WHITE)
    pygame.draw.rect(screen, GRAY, (50, 50, 300, 500), 0)
    pygame.draw.rect(screen, GRAY, (350, 50, 300, 500), 0)
    pygame.draw.rect(screen, GRAY, (650, 50, 300, 500), 0)


# Fonction pour dessiner un bouton
def draw_button(surface, rect, text):
    pygame.draw.rect(surface, BLACK, rect)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)


# Fonction principale pour exécuter le programme
def main():
    # Création des instances pour chaque type de hachage
    cryptographic_hash = CryptographicHash()
    extendable_hashing = ExtendableHashing()

    # Variables pour la saisie de données
    input_rect = pygame.Rect(50, 20, 200, 30)
    input_text = ""
    hash_result = ""

    # Boucle de jeu
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    input_text = ""
                elif hash_button_rect.collidepoint(event.pos):
                    extendable_hashing.add_data(input_text)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    extendable_hashing.add_data(input_text)
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

        # Dessiner l'arrière-plan
        draw_background()

        # Dessiner la zone de saisie de données
        pygame.draw.rect(screen, BLACK, input_rect, 2)
        input_surface = font.render(input_text, True, BLACK)
        screen.blit(input_surface, (input_rect.x + 5, input_rect.y + 5))

        # Dessiner le bouton pour appliquer le hachage
        hash_button_rect = pygame.Rect(50, 70, 200, 30)
        draw_button(screen, hash_button_rect, "Ajouter à la Table de Hachage")

        # Afficher la table de hachage
        extendable_hashing.draw(screen, 350, 100)

        pygame.display.flip()

    # Fermeture de Pygame
    pygame.quit()


# Appel de la fonction principale
if __name__ == "__main__":
    main()
