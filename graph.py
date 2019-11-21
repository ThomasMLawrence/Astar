#Michael Lawrence

import math

class Vertex:

    def __init__(self, name):
        self.name = name
        self.adjacent = {}
        self.prev = None
        self.distance = math.inf


    def printSelf(self):
        print(self.name)
        print(self.adjacent)


class Graph:

    def __init__(self):
        self.numV = 0
        self.vertices = {}

    def buildVertices(self):
        fin = open("cities.txt")
        line = fin.readline()
        while(line):
            self.numV += 1
            line = line[0:len(line) - 1]
            newVertex = Vertex(line)
            self.vertices[line] = newVertex
            line = fin.readline()

    def buildAdjacent(self):
        fin = open("routes.txt")
        line = fin.readline()
        while(line):
            line = line[1:len(line) - 2]
            city1, city2, weight = line.split(',')
            city1 = city1.strip()
            city2 = city2.strip()
            weight = weight.strip()
            self.vertices[city1].adjacent[city2] = float(weight)
            self.vertices[city2].adjacent[city1] = float(weight)
            line = fin.readline()

    def printVertices(self):
        for keys in self.vertices:
            self.vertices[keys].printSelf()

    def printShortest(self):
        print("Please enter the starting location.")
        source = input()
        print("Please enter the ending location.")
        target = input()
        end = self.Astar(source, target)
        #find the route.

        #use a stack to print the route in the right order
        #and get the distance from the weights.
        route = []
        route.append(end)
        end = end.prev
        while(end):
            route.append(end)
            end = end.prev

        current = route.pop()
        distance = 0
        print(current.name, end = " ")
        while(route):
            here = current.name
            current = route.pop()
            distance += current.adjacent[here]
            print("->{}".format(current.name, end = " "))
        print()
        print("The total distance was {} miles.".format(distance))
            


    def Astar(self, source, target): 
       #initialize the set 
       Vleft = set() 
       for keys in self.vertices:
           #the source is set to 0 distance
           if(keys == source):
               self.vertices[keys].distance = 0
           #everything else is infinity 
           else:
               self.vertices[keys].distance = math.inf
           #previous is for the route we took
           self.vertices[keys].prev = None

           #add every initialized value to the set 
           Vleft.add(self.vertices[keys])

       current = None 
       #go until the set is empty
       while(Vleft):
           minimum = math.inf
           current = None
           for i in Vleft:
               #locate the minimum distance vertex.
               #at the beginning this will be source.
               if i.distance < minimum:
                   current = i
                   minimum = current.distance
           #get that vertex out of the set 
           Vleft.remove(current)
           #make sure we are not at our destination
           if current.name == target:
               #if this is our destintation we are done
               return current
           #get the adjacency list for currents neighbors
           adjacent = current.adjacent
           current.printSelf()
           #check all the neighbors
           for keys in adjacent:
               #keys is the neighbor we are currently investigating
               if self.vertices[keys] in Vleft:
                   #only bother with the neighbors still in the set.
                   #in other words those that haven't been checked.
                   if __debug__:
                       #this is the A star part of the code.
                       fin = open("euclidian.txt")
                       line = fin.readline()
                       while(line):
                           #find the euclidian distance from our neighbor to our target.
                           #this is our heuristic for A star. We don't want to go in the
                           #wrong direction
                           here, destination, distance = line.split(',')
                           if here == keys and destination == target:
                               break
                           line = fin.readline()
                   #add the weight, total trip so far, and euclidian distance up 
                       check = current.distance + adjacent[keys] + float(distance)
                   else:
                       check = current.distance + adjacent[keys]
                   #if thats less than the neighbors distance, set it to the neighbors distance
                   #and set previous to where we currently are.
                   if check < self.vertices[keys].distance:
                       self.vertices[keys].distance = check
                       self.vertices[keys].prev = current
       return current




if __name__ == '__main__':
    cities = Graph()
    cities.buildVertices()
    cities.buildAdjacent()
    cities.printShortest()
