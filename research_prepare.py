import matplotlib.pyplot as plt
import sys
import time
import networkx as nx

# sys.setrecursionlimit(2 ** 11)
file = "graphs/s1.txt"


class Graph:

    def __init__(self, data, reverse=False):
        self.adjList = {}        # {vertexNum: [visitedBool, set()]}
        self.directedList = {}   # {vertexNum: [visitedBool, set()]}
        self.file = data
        if type(data) == str:
            with open(data) as f:
                vertexNum = int(f.readline())
                self.vertexNum = vertexNum
                for v in range(vertexNum):
                    self.adjList[v] = [False, set()]
                    self.directedList[v] = [False, set()]
                for edge in f:
                    v1 = int(edge.split()[0])
                    v2 = int(edge.split()[1])
                    self.adjList[v1][1].add(v2)
                    self.adjList[v2][1].add(v1)
                    if not reverse:
                        self.directedList[v1][1].add(v2)
                    else:
                        self.directedList[v2][1].add(v1)


        self.G = nx.DiGraph()
        for n in range(self.vertexNum):
            self.G.add_node(n)
        for v1 in self.directedList:
            for v2 in self.directedList[v1][1]:
                self.G.add_edge(v1, v2)


    # @staticmethod
    # def DFTr(graph, vertex):
    #     graph.adjList[vertex][0] = True
    #     for w in graph.adjList[vertex][1]:
    #         if not graph.adjList[w][0]:
    #             Graph.DFTr(graph, w)

    @staticmethod
    def DFTr(graph, vertex):
        stack = [vertex]
        while stack:
            currentVertex = stack.pop()
            if not graph.adjList[currentVertex][0]:
                graph.adjList[currentVertex][0] = True
            for v in graph.adjList[currentVertex][1]:
                if not graph.adjList[v][0]:
                    stack.append(v)



    # @staticmethod
    # def directedDFTr(graph, vertex):
    #     graph.directedList[vertex][0] = True
    #     for w in graph.directedList[vertex][1]:
    #         if not graph.directedList[w][0]:
    #             Graph.directedDFTr(graph, w)

    @staticmethod
    def directedDFTr(graph, vertex):
        stack = [vertex]
        while stack:
            currentVertex = stack.pop()
            if not graph.directedList[currentVertex][0]:
                graph.directedList[currentVertex][0] = True
            for v in graph.directedList[currentVertex][1]:
                if not graph.directedList[v][0]:
                    stack.append(v)




    @staticmethod
    def findConnectedComponents(undirectedGraph):
        for v in undirectedGraph.adjList:
            undirectedGraph.adjList[v][0] = False
        componentNum = 0
        for v in undirectedGraph.adjList:
            if not undirectedGraph.adjList[v][0]:
                Graph.DFTr(undirectedGraph, v)
                componentNum += 1
        return componentNum


    # @staticmethod
    # def fillStack(graph, vertex, stack):
    #     graph.directedList[vertex][0] = True
    #     for w in graph.directedList[vertex][1]:
    #         if not graph.directedList[w][0]:
    #             Graph.fillStack(graph, w, stack)
    #     stack.append(vertex)

    @staticmethod
    def fillStack(graph, vertex):

        return nx.dfs_postorder_nodes(graph.G)

    # @staticmethod
    # def fillStack(graph, vertex):
    #     stack = [vertex]
    #     returnStack = []
    #     while stack:
    #         currentVertex = stack.pop()
    #
    #         if not graph.directedList[currentVertex][0]:
    #             graph.directedList[currentVertex][0] = True
    #             returnStack.append(currentVertex)
    #
    #         for v in graph.directedList[currentVertex][1]:
    #             if not graph.directedList[v][0]:
    #                 stack.append(v)
    #     return returnStack



    # @staticmethod
    # def fillStack(graph, vertex):
    #     print("fillStack start")
    #     stack = [vertex]
    #     returnStack = []
    #     postOrderStatus = [-1] * graph.vertexNum
    #
    #     x = 0
    #
    #     while stack:
    #         currentVertex = stack[-1]
    #         print(postOrderStatus)
    #         print('curvertex',currentVertex)
    #         # input()
    #         if postOrderStatus[currentVertex] == -1 or postOrderStatus[currentVertex] > 0:
    #             postOrderStatus[currentVertex] = 0
    #             for child in graph.directedList[currentVertex][1]:
    #                 if postOrderStatus[child] == -1:
    #                     stack.append(child)
    #                     postOrderStatus[currentVertex] += 1
    #         elif postOrderStatus[currentVertex] == 0:
    #             graph.directedList[currentVertex][0] = True
    #             returnStack.append(currentVertex)
    #             postOrderStatus[currentVertex] = -2
    #             stack.pop()
    #             print(x)
    #             x += 1
    #         elif postOrderStatus[currentVertex] == -2:
    #             stack.pop()
    #     print("fillStack end")
    #     return returnStack



    @staticmethod
    def findStronglyConnectedComponents(graph):
        stack = []
        sccNum = 0

        for v in graph.directedList:
            graph.directedList[v][0] = False

        for v in graph.directedList:
            if not graph.directedList[v][0]:
                stack.extend(Graph.fillStack(graph, v))
                # Graph.fillStack(graph, v, stack)


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

# print(Graph.findUndirectedDegree(g1))
# print(Graph.findOutdegree(g1))
# print(Graph.findIndegree(g1))
