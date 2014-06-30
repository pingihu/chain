import graph
import random
import sys
import string
from bs4 import BeautifulSoup
import urllib2
import argparse

class MarkovChainWalker:

    def __init__(self, graph, max_words):
        self.graph = graph
        self.max_words = max_words
        self.ctr = 0

    def nextWord(self, curr_word):
        num = random.randint(0, 100)
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
        while self.ctr < self.max_words:
            if next != -1:
                sys.stdout.write(next + " ")
                next = self.nextWord(next)
            else:
                next = self.graph.nodes.keys()[random.randint(0, len(self.graph.nodes) - 1)]
            self.ctr += 1

    def start(self):
        source = self.graph.nodes.keys()[random.randint(0,len(self.graph.nodes) - 1)]
        self.walk(source)


def stripPunct(text):
    for p in string.punctuation:
        text = text.replace(p, " " + p + " ")
    textAsList = text.split()
    for line in textAsList:
        line = line.strip()
    return textAsList


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('sources', metavar='S', type=str, nargs='+',
                        help='list of url and/or filenames to process')
    parser.add_argument('-wc', type=int, nargs='?',
                        help='# of words to generate (default=100)')
    args = parser.parse_args()
    for source in args.sources:
        if "http://" in source:
            soup = BeautifulSoup(urllib2.urlopen(source).read())
            for script in soup(['script', 'style']):
                script.extract()
            textList = stripPunct(soup.getText())
        else:
            f = open(source, 'r')
            textList = stripPunct(f.read())
        markovGraph = graph.Graph(textList[0])
        for i in xrange(0, len(textList) - 1):
            markovGraph.addNode(textList[i], textList[i+1])
    if args.wc is not None:
        num_words = args.wc
    else:
        num_words = 100
    markovWalker = MarkovChainWalker(markovGraph, num_words)
    markovWalker.start()
    sys.stdout.write('.')


main()
