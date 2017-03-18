#!/usr/bin/python

import sys
import MySQLdb
from math import radians, sin, cos, sqrt, asin
import math

#calulate the distance between 2 coordinatescord
def haversine(lat1, lon1, lat2, lon2):
        R = 6371000 #Earth radius in meters

        dLat = radians(lat2 - lat1)
        dLon = radians(lon2 - lon1)
        lat1 = radians(lat1)
        lat2 = radians(lat2)
 
        a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2
        c = 2*asin(sqrt(a))
 
        return R * c
# given gps coordinates calculates the direction of cord1 with repect to cord 2
def direction(lat2, long2, lat1, long1):
    margin = math.pi/90; #2 degree tolerance for cardinal directions
    o = lat1 - lat2;
    a = long1 - long2;
    angle = math.atan2(o,a)
    
    if angle > -margin and angle < margin:
            return "E"
    elif angle > math.pi/2 - margin and angle < math.pi/2 + margin:
            return "N";
    elif angle > math.pi - margin and angle < -math.pi + margin:
            return "W"
    elif angle > -math.pi/2 - margin and angle < -math.pi/2 + margin:
            return "S"
    
    if angle > 0 and angle < math.pi/2:
        return"NE"
    elif angle > math.pi/2 and angle < math.pi: 
        return "NW"
    elif angle > -math.pi/2 and angle < 0: 
        return "SE"
    else:
        return "SW"

#given 2 nodes directions calculates the turn the user will need to make   
def direction2(node1,node2):
        if (node1 == node2) or (node1 == "NW" and node2 == "SE") or (node1 == "SE" and node2 == "NW")  or (node1 == "SW" and node2 == "NE") or (node1 == "NE" and node2 == "SW"):
                return "straight"
        elif (node1 == "SW" and node2 == "SE") or (node1 == "SE" and node2 == "NE") or (node1 == "NE" and node2 == "NW") or (node1 == "NW" and node2 == "SW"):
                return "left"
        elif (node1 == "SW" and node2 == "NW") or (node1 == "SE" and node2 == "SW") or (node1 == "NW" and node2 == "NE") or (node1 == "NE" and node2 == "SE"):
                return "right"

        else:
                print "Error: Determining direction2"
                print node1
                print node2
# fineds the php id of a node
def findid(index):
        j=0
        while index != map[j][0]:
                j=j+1
        
        return j
def distTillTurn(index, dist):
        
        if route[index]=="straight":
                dist = dist+haversine(map[findid(path[index])][3], map[findid(path[index])][4], map[findid(path[index+1])][3], map[findid(path[index+1])][4])
        else:
                dist = haversine(map[findid(path[index])][3], map[findid(path[index])][4], map[findid(path[index+1])][3], map[findid(path[index+1])][4])
        return dist
        
# Openning DB connection 

db = MySQLdb.connect("localhost","root","hearmeout","thebat")
# Preparing cursor object using cursor() method

cursor = db.cursor()

###  Get current_user lat & long   #####################
sql = "SELECT * FROM currentUser"

try:
        #Execute SQL commands
        cursor.execute(sql)
        results = cursor.fetchall()

        currentlat = float(results[0][0])
        currentlong = float(results[0][1])
        exitid = results[0][2]

except:
        print "Error: Unable to fetch current_user lat & long"
del results

print "User Coordinates: %f,%f" % (currentlat,currentlong)

#currentlat=33.252671
#currentlong=-97.152838

sql = "SELECT * FROM maps"


try:
	#Execute SQL commands
	cursor.execute(sql)
	results = cursor.fetchall()
	numrows = len(results)
	i = 0
	minimum = None
	for line in results:
                location =  results[i][1]
                latitude = results[i][2]
                longitude = results[i][3]
                i+=1
                distance = haversine(latitude, longitude, currentlat, currentlong)
                if minimum is None or distance < minimum:
                        minimum = distance
                        minlocation = location
        print "Closest map: %s" %minlocation

except:
	print "Error: Unable to fetch data"
	 
sql = "SELECT * FROM coordinates"
try:
        #Execute SQL commands
        cursor.execute(sql)
        map = cursor.fetchall()
        i = 0
        minimum = None
        for line in map:
                location = map[i][2]
                latitude = map[i][3]
                longitude = map[i][4]
                startnodeid = map[i][0]
                i+=1
                distance = haversine(latitude, longitude, currentlat, currentlong)
                if minimum is None or distance < minimum:
                        minimum = distance
                        minlocation = startnodeid
        print "Closest node: %s" %minlocation
                
except:
        print "Error: Unable to fetch data"



########################################################################################3
### Calculates the sortest path given starting node and exit node
########################################################################################
class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}
        # Set distance to infinity for all nodes
        self.distance = sys.maxint
        # Mark all nodes unvisited        
        self.visited = False
        # Predecessor
        self.previous = None

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

    def set_distance(self, dist):
        self.distance = dist

    def get_distance(self):
        return self.distance

    def set_previous(self, prev):
        self.previous = prev

    def set_visited(self):
        self.visited = True

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())
    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, cost = 0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def get_vertices(self):
        return self.vert_dict.keys()

    def set_previous(self, current):
        self.previous = current

    def get_previous(self, current):
        return self.previous

def shortest(v, path):
    ''' make shortest path from v.previous'''
    if v.previous:
        path.append(v.previous.get_id())
        shortest(v.previous, path)
    return

import heapq

def dijkstra(aGraph, start, target):
    #print '''Dijkstra's shortest path'''
    # Set the distance for the start node to zero 
    start.set_distance(0)

    # Put tuple pair into the priority queue
    unvisited_queue = [(v.get_distance(),v) for v in aGraph]
    heapq.heapify(unvisited_queue)

    while len(unvisited_queue):
        # Pops a vertex with the smallest distance 
        uv = heapq.heappop(unvisited_queue)
        current = uv[1]
        current.set_visited()

        #for next in v.adjacent:
        for next in current.adjacent:
            # if visited, skip
            if next.visited:
                continue
            new_dist = current.get_distance() + current.get_weight(next)

            if new_dist < next.get_distance():
                next.set_distance(new_dist)
                next.set_previous(current)
                #print 'updated : current = %s next = %s new_dist = %s' \
                       #%(current.get_id(), next.get_id(), next.get_distance())
            #else:
                #print 'not updated : current = %s next = %s new_dist = %s' \
                       #%(current.get_id(), next.get_id(), next.get_distance())
                

        # Rebuild heap
        # 1. Pop every item
        while len(unvisited_queue):
            heapq.heappop(unvisited_queue)
        # 2. Put all vertices not visited into the queue
        unvisited_queue = [(v.get_distance(),v) for v in aGraph if not v.visited]
        heapq.heapify(unvisited_queue)
if __name__ == '__main__':

        # Openning DB connection 

        db = MySQLdb.connect("localhost","root","hearmeout","thebat")
        # Preparing cursor object using cursor() method

        cursor = db.cursor()

###  Get current_user lat & long   #####################
###  Get current_user lat & long   #####################
	sql = "SELECT * FROM dijkstra"

	try:
	        #Execute SQL commands
	        cursor.execute(sql)
	        results = cursor.fetchall()

	except:
	        print "Error: Unable to fetch node wights"

	g = Graph()
	i=0
	for i in range(16):
		g.add_vertex(i)
	i=0
	while i < len(results):
		g.add_edge(results[i][1], results[i][2], float(results[i][3]))  
		i =i+ 1
		
##      prints out the dijkstra's map
##    	print 'Graph data:'
##    	for v in g:
##    	    for w in v.get_connections():
##    	        vid = v.get_id()
##    	        wid = w.get_id()
##    	        print '( %s , %s, %.4f)'  % ( vid, wid, v.get_weight(w))

    	dijkstra(g, g.get_vertex(minlocation), g.get_vertex(exitid)) 
	
	target = g.get_vertex(exitid)
	path = [target.get_id()]
	shortest(target, path)
	print 'The shortest path : %s' %(path[::-1])
	
        #print path[len(path)-1]

# disconnect from server
db.close
#######################################################################
##Get directions given path
#######################################################################

path=path[::-1]
route = []

i=0

#print "Head %s %f meters to reach the first node" %(direction(currentlat, currentlong,map[findid(path[i])][3], map[findid(path[i])][4]), haversine(currentlat, currentlong,map[findid(path[i])][3], map[findid(path[i])][4])) 
while i < len(path)-1:
        if i==0:
                node1 = direction(map[findid(path[i])][3], map[findid(path[i])][4],map[findid(path[i+1])][3], map[findid(path[i+1])][4])
                node2 = direction(map[findid(path[i+1])][3], map[findid(path[i+1])][4],map[findid(path[i+2])][3], map[findid(path[i+2])][4])
        else:
                node1 = node2
                node2 = direction(map[findid(path[i])][3], map[findid(path[i])][4],map[findid(path[i+1])][3], map[findid(path[i+1])][4])
                
        route.append(direction2(node1,node2))
        i = i+1
print route
dist = 0
for i in range(len(route)):
        if i == 0:
                dist = distTillTurn(i,0)
        else:
                if route[i] != "straight":
                        print "%f meters till %s turn" %(dist,route[i])
                dist = distTillTurn(i,dist)
print "%f meters till %s" %(dist, map[findid(path[i+1])][2])

#print "Head %s %f meters to reach the first node then turn %s" %(direction(currentlat, currentlong,map[findid(path[i])][3], map[findid(path[i])][4]), haversine(currentlat, currentlong,map[findid(path[i])][3], map[findid(path[i])][4]))
        

        
