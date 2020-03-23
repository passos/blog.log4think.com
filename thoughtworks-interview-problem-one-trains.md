---
title: ThoughtWorks 的一道笔试题
date: '2008-12-11 23:37:38 +0800'
---

# 2008-12-11  ThoughtWorks 的一道笔试题

PROBLEM ONE: TRAINS

Problem: The local commuter railroad services a number of towns in Kiwiland. Because of monetary concerns, all of the tracks are 'one-way.' That is, a route from Kaitaia to Invercargill does not imply the existence of a route from Invercargill to Kaitaia. In fact, even if both of these routes do happen to exist, they are distinct and are not necessarily the same distance!

The purpose of this problem is to help the railroad provide its customers with information about the routes. In particular, you will compute the distance along a certain route, the number of different routes between two towns, and the shortest route between two towns.

Input: A directed graph where a node represents a town and an edge represents a route between two towns. The weighting of the edge represents the distance between the two towns. A given route will never appear more than once, and for a given route, the starting and ending town will not be the same town.

Output: For test input 1 through 5, if no such route exists, output 'NO SUCH ROUTE'. Otherwise, follow the route as given; do not make any extra stops! For example, the first problem means to start at city A, then travel directly to city B \(a distance of 5\), then directly to city C \(a distance of 4\).

1. The distance of the route A-B-C.
2. The distance of the route A-D.
3. The distance of the route A-D-C.
4. The distance of the route A-E-B-C-D.
5. The distance of the route A-E-D.
6. The number of trips starting at C and ending at C with a maximum of 3 stops.  In the sample data below, there are two such trips: C-D-C \(2 stops\). and C-E-B-C \(3 stops\).
7. The number of trips starting at A and ending at C with exactly 4 stops.  In the sample data below, there are three such trips: A to C \(via B,C,D\); A to C \(via D,C,D\); and A to C \(via D,E,B\).
8. The length of the shortest route \(in terms of distance to travel\) from A to C.
9. The length of the shortest route \(in terms of distance to travel\) from B to B.
10. The number of different routes from C to C with a distance of less than 30.  In the sample data, the trips are: CDC, CEBC, CEBCDC, CDCEBC, CDEBC, CEBCEBC, CEBCEBCEBC.

Test Input:

For the test input, the towns are named using the first few letters of the alphabet from A to D. A route between two towns \(A to B\) with a distance of 5 is represented as AB5.

Graph: AB5, BC4, CD8, DC8, DE6, AD5, CE2, EB3, AE7

Expected Output:

Output \#1: 9 Output \#2: 5 Output \#3: 13 Output \#4: 22 Output \#5: NO SUCH ROUTE Output \#6: 2 Output \#7: 3 Output \#8: 9 Output \#9: 9

## Output \#10: 7

用一个带权重的有向图表示节点之间的关系，使用深度优先搜索。

1-5:

```text
package com.log4think.code;

public class TrainMap {

    public int[][] map = {
        //    A   B   C   D   E
            {-1,  5, -1,  5,  7},
            {-1, -1,  4, -1, -1},
            {-1, -1, -1,  8,  2},
            {-1, -1,  8, -1,  6},
            {-1,  3, -1, -1, -1},
    };

    public int getDistance(String path)
    {
        int distance = 0;

        for (int i=0; i
<path.length()-1; i++) {
            // get the node index in map
            int fromNodeIndex = path.charAt(i) - 'A';
            int toNodeIndex = path.charAt(i+1) - 'A';

            // check the distance of two node in map
            if (map[fromNodeIndex][toNodeIndex] == -1) {
                return -1;
            } else {
                distance += map[fromNodeIndex][toNodeIndex];
            }
        }

        return distance;
    }

    public static void main(String[] args) {
        TrainMap g = new TrainMap();

        int distance = g.getDistance("ABC");
        if (distance > 0)
            System.out.println(distance);
        else
            System.out.println("NO SUCH ROUTE");

//        g.findDistance("AD");
//        g.findDistance("ADC");
//        g.findDistance("AEBCD");
//        g.findDistance("AED");
    }
}
```

6:

```text
public class TrainMap {

    public int[][] map = {
            {-1, 5, -1, 5, 7},
            {-1, -1, 4, -1, -1},
            {-1, -1, -1, 8, 2},
            {-1, -1, 8, -1, 6},
            {-1, 3, -1, -1, -1},
    };

    // used to record the trip round count
    public int tripCount = 0;

    /***
     *
     * @param end , the end node. if we reach it we found a path
     * @param path , the current path we already have
     * @param maxLength, the maximum stops
     */
    public void dfs(String end, String path, int maxLength)
    {
        // this is for debug and trace
        // System.out.println(";; " + path);

        // if the path reach the maximum stops, then cancel search
        if (path.length() - 1 > maxLength) return;

        // check if we have reach the "end" node
        if ( path.length() > 1 && path.endsWith(end) ) {
            System.out.println(path + ", " + tripCount);
            tripCount ++;
        }

        // caculate the lastest node index in map
        char lastChar = path.charAt(path.length()-1);
        int lastNodeIndex = lastChar - 'A';

        // loop all nodes in map which connected to lastNode, and try it
        for ( int i=0; i
<map[lastNodeIndex].length; i++ )
        {
            // convert index to node name
            char newChar = (char)(i + 'A');
            // try and search
            if ( map[lastNodeIndex][i] > 0) {
                dfs(end, path + newChar, maxLength);
            }
        }
    }

    public static void main(String[] args) {
        TrainMap g = new TrainMap();

        g.dfs("C", "C", 3);
    }
}
```

7:

```text
public class TrainMap {

    public int[][] map = {
            { -1, 5, -1, 5, 7 },
            { -1, -1, 4, -1, -1 },
            { -1, -1, -1, 8, 2 },
            { -1, -1, 8, -1, 6 },
            { -1, 3, -1, -1, -1 }
    };

    public void bfs(String start, String end, int hops) {
        String lastRoute = start;

        for (int hop = 0; hop < hops; hop++) {
            String route = "";
            for (int i = 0; i < lastRoute.length(); i++) {
                char c = lastRoute.charAt(i);
                int id = c - 'A';

                for (int j = 0; j < map[id].length; j++) {
                    if (map[id][j] > 0)
                        route = route + (char) (j + 'A');
                }
            }
//          System.out.println(lastRoute);
            lastRoute = route;
        }

//      System.out.println(lastRoute);
        System.out.println(lastRoute.split(end).length - 1);
    }

    public static void main(String[] args) {
        TrainMap g = new TrainMap();

        g.bfs("A", "C", 4);
    }
}
```

8/9:

```text
public class TrainMap {

    public int[][] map = {
            {-1, 5, -1, 5, 7},
            {-1, -1, 4, -1, -1},
            {-1, -1, -1, 8, 2},
            {-1, -1, 8, -1, 6},
            {-1, 3, -1, -1, -1},
    };

    public void dfs(String end, String path, int cost) {
        if (path.endsWith(end) && cost < bestCost && cost > 0) {
            bestPath = path;
            bestCost = cost;
            return;
        }
        char lastChar = path.charAt(path.length() - 1);
        int lastNodeIndex = lastChar - 'A';

        for (int i = 0; i < map[lastNodeIndex].length; i++) {
            char newChar = (char) (i + 'A');
            int newCost = map[lastNodeIndex][i];
            if (newCost > 0) {
                if (path.indexOf(newChar) > 0)
                    continue;
                dfs(end, path + newChar, cost + newCost);
            }
        }
    }

    public String bestPath = "";
    public int bestCost = Integer.MAX_VALUE;

    public static void main(String[] args) {
        TrainMap g = new TrainMap();

        g.dfs("C", "A", 0); // 8
//      g.dfs("B", "B", 0); // 9

        System.out.println("Best Path: " + g.bestPath + "\nCost: " + g.bestCost);
    }
}
```

10:

```text
public class TrainMap {

    public int[][] map = {
            {-1, 5, -1, 5, 7},
            {-1, -1, 4, -1, -1},
            {-1, -1, -1, 8, 2},
            {-1, -1, 8, -1, 6},
            {-1, 3, -1, -1, -1},
    };

    public void dfs(String end, String path, int cost) {
        if (cost >= 30)
            return;

        if (cost > 0 && path.endsWith(end)) {
            System.out.println(path + ", " + cost);
        }

        char lastChar = path.charAt(path.length() - 1);
        int lastNodeIndex = lastChar - 'A';

        for (int i = 0; i < map[lastNodeIndex].length; i++) {
            char newChar = (char) (i + 'A');
            int newCost = map[lastNodeIndex][i];
            if (newCost > 0) {
                dfs(end, path + newChar, cost + newCost);
            }
        }
    }

    public static void main(String[] args) {
        TrainMap g = new TrainMap();

        g.dfs("C", "C", 0);
    }
}
```

