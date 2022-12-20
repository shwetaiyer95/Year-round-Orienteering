from PIL import Image
import sys
import math
from queue import *


class seasonNode:
    """
    Class to represent pixels in the terrain during seasonal changes for winter and spring
    """
    __slots__ = "coor", "count", "elevation", "terrainType"

    def __init__(self, coor):
        """
        Initializing the node
        :param coor: tuple of the x and y coordinate (x,y)
        """
        self.coor = coor
        self.count = 0
        self.elevation = 0


class starNode:
    """
    Class to represent pixels in the terrain while performing a* algorithm.
    """
    __slots__ = "parent", "xcoor", "ycoor", "elevation", "terrainType", "g","h","f"

    def __init__(self, parent, xcoor, ycoor):
        """
        Initialising the starNode
        :param parent: parent of the node in the algorithm
        :param xcoor: xcoordinate of this pixel
        :param ycoor: y-coordinate of this pixel
        """
        self.parent = parent
        self.xcoor = int(xcoor)
        self.ycoor = int(ycoor)
        self.elevation = 0
        self.g = float('inf')
        self.h = float('inf')
        self.f = float('inf')


terrainSlowness = {"Open land": 15, "Rough meadow": 40, "Easy movement forest": 25,
                "Slow run forest": 30, "Walk forest": 35, "Impassible vegetation": 90,
                "Lake": 100, "Paved road": 5, "Footpath": 10,
                "Out of bounds": 1000, "pathColor": 5, "Ice": 28, "Mud": 33}
terrainColor = {"Open land": (248,148,18), "Rough meadow": (255,192,0), "Easy movement forest": (255,255,255),
                "Slow run forest": (2,208,60), "Walk forest": (2,136,40), "Impassible vegetation": (5,73,24),
                "Lake": (0,0,255), "Paved road": (71,51,3), "Footpath": (0,0,0),
                "Out of bounds": (205,0,101), "pathColor": (255,0,255), "Ice": (0,255,255), "Mud": (153,76,0)}
pathColor = (255,0,255)

longitude = 10.29
latitude = 7.55


def distance(x,y):
    """
    Distance calculation when difference between one coordinate (x or y) is 0
    :param x: Either x or y distance
    :param y: difference in elevation between the two points
    :return: distance
    """
    return math.sqrt(x*x + y*y)


def distanceH(x,y,z):
    """
    Distance Calculation between two points including their elevation
    :param x: x axis distance between 2 points
    :param y: y axis distance between 2 points
    :param z: difference in elevation of the 2 points
    :return: distance
    """
    return math.sqrt(x * x + y * y + z * z)


def getG(current, neighbor, season):
    """
    Get the g cost between current and neighbor node.
    The cost calculation varies during fall season as the leaves fall. So, We have to increase the time for any paths
    through easy movement forest.
    :param current: point 1 for cost calculation
    :param neighbor: point 2 for cost calculation
    :param season: the current season
    :return: cost g of travelling from point 1 to point 2
    """
    if current.xcoor == neighbor.xcoor:
        dist = distance(latitude, abs(abs(neighbor.elevation) - abs(current.elevation)))
    else:
        dist = distance(longitude, abs(abs(neighbor.elevation) - abs(current.elevation)))
    if season.lower() == "fall":
        if current.terrainType == "Easy movement forest" or neighbor.terrainType == "Easy movement forest":
            return dist * (terrainSlowness[neighbor.terrainType] + 5)
        else:
            return dist * terrainSlowness[neighbor.terrainType]
    else:  # for summer, winter, spring
        return dist * terrainSlowness[neighbor.terrainType]


def getTerrainType(xcoor, ycoor, colors):
    """
    To get the type of terrain at current pixel coordinates
    :param xcoor: x coordinate of the point
    :param ycoor: y coordinate of the point
    :param colors: contains the RGB color code of the terrain
    :return: the terrain type of point (xcoor, ycoor)
    """
    color = colors[xcoor, ycoor]
    for terrainType in terrainColor:
        if terrainColor[terrainType] == color:
            return terrainType


def getH(current, destination, destElevation):
    """
    This function calculates the straight line distance from current to destination.
    That will give us the actual distance between the two points.
    We multiply the pixel difference by the meter distance (10.29 in longitude
    (X) and 7.55 m in latitude (Y))
    :param current: Point 1 for distance calculation. This is a starNode.
    :param destination: Point 2 for distance calculation. It is a tuple.
    :param destElevation: Elevation at Point 2
    :return: The H cost for travelling from current to destination
    """
    x = abs(abs(current.xcoor) - abs(int(destination[0]))) * longitude
    y = abs(abs(current.ycoor) - abs(int(destination[1]))) * latitude
    z = abs(abs(current.elevation) - abs(destElevation))
    return distanceH(x,y,z)


def getNeighborsList(terrain, current, colors, elevation, visited, notVisited):
    """
    This function will return a list of square neighbor nodes.
    If the node already exists, it is returned or a new node is created fro new pixel coordinates.
    If the coordinate has already been visited, then it is not returned as a part of the list.
    :param terrain: the terrain provided as input
    :param current: the x and y coordinate whose neighbors have to be listed
    :param colors: contains the RGB color code of the terrain
    :param elevation: elevation values from input file
    :param visited: dictionary of visited nodes
    :param notVisited: dictionary of nodes that have not been visisted yet
    :return: list of neighbors (square)
    """
    neighbors = list()
    width, height = terrain.size
    if current.xcoor > 0 and ((current.xcoor - 1, current.ycoor) not in visited):
        if (current.xcoor - 1, current.ycoor) not in notVisited:
            left = starNode(None, current.xcoor - 1, current.ycoor)
            left.elevation = elevation[current.xcoor - 1][current.ycoor]
            left.terrainType = getTerrainType(left.xcoor, left.ycoor, colors)
            neighbors.append(left)
        else:
            neighbors.append(notVisited[(current.xcoor - 1, current.ycoor)])
    if current.xcoor < width - 1 and ((current.xcoor + 1, current.ycoor) not in visited):
        if (current.xcoor + 1, current.ycoor) not in notVisited:
            right = starNode(None, current.xcoor + 1, current.ycoor)
            right.elevation = elevation[current.xcoor + 1][current.ycoor]
            right.terrainType = getTerrainType(right.xcoor, right.ycoor, colors)
            neighbors.append(right)
        else:
            neighbors.append(notVisited[(current.xcoor + 1, current.ycoor)])
    if current.ycoor > 0 and ((current.xcoor, current.ycoor - 1) not in visited):
        if (current.xcoor, current.ycoor - 1) not in notVisited:
            top = starNode(None, current.xcoor, current.ycoor - 1)
            top.elevation = elevation[current.xcoor][current.ycoor - 1]
            top.terrainType = getTerrainType(top.xcoor, top.ycoor, colors)
            neighbors.append(top)
        else:
            neighbors.append(notVisited[(current.xcoor, current.ycoor - 1)])
    if current.ycoor < height - 1 and ((current.xcoor, current.ycoor + 1) not in visited):
        if (current.xcoor, current.ycoor + 1) not in notVisited:
            bottom = starNode(None, current.xcoor, current.ycoor + 1)
            bottom.elevation = elevation[current.xcoor][current.ycoor + 1]
            bottom.terrainType = getTerrainType(bottom.xcoor, bottom.ycoor, colors)
            neighbors.append(bottom)
        else:
            neighbors.append(notVisited[(current.xcoor, current.ycoor + 1)])
    return neighbors


def astar(source, destination, terrain, colors, elevation, season):
    """
    Performs a* algorithm to find the path between two points on the terrain.
    Uses priority queue to get the lowest f cost node from the list of not visited nodes
    :param source: The starting point of the algorithm
    :param destination: End point of the algorithm
    :param terrain: the terrain provided as input
    :param colors: contains the RGB color code of the terrain
    :param elevation: elevation values from input file
    :param season: the current season
    :return: True if path is found. False otherwise. Also returns the dictionary of visited
    nodes so the path from source to destination can be constructed
    """
    notVisitedQueue = PriorityQueue()
    source = starNode(None, source[0], source[1])
    source.elevation = elevation[source.xcoor][source.ycoor]
    source.terrainType = getTerrainType(source.xcoor, source.ycoor, colors)
    source.g = 0
    source.h = getH(source, destination, elevation[int(destination[0])][int(destination[1])])
    source.f = source.g + source.h
    notVisited = dict()
    visited = dict()
    counter = 0
    notVisited[(source.xcoor, source.ycoor)] = source
    notVisitedQueue.put((source.f, counter, source))
    counter += 1
    while len(notVisited) > 0:
        current = notVisitedQueue.get()
        current = current[2]
        del notVisited[(current.xcoor, current.ycoor)]
        visited[(current.xcoor, current.ycoor)] = current
        if (current.xcoor, current.ycoor) == (int(destination[0]), int(destination[1])):
            return True, visited
        neighborList = getNeighborsList(terrain, current, colors, elevation, visited, notVisited)
        for neighbor in neighborList:
            g = getG(current, neighbor, season) + current.g
            h = getH(neighbor, destination, elevation[int(destination[0])][int(destination[1])])
            f = g + h
            if f < neighbor.f:
                neighbor.parent = current
                neighbor.g = g
                neighbor.h = h
                neighbor.f = f
                if (neighbor.xcoor, neighbor.ycoor) not in notVisited:
                    notVisitedQueue.put((neighbor.f, counter, neighbor))
                    counter += 1
                notVisited[(neighbor.xcoor, neighbor.ycoor)] = neighbor
    return False, visited


def getWaterNeighborList(row, column, width, height):
    """
    Returns a list of valid neighbors (square) within the terrain for given x and y coordinates
    :param row: x coordinate of the point
    :param column: y coordinate of the point
    :param width: width of the input terrain
    :param height: height of the input terrain
    :return: list of neighbors
    """
    neighborList = []
    if row > 0:
        neighborList.append((row - 1, column))
    if row < height - 1:
        neighborList.append((row + 1, column))
    if column > 0:
        neighborList.append((row, column - 1))
    if column < width - 1:
        neighborList.append((row, column + 1))
    return neighborList


def isWaterEdge(row, column, colors, width, height):
    """
    Determines if the pixel being considered is at the edge of a lake
    To be at the edge of a lake, the pixel itself has to be a lake and one of it's neighboring
    pixels but be non-lake
    :param row: the x coordinate of the point
    :param column: the y coordinate of the point
    :param colors: contains the RGB color code of the terrain
    :param width: width of the input terrain
    :param height: height of the input terrain
    :return: True if the given pixel is a at the edge of a lake. False, otherwise.
    """
    if getTerrainType(row, column, colors) == "Lake":
        neighborList = getWaterNeighborList(row, column, width, height)
        for eachNeighbor in neighborList:
            if getTerrainType(eachNeighbor[0], eachNeighbor[1], colors) != "Lake":
                return True
        return False
    else:
        return False


def getWaterEdges(terrain, colors):
    """
    Returns a list of pixel values that are at the edge of a lake
    :param terrain: input terrain
    :param colors: contains the RGB color code of the terrain
    :return: list of (x,y) points that are at the edges of the lake (water)
    """
    width, height = terrain.size
    waterEdgeList = []
    for row in range(width):
        for column in range(height):
            if isWaterEdge(row, column, colors, width, height):
                waterEdgeList.append((row,column))
    return waterEdgeList


def changeWinter(waterEdgeList, terrain, colors):
    """
    If the season is winter then, water within 7 pixels of non-water is safe to walk on.
    For this we first get the waterEdgeList and then perform BFS to search out all the affected
    pixel values
    :param waterEdgeList: list of (x,y) points that are at the edges of a lake
    :param terrain: the input terrain
    :param colors: contains the RGB color code of the terrain
    :return: None
    """
    width, height = terrain.size
    changeQueue = Queue()
    for eachPixel in waterEdgeList:
        node = seasonNode(eachPixel)
        changeQueue.put(node)
    while not changeQueue.empty():
        current = changeQueue.get()
        if current.count < 7:
            colors[current.coor[0], current.coor[1]] = terrainColor["Ice"]
            neighborList = getWaterNeighborList(current.coor[0], current.coor[1], width, height)
            for eachNeighbor in neighborList:
                if getTerrainType(eachNeighbor[0], eachNeighbor[1], colors) == "Lake":
                    node = seasonNode((eachNeighbor))
                    node.count = current.count + 1
                    changeQueue.put(node)


def changeSpring(waterEdgeList, terrain, colors, elevation):
    """
    If the season is spring, then, Any pixels within fifteen pixels of water that can be reached
    from a water pixel without gaining more than one meter of elevation (total) are now underwater.
    For this we first get the waterEdgeList and then perform BFS to search out all the affected
    pixel values.
    We mark these pixels as Mud.
    :param waterEdgeList: list of (x,y) points that are at the edges of a lake
    :param terrain: the input terrain
    :param colors: contains the RGB color code of the terrain
    :param elevation: elevation values from input file
    :return: None
    """
    width, height = terrain.size
    changeQueue = Queue()
    for eachPixel in waterEdgeList:
        nodeWater = seasonNode(eachPixel)
        neighborList = getWaterNeighborList(nodeWater.coor[0], nodeWater.coor[1], width, height)
        for eachNeighbor in neighborList:
            terrainType = getTerrainType(eachNeighbor[0], eachNeighbor[1], colors)
            if terrainType != "Lake":
                node = seasonNode((eachNeighbor))
                node.terrainType = terrainType
                changeQueue.put(node)
    while not changeQueue.empty():
        current = changeQueue.get()
        if current.count < 15 and current.elevation <= 1 and current.terrainType != "Out of bounds":
            colors[current.coor[0], current.coor[1]] = terrainColor["Mud"]
            neighborList = getWaterNeighborList(current.coor[0], current.coor[1], width, height)
            for eachNeighbor in neighborList:
                terrainType = getTerrainType(eachNeighbor[0], eachNeighbor[1], colors)
                if terrainType != "Lake" and terrainType != "Mud":
                    node = seasonNode((eachNeighbor))
                    node.elevation = abs(elevation[eachNeighbor[0]][eachNeighbor[1]] -
                                         abs(elevation[current.coor[0]][current.coor[1]]))
                    node.count = current.count + 1
                    node.terrainType = terrainType
                    changeQueue.put(node)


def main():
    """
    Takes input from user and creates a 2D array of elevation from elevation file.
    Depending on the season, changes the terrain if required.
    Finds the path between given points. Also calculates the total path length.
    :return: None
    """
    terrainImageName = sys.argv[1]
    elevationFileName = sys.argv[2]
    pathFileName = sys.argv[3]
    season = sys.argv[4]
    outputFileName = sys.argv[5]
    terrain = Image.open(terrainImageName).convert('RGB')
    colors = terrain.load()
    width, height = terrain.size
    elevationFileValues = open(elevationFileName)
    # creating elevation 2D array
    elevation = [[0 for _ in range(height)] for _ in range(width)]
    # setting the values in array from the elevation file
    for row in range(height):
        eachRow = elevationFileValues.readline().split()
        for column in range(width):
            elevation[column][row] = float(eachRow[column])
    elevationFileValues.close()

    #Season change
    if season.lower() == "winter":
        waterEdgeList = getWaterEdges(terrain, colors)
        changeWinter(waterEdgeList, terrain, colors)
    if season.lower() == "spring":
        waterEdgeList = getWaterEdges(terrain, colors)
        changeSpring(waterEdgeList, terrain, colors, elevation)

    paths = []
    # Reading the paths
    with open(pathFileName) as file:
        for eachLine in file:
            x, y = eachLine.split()
            paths.append((x,y))

    # performing a*
    totalDistance = 0
    for i in range(len(paths)-1):
        source = paths[i]
        destination = paths[i+1]
        result, visited = astar(source, destination, terrain, colors, elevation, season)
        if result is True:
            current = visited[(int(destination[0]), int(destination[1]))]
            colors[current.xcoor, current.ycoor] = pathColor
            while (current.xcoor, current.ycoor) != (int(source[0]), int(source[1])):
                colors[current.xcoor, current.ycoor] = terrainColor["pathColor"]
                totalDistance = totalDistance + distanceH((current.xcoor - current.parent.xcoor)*longitude,
                                                          (current.ycoor - current.parent.ycoor)*latitude,
                                                          (current.elevation - current.parent.elevation))
                current = current.parent
            colors[current.xcoor, current.ycoor] = pathColor
    for path in paths:
        xcoor = int(path[0])
        ycoor = int(path[1])
        colors[xcoor + 1, ycoor + 1] = pathColor
        colors[xcoor - 1, ycoor - 1] = pathColor
        colors[xcoor + 1, ycoor - 1] = pathColor
        colors[xcoor - 1, ycoor + 1] = pathColor
        colors[xcoor + 1, ycoor] = pathColor
        colors[xcoor - 1, ycoor] = pathColor
        colors[xcoor, ycoor + 1] = pathColor
        colors[xcoor, ycoor - 1] = pathColor
    terrain.save(outputFileName)
    terrain.show()
    print("Total Path Length (in meters):", round(totalDistance))


if __name__ == '__main__':
    main()
