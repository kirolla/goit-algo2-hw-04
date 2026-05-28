from trie_ds import Trie

class Homework(Trie):

    def count_words_with_suffix(self, pattern) -> int:
        """
        Підрахунок кількості слів, що закінчуються на заданий суфікс.
        """
        if not isinstance(pattern, str):
            raise ValueError("Pattern must be a string")

        words = self.keys()

        count = 0
        for word in words:
            if word.endswith(pattern):
                count += 1

        return count

    def has_prefix(self, prefix) -> bool:
        """
        Перевірка наявності хоча б одного слова з заданим префіксом.
        """
        if not isinstance(prefix, str):
            raise ValueError("Prefix must be a string")

        if prefix == "":
            return bool(self.keys())

        node = self.root

        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]

        return True

# =========================
# TESTS
# =========================
if __name__ == "__main__":
    trie = Homework()

    words = ["apple", "application", "banana", "cat"]

    for i, word in enumerate(words):
        trie.put(word, i)

    # ===== suffix tests =====
    assert trie.count_words_with_suffix("e") == 1
    assert trie.count_words_with_suffix("ion") == 1
    assert trie.count_words_with_suffix("a") == 1
    assert trie.count_words_with_suffix("at") == 1
    assert trie.count_words_with_suffix("xyz") == 0
    assert trie.count_words_with_suffix("") == 4

    # ===== prefix tests =====
    assert trie.has_prefix("app") is True
    assert trie.has_prefix("bat") is False
    assert trie.has_prefix("ban") is True
    assert trie.has_prefix("ca") is True
    assert trie.has_prefix("") is True
    assert trie.has_prefix("xyz") is False

    # ===== error handling =====
    try:
        trie.count_words_with_suffix(123)
        assert False
    except ValueError:
        pass

    try:
        trie.has_prefix(456)
        assert False
    except ValueError:
        pass

    print("ALL TESTS PASSED ✅")
