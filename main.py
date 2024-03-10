import pygame
import sys
from tree import BTreeNode, display_tree
from hashing import CryptographicHash, ExtendableHashing

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
font = pygame.font.SysFont(None, 32)
small_font = pygame.font.SysFont(None, 24)

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

hash_table = {}

def hachage_level():
    global hash_table

    screen.fill(WHITE)

    # Choose the type of hashing
    hash_types = ["Cryptographic Hash", "Extendable Hashing"]
    dropdown_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 40)
    pygame.draw.rect(screen, WHITE, dropdown_rect)
    pygame.draw.rect(screen, BLACK, dropdown_rect, 2)
    draw_text("Choose Hash Type", small_font, BLACK, WIDTH // 2, HEIGHT // 2 - 70)
    draw_text("▼", small_font, BLACK, WIDTH // 2 + 90, HEIGHT // 2 - 30)

    # Placeholder for element input
    input_placeholder = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2, 300, 40)
    pygame.draw.rect(screen, WHITE, input_placeholder)
    pygame.draw.rect(screen, BLACK, input_placeholder, 2)
    draw_text("Enter Element", small_font, BLACK, WIDTH // 2, HEIGHT // 2 + 20)

    # Hash button
    hash_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 70, 200, 40)
    pygame.draw.rect(screen, BLUE, hash_button)
    draw_text("Hash", font, WHITE, WIDTH // 2, HEIGHT // 2 + 90)

    # Show table button
    show_table_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 120, 200, 40)
    pygame.draw.rect(screen, GREEN, show_table_button)
    draw_text("Show Table", font, WHITE, WIDTH // 2, HEIGHT // 2 + 140)

    pygame.display.update()

    selected_hash_type = None
    element = ""
    hashed_text = ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if dropdown_rect.collidepoint(mouse_pos):
                    # Display dropdown options
                    selected_hash_type = dropdown_menu(hash_types, WIDTH // 2 - 100, HEIGHT // 2 - 10, dropdown_rect.w, dropdown_rect.h)
                elif input_placeholder.collidepoint(mouse_pos):
                    # Input for the element
                    element = input_text()
                elif hash_button.collidepoint(mouse_pos):
                    # Hash the element based on selected hash type
                    if selected_hash_type:
                        if selected_hash_type == "Cryptographic Hash":
                            hashed_text = CryptographicHash().sha256_hash(element)
                        elif selected_hash_type == "Extendable Hashing":
                            # Perform Extendable Hashing logic here
                            pass
                        print(f"Element: {element}, Hash: {hashed_text}")
                        hash_table[element] = hashed_text
                    else:
                        print("Select a hash type first.")
                elif show_table_button.collidepoint(mouse_pos):
                    # Show hash table
                    show_hash_table(hash_table)

        screen.fill(WHITE)
        pygame.draw.rect(screen, WHITE, dropdown_rect)
        pygame.draw.rect(screen, BLACK, dropdown_rect, 2)
        draw_text(selected_hash_type if selected_hash_type else "Select Hash Type", small_font, BLACK, WIDTH // 2, HEIGHT // 2 - 30)
        pygame.draw.rect(screen, WHITE, input_placeholder)
        pygame.draw.rect(screen, BLACK, input_placeholder, 2)
        draw_text(element, small_font, BLACK, WIDTH // 2, HEIGHT // 2 + 20)
        pygame.draw.rect(screen, BLUE, hash_button)
        draw_text("Hash", font, WHITE, WIDTH // 2, HEIGHT // 2 + 90)
        pygame.draw.rect(screen, GREEN, show_table_button)
        draw_text("Show Table", font, WHITE, WIDTH // 2, HEIGHT // 2 + 140)
        pygame.display.update()

def dropdown_menu(options, x, y, w, h):
    for i, option in enumerate(options):
        option_rect = pygame.Rect(x, y + i * h, w, h)
        pygame.draw.rect(screen, WHITE, option_rect)
        pygame.draw.rect(screen, BLACK, option_rect, 1)
        draw_text(option, small_font, BLACK, x + w // 2, y + i * h + h // 2)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, option in enumerate(options):
                    option_rect = pygame.Rect(x, y + i * h, w, h)
                    if option_rect.collidepoint(mouse_pos):
                        return option

def input_text():
    input_box = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2, 300, 40)
    text = ""
    draw_text("Enter Element", small_font, BLACK, WIDTH // 2, HEIGHT // 2 - 50)
    while True:
        pygame.draw.rect(screen, WHITE, input_box)
        pygame.draw.rect(screen, BLACK, input_box, 2)
        draw_text(text, small_font, BLACK, input_box.x + 5, input_box.y + 5)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return text
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def show_hash_table(hash_table):
    screen.fill(WHITE)
    draw_text("Hash Table", font, BLACK, WIDTH // 2, HEIGHT // 4)
    draw_text("Key -> Hashed Element", small_font, BLACK, WIDTH // 2, HEIGHT // 4 + 30)

    y_offset = 0
    for key, value in hash_table.items():
        draw_text(f"{key} -> {value}", small_font, BLACK, WIDTH // 2, HEIGHT // 4 + 60 + y_offset)
        y_offset += 30

    pygame.display.update()


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

    # Input box
    input_rect = pygame.Rect(200, 50, 400, 30)
    input_text = ""

    # Buttons
    button_width, button_height = 100, 40
    add_button = pygame.Rect(80, 120, button_width, button_height)
    remove_button = pygame.Rect(240, 120, button_width, button_height)
    search_button = pygame.Rect(400, 120, button_width, button_height)
    update_button = pygame.Rect(560, 120, button_width, button_height)

    # Create root node
    root_node = BTreeNode()

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    data = input_text
                    print("Entered data:", data)
                    input_text = ""
                    root_node.insert(data, None)
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if add_button.collidepoint(mouse_pos):
                    data = input_text
                    print("Add data:", data)
                    input_text = ""
                    root_node.insert(data, None)
                elif remove_button.collidepoint(mouse_pos):
                    print("Remove data")
                elif search_button.collidepoint(mouse_pos):
                    print("search")
                elif update_button.collidepoint(mouse_pos):
                    print("update")

        screen.fill(WHITE)

        # Input box
        pygame.draw.rect(screen, BLACK, input_rect, 2)
        text_surface = font.render(input_text, True, BLACK)
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

        # Information message
        info_text = small_font.render("Welcome to the indexing application!", True, BLACK)
        screen.blit(info_text, (200, 10))

        # Buttons
        pygame.draw.rect(screen, BLACK, add_button)
        add_text = small_font.render("Add", True, WHITE)
        screen.blit(add_text, (add_button.x + 40, add_button.y + 10))

        pygame.draw.rect(screen, BLACK, remove_button)
        remove_text = small_font.render("Remove", True, WHITE)
        screen.blit(remove_text, (remove_button.x + 20, remove_button.y + 10))

        pygame.draw.rect(screen, BLACK, search_button)
        show_tree_text = small_font.render("Search", True, WHITE)
        screen.blit(show_tree_text, (search_button.x + 20, search_button.y + 10))

        pygame.draw.rect(screen, BLACK, update_button)
        show_tree_text = small_font.render("Update", True, WHITE)
        screen.blit(show_tree_text, (update_button.x + 20, update_button.y + 10))

        # Draw the tree centered below the buttons
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
