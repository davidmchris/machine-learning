# Machine Learning Engineer Nanodegree
## Capstone Proposal
David Christensen
December 10th, 2016

### Domain Background
_(approx. 1-2 paragraphs)_

In this section, provide brief details on the background information of the domain from which the project is proposed. Historical information relevant to the project should be included. It should be clear how or why a problem in the domain can or should be solved. Related academic research should be appropriately cited in this section, including why that research is relevant. Additionally, a discussion of your personal motivation for investigating a particular problem in the domain is encouraged but not required.

Micromouse competitions have been around since the late 1970's. In the competition, a robot mouse solves a 16x16 maze. The mouse gets two runs, the first to explore the maze and the second to find it's way to the goal (the center of the maze). Whichever mouse reaches the center in the shortest amount of time wins. Different graph traversal algorithms have been used to determine the path to the center. Djikstra's algorithm and A* are popular search algorithms to find the shortest path between two nodes on a graph. Exploration of the maze (or graph) could be accomplished many ways. One possible solution is to use Q-learning to make the mouse avoid areas it has already been to by assigning negative reward for each move that puts the mouse in a location it has already visited.

I'm interested in this problem because I am interested in robotics in general and it could advance my career since I am a mechanical engineer.

### Problem Statement

A micromouse must be able to explore, map and solve a maze as fast as possible. Unlike the real micromouse competition, the mouse will do it in a discrete domain. The maze is a 16x16 grid of squares. Each turn will consist of two parts:<br>
1. deciding which direction to turn (if any)
2. moving up to 3 squares in the chosen direction

The robot will be scored based on this formula:

N2 + N1/30 where N1+N2 <= 1000

Where N1 is the number of timesteps in the first run and N2 is the number of timesteps in the second run. This means each timestep in the second run is 30 times more costly than each move in the first run. The goal is to get the lowest total score. 


### Datasets and Inputs
_(approx. 2-3 paragraphs)_

In this section, the dataset(s) and/or input(s) being considered for the project should be thoroughly described, such as how they relate to the problem and why they should be used. Information such as how the dataset or input is (was) obtained, and the characteristics of the dataset or input, should be included with relevant references and citations as necessary It should be clear how the dataset(s) or input(s) will be used in the project and whether their use is appropriate given the context of the problem.

The inputs to this project are three mazes. The mazes were collected by Udacity for this project.

### Solution Statement
_(approx. 1 paragraph)_

In this section, clearly describe a solution to the problem. The solution should be applicable to the project domain and appropriate for the dataset(s) or input(s) given. Additionally, describe the solution thoroughly such that it is clear that the solution is quantifiable (the solution can be expressed in mathematical or logical terms) , measurable (the solution can be measured by some metric and clearly observed), and replicable (the solution can be reproduced and occurs more than once).

Q learning
Sarsa - variation on Q learning where Q update depends on Q(s',a') http://www.cse.unsw.edu.au/~cs9417ml/RL1/algorithms.html
Not sure how either of those would work...
A* algorithm
Flood fill algorithm
Djikstra's algoritm


### Benchmark Model
_(approximately 1-2 paragraphs)_

In this section, provide the details for a benchmark model or result that relates to the domain, problem statement, and intended solution. Ideally, the benchmark model or result contextualizes existing methods or known information in the domain and problem given, which could then be objectively compared to the solution. Describe how the benchmark model or result is measurable (can be measured by some metric and clearly observed) with thorough detail.

### Evaluation Metrics
_(approx. 1-2 paragraphs)_

In this section, propose at least one evaluation metric that can be used to quantify the performance of both the benchmark model and the solution model. The evaluation metric(s) you propose should be appropriate given the context of the data, the problem statement, and the intended solution. Describe how the evaluation metric(s) are derived and provide an example of their mathematical representations (if applicable). Complex evaluation metrics should be clearly defined and quantifiable (can be expressed in mathematical or logical terms).

### Project Design
_(approx. 1 page)_

In this final section, summarize a theoretical workflow for approaching a solution given the problem. Provide thorough discussion for what strategies you may consider employing, what analysis of the data might be required before being used, or which algorithms will be considered for your implementation. The workflow and discussion that you provide should align with the qualities of the previous sections. Additionally, you are encouraged to include small visualizations, pseudocode, or diagrams to aid in describing the project design, but it is not required. The discussion should clearly outline your intended workflow of the capstone project.

-----------

**Before submitting your proposal, ask yourself. . .**

- Does the proposal you have written follow a well-organized structure similar to that of the project template?
- Is each section (particularly **Solution Statement** and **Project Design**) written in a clear, concise and specific fashion? Are there any ambiguous terms or phrases that need clarification?
- Would the intended audience of your project be able to understand your proposal?
- Have you properly proofread your proposal to assure there are minimal grammatical and spelling mistakes?
- Are all the resources used for this project correctly cited and referenced?
