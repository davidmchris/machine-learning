# Machine Learning Engineer Nanodegree
## Capstone Project
David Christensen  
January 17th, 2017

## I. Definition
_(approx. 1-2 pages)_

### Project Overview
In this section, look to provide a high-level overview of the project in layman’s terms. Questions to ask yourself when writing this section:
- _Has an overview of the project been provided, such as the problem domain, project origin, and related datasets or input data?_
- _Has enough background information been given so that an uninformed reader would understand the problem domain and following problem statement?_

Micromouse competitions have been around since the late 1970's. In the competition, a robot mouse solves a 16x16 maze. The mouse gets two runs, the first to explore the maze and the second to find it's way to the goal in the center of the maze. The mice are ranked based on how much time they use in the first and second runs. 

While the real micromouse competitions use physical robot mice, this project just simulates the maze and movement of the mouse in discrete timesteps. Each maze is a virtual grid. It is stored in a text file that defines where the walls are. The mazes range from 12x12 to 16x16.

### Problem Statement
In this section, you will want to clearly define the problem that you are trying to solve, including the strategy (outline of tasks) you will use to achieve the desired solution. You should also thoroughly discuss what the intended solution will be for this problem. Questions to ask yourself when writing this section:
- _Is the problem statement clearly defined? Will the reader understand what you are expecting to solve?_
- _Have you thoroughly discussed how you will attempt to solve the problem?_
- _Is an anticipated solution clearly defined? Will the reader understand what results you are looking for?_

Like the real competitions, the mouse gets two runs, the first to explore the maze and the second to get to the center as fast as possible.

The purpose of the first run is to explore the maze. In Naoki Shibuya's capstone project he uses four types of exploration algorithms:
 - Random
 - Dead end avoidance
 - Visit count
 - Visit count with heuristic
 For more information see [his paper](https://github.com/udacity/machine-learning/blob/master/projects/capstone/report-example-3.pdf).
 
 I will use the random and visit count methods to do my exploration as well as trying A\*. A\* is normally used to find the shortest path to the goal when the maze is already known. My algorithm uses A\* to reach the goal by replanning every time something new is learned like Stanley, the car that won the DARPA challenge for self driving cars. It then switches the heuristic to go back to the start. Once it reaches the start, it goes back towards the goal again. It continues in this way until it traverses the same path to the goal twice. This should be the shortest path.
 
 The greater the maze coverage that the robot can get in the first run, the more likely it is to find the shortest path in the second run. Since the moves in the second run are 30 times more expensive than the moves in the first run, it makes sense to use 30 more moves during run 1 to decrease the shortest path by one move during run 2.

The purpose of the second run is to get to the goal as fast as possible. While there are multiple ways to find the path to the goal of a maze, A\* will find the shortest path efficiently. If the whole maze is not explored, the algorithm will have to be re-run every time something new is seen just like in the exploration phase. I use A\* in the second run for all of my controllers.

I expect that the visit count with heuristic controller will be the most consistently best performer, but I expect the A\* return algorithm to work better on some mazes.


### Metrics
In this section, you will need to clearly define the metrics or calculations you will use to measure performance of a model or result in your project. These calculations and metrics should be justified based on the characteristics of the problem and problem domain. Questions to ask yourself when writing this section:
- _Are the metrics you’ve chosen to measure the performance of your models clearly discussed and defined?_
- _Have you provided reasonable justification for the metrics chosen based on the problem and solution?_

These are the metrics I have defined for evaluating my algorithms:

 - N1: Number of moves in the first run
 - N2: Number of moves in the second run
 - Mouse score: N2 + N1/30
 - Exploration efficiency: (j / j\_total) / N1 where j is number of known maze cell junctions and j\_total is the total number of cell junctions in the maze.
 
 N1 will give an idea of how many moves 

## II. Analysis
_(approx. 2-4 pages)_

### Data Exploration
In this section, you will be expected to analyze the data you are using for the problem. This data can either be in the form of a dataset (or datasets), input data (or input files), or even an environment. The type of data should be thoroughly described and, if possible, have basic statistics and information presented (such as discussion of input features or defining characteristics about the input or environment). Any abnormalities or interesting qualities about the data that may need to be addressed have been identified (such as features that need to be transformed or the possibility of outliers). Questions to ask yourself when writing this section:
- _If a dataset is present for this problem, have you thoroughly discussed certain features about the dataset? Has a data sample been provided to the reader?_
- _If a dataset is present for this problem, are statistics about the dataset calculated and reported? Have any relevant results from this calculation been discussed?_
- _If a dataset is **not** present for this problem, has discussion been made about the input space or input data for your problem?_
- _Are there any abnormalities or characteristics about the input space or dataset that need to be addressed? (categorical variables, missing values, outliers, etc.)_

The mazes are defined by input files which have 4-bit integers where the bits represent which sides of each square have walls. The mouse can occupy one square at a time and moves in discrete jumps. The mouse cannot move through walls. The center of the maze is a 2x2 goal area. After the mouse reaches the goal on the first run, it can keep exploring or choose to end the run. The mouse starts both runs in the bottom left corner, facing up. The starting square has walls on three sides with the open side facing up. There is a wall running around the outside of the maze blocking the mouse from leaving.

Some of the first questions I had when starting this project was why the mouse doesn't have a back sensor and why the tester does not provide the location of the robot in the next_move method. After thinking it through, the mouse does not need a back sensor since it is known the mouse starts at 0,0 with walls on three sides. Since the mouse first rotates, then moves, it will see any square using its sensors before it gets there. The tester does not provide the location of the robot because robots in the real world have to perform localization. Due to the discrete nature of the simulation and the exact movements, there will never be any doubt about where the robot is as long as it doesn't make a move that would crash it into a wall.

Each maze has some charactersitics that make it difficult or impossible for some maze solving algorithms to work. For example, in all three test mazes the goal walls are not connected to the outer walls of the maze. This would prevent a wall-following algorithm from finding the goal.

### Exploratory Visualization
In this section, you will need to provide some form of visualization that summarizes or extracts a relevant characteristic or feature about the data. The visualization should adequately support the data being used. Discuss why this visualization was chosen and how it is relevant. Questions to ask yourself when writing this section:
- _Have you visualized a relevant characteristic or feature about the dataset or input data?_
- _Is the visualization thoroughly analyzed and discussed?_
- _If a plot is provided, are the axes, title, and datum clearly defined?_

Shortest paths:

####Maze 1
![Maze 1](images/maze_1_shortest_path.png )
####Maze 2
![Maze 2](images/maze_2_shortest_path.png )
####Maze 3
![Maze 3](images/maze_3_shortest_path.png )

As can be seen in each of these mazes, the shortest path (in terms of number of moves) goes to the outside of the maze. Due to the heuristic, A\* is not ideally suited to explore the outer edges of the maze. For example, here is a visualization of the heuristic value for each cell in maze 1:

4, 4, 3, 3, 3, 2, 2, 3, 3, 3, 4, 4
4, 4, 3, 3, 3, 2, 2, 3, 3, 3, 4, 4
3, 3, 2, 2, 2, 1, 1, 2, 2, 2, 3, 3
3, 3, 2, 2, 2, 1, 1, 2, 2, 2, 3, 3
3, 3, 2, 2, 2, 1, 1, 2, 2, 2, 3, 3
2, 2, 1, 1, 1, 0, 0, 1, 1, 1, 2, 2
2, 2, 1, 1, 1, 0, 0, 1, 1, 1, 2, 2
3, 3, 2, 2, 2, 1, 1, 2, 2, 2, 3, 3
3, 3, 2, 2, 2, 1, 1, 2, 2, 2, 3, 3
3, 3, 2, 2, 2, 1, 1, 2, 2, 2, 3, 3
4, 4, 3, 3, 3, 2, 2, 3, 3, 3, 4, 4
4, 4, 3, 3, 3, 2, 2, 3, 3, 3, 4, 4

At the goal the heuristic is 0 and the numbers get higher the further away the cell is. This causes the A* algorithm to want to stay aligned with the goal and as close to it as possible. In maze 1 the shortest path goes around the outside of the maze in the bottom right corner where the heuristic is the highest. The A\* algorithm will not find the shortest path quickly in this circumstance. There is a difference though in how fast the algorithm runs versus how fast the robot finds the goal. Once A\* is done, it has found the shortest path (according to the knowledge it has of the maze). This means it will find the center of the maze quickly.

As Shibuya has shown, the robot must avoid dead ends and loops. The random algorithm will not avoid them and A* and the visit count both will avoid them as soon as they are known.

### Algorithms and Techniques
In this section, you will need to discuss the algorithms and techniques you intend to use for solving the problem. You should justify the use of each one based on the characteristics of the problem and the problem domain. Questions to ask yourself when writing this section:
- _Are the algorithms you will use, including any default variables/parameters in the project clearly defined?_
- _Are the techniques to be used thoroughly discussed and justified?_
- _Is it made clear how the input data or datasets will be handled by the algorithms and techniques chosen?_

There are two kinds of algorithms the robot needs to use. The first is for exploration and the second is for seeking the goal. If the robot has explored enough of the maze to have discovered the shortest path in run 1, A* is the optimal algorithm for using on the second run since it is guaranteed to find the shortest path. I used A* for each of the algorithms on the second run which makes the exploration algorithms of more interest. In the following sections I will describe each of the exploration algorithms.

####Random algorithm
The random algorithm simply chooses a move at random from the possible moves. It will not move in any specific direction, avoid loops or dead ends. This algorithm is included only as a benchmark. Any algorithm that is worth using should outperform it.

####Visit count algorithm
This algorithm keeps track how many times it has visited each cell. When it chooses between the possible moves, it will choose the one with the lowest number of visits. This basically provides a gradient which the robot follows down-hill. This pushes the robot away from areas it has already explored. This algorithm is efficient for exploring the maze. It is not directional like A\*, but as long as the algorithm enters the goal at some point, that's fine. The stopping criteria could have a large effect on the final score. Shibuya added a heuristic to break ties for this algorithm and it seems to have worked quite well. 

####A\* Return Algorithm
The idea behind this algorithm is that you don't need to explore the entire maze to find the shortest path. Since A\* is guaranteed to find the shortest path, if it goes from the start to the goal enough times, it will discover the shortest path. The mouse first tries to make its way to the goal. When it discovers a new wall, it re-plans the route. Once at the goal, it returns to the start, re-planning when necessary. The first time it makes it all the way to the goal without  seeing any new walls, it will have found the shortest path and the mouse is reset for run 2.

### Benchmark
In this section, you will need to provide a clearly defined benchmark result or threshold for comparing across performances obtained by your solution. The reasoning behind the benchmark (in the case where it is not an established result) should be discussed. Questions to ask yourself when writing this section:
- _Has some result or value been provided that acts as a benchmark for measuring performance?_
- _Is it clear how this result or value was obtained (whether by data or by hypothesis)?_

The benchmark for the different algorithms is the random algorithm. I will be comparing results for the other algorithms against this one.

## III. Methodology
_(approx. 3-5 pages)_

### Data Preprocessing
There was no data pre-processing required because the mouse knows nothing about the maze in the beginning.

### Implementation
In this section, the process for which metrics, algorithms, and techniques that you implemented for the given data will need to be clearly documented. It should be abundantly clear how the implementation was carried out, and discussion should be made regarding any complications that occurred during this process. Questions to ask yourself when writing this section:
- _Is it made clear how the algorithms and techniques were implemented with the given datasets or input data?_
- _Were there any complications with the original metrics or techniques that required changing prior to acquiring a solution?_
- _Was there any part of the coding process (e.g., writing complicated functions) that should be documented?_

####Controllers
I created a base class and 4 sub-classes for controlling the robot:
 - RobotController (the base class)
 - RandomController
 - VisitCountController
 - PureAStarController
 - AStarReturnController
 
#####RobotController
The RobotController class is responsible for directing the overall strategy of the robot. The RobotController base class defines the next\_move method which all of the other subclasses must implement. This is the method called by the robot class. It also implements a number of other useful methods that the subclasses can take advantage of. The base class owns the maze map, the location and heading of the robot, and the planner used to get the next move.

#####RandomController
This class implements the random mouse algorithm. It chooses the next move from a list of possible moves. The possible moves are the ones that won't run the robot into a wall.

#####VisitCountController
This class uses two different planners. It uses the VisitCountPlanner during run 1 and the AStarPlanner during run 2. To end the first run the controller must have explored a certain percentage of the maze as well as enter the goal area at some point during the process. Once in run 2, the planner is switched over to the AStarPlanner and the controller tries to make it to the goal as fast as possible.

#####PureAStarController
This controller uses the AStarPlanner exclusively and is very simple. It just uses A\* to get to the goal as fast as possible for both runs.

####Planners
I created a Planner base class and three planner sub-classes:

#####Planner
The Planner is responsible for deciding what the next move should be. This is the base class for the other planners and is used by the different controller classes. It defines a next_move method which is overridden by each of the sub-classes. It also defines the replan method which is called whenever the map is updated. It is really only necessary for the AStarPlanner, but is included for convenience. The Planner class also keeps track of the percentage of the maze visited by the robot.

#####RandomPlanner
The RandomPlanner just chooses a random move from the list of available moves every time next_move is called.

#####VisitCountPlanner
The VisitCountPlanner keeps track of the places it has been in the maze and chooses the move that gets it to the square with the least amount of visits.

#####AStarPlanner
This is the planner used in run 2 by all controllers. It implements the A* algorithm. It is initialized with the maze map and a MazeHeuristic class. The MazeHeuristic can be switched out by the AStarReturnController to direct the robot either to the goal or back to the start.

####The maze map
The MazeMap class is used by the planner classes, the heuristic classes and the controller classes. It keeps track of known walls and can provide a list of possible moves given a location and direction. It is basically a graph where the nodes are positions in the maze and the edges are the junctions between the cells (whether is has a wall or not).

### Refinement
In this section, you will need to discuss the process of improvement you made upon the algorithms and techniques you used in your implementation. For example, adjusting parameters for certain models to acquire improved solutions would fall under the refinement category. Your initial and final solutions should be reported, as well as any significant intermediate results as necessary. Questions to ask yourself when writing this section:
- _Has an initial solution been found and clearly reported?_
- _Is the process of improvement clearly documented, such as what techniques were used?_
- _Are intermediate and final solutions clearly reported as the process is improved?_

After trying out the PureAStarController, I was unable to get a better score than using the VisitCountPlanner. I started thinking of ways that would improve the exploration. I came to the conclusion that the VisitCountPlanner was hard to beat in terms of efficiently exploring an unknown maze since it will always choose a cell it hasn't been to over a cell it has been to. Once I realized that I actually don't want to explore the whole maze, I made a breakthrough. The only part of the maze that I actually want to explore is the shortest path. The A* algorithm is guranteed to get the shortest path given an admissible heuristic (one that does not over estimate the number of moves to the goal). It makes sense then, that if you were to send the robot back and forth between the goal and the start square, it would learn the shortest path eventually without exploring the entire maze. That's where the idea for the AStarReturnController came from.

#####AStarReturnController
Similar to the PureAStarController, this controller exclusively uses A*, but instead of resetting after hitting the goal, it changes the heuristic in the A* planner to get back to the start square at (0,0). When it reaches the start square, it switches the heuristic back to get back to the goal. It will go back and forth between the start square and the goal until it no longer has to replan on the way to the goal. At this point it has found the optimal path since if there was a better path in an unexplored part of the maze (which has no walls as far as A* is concerned) it would go towards the unexplored part of the maze, discover new walls, and have to replan. On the second run, it just goes to the goal as fast as possible using A* since it has found the optmal path.

## IV. Results
_(approx. 2-3 pages)_

### Model Evaluation and Validation
In this section, the final model and any supporting qualities should be evaluated in detail. It should be clear how the final model was derived and why this model was chosen. In addition, some type of analysis should be used to validate the robustness of this model and its solution, such as manipulating the input data or environment to see how the model’s solution is affected (this is called sensitivity analysis). Questions to ask yourself when writing this section:
- _Is the final model reasonable and aligning with solution expectations? Are the final parameters of the model appropriate?_
- _Has the final model been tested with various inputs to evaluate whether the model generalizes well to unseen data?_
- _Is the model robust enough for the problem? Do small perturbations (changes) in training data or the input space greatly affect the results?_
- _Can results found from the model be trusted?_

| Controller | Run 1 moves | Run 2 moves | Score | Efficiency |
| :--- | :---: | :---: | :---: | :---: |
| RandomController | 1000 | 35 | 67.42 | 234 |
| VisitCountController | 100 | 35 | 24.13 | 234 |
| PureAStarController | 45 | 35 | 28.34 | 234 |
| AStarReturnController | 65 | 35 | 25.97 | 234 |


### Justification
In this section, your model’s final solution and its results should be compared to the benchmark you established earlier in the project using some type of statistical analysis. You should also justify whether these results and the solution are significant enough to have solved the problem posed in the project. Questions to ask yourself when writing this section:
- _Are the final results found stronger than the benchmark result reported earlier?_
- _Have you thoroughly analyzed and discussed the final solution?_
- _Is the final solution significant enough to have solved the problem?_


## V. Conclusion
_(approx. 1-2 pages)_

### Free-Form Visualization
In this section, you will need to provide some form of visualization that emphasizes an important quality about the project. It is much more free-form, but should reasonably support a significant result or characteristic about the problem that you want to discuss. Questions to ask yourself when writing this section:
- _Have you visualized a relevant or important quality about the problem, dataset, input data, or results?_
- _Is the visualization thoroughly analyzed and discussed?_
- _If a plot is provided, are the axes, title, and datum clearly defined?_

### Reflection
In this section, you will summarize the entire end-to-end problem solution and discuss one or two particular aspects of the project you found interesting or difficult. You are expected to reflect on the project as a whole to show that you have a firm understanding of the entire process employed in your work. Questions to ask yourself when writing this section:
- _Have you thoroughly summarized the entire process you used for this project?_
- _Were there any interesting aspects of the project?_
- _Were there any difficult aspects of the project?_
- _Does the final model and solution fit your expectations for the problem, and should it be used in a general setting to solve these types of problems?_

### Improvement
In this section, you will need to provide discussion as to how one aspect of the implementation you designed could be improved. As an example, consider ways your implementation can be made more general, and what would need to be modified. You do not need to make this improvement, but the potential solutions resulting from these changes are considered and compared/contrasted to your current solution. Questions to ask yourself when writing this section:
- _Are there further improvements that could be made on the algorithms or techniques you used in this project?_
- _Were there algorithms or techniques you researched that you did not know how to implement, but would consider using if you knew how?_
- _If you used your final solution as the new benchmark, do you think an even better solution exists?_

-----------

**Before submitting, ask yourself. . .**

- Does the project report you’ve written follow a well-organized structure similar to that of the project template?
- Is each section (particularly **Analysis** and **Methodology**) written in a clear, concise and specific fashion? Are there any ambiguous terms or phrases that need clarification?
- Would the intended audience of your project be able to understand your analysis, methods, and results?
- Have you properly proof-read your project report to assure there are minimal grammatical and spelling mistakes?
- Are all the resources used for this project correctly cited and referenced?
- Is the code that implements your solution easily readable and properly commented?
- Does the code execute without error and produce results similar to those reported?
