import graph
import random
import sys
import string


class MarkovChainWalker:

    def __init__(self, graph, max_words):
        self.graph = graph
        self.max_words = max_words
        self.ctr = 0

    def nextWord(self, curr_word):
        num = random.randint(0,100)
        if self.graph.nodes[curr_word] != []:
            total = 0
            for edge in self.graph.nodes[curr_word]:
                old_total = total
                total += edge.weight * 100
                if old_total <= num and num <= total:
                    return edge.end
        return -1

    def walk(self, curr_node):
        sys.stdout.write(curr_node + " ")
        next = self.nextWord(curr_node)
        if self.ctr < self.max_words:
            self.ctr += 1
            if next != -1:
                self.walk(next)
            else:
                source = self.graph.nodes.keys()[random.randint(0,len(self.graph.nodes) - 1)]
                self.walk(source)

    def start(self):
        source = self.graph.nodes.keys()[random.randint(0,len(self.graph.nodes) - 1)]
        self.walk(source)


def main():
    if (len(sys.argv) < 2):
        print "usage : requires a text file"
    if (len(sys.argv) > 2):
        print "usage : only one text file at a time!"
    f = open(sys.argv[1], "r")
    text = f.read()
    for p in string.punctuation:
        text = text.replace(p, " " + p + " ")
    textAsList = text.split()
    markovGraph = graph.Graph(textAsList[0])
    for i in xrange(0, len(textAsList) - 1):
        markovGraph.addNode(textAsList[i], textAsList[i+1])

    markovWalker = MarkovChainWalker(markovGraph, 100)
    markovWalker.start()
    sys.stdout.write(".")
    
main()
