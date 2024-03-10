import PySimpleGUI as sg
from tkinter import messagebox
import time

class BTreeNode:
    def __init__(self, leaf=True):
        self.leaf = leaf
        self.keys = []
        self.children = []

class BTree:
    def __init__(self, t):
        self.root = BTreeNode()
        self.t = t

    def insert(self, key):
        root = self.root
        if len(root.keys) == (2 * self.t) - 1:
            new_root = BTreeNode(leaf=False)
            new_root.children.append(self.root)
            self.split(new_root, 0)
            self.root = new_root
        self._insert_non_full(self.root, key)

    def _insert_non_full(self, x, key):
        i = len(x.keys) - 1
        if x.leaf:
            while i >= 0 and key < x.keys[i]:
                i -= 1
            x.keys.insert(i + 1, key)
        else:
            while i >= 0 and key < x.keys[i]:
                i -= 1
            i += 1
            if len(x.children[i].keys) == (2 * self.t) - 1:
                self.split(x, i)
                if key > x.keys[i]:
                    i += 1
            self._insert_non_full(x.children[i], key)

    def split(self, x, i):
        t = self.t
        y = x.children[i]
        z = BTreeNode(leaf=y.leaf)
        x.children.insert(i + 1, z)
        x.keys.insert(i, y.keys[t - 1])
        z.keys = y.keys[t:2 * t - 1]
        y.keys = y.keys[0:t - 1]

        if not y.leaf:
            z.children = y.children[t:2 * t]
            y.children = y.children[0:t - 1]

    def search(self, key, x=None):
        if x is None:
            x = self.root
        i = 0
        while i < len(x.keys) and key > x.keys[i]:
            i += 1
        if i < len(x.keys) and key == x.keys[i]:
            return True
        elif x.leaf:
            return False
        else:
            return self.search(key, x.children[i])

    def delete(self, key):
        self._delete(self.root, key)

    def _delete(self, x, key):
        t = self.t
        i = 0
        while i < len(x.keys) and key > x.keys[i]:
            i += 1

        if x.leaf:
            if i < len(x.keys) and key == x.keys[i]:
                x.keys.pop(i)
            else:
                sg.popup("Erreur", "La clé {} n'est pas présente dans l'arbre.".format(key))
        else:
            if i < len(x.keys) and key == x.keys[i]:
                # The key to delete is in an internal node
                self.delete_internal_node(x, i)
            else:
                # The key to delete is not in this node; recurse to the appropriate child
                self._delete_nonempty_node(x, i, key)

            # After deletion, if the root has no keys and has one child, update the root
            if x == self.root and not x.keys and len(x.children) == 1:
                self.root = x.children[0]

    def delete_internal_node(self, x, i):
        t = self.t
        key = x.keys[i]
        if len(x.children[i].keys) >= t:
            predecessor = self.get_predecessor(x, i)
            x.keys[i] = predecessor
            self._delete(x.children[i], predecessor)
        elif len(x.children[i + 1].keys) >= t:
            successor = self.get_successor(x, i)
            x.keys[i] = successor
            self._delete(x.children[i + 1], successor)
        else:
            self.merge(x, i)
            self._delete(x.children[i], key)

    def _delete_nonempty_node(self, x, i, key):
        t = self.t
        if len(x.children[i].keys) == t - 1:
            if i > 0 and len(x.children[i - 1].keys) >= t:
                self.borrow_from_left(x, i)
            elif i < len(x.children) - 1 and len(x.children[i + 1].keys) >= t:
                self.borrow_from_right(x, i)
            elif i > 0:
                self.merge(x, i - 1)
            else:
                self.merge(x, i)

        self._delete(x.children[i], key)

    def borrow_from_left(self, x, i):
        child = x.children[i]
        sibling = x.children[i - 1]
        child.keys.insert(0, x.keys[i - 1])
        x.keys[i - 1] = sibling.keys.pop()

        if not child.leaf:
            child.children.insert(0, sibling.children.pop())

    def borrow_from_right(self, x, i):
        child = x.children[i]
        sibling = x.children[i + 1]
        child.keys.append(x.keys[i])
        x.keys[i] = sibling.keys.pop(0)

        if not child.leaf:
            child.children.append(sibling.children.pop(0))

    def merge(self, x, i):
        t = self.t
        child = x.children[i]
        sibling = x.children[i + 1]
        child.keys.append(x.keys[i])
        child.keys.extend(sibling.keys)
        x.keys.pop(i)
        x.children.pop(i + 1)

        if not child.leaf:
            child.children.extend(sibling.children)

    def is_node_full(self, node):
        return len(node.keys) == (2 * self.t) - 1

    def update(self, old_key, new_key):
        # Check if the old key exists before updating
        if not self.search(old_key):
            sg.popup("Update Error", f"Key {old_key} does not exist in the tree.")
            return

        # First, delete the old key
        self.delete(old_key)

        # Then, insert the new key
        self.insert(new_key)


class BTreeGUI:
    def __init__(self, b_tree):
        self.b_tree = b_tree

        layout = [
            [sg.Canvas(size=(800, 500), background_color='white', key='canvas')],
            [sg.InputText("Add a number to insert", key='input_insert'), sg.Button('Insert'),
             sg.InputText("Add a number to delete", key='input_delete'), sg.Button('Delete')],
            [sg.InputText("Add a number to search", key='input_search'), sg.Button('Search'),
             sg.InputText("Add a number to update", key='input_update'), sg.Button('Update')],
            [sg.Text("Current Node: Not Full", key='status')]
        ]

        self.window = sg.Window("B-Tree Visualization", layout, finalize=True)
        self.canvas = self.window['canvas'].TKCanvas
        self.draw_tree_step_by_step()

    def draw_tree_step_by_step(self):
        self.canvas.delete("all")  # Clear the canvas
        self._draw_step_by_step_recursive(self.b_tree.root, 400, 50, 100)
        time.sleep(1)  # Introduce a delay (adjust as needed)

    def _draw_step_by_step_recursive(self, node, x, y, spacing, parent_range=None, is_left_child=True):
        if node:
            key_ranges = []
            is_current_node_full = len(node.keys) + len(node.children) == (2 * self.b_tree.t) - 1

            # Update node status label based on whether the node is full
            self.set_node_status(is_current_node_full)

        if node:
            key_ranges = []
            for i, key in enumerate(node.keys):
                new_x = x + i * spacing - (len(node.keys) - 1) * spacing / 2

                if i == 0 and parent_range is not None and is_left_child:
                    key_ranges.append((float('-inf'), key))
                elif i == len(node.keys) - 1 and parent_range is not None and not is_left_child:
                    key_ranges.append((key, float('inf')))
                else:
                    key_ranges.append((node.keys[i - 1], key))

                if i == 0 and parent_range is not None and is_left_child:
                    rect_x = new_x - 30
                else:
                    rect_x = new_x - 15

                self.canvas.create_rectangle(rect_x, y - 20, new_x + 15, y + 20, outline="black", width=2)
                self.canvas.create_text(new_x, y, text=str(key), font='Helvetica 10 bold')

                if not node.leaf and i < len(node.children):
                    child_x = new_x + i * spacing / 2
                    self._draw_step_by_step_recursive(node.children[i], child_x, y + 60, spacing / 2, key_ranges[i],
                                                      True)
                    self.canvas.create_line(new_x, y + 20, child_x, y + 60 - 20, fill="black")


            if not node.leaf and len(node.children) > len(node.keys):
                key_ranges.append((node.keys[-1], float('inf')))
                child_x = new_x + spacing
                self._draw_step_by_step_recursive(node.children[-1], child_x, y + 60, spacing / 2, key_ranges[-1], True)
                self.canvas.create_line(new_x, y + 20, child_x, y + 60 - 20, fill="black")

        self.window.finalize()

    def set_node_status(self, is_full):
        status_text = "Current Node: Full" if is_full else "Current Node: Not Full"
        self.window['status'].update(status_text)

    def update_key(self, old_key, new_key):
        # Check if the old key exists before updating
        if not self.b_tree.search(old_key):
            sg.popup("Update Error", f"Key {old_key} does not exist in the tree.")
            return

        self.b_tree.update(old_key, new_key)
        self.draw_tree_step_by_step()

    def __del__(self):
        self.window.close()


def main():
    t = 2
    b_tree = BTree(t)
    gui = BTreeGUI(b_tree)

    while True:
        event, values = gui.window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'Insert':
            key = int(values['input_insert'])
            b_tree.insert(key)
            gui.draw_tree_step_by_step()
        elif event == 'Delete':
            key = int(values['input_delete'])
            b_tree.delete(key)
            gui.draw_tree_step_by_step()
        elif event == 'Search':
            key = int(values['input_search'])
            result = b_tree.search(key)
            if result:
                sg.popup("Search Result", f"Key {key} found in the tree.")
            else:
                sg.popup("Search Result", f"Key {key} not found in the tree.")
        elif event == 'Update':
            old_key = int(values['input_update'])
            new_key = int(values['input_insert'])
            gui.update_key(old_key, new_key)

if __name__ == "__main__":
    main()




