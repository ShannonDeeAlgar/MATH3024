# Practice questions

1. On a small weighted graph, calculate the probability that an ACO ant selects each allowed outgoing edge. Explain separately what the pheromone and edge-cost terms contribute.
2. Write the complete route cost for one ant and carry out one pheromone update, including evaporation, on every edge of its route.
3. Pheromone reinforcement creates positive feedback: using a route strengthens it, making later ants more likely to use it. Evaporation counteracts this amplification. Does that make evaporation a negative-feedback process, or is it passive decay? Explain the distinction. Then explain how reinforcement can produce either useful exploitation or premature reinforcement, and what the distribution of best route costs across repeated runs reveals about the outcome.
4. The current ACO model constructs complete routes and rewards shorter ones using the deposit $Q/L$. Redesign it so ants move continuously, deposit pheromone at a fixed rate as they walk and begin another trip immediately on arrival. Explain how a shorter route could retain more pheromone without an explicit $1/L$ reward. What roles do travel time and evaporation play, and what additional state must the model record?
5. Design an ensemble experiment that measures ACO solution quality and reliability. Also record the number of complete routes evaluated before the algorithm first finds a route at or below a target cost chosen in advance.
6. Read Kennedy and Eberhart's original PSO paper. Explain each update equation and connect every term to its implementation.
7. Define an objective function formally and show how a maximisation problem can be written as a minimisation problem.
8. Set the shared-information weight in PSO to zero and trace how one particle moves using only its current velocity and personal-best record. What can it achieve, and what additional information makes the full algorithm collective?
9. Sweep personal-memory and shared-information weights. Which summaries distinguish reliable success, efficient search and premature concentration?
10. Define swarm diversity and propose two non-equivalent ways to measure it.
11. Particle number increases both sampling and computational cost. Design an ensemble experiment that could reveal diminishing returns.
12. Compare ACO and PSO in terms of candidate representation, objective, memory, communication, forgetting and stopping rule.
13. Choose a new optimisation problem. Justify whether its representation is better suited to ACO, PSO or another method.
14. ACO and PSO normally assume that agents share an objective and report information honestly. Human organisations, firms and organisms may instead have partly aligned or conflicting objectives. What changes if an agent benefits from withholding or falsifying its result? Consider incentives, trust and the responses of other agents.
