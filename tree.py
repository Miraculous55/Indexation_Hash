import pygame

# Initialize Pygame
pygame.init()

small_font = pygame.font.SysFont(None, 30)

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

ORDER=3

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
        if not self.keys:  # If the node is empty
            self.keys.append(key)
            self.values.append(value)
        else:
            index = 0
            while index < len(self.keys) and key > self.keys[index]:
                index += 1

            if index < len(self.children):  # If the node has children
                self.children[index].insert(key, value)
            else:
                self.keys.insert(index, key)
                self.values.insert(index, value)

            if len(self.keys) > ORDER:  # If the node exceeds the order of the B-tree
                # Split the node into two and promote the median key
                middle_index = len(self.keys) // 2
                new_node = BTreeNode()
                new_node.keys = self.keys[middle_index + 1:]
                new_node.values = self.values[middle_index + 1:]
                new_node.children = self.children[middle_index + 1:]

                del self.keys[middle_index:]
                del self.values[middle_index:]
                del self.children[middle_index + 1:]

                if not self.children:  # If the node is a leaf
                    self.children = [new_node]
                else:
                    self.children.insert(index + 1, new_node)

    def draw(self, surface, x, y, level):
        if level == 0:  # Si c'est la racine, on centre
            x -= sum(len(child.keys) + 1 for child in self.children) * 20 // 2

        # Dessiner les clés du nœud actuel
        for i, key in enumerate(self.keys):
            pygame.draw.circle(surface, BLACK, (x + i * 40, y), 15 + len(str(key)) * 2)
            text_surface = small_font.render(str(key), True, WHITE)
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

