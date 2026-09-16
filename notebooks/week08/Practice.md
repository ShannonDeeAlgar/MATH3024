# Practice questions

1. Use the [site-percolation pseudocode at the end of the reader](https://shannondeealgar.github.io/MATH3024/notebooks/week08/l-critical-phenomena/#pseudocode) to implement or adapt a model on a $20\times20$ lattice. Sweep occupation probability $p$ using independent realisations. Choose and justify a quantity that reveals the transition. Why is one realisation at each $p$ insufficient?
2. For water passing through coffee grounds, a spanning path is not the only quantity of interest. Propose another property, explain how to represent it, and state how the model and measurements must change.
3. Design a percolation model where liquid enters at the top and flows through passable sites. Choose whether it can move directly down, diagonally down or sideways. Define the states, neighbourhood, update rule and stopping condition. How would you measure penetration, and how would the spread differ from undirected percolation?
4. Contrast percolation and the sandpile model. Which requires external tuning to a threshold, and which combines slow driving with fast relaxation?
5. Does the added grain or the existing pile cause an avalanche? Explain the role of each.
6. Define avalanche size $S$, area $A_{\mathrm{av}}$ and duration $T$ using the reader's parallel-update convention. Why can size differ from area? How would duration change if each sequential toppling counted as one step?
7. A distribution looks straight on log–log axes. How would you test whether it follows a power law? What would comparison with exponential and lognormal distributions tell you?
8. Why do finite lattices make the percolation transition appear gradual and limit avalanche sizes? What should change as the lattice grows?
9. Why might evolution favour operating near a transition? Give a possible benefit, a cost and a measurement that could test the benefit.
10. You borrow sandpile code. Find its inputs, state changes and outputs. How would you check toppling order, boundary loss and event measurements? How would you check driving, stopping and burn-in? Note the source and any changes you make.
11. In the [Bak–Sneppen model](https://doi.org/10.1103/PhysRevLett.71.4083), species lie on a ring, each with a barrier to evolutionary change between 0 and 1. At each step, the species with the lowest barrier and its two neighbours receive new independent values drawn uniformly between 0 and 1.

    - Identify the agents, their states, the interaction network and the update rule.
    - What should count as an avalanche, and what would you measure to test for self-organised criticality?
    - Why is identifying the lowest barrier in the whole population a strong assumption?
    - Propose a version in which agents use only local information. Would you still expect the system to approach a critical state?

12. Does every system have a correlation length? Choose two models from the unit. What would you correlate, and how would you define distance? Sketch or describe each correlation function. Would one finite correlation length describe its spatial range?
13. The reader's sandpile activity autocorrelation falls to $1/e$ at about 30 recorded steps and is close to zero by about 100 steps. What does the 30-step value tell us? Is it an avalanche duration? What would you compare to investigate critical slowing down?

## Suggested answers

<details class="reader-answer">
<summary>1. Measuring the percolation transition</summary>
<div><p>At each <i>p</i>, record whether a cluster joins opposite boundaries and average across independent lattices. This estimates spanning probability. Mean largest-cluster fraction is another useful quantity. Near the threshold, different lattices can give very different results. One lattice cannot tell you how likely spanning is.</p></div>
</details>

<details class="reader-answer">
<summary>4. Tuned and self-organised criticality</summary>
<div><p>Percolation is tuned by varying occupation probability towards its connectivity threshold. In the driven sandpile, grain additions increase load and boundary losses reduce it. The load density evolves under these rules. The local toppling threshold determines when one site redistributes load.</p></div>
</details>

<details class="reader-answer">
<summary>5. What caused the avalanche?</summary>
<div><p>The added grain triggers the event. Existing loads determine whether toppling stops locally or propagates. Adding one grain to different configurations can produce no toppling, a small avalanche or a large cascade.</p></div>
</details>

<details class="reader-answer">
<summary>6. Defining an event</summary>
<div><p>Size <i>S</i> counts total topplings, area <i>A</i><sub>av</sub> counts distinct toppled sites, and duration <i>T</i> counts parallel relaxation steps. A site may topple repeatedly, so <i>A</i><sub>av</sub> ≤ <i>S</i>. Each parallel step topples every site unstable at its start once. Counting each sequential toppling as one step gives <i>T</i> = <i>S</i>. Compare exponents using the same measurement definitions.</p></div>
</details>

<details class="reader-answer">
<summary>7. Testing a power-law claim</summary>
<div><p>Choose the quantity and fitted range. Fit a power law, an exponential and a lognormal to the same tail data. Check their agreement with the data, uncertainty and sensitivity to the fitted range. Repeat across seeds and lattice sizes to check sampling variation and finite-size cutoffs.</p><p>An exponential has a fixed decay scale; a lognormal can also have a broad, heavy tail.</p></div>
</details>

<details class="reader-answer">
<summary>8. Finite-size effects</summary>
<div><p>At the same occupation probability, some lattices span and others do not. For larger lattices, the change in spanning probability occurs over a narrower range near the threshold.</p><p>Open sandpile boundaries let grains leave, limiting avalanche growth. Larger lattices allow larger avalanches. Since sites can topple repeatedly, total topplings can exceed the number of sites. The largest observed event also depends on the number of trials.</p></div>
</details>

<details class="reader-answer">
<summary>9. Why operate near criticality?</summary>
<div><p>High sensitivity could help detect weak signals, but noise amplification could reduce reliability. Compare detection performance near and away from the transition, with the same input and noise levels. An evolutionary explanation would also need evidence of a benefit to survival or reproduction.</p><p>Sensitivity to a control parameter measures response; dynamical instability means a disturbance grows with time.</p></div>
</details>

<details class="reader-answer">
<summary>12. Does every system have a correlation length?</summary>
<div><p>Choose the quantity and a definition of distance first. For percolation, correlate membership of the same open cluster. Below the threshold, the probability falls with a finite exponential decay length. It has no sharp cutoff. At criticality, the infinite system has no finite exponential decay length.</p><p>For starlings, subtract the flock's mean velocity and correlate the fluctuations against distance between birds. The first zero crossing estimates the size of the positively correlated domain. These two definitions describe spatial range but give different numerical measures. A constant quantity has zero variance, so its normalised correlation is undefined.</p></div>
</details>

<details class="reader-answer">
<summary>13. Interpreting correlation time</summary>
<div><p>The 30-step value is an effective e-folding time: activity fluctuations 30 recorded steps apart have an average normalised correlation of about 0.37. The record joins successive avalanches and their terminal zeros. The decay time measures persistence across this record. <i>T</i> measures one avalanche's duration; <i>n</i> counts grain additions.</p><p>Compare consistently defined decay times across lattice sizes to see how persistence changes with system size. For critical slowing down in a tuned model, compare recovery or correlation times as the control parameter approaches the transition. One curve measures persistence in that record.</p></div>
</details>
