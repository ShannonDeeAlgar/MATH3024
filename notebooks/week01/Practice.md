# Practice questions

1. Why can Schelling's segregation model be described as a complex system?

    ```{dropdown} Answer
    Agents respond to their local neighbours. Their moves change what other agents encounter, producing a collective pattern that no agent chooses directly.
    ```

2. A reductionist analysis might conclude that segregation occurs because people prefer segregation. Explain the flaw in that conclusion.

    ```{dropdown} Answer
    A segregated outcome does not establish a strong individual preference for segregation. Schelling shows that mild local preferences can produce substantial collective segregation. The model demonstrates a possible mechanism, not the actual cause of every segregated neighbourhood.
    ```

3. Write pseudocode for the Schelling model described in the Reader. Include the world, initial state, parameters, update order, stopping rule and quantities recorded. Then rewrite it so that an experiment can sweep over the model parameters.

    ```{dropdown} Suggested considerations
    Make one agent's decision and move explicit before describing repeated updates. For the sweep, keep other settings fixed and repeat each parameter value with recorded seeds.
    ```

4. For spatial areas $i$, the dissimilarity index is $D=\tfrac12\sum_i|X_i/X-Y_i/Y|$, where $X_i,Y_i$ are the group counts in each area and $X,Y$ their totals. Which dimensions of segregation are captured by the dissimilarity index? Which are missed? Propose a complementary measure.

    ```{dropdown} Answer and considerations
    It measures evenness across the chosen areas. It does not describe which areas are adjacent, contact between groups or location relative to the centre. Choose a second measure for a spatial feature you want to understand, and check how the area boundaries affect both measures.
    ```

5. Identify features of complex systems in *Parable of the Polygons* and point to the model detail producing each feature.

    ```{dropdown} Suggested considerations
    Connect each proposed feature to a rule or an observation. Local decisions and the effects of one move on neighbouring agents offer a starting point.
    ```

6. Two implementations use the same tolerance and population composition but different update orders. Should they be treated as the same model? State what evidence would settle the question.

    ```{dropdown} Answer and considerations
    Update order is part of the rules, so the implementations are not identical. They might give similar results for a specified question. Compare repeated runs using the same starting states and chosen summaries, including transients as well as final states.
    ```

7. Design an experiment separating the effects of initial condition, random seed and tolerance. What should be held fixed, repeated and reported?

    ```{dropdown} Suggested considerations
    Separate the seed used to create the initial state from the seed used for movement. Compare tolerance values on saved starting states, then repeat across starting states and movement seeds.
    ```

8. Give one observation that would verify an implementation of Schelling's rule and one observation that would test whether the model is a useful account of residential segregation. Why are these different tests?

    ```{dropdown} Answer and considerations
    Checking that an agent below the tolerance moves according to the rule verifies the implementation. Comparing simulated and observed residential patterns addresses validation. Choose observations relevant to the model's purpose, since matching one pattern need not establish its cause.
    ```

9. Compare two segregation measures on a configuration you construct yourself. Explain why a single number cannot capture every spatial feature.

    ```{dropdown} Suggested considerations
    Try configurations with similar group proportions but different adjacency or clustering. State what each measure counts and which differences it misses.
    ```
