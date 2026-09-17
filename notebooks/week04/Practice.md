# Practice questions

Consider an elementary cellular automaton with periodic boundaries and lookup table

$$111\mapsto0,\ 110\mapsto1,\ 101\mapsto1,\ 100\mapsto0,\ 011\mapsto1,\ 010\mapsto1,\ 001\mapsto1,\ 000\mapsto0.$$

1. Starting from the row $0001000$, determine the next generation.

    ```{dropdown} Answer
    The next row is $0011000$. The neighbourhoods $001$ and $010$ give the two live cells.
    ```

2. Find a possible previous generation of the row you obtained and explain whether it is unique.

    ```{dropdown} Answer
    The previous row is $0001000$. Checking all $2^7=128$ periodic rows finds no other predecessor for $0011000$. A unique predecessor for this row does not make the whole rule reversible.
    ```

3. Identify the rule number. Simulate several initial conditions and make a reasoned qualitative classification using Wolfram's scheme.

    ```{dropdown} Answer and considerations
    The output bits are $01101110$, giving Rule 110. Compare several starting rows over enough updates to see persistent structures and their interactions. State the world size and duration supporting your classification.
    ```

4. Find elementary cellular automata exhibiting a fixed point, period-two behaviour and complex-looking evolution.

    ```{dropdown} Answer
    Rule 0 reaches the all-zero fixed point. Rule 51 complements every cell, returning to the starting row after two updates. Rule 110 can produce complex-looking evolution from suitable starting rows. Show the initial conditions used.
    ```

5. Why are cellular automata useful in complex-systems research?

    ```{dropdown} Answer
    Simple local rules can produce collective patterns that are difficult to anticipate. Cellular automata let us study those mechanisms through controlled changes to rules, initial states and boundaries.
    ```

6. Find a cellular-automaton paper relevant to a system you might study and summarise what the automaton contributes.

    ```{dropdown} Suggested considerations
    Identify what the cells and updates represent. Explain which behaviour the automaton helps investigate and what comparison supports its use.
    ```

7. Translate B3/S23 into an explicit Game of Life update rule. Then state precisely how B4/S2 differs.

    ```{dropdown} Answer
    B3/S23 makes a dead cell live with exactly three live neighbours. A live cell survives with two or three; all other cells are dead at the next update. B4/S2 changes birth to exactly four neighbours and survival to exactly two.
    ```

8. Does a loop in a small state-transition graph prove reversibility? Explain injectivity, surjectivity and the role of world size.

    ```{dropdown} Answer
    A loop shows a periodic orbit. Reversibility requires every state to have exactly one predecessor. Injectivity means distinct states have distinct successors; surjectivity means every state has a predecessor. These conditions coincide on a finite complete state space, but a result for one world size need not hold at another.
    ```

9. For Rule 90, explain why damage from a one-cell perturbation reproduces a Sierpiński pattern. Propose one number summarising that damage and one feature it loses.

    ```{dropdown} Answer and considerations
    Rule 90 updates by XOR, so the disagreement between two runs follows the same rule, starting from one live cell. This produces a Sierpiński pattern before periodic wraparound affects it. Normalised Hamming distance measures the fraction of disagreeing cells at an update but loses their locations. A box-counting dimension instead summarises the full space–time geometry.
    ```

10. Estimate how the computational work changes when world size (number of cells), duration, number of rules and number of initial states are each doubled.

    ```{dropdown} Answer
    With a fixed neighbourhood, work is approximately proportional to cells × updates × rules × initial states. Doubling any one doubles the work; doubling all four multiplies it by 16. Doubling linear width instead quadruples the cells in a two-dimensional world.
    ```
