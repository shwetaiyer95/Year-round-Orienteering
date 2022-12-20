# Year-round Orienteering

## Cost Function (G):
To calculate the cost g, the straight-line distance between the two points is needed and the estimated impact of the terrain on the overall time taken.

**The distance is calculated by the formula -> sqrt(Δx2 + Δy2 + Δz2).**

Only square edges are considered as neighbors i.e. pixel to the right, left, top and bottom are considered as neighbors. Therefore, For a neighbor node from the current node, either the x or y coordinate would be the same.
The distance is calculated in meters.

***Impact due to Terrain type***<br>
Some terrains are easier to travel through while others aren’t. To calculate the cost of travelling to that terrain, a dictionary has been created with terrain types as key and time as value. The time is written based on how long it will take to travel x meters in that terrain.

For example, paved road will take the least time as it is a wide flat road, followed closely by footpath as the road is not as wide as the paved road. The values are written based on how easy/difficult it would be to travel through these terrains by foot. Similarly, impassible vegetation would be of a higher value as it is difficult to travel through. Lake would also be difficult to travel through by foot so it also has a higher value. Out of bounds would be the highest value as it is a path that should not be taken.

***The final g cost calculation = straight-line distance between the 2 points * impact of terrain type***

Accounting for the difficulty to travel through the terrain ensures that if there are two paths from point A to B. Path 1 whose distance is slightly longer but includes passing through easier terrains. Path 2 whose distance is shorter but includes travelling through difficult terrains. If path 1 and 2 are weighed against each other, Path 1 is picked as it will get to Point 2 faster.<br>

## Heuristic Cost Function (H):
The heuristic cost calculation is the straight line distance between two points, sqrt(Δx2 + Δy2 + Δz2)

The distance is calculated in meters.

The impact of terrain type is not multiplied by the distance for heuristic cost calculation, as heuristic cost is the optimal cost. Only the straight-line distance which is not affected by the difficulty of travelling through any type of terrain is required.

## Seasonal changes:
There are 4 seasons - Summer, Fall, Winter and Spring

For summer, there are no changes to the terrain. For fall, the time taken to cross any path through and adjacent to ‘Easy movement forest’ is increased during g cost calculation.

For Winter, first, a list of all the pixels that are at the edges of lake is obtained. From those points, BFS is performed inwards to color the relevant pixels to indicate ice.

Similarly, for Spring, a list of all the pixels that are at the edges of lake is obtained. From those points, BFS is performed outwards to color the relevant pixels in-order to indicate mud.

## Output:
A* algorithm is performed for every consecutive (x,y) pair in the given file. For example, For the first run, the first (x,y) pair is the source and second is the destination. For the second run, the second (x,y) pair is the source and the third (x,y) pair is the destination and so on.

The total path length is calculated in meters and displayed on the terminal. Additionally, the path that is travelled is colored in pink on the terrain and displayed at the end of all the runs. The (x,y) coordinate pairs mentioned in the input file are highlighted by coloring all the 8 adjacent pixels to pink. The updated image is also saved in the directory with the same name as the one provided in the command line arguments.
