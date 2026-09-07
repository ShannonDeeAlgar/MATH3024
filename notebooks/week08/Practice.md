# Practice questions

1. Starting from a percolation implementation, sweep occupation probability $p$ using ensembles on a $20\times20$ world. Choose and justify a quantity that reveals the transition.
2. For water passing through coffee grounds, a spanning path is not the only quantity of interest. Propose another property, explain how to represent it, and state how the model and measurements must change.
3. Design a gravity-directed percolation model in which liquid enters along the top boundary and moves through passable sites. Decide whether it can move directly down, diagonally down or sideways. Specify the states, neighbourhood, update rule and stopping condition. Choose measurements that show whether and how far the liquid penetrates the medium. How would its spread differ from undirected percolation?
4. Contrast percolation and the sandpile model. Which requires external tuning to a threshold, and which combines slow driving with fast relaxation?
5. What caused an avalanche: the final added grain, or the state of the pile before it was added? Explain the role of each.
6. Define avalanche size $S$ and duration $T$. Give two plausible conventions for each and explain why published exponents cannot be compared until the conventions are checked.
7. A log–log plot looks approximately straight. List the evidence required before claiming power-law scaling.
8. Explain why finite systems round a transition and truncate large avalanches. What should change as system size increases?
9. Critical points are usually unstable. Give several reasons critical-looking behaviour may nevertheless be widespread, including self-organisation, broad crossover regimes and external tuning or adaptation.
10. You borrow a sandpile implementation. Write an audit checklist covering state, boundary, toppling order, driving, stopping, observables and attribution.
11. In the Bak–Sneppen model, each species has a barrier to evolutionary change. At each step, the species with the lowest barrier and its neighbours receive new random values.
   - Identify the agents, their states, the interaction network and the update rule.
   - What should count as an avalanche, and what would you measure to test for self-organised criticality?
   - Why is identifying the lowest barrier in the whole population a strong assumption?
   - Propose a version in which agents use only local information. Would you still expect the system to approach a critical state?
