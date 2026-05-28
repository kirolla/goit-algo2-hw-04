class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def put(self, word, value=None):
        """
        Додає слово в Trie.
        value поки не використовується (для сумісності з майбутніми задачами)
        """
        node = self.root

        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]

        node.is_end = True

    def keys(self):
        """
        Повертає всі слова, що зберігаються в Trie
        """
        result = []

        def dfs(node, path):
            if node.is_end:
                result.append("".join(path))

            for char, next_node in node.children.items():
                dfs(next_node, path + [char])

        dfs(self.root, [])
        return result