from ..binary_tree import BinaryTree
from ..physical import Storage
import unittest
class BinaryTreeTests(unittest.TestCase):
    def setUp(self):
        self.storage = Storage()
        self.tree = BinaryTree(self.storage)
        self.tree.set('a', 'apple')
        self.tree.set('b', 'banana')
        self.tree.set('c', 'cherry')
        self.tree.set('d', 'date')
    
    def test_get(self):
        self.assertEqual(self.tree.get('a'), 'apple')
        self.assertEqual(self.tree.get('b'), 'banana')
        self.assertEqual(self.tree.get('c'), 'cherry')
        self.assertEqual(self.tree.get('d'), 'date')
    
    def test_set(self):
        self.tree.set('d', 'dragonfruit')
        self.assertEqual(self.tree.get('d'), 'dragonfruit')
    
    def test_delete(self):
        self.tree.delete('d')
        with self.assertRaises(KeyError):
            self.tree.get('d')
    
    def test_get_with_non_existent_key(self):
        with self.assertRaises(KeyError):
            self.tree.get('z')
    
    def test_large_tree(self):
        for i in range(1000):
            self.tree.set(str(i), str(i))
        for i in range(1000):
            self.assertEqual(self.tree.get(str(i)), str(i))
    
    def tearDown(self):
        self.storage.close()

if __name__ == '__main__':
    unittest.main()
