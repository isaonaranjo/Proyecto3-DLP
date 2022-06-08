'''
    Maria Isabel Ortiz Naranjo
    example: https://www.geeksforgeeks.org/print-binary-tree-2-dimensions/
'''
class Tree(object):
    def __init__(self):
        self.left = None
        self.right = None
        self.data = None
    
    def printTree(self):
        print(self.data)
        
    def __str__(self):
        string = 'Symbol: ' + self.data + '\n'
        string = string + 'Left: ' + self.left.data + '\n'
        if self.right:
            string = string + 'Right: ' + self.right.data + '\n'
        
        return string
