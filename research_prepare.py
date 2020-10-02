import matplotlib.pyplot as plt
import sys
import time

sys.setrecursionlimit(2 ** 15)
file = "graphs/n10000.txt"


class Graph:

    def __init__(self, data, reverse=False):
        self.adjList = {}        # {vertexNum: [visitedBool, set()]}
        self.directedList = {}   # {vertexNum: [visitedBool, set()]}
        self.file = data
        if type(data) == str:
            print("start reading file")
            t0 = time.time()
            with open(data) as f:
                content = f.read()
            print("finished reading file")
            t1 = time.time()
            print("total time: ", t1-t0)
            print()
            edges = content.split("\n")
            for v in range(int(edges[0])):
                self.adjList[v] = [False, set()]
                self.directedList[v] = [False, set()]
                for edge in edges[1:-1]:
                    v1 = int(edge.split()[0])
                    v2 = int(edge.split()[1])
                    if v1 == v:
                        self.adjList[v][1].add(v2)
                        if reverse == False:
                            self.directedList[v][1].add(v2)
                    if v2 == v:
                        self.adjList[v][1].add(v1)
                        if reverse == True:
                            self.directedList[v][1].add(v1)
            print("finished init")
            t2 = time.time()
            print("total time: ", t2-t1)
            print()
            # with open(data) as f:
            #     vertexNum = f.readline()
            #     for edge in f:


    @staticmethod
    def DFT(graph):
        for v in graph.adjList:
            graph.adjList[v][0] = False
        for v in graph.adjList:
            if not graph.adjList[v][0]:
                Graph.DFTr(graph, v)


    @staticmethod
    def DFTr(graph, vertex):
        graph.adjList[vertex][0] = True
        for w in graph.adjList[vertex][1]:
            if not graph.adjList[w][0]:
                Graph.DFTr(graph, w)

    @staticmethod
    def directedDFTr(graph, vertex):
        graph.directedList[vertex][0] = True
        for w in graph.directedList[vertex][1]:
            if not graph.directedList[w][0]:
                Graph.directedDFTr(graph, w)




    @staticmethod
    def findConnectedComponents(undirectedGraph):
        for v in undirectedGraph.adjList:
            undirectedGraph.adjList[v][0] = False
        componentNum = 0
        print("start dft")
        t3 = time.time()
        for v in undirectedGraph.adjList:
            if not undirectedGraph.adjList[v][0]:
                Graph.DFTr(undirectedGraph, v)
                componentNum += 1
                print("current cc #", componentNum)
        t4 = time.time()
        print("total time: ", t4- t3)
        return componentNum


    @staticmethod
    def fillStack(graph, vertex, stack):
        graph.directedList[vertex][0] = True
        for w in graph.directedList[vertex][1]:
            if not graph.directedList[w][0]:
                Graph.fillStack(graph, w, stack)
        stack.append(vertex)




    @staticmethod
    def findStronglyConnectedComponents(graph):
        stack = []
        sccNum = 0

        for v in graph.directedList:
            graph.directedList[v][0] = False

        for v in graph.directedList:
            if not graph.directedList[v][0]:
                Graph.fillStack(graph, v, stack)

        gr = Graph(graph.file, reverse=True)

        for v in gr.directedList:
            gr.directedList[v][0] = False

        while stack:
            v = stack.pop()
            if not gr.directedList[v][0]:
                sccNum += 1
                Graph.directedDFTr(gr, v)

        return sccNum



    @staticmethod
    def findUndirectedDegree(undirectedGraph):
        histogram = {}      # {degreeNum: vertexNum}
        for v in undirectedGraph.adjList:
            histogram.setdefault(len(undirectedGraph.adjList[v][1]), 0)
            histogram[len(undirectedGraph.adjList[v][1])] += 1
        return histogram


    @staticmethod
    def findIndegree(graph):
        gr = Graph(graph.file, reverse=True)
        return Graph.findOutdegree(gr)


    @staticmethod
    def findOutdegree(graph):
        histogram = {}
        for v in graph.directedList:
            histogram.setdefault(len(graph.directedList[v][1]), 0)
            histogram[len(graph.directedList[v][1])] += 1
        return histogram





g1 = Graph(file)
print(Graph.findConnectedComponents(g1))
print(Graph.findStronglyConnectedComponents(g1))

print(Graph.findUndirectedDegree(g1))
print(Graph.findOutdegree(g1))
print(Graph.findIndegree(g1))

