# Practice questions

1. Use the [site-percolation pseudocode in the reader](https://shannondeealgar.github.io/MATH3024/notebooks/week08/l-critical-phenomena/#pseudocode) to implement or adapt a model on a $20\times20$ lattice. Sweep open-site probability $p$ using independent realisations. Choose and justify a quantity that reveals the transition. Why is one realisation at each $p$ insufficient?

    ~~~{dropdown} Answer and considerations
    At each $p$, record whether an open cluster joins opposite boundaries. The fraction of independent lattices that span estimates spanning probability. Mean largest-cluster fraction is another option. One lattice gives one outcome and cannot tell us how likely spanning is. Add runs until uncertainty is small enough for the comparison you want to make.
    ~~~

2. For water passing through coffee grounds, a spanning path is not the only quantity of interest. Propose another property, explain how to represent it, and state how the model and measurements must change.

    ~~~{dropdown} Suggested considerations
    Consider flow rate or time spent in the grounds. Passable sites alone do not describe either quantity. You might add resistance to connections or a travel time along paths.
    ~~~

3. Design a percolation model where liquid enters at the top and flows through passable sites. Choose whether it can move directly down, diagonally down or sideways. Define the states, neighbourhood, update rule and stopping condition. How would you measure penetration, and how would the spread differ from undirected percolation?

    ~~~{dropdown} Suggested considerations
    Start by marking which open sites the liquid has reached. Choose the allowed directions and stop when no new sites can be reached. Penetration could be the greatest depth reached or the fraction of runs reaching the bottom. Directional rules can prevent access to paths available in undirected percolation.
    ~~~

4. Contrast percolation and the sandpile model. Which requires external tuning to a threshold, and which combines slow driving with fast relaxation?

    ~~~{dropdown} Answer
    Percolation is tuned by setting $p$ near $p_c$. In the driven sandpile, additions increase load and avalanches carry load to the open boundaries. Boundary loss reduces load. This balance produces a stationary regime without setting the global load density to a chosen critical value.
    ~~~

5. Does the added grain or the existing pile cause an avalanche? Explain the role of each.

    ~~~{dropdown} Answer
    The grain triggers the avalanche. Existing loads determine how far toppling spreads. The same addition can produce no toppling, a small avalanche or a large cascade in different piles.
    ~~~

6. Define avalanche size $S$, area $A_{\mathrm{av}}$ and duration $T$ using the reader's parallel-update convention. Why can size differ from area? How would duration change if each sequential toppling counted as one step?

    ~~~{dropdown} Answer
    $S$ counts all topplings. $A_{\mathrm{av}}$ counts distinct sites that topple. $T$ counts parallel relaxation steps. Sites can topple repeatedly, so $A_{\mathrm{av}}\leq S$. Counting each sequential toppling as one step instead gives $T=S$.
    ~~~

7. A distribution looks straight on log–log axes. How would you test whether it follows a power law? What would comparison with exponential and lognormal distributions tell you?

    ~~~{dropdown} Suggested considerations
    Compare the distributions over the same tail range. Check uncertainty and whether the result changes with the fitted range or lattice size. An exponential has a fixed decay scale. A lognormal can also produce a broad tail, so a straight-looking section alone does not establish a power law.
    ~~~

8. Why do finite lattices make the percolation transition appear gradual and limit avalanche sizes? What should change as the lattice grows?

    ~~~{dropdown} Answer
    At the same $p$, some lattices span and others do not. Larger lattices give a sharper change in spanning probability near $p_c$. Sandpile boundaries allow load to escape and limit avalanche growth. Larger lattices allow larger events, but total topplings can exceed the number of sites because sites can topple repeatedly.
    ~~~

9. Why might evolution favour operating near a transition? Give a possible benefit, a cost and a measurement that could test the benefit.

    ~~~{dropdown} Suggested considerations
    Greater sensitivity could help detect weak signals. It could also amplify noise. Compare detection performance near and away from the transition with the same input and noise. An evolutionary explanation would need evidence that this improves survival or reproduction.
    ~~~

10. You borrow sandpile code. Find its inputs, state changes and outputs. How would you check toppling order, boundary loss and event measurements? How would you check driving, stopping and burn-in? Note the source and any changes you make.

    ~~~{dropdown} Suggested considerations
    Follow one small avalanche step by step. Check where grains go and reconstruct its measurements from the trace. Then compare a short run with repeated individual additions. Try different initial piles and later measurement windows before trusting the summaries.
    ~~~

11. In the [Bak–Sneppen model](https://doi.org/10.1103/PhysRevLett.71.4083), species lie on a ring, each with a barrier to evolutionary change between 0 and 1. At each step, the species with the lowest barrier and its two neighbours receive new independent values drawn uniformly between 0 and 1.

    - Identify the agents, their states, the interaction network and the update rule.
    - What should count as an avalanche, and what would you measure to test for self-organised criticality?
    - Why is identifying the lowest barrier in the whole population a strong assumption?
    - Propose a version in which agents use only local information. Would you still expect the system to approach a critical state?

    ~~~{dropdown} Answer and considerations
    Each species has one barrier value. Neighbours lie on a ring, but selecting the minimum requires information from the whole population. One avalanche definition is a consecutive sequence of updates while the minimum lies below a chosen barrier level. Check the stationary barrier distribution and avalanche durations across system sizes. A local replacement rule would need its own investigation.
    ~~~

12. Does every system have a correlation length? Choose two models from the unit. What would you correlate, and how would you define distance? Sketch or describe each correlation function. Would one finite correlation length describe its spatial range?

    ~~~{dropdown} Answer and considerations
    Choose a quantity and a distance first. Percolation uses the probability of sharing an open cluster and estimates a decay length below $p_c$. At criticality, the infinite system has no finite exponential decay length. Starlings use velocity fluctuations and a first zero crossing to estimate the positively correlated domain's size. Both describe spatial range, but their numerical values have different meanings.
    ~~~

13. The reader's sandpile activity autocorrelation falls to $1/e$ at about 30 recorded steps and is close to zero by about 100 steps. What does the 30-step value tell us? Is it an avalanche duration? What would you compare to investigate critical slowing down?

    ~~~{dropdown} Answer
    Activity fluctuations 30 recorded steps apart have an average normalised correlation of about $0.37$. This estimates persistence in the joined activity record. $T$ measures one avalanche's duration. To test critical slowing down, compare consistently measured recovery or correlation times as a control parameter approaches a transition.
    ~~~
