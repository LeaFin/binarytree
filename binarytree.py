# -*- coding: utf-8 -*-
import pydot
# Draw benötigt pydot, pyparsing<=1.5.7 (zuerst pyparsing installieren, sonst ist version 2.x statt 1.x)
# Ausserdem wird Graphviz benötigt (http://www.graphviz.org/)

# Tree([3,5,6,2], True), erzeugt neuen Baum uns speichert Ausgabe als Tree.png im Ordener in welchem dieses File liegt.

class Tree(object):
    left = None
    right = None
    value = None

    # Wenn draw=True gesetzt wird, wird der Baum beim erstellen gezeichnet.
    def __init__(self, values=None, draw=False):
        super(Tree, self).__init__()

        if values:
            self.value = values.pop(0)

            for value in values:
                self.add(value)
        if draw:
            self.draw()

    def add(self, value):
        if not self.value:
            self.value = value
        else:
            if value >= self.value:
                if self.right:
                    self.right.add(value)
                else:
                    self.right = Tree([value])
            else:
                if self.left:
                    self.left.add(value)
                else:
                    self.left = Tree([value])

    def addList(self, values):
        for value in values:
            self.add(value)

    def find(self, value, pred=None):
        if not self.value:
            raise 'Empty Tree'
        if value > self.value:
            if self.right:
                return self.right.find(value, self)
            else:
                return False
        elif value == self.value:
            return (self, pred)
        else:
            if self.left:
                return self.left.find(value, self)
            else:
                return False

    def getLowestRightSuccessor(self):
        if self.right.left:
            return self.right.getLowestSuccessor(self.right)
        else:
            return self.right, self

    def getLowestSuccessor(self, pred):
        if self.left:
            return self.left.getLowestSuccessor(self)
        else:
            return self, pred

    def remove(self, value):
        while self.find(value):
            node, pred = self.find(value)
            if node.left and node.right:
                replaceNode, replacePred = node.getLowestRightSuccessor()
                node.value = replaceNode.value
                if replacePred != self:
                    replacePred.left = replaceNode.right
                del replaceNode
            elif node.left:
                if pred.value >= value:
                    pred.right = node.left
                else:
                    pred.left = node.left
                del node
            elif node.right:
                if pred.value >= value:
                    pred.right = node.right
                else:
                    pred.left = node.right
                del node
            else:
                if pred.value >= value:
                    pred.right = None
                else:
                    pred.left = None
                del node

    def depth(self):
        if self.left:
            if self.right:
                return max(self.left.depth(), self.right.depth()) + 1
            return self.left.depth() + 1
        elif self.right:
            return self.right.depth() + 1
        else:
            return 0

    def contains(self, value):
        if self.find(value):
            return True
        return False

    # mytree.draw('asfd') speichert asfd.png mit Graphik des Baums
    def draw(self, filename='Tree', graph=None, parent='', side='', print_out=True):
        if not graph:
            graph = pydot.Dot(graph_type='graph')
            name = 'w'
        else:
            name = parent + side
        graph.add_node(pydot.Node(name, label='%s' % self.value))
        if name != 'w':
            graph.add_edge(pydot.Edge(parent, name))
        if self.left:
            self.left.draw(filename, graph, name, 'l', False)
        if self.right:
            self.right.draw(filename, graph, name, 'r', False)
        graph.write_png('%s.png' % filename)
        if print_out:
            print '%s.png wurde gespeichert.' % filename 
