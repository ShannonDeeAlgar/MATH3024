# Practice questions

1. On a small weighted graph, calculate the probability that an ACO ant selects each allowed outgoing edge. Explain separately what the pheromone and edge-cost terms contribute.
2. Write the complete route cost for one ant and carry out one pheromone update, including evaporation, on every edge of its route.
3. Explain why a high pheromone concentration can represent either useful exploitation or premature reinforcement. What additional result distinguishes those cases?
4. Design an ensemble experiment that measures ACO solution quality, reliability and evaluations to first find a target-cost route.
5. Read Kennedy and Eberhart's original PSO paper. Explain each update equation and connect every term to its implementation.
6. Define an objective function formally and show how a maximisation problem can be written as a minimisation problem.
7. Run the reasoning for one particle without social information. What can it achieve, and what specifically makes the full algorithm collective?
8. Sweep personal-memory and shared-information weights. Which summaries distinguish reliable success, efficient search and premature concentration?
9. Define swarm diversity and propose two non-equivalent ways to measure it.
10. Particle number increases both sampling and computational cost. Design an ensemble experiment that could reveal diminishing returns.
11. Compare ACO and PSO in terms of candidate representation, objective, memory, communication, forgetting and stopping rule.
12. Choose a new optimisation problem. Justify whether its representation is better suited to ACO, PSO or another method.
13. ACO and PSO normally assume that agents share an objective and report information honestly. Human organisations, firms and organisms may instead have partly aligned or conflicting objectives. What changes if an agent benefits from withholding or falsifying its result? Consider incentives, trust and the responses of other agents.
