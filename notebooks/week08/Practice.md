# Practice questions

1. Use the [site-percolation pseudocode at the end of the reader](https://shannondeealgar.github.io/MATH3024/notebooks/week08/l-critical-phenomena/#pseudocode) to implement or adapt a model on a $20\times20$ lattice. Sweep occupation probability $p$ using independent realisations. Choose and justify a quantity that reveals the transition. Why is one realisation at each $p$ insufficient?
2. For water passing through coffee grounds, a spanning path is not the only quantity of interest. Propose another property, explain how to represent it, and state how the model and measurements must change.
3. Design a gravity-directed percolation model in which liquid enters along the top boundary and moves through passable sites. Decide whether it can move directly down, diagonally down or sideways. Specify the states, neighbourhood, update rule and stopping condition. Choose measurements that show whether and how far the liquid penetrates the medium. How would its spread differ from undirected percolation?
4. Contrast percolation and the sandpile model. Which requires external tuning to a threshold, and which combines slow driving with fast relaxation?
5. What caused an avalanche: the final added grain, or the state of the pile before it was added? Explain the role of each.
6. Define avalanche size $S$, area $A_{\mathrm{av}}$ and duration $T$ using the reader's parallel-update convention. How would counting distinct toppled sites instead of total topplings change the size measurement? How would sequential single-site updates change the meaning of duration?
7. A log–log plot looks approximately straight. What additional analysis would help establish whether the distribution follows a power law? What would comparison with exponential and lognormal distributions tell you?
8. Explain why finite systems round a transition and truncate large avalanches. What should change as system size increases?
9. A small change in a control parameter can move a system away from criticality. Why might evolution favour operating near a transition? Give one possible benefit, one cost and a measurement that could test the proposed benefit.
10. You borrow a sandpile implementation. Identify its inputs, state changes and outputs. Design tests covering boundary loss, toppling order, stopping and event measurements. Explain how you would check the driving and burn-in conventions, and record the source and any changes you make.
11. In the [Bak–Sneppen model](https://doi.org/10.1103/PhysRevLett.71.4083), species lie on a ring, each with a barrier to evolutionary change between 0 and 1. At each step, the species with the lowest barrier and its two neighbours receive new independent values drawn uniformly between 0 and 1.

    - Identify the agents, their states, the interaction network and the update rule.
    - What should count as an avalanche, and what would you measure to test for self-organised criticality?
    - Why is identifying the lowest barrier in the whole population a strong assumption?
    - Propose a version in which agents use only local information. Would you still expect the system to approach a critical state?

12. Does every system have a correlation length? Choose two models from the unit. For each, identify a quantity to correlate and define distance. Sketch or describe the expected correlation function. Decide whether one finite correlation length is meaningful.
13. Interpreting correlation time. The reader's sandpile activity autocorrelation falls to $1/e$ at about 30 recorded steps and is close to zero by about 100 steps. What does the 30-step value tell us? Is it an avalanche duration? What would you compare to investigate critical slowing down?

## Suggested answers

<details class="reader-answer">
<summary>1. Measuring the percolation transition</summary>
<div><p>Estimate spanning probability by recording whether each lattice has an occupied cluster joining opposite boundaries, then averaging at each <i>p</i>. Mean largest-cluster fraction is another useful response. Independent realisations vary, especially near the threshold; one lattice cannot estimate how likely spanning is.</p></div>
</details>

<details class="reader-answer">
<summary>4. Tuned and self-organised criticality</summary>
<div><p>In percolation, the experimenter varies occupation probability to approach the global connectivity threshold. In the driven sandpile, additions increase total load and boundary losses reduce it. The density evolves under these rules. The local toppling threshold specifies when one site redistributes load; it plays a different role from the percolation threshold.</p></div>
</details>

<details class="reader-answer">
<summary>5. What caused the avalanche?</summary>
<div><p>The added grain triggers the event. Existing loads determine whether toppling stops locally or propagates. Adding one grain to different configurations can produce no toppling, a small avalanche or a large cascade.</p></div>
</details>

<details class="reader-answer">
<summary>6. Defining an event</summary>
<div><p>Size <i>S</i> counts total topplings, area <i>A</i><sub>av</sub> counts distinct toppled sites, and duration <i>T</i> counts parallel relaxation steps. A site may topple repeatedly, so <i>A</i><sub>av</sub> ≤ <i>S</i>. Each parallel step topples every site unstable at its start once. Counting one sequential toppling as a time step instead makes duration equal to total topplings. Exponents must be compared using matching definitions.</p></div>
</details>

<details class="reader-answer">
<summary>7. Testing a power-law claim</summary>
<div><p>Specify the observable and fitted range, estimate uncertainty and examine sensitivity to that range. Fit plausible alternatives to the same tail observations and assess goodness of fit. Repeat across seeds and system sizes to examine sampling variation and finite-size cutoffs.</p><p>An exponential has a fixed decay scale. A lognormal can have a broad, heavy tail too. Comparing these alternatives tests whether a power law describes the observations better; a straight section alone is insufficient.</p></div>
</details>

<details class="reader-answer">
<summary>8. Finite-size effects</summary>
<div><p>Finite random lattices differ, so some span and others fail at the same occupation probability. For larger lattices, the change in spanning probability occurs over a narrower range near the threshold.</p><p>Open sandpile boundaries dissipate load and limit avalanche growth. Larger lattices allow a broader range of large events. Total topplings can exceed the number of sites because sites can topple repeatedly; the largest sampled event also depends on the number of trials.</p></div>
</details>

<details class="reader-answer">
<summary>9. Why operate near criticality?</summary>
<div><p>High sensitivity could improve detection of weak signals, while increased noise amplification could reduce reliability. Vary the operating regime and measure detection performance at matched input and noise levels. Evidence of improved performance supports the proposed function; an evolutionary explanation also requires a connection to survival or reproduction.</p><p>Sensitivity to a control parameter differs from dynamical instability, where a disturbance grows with time.</p></div>
</details>

<details class="reader-answer">
<summary>12. Does every system have a correlation length?</summary>
<div><p>A correlation length depends on the observable and definition of distance. In percolation, pair-connectedness measures whether two sites belong to the same open cluster. Below the threshold, connectivity decays with a finite exponential decay length, not a sharp cutoff. At criticality, the infinite system has no finite exponential decay length.</p><p>For a flock, correlate velocity fluctuations after subtracting the mean velocity, using physical separation between birds. For the starling data, the first zero crossing gives the approximate size of the positively correlated domain. These definitions summarise spatial range but their values are not interchangeable. A constant quantity has zero variance, making its normalised correlation undefined.</p></div>
</details>

<details class="reader-answer">
<summary>13. Interpreting correlation time</summary>
<div><p>The value is an effective e-folding time for fluctuations in toppling activity. Values separated by about 30 recorded steps have a normalised autocorrelation of approximately 0.37. The joined record includes successive avalanches and terminal zeros, so this time differs from both individual avalanche duration and grain-addition count.</p><p>Across lattice sizes, compare consistently defined decay times to test how persistence changes with system size. To investigate critical slowing down in a tuned model, compare recovery or correlation times as its control parameter approaches the transition. One curve gives a time scale for that record.</p></div>
</details>
