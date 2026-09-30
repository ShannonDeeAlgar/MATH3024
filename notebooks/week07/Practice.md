# Practice questions

1. On a small weighted graph, calculate the probability that an ACO ant selects each allowed outgoing edge. Use costs $(1,2,4)$, pheromones $(1,2,1)$ and $\alpha=\beta=1$ for three allowed outgoing edges. Explain separately what the pheromone and edge-cost terms contribute.

    ```{dropdown} Answer
    The unnormalised weights are $\tau_e/c_e=(1,1,1/4)$. Dividing by their sum gives probabilities $(4/9,4/9,1/9)$. Higher pheromone increases an edge's weight; higher cost decreases it.
    ```

2. Write the complete route cost for one ant and carry out one pheromone update, including evaporation, on every edge of its route. Use two edges with costs $2,3$, pheromones $1,2$, evaporation fraction $\rho=0.2$ and $Q=5$. No other ants contribute to this update.

    ```{dropdown} Answer
    The route cost is $L=2+3=5$, so each used edge receives $Q/L=1$. Applying $\tau'_e=(1-\rho)\tau_e+Q/L$ gives pheromones $1.8$ and $2.6$. An unused edge receives evaporation only.
    ```

3. Pheromone reinforcement creates positive feedback. Using a route strengthens it, making later ants more likely to use it. Evaporation counteracts this amplification. Does that make evaporation a negative-feedback process, or is it passive decay? Explain the distinction. Then explain how reinforcement can produce either useful exploitation or premature reinforcement, and what the distribution of best route costs across repeated runs reveals about the outcome.

    ```{dropdown} Answer
    Evaporation is passive loss proportional to current pheromone. It damps reinforcement without assessing route quality. Reinforcement can amplify a good route or an early poor choice; repeated best costs show how reliably good routes are found.
    ```

4. The current ACO model constructs complete routes and rewards shorter ones using the deposit $Q/L$. Redesign it so ants move continuously, deposit pheromone at a fixed rate as they walk and begin another trip immediately on arrival. Explain how a shorter route could sustain a higher pheromone level without an explicit {math}`1/L` reward. What roles do travel time and evaporation play, and what additional state must the model record?

    ```{dropdown} Answer and considerations
    At equal speed, the same number of ants can complete shorter trips more often. Repeated trips can then give each edge more visits per unit time, while evaporation removes deposits between visits. Decide how ants restart and record their positions, directions and deposits through time.
    ```

5. Design an ensemble experiment that measures ACO solution quality and reliability. Also record the number of complete routes evaluated before the algorithm first finds a route at or below a target cost chosen in advance.

    ```{dropdown} Suggested considerations
    Compare best cost and the fraction reaching the target at equal evaluation budgets. Show runs that exhaust the budget without success when summarising evaluations to first success. Use independent seeds.
    ```

6. Read [Kennedy and Eberhart's original PSO paper](https://doi.org/10.1109/ICNN.1995.488968). Explain each update equation and connect every term to its implementation. Identify any differences from the Reader's version.

    ```{dropdown} Answer
    Previous displacement supplies momentum; random pulls point towards personal and shared best positions. The paper's final rule corresponds to $w=1$ and $c_1=c_2=2$ in the Reader's notation. The Reader makes these coefficients adjustable. Add the new displacement to the current position.
    ```

7. Define an objective function formally and show how a maximisation problem can be written as a minimisation problem.

    ```{dropdown} Answer
    An objective $f$ maps a feasible set $\mathcal X$ to $\mathbb R$, assigning a score to each candidate. Maximising $f(x)$ is equivalent to minimising $-f(x)$ over the same feasible set.
    ```

8. Set the shared-information weight in PSO to zero and trace how one particle moves using only its current velocity and personal-best record. For two steps, use $f(x)=x^2$, $x=2$, $v=-1$, $p=1$, $w=0.5$, $c_1=1$ and $r_1=0.5$, with no boundary restriction. What can it achieve, and what additional information makes the full algorithm collective?

    ```{dropdown} Answer
    The first step gives $(v,x)=(-1,1)$; the second gives $(-0.5,0.5)$. Evaluating the new position improves the personal best to $p=0.5$. A particle can improve its own record without sharing, but success is not guaranteed. The full model also uses discoveries made by other particles.
    ```

9. Sweep personal-memory and shared-information weights. Which summaries distinguish reliable success, efficient search and premature concentration?

    ```{dropdown} Suggested considerations
    Compare success frequency and evaluations to success at a common budget. Track swarm spread alongside the best objective. Small spread with a poor objective suggests premature concentration.
    ```

10. Define swarm diversity and propose two non-equivalent ways to measure it.

    ```{dropdown} Answer and considerations
    Swarm diversity describes differences between candidate positions. You could compare mean distance from the centroid with the number of occupied regions. State the region size; these measures capture different aspects of spread.
    ```

11. Particle number increases both sampling and computational cost. Design an ensemble experiment that could reveal diminishing returns.

    ```{dropdown} Suggested considerations
    Compare particle counts at equal objective-evaluation budgets, using repeated runs. Plot success frequency or final best objective against particle count. Look for a point where added particles give little improvement.
    ```

12. Compare ACO and PSO in terms of candidate representation, objective, memory, communication, forgetting and stopping rule.

    ```{dropdown} Answer
    ACO searches graph routes and minimises route cost; PSO searches points scored by $f(x)$. ACO communicates through edge pheromone; PSO uses personal and shared best positions. Pheromone evaporates, while best-so-far records usually persist. Both need a stated target or evaluation budget.
    ```

13. Choose a new optimisation problem. Justify whether its representation is better suited to ACO, PSO or another method.

    ```{dropdown} Suggested considerations
    Decide what one candidate stores and how its quality is scored. Paths or discrete combinations may suit ACO; continuous coordinates may suit PSO. Check how the method would handle your constraints.
    ```

14. ACO and PSO normally assume that agents share an objective and report information honestly. Human organisations, firms and organisms may instead have partly aligned or conflicting objectives. What changes if an agent benefits from withholding or falsifying its result? Consider incentives, trust and the responses of other agents.

    ```{dropdown} Suggested considerations
    Identify which reported information changes other agents' choices. Compare a setting where sharing helps everyone with one where deception benefits the reporting agent. What could others observe or verify?
    ```

15. In the ACO edge-choice rule, does $\alpha=2\beta$ mean an ant pays twice as much attention to pheromone as to edge cost? Derive the ratio of the probabilities of choosing two allowed edges. For $\alpha=2$ and $\beta=1$, compare the effect of doubling an edge's pheromone with halving its cost, holding everything else fixed. Explain why the exponents alone do not determine which source of information dominates a choice.

    ```{dropdown} Answer
    The common denominator cancels between two allowed edges.

    $$
    \frac{P(e_1\mid i)}{P(e_2\mid i)}
    =\left(\frac{\tau_1}{\tau_2}\right)^\alpha
     \left(\frac{c_{e_2}}{c_{e_1}}\right)^\beta.
    $$

    Here $c_e$ is edge cost. Doubling $\tau_1$ multiplies this ratio by $4$; halving $c_{e_1}$ multiplies it by $2$. The exponents set sensitivity to proportional differences. Their contributions also depend on the pheromone and cost ratios; equal pheromones create no preference, however large $\alpha$ is.
    ```
