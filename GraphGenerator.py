#Graph Generator Function
#Created by Chase Ladwig
#Algorithm Analysis Section W03 Group 07

import random

#Return a random graph of a random size set by the user
def random_graph(vertices, variance):
    
    #Gets a random number for RNG seeding
    randomSeed = random.Random()
    
    #Creates a set that will be populated with values from below
    graph = {x: set() for x in range(vertices)}

    #Parses the nodes of the graph and uses the RNG seed and the variance function to determine if two nodes should be connected
    for x in range(vertices):
        for y in range(x + 1, vertices):    
            if randomSeed.random() < variance:     
                graph[x].add("V" + str(y))
                graph[y].add("V" + str(x))     
    return graph

#Generates a random graph and prints it to the console to be copy/pasted to the other programs
if __name__ == "__main__":
    generatedGraph = random_graph(vertices=100, variance=0.2)
    
    #Prints the graph. The brackets are added for optimal copy/pasting to the program.
    print("{")
    for x, neighbors in generatedGraph.items():
        print("V" + f"{x}: {sorted(neighbors)}")

        #print("V" + f"{x}: {neighbors}")
    print("}")
    
    #Error handling to ensure that the graph generated is the correct amount of vertices
    print(f"\nVertices: {len(generatedGraph)}")
