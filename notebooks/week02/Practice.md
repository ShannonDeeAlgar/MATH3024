# Practice questions

1. Calculate the self-similarity dimension of the Sierpiński triangle.

    ```{dropdown} Answer
    Each stage has three copies at half the linear scale. Thus $3=2^D$ and $D=\log 3/\log 2\approx1.585$.
    ```

2. Begin with an equilateral triangle of side length $a$ at iteration $n=0$. At each iteration, replace every line segment by the four-segment Koch generator, in which each new segment has one third of the old segment's length and the triangular bump points outwards. For the resulting Koch snowflake, calculate perimeter and area through four iterations, obtain expressions for iteration $n$, and determine their limiting behaviour.

    ```{dropdown} Answer
    Let $P_0=3a$ and $A_0=\sqrt3a^2/4$. Iterations $1,2,3,4$ give perimeters $4a,16a/3,64a/9,256a/27$ and areas $4A_0/3,40A_0/27,376A_0/243,3448A_0/2187$.

    Each perimeter is multiplied by $4/3$, while the added areas form a geometric series.

    $$P_n=3a\left(\frac43\right)^n,\qquad A_n=A_0\left[\frac85-\frac35\left(\frac49\right)^n\right].$$

    The perimeter diverges and the area approaches $8A_0/5$.
    ```

3. Is the generator alone sufficient to determine the fractal dimension? Explain.

    ```{dropdown} Answer
    Copy number and contraction ratio give the similarity dimension when the copies meet the required separation conditions. Overlapping copies can give a different dimension, so their placement matters too. For contraction maps, the limiting set is independent of the nonempty compact starting shape.
    ```

4. If a Sierpiński triangle is enlarged by a factor of two, how many copies of the original are required to cover it?

    ```{dropdown} Answer
    Three copies. This gives $N=2^D=3$ for $D=\log3/\log2$.
    ```

5. What happens if the Sierpiński iterated function system is applied to a square or an irregular image rather than a triangle?

    ```{dropdown} Answer
    With the same three contraction maps, any nonempty compact starting set approaches the same Sierpiński attractor. The early images differ, but repeated contraction reduces the influence of the starting shape.
    ```

6. Explain the self-similar structure of Pascal's triangle modulo 3.

    ```{dropdown} Answer
    The first three rows are $1$, $1\;1$ and $1\;2\;1$. In the first nine rows this small triangle appears in six positions, with one copy exchanging $1$ and $2$. The arrangement repeats at row counts $3,9,27,\ldots$ with some copies exchanging the two nonzero values. Plotting zeros as gaps reveals the self-similar pattern.
    ```

7. A box-counting plot is straight over only three adjacent scales. What evidence would you require before reporting its slope as a fractal dimension?

    ```{dropdown} Suggested considerations
    Test more scales and check whether changing the fitted range changes the slope. Consider resolution, object size and grid placement before interpreting a short straight section.
    ```

8. Construct two different generators with the same similarity dimension. What does their shared dimension fail to describe?

    ```{dropdown} Suggested considerations
    Keep copy number and contraction ratio fixed while changing a valid arrangement of the copies. Compare shape, gaps or connectivity, and check that overlap has not invalidated the similarity calculation.
    ```

9. Classify the Sierpiński triangle and Cantor set as patterns, models, algorithms or complex systems. More than one label may be defensible; justify your choice.

    ```{dropdown} Suggested considerations
    Distinguish the resulting set from the procedure generating it. If you call it a model or a complex system, explain what it represents or which interacting components you mean.
    ```

10. Compare an initiator–generator construction, an iterated function system and an L-system. What information must each representation specify before another person could reproduce the object?

    ```{dropdown} Answer
    A replacement construction needs its initiator, replacement geometry and iteration rule. An IFS needs the contraction maps and whether all maps act on a set or are selected for point iteration. An L-system needs an alphabet, initial word, production rules and drawing interpretation. Every finite output also needs a stopping depth or sample count; random iteration needs its sampling probabilities and seed.
    ```
