class Edge:
    def __init__(self, start, end, weight):
        self.start = start
        self.end = end 
        self.weight = weight

class Graph:
    nodes = {} #valued on list of edge

    def __init__(self, first_node):
	first_node = first_node.lower()
        self.source = first_node
        self.nodes[first_node] = []

    def updateWeights(self, start_node, curr, curr_exists):
	for edge in self.nodes[start_node]:
	    if edge.end != curr:
		edge.weight = (edge.weight * len(self.nodes[start_node])) / (len(self.nodes[start_node]) + 1)
	    else:
		if curr_exists:
		    edge.weight = ((edge.weight * len(self.nodes[start_node])) + 1) / (len(self.nodes[start_node]) + 1)
	

    def addNode(self, start_node, end_node):
	start_node = start_node.lower()
	end_node = end_node.lower()
        if end_node not in self.nodes.keys():
            self.nodes[end_node] = []

        for edge in self.nodes[start_node]:
	    """ Case 1: x_f is in edges. """
            if edge.end == end_node:
		self.updateWeights(start_node, end_node, True)
                return  
          
	self.updateWeights(start_node, end_node, False)
	self.nodes[start_node] += [Edge(start_node, end_node, 1.0 / (len(self.nodes[start_node]) + 1))]

    def toString(self):
	for key,value in self.nodes.iteritems():
	    print key + "-> "
            for edge in value:
	        print "start : " + edge.start + ", end: " + edge.end + ", weight: " + str(edge.weight) 


def main():
    text = ["The", "lamb", "loves", "eating", "gyro", "but", "the", 
        "gyro", "is", "made", "of", "lamb", "loves"]
    #text = ["the","lamb","the","love"]
    myGraph = Graph(text[0])
    for i in xrange(0,len(text) - 1):
        myGraph.addNode(text[i], text[i+1])

    myGraph.toString()
        

    
    
#main()

        


    

