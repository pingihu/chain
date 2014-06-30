import graph
import random
import sys
import string
from bs4 import BeautifulSoup
import urllib2


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
    num_words = 100
    urls = []
    files = []
    parse_file = parse_url = False
    if len(sys.argv) == 1:
        print "usage: requires at least one input source"
        exit(1)
    elif len(sys.argv) > 1:
        for input in sys.argv[1:]:
            if "http" in input:
                parse_url = True
                urls += input
            elif ".txt" in input or ".dat" in input or ".rtf" in input:
                parse_file = True
                files += input
            else:
                print "usage: invalid text source"
                exit(1)
    if parse_file:
        for file_name in files:
            f = open(file_name, "r")
            text = f.read()
            textAsList = stripPunct(text)
            markovGraph = graph.Graph(textAsList[0])
            for i in xrange(0, len(textAsList) - 1):
                markovGraph.addNode(textAsList[i], textAsList[i+1])
    if parse_url:
        for url in urls:
            readString = ""
            response = url
            response = urllib2.urlopen(sys.argv[1])
            html = response.read()
            soup = BeautifulSoup(html)
            for script in soup(["script", "style"]):
                script.extract()
            readString = soup.get_text()
            textAsList = stripPunct(readString)
            markovGraph = graph.Graph(textAsList[0])
            for i in xrange(0, len(textAsList) - 1):
                markovGraph.addNode(textAsList[i], textAsList[i+1])

    markovWalker = MarkovChainWalker(markovGraph, num_words)
    markovWalker.start()
    sys.stdout.write(".")

main()
