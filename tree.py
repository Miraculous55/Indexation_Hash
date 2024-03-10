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
        self.MAX_LEVEL = 10

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
                new_node = BTreeNode(
                    keys=self.keys[middle_index + 1:],
                    values=self.values[middle_index + 1:],
                    children=self.children[middle_index + 1:]
                )

                self.keys = self.keys[:middle_index]
                self.values = self.values[:middle_index]
                self.children = self.children[:middle_index + 1]

                if not self.children:  # If the node is a leaf
                    self.children = [new_node]
                else:
                    self.children.insert(index, new_node)


    def delete(self, key):
        if key in self.keys:
            index = self.keys.index(key)
            if self.children:
                # Node is not a leaf
                child = self.children[index]
                if len(child.keys) >= ORDER // 2:
                    # Case 1: If the child has enough keys, just delete the key and value from this node
                    del self.keys[index]
                    del self.values[index]
                else:
                    # Case 2: If the child doesn't have enough keys, borrow from the sibling or merge
                    if index > 0 and len(self.children[index - 1].keys) > ORDER // 2:
                        # Borrow from the left sibling
                        left_sibling = self.children[index - 1]
                        self.keys[index] = left_sibling.keys[-1]
                        self.values[index] = left_sibling.values[-1]
                        del left_sibling.keys[-1]
                        del left_sibling.values[-1]
                    elif index < len(self.children) - 1 and len(self.children[index + 1].keys) > ORDER // 2:
                        # Borrow from the right sibling
                        right_sibling = self.children[index + 1]
                        self.keys[index] = right_sibling.keys[0]
                        self.values[index] = right_sibling.values[0]
                        del right_sibling.keys[0]
                        del right_sibling.values[0]
                    else:
                        # Merge with a sibling
                        if index > 0:
                            # Merge with left sibling
                            left_sibling = self.children[index - 1]
                            left_sibling.keys.extend(self.keys[index:])
                            left_sibling.values.extend(self.values[index:])
                            del self.keys[index:]
                            del self.values[index:]
                            del self.children[index]
                        else:
                            # Merge with right sibling
                            right_sibling = self.children[index + 1]
                            self.keys.extend(right_sibling.keys)
                            self.values.extend(right_sibling.values)
                            del right_sibling.keys[:]
                            del right_sibling.values[:]
                            del self.children[index + 1]
            else:
                # Node is a leaf
                del self.keys[index]
                del self.values[index]

        else:
            # Key not found in this node, continue searching in child nodes
            for i, child_key in enumerate(self.keys):
                if key < child_key:
                    if self.children:
                        self.children[i].delete(key)
                    break
            else:
                if self.children:
                    self.children[-1].delete(key)

    def search(self, key):
        if key in self.keys:
            return True
        elif self.children:
            for i, child_key in enumerate(self.keys):
                if key < child_key:
                    return self.children[i].search(key)
            return self.children[-1].search(key)
        else:
            return False


    def draw(self, surface, x, y, level, level_height=100):
        if level == 0:
            x -= sum(len(child.keys) + 1 for child in self.children) * 20 // 2

        # Calculate the total width needed for the keys in the node
        total_width = sum(len(str(key)) * 12 + 20 for key in self.keys)

        # Draw current node as a rectangle
        node_rect = pygame.Rect(x - total_width // 2, y - 15, total_width, 30)
        pygame.draw.rect(surface, BLACK, node_rect)
        text_x = x - total_width // 2 + 10
        for key in self.keys:
            text_surface = small_font.render(str(key), True, WHITE)
            surface.blit(text_surface, (text_x, y - 10))
            text_x += len(str(key)) * 12 + 20

        # Draw children nodes and connect them
        if level < self.MAX_LEVEL:  # Limit drawing recursion
            for i, child in enumerate(self.children):
                child_x = x + (i - len(self.children) // 2) * 200
                child_y = y + level_height
                pygame.draw.line(surface, BLACK, (x, y), (child_x, child_y - 15), 2)
                child.draw(surface, child_x, child_y, level + 1, level_height)

# Création de la racine de l'arbre B-tree
root_node = BTreeNode()

# Fonction pour afficher l'arbre
def display_tree():
    global root_node
    tree_text = "Arbre B-tree : " + str(root_node.keys)
    return tree_text

