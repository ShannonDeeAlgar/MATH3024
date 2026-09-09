# Practice questions

1. On a small weighted graph, calculate the probability that an ACO ant selects each allowed outgoing edge. Explain separately what the pheromone and edge-cost terms contribute.
2. Write the complete route cost for one ant and carry out one pheromone update, including evaporation, on every edge of its route.
3. Pheromone reinforcement creates positive feedback: using a route strengthens it, making later ants more likely to use it. Evaporation counteracts this amplification. Does that make evaporation a negative-feedback process, or is it passive decay? Explain the distinction. Then explain how reinforcement can produce either useful exploitation or premature reinforcement, and what the distribution of best route costs across repeated runs reveals about the outcome.
4. The current ACO model constructs complete routes and rewards shorter ones using the deposit $Q/L$. Redesign it so ants move continuously, deposit pheromone at a fixed rate as they walk and begin another trip immediately on arrival. Explain how a shorter route could retain more pheromone without an explicit {math}`1/L` reward. What roles do travel time and evaporation play, and what additional state must the model record?
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

15. In the ACO edge-choice rule, does $\alpha=2\beta$ mean an ant pays twice as much attention to pheromone as to edge cost? Derive the ratio of the probabilities of choosing two allowed edges. For $\alpha=2$ and $\beta=1$, compare the effect of doubling an edge's pheromone with halving its cost, holding everything else fixed. Explain why the exponents alone do not determine which source of information dominates a choice.

```{dropdown} Solution: interpreting the ACO exponents
For two allowed edges, the common normalising denominator cancels:

$$
\frac{P(e_1\mid i)}{P(e_2\mid i)}
=\left(\frac{\tau_1}{\tau_2}\right)^\alpha
 \left(\frac{\eta_1}{\eta_2}\right)^\beta,
\qquad \eta_e=\frac{1}{d_e}.
$$

With $\alpha=2$ and $\beta=1$, doubling $\tau_1$ multiplies this probability ratio by {math}`4`. Halving $d_1$ doubles $\eta_1$ and multiplies the ratio by {math}`2`. These are changes in relative choice probability; the individual probabilities are still normalised across all allowed edges.

Taking logarithms makes the role of each exponent explicit:

$$
\log\frac{P(e_1\mid i)}{P(e_2\mid i)}
=\alpha\log\frac{\tau_1}{\tau_2}
+\beta\log\frac{\eta_1}{\eta_2}.
$$

Thus $\alpha=2\beta$ gives the same proportional difference in pheromone twice the effect on the log probability ratio as that difference in the heuristic. The actual contribution also depends on how much the pheromone and costs differ between edges. If all pheromone values are equal, the pheromone term creates no preference, however large $\alpha$ is.

The exponents control sensitivity to proportional differences. “Twice as much attention” does not capture that distinction.
```
