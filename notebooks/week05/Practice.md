# Practice questions

1. Choose a flock of birds, a pedestrian crowd or a traffic stream and propose an agent-based model for it. Your pseudocode should specify the world, initialisation, agent state, local information, interaction network, update rule and parameters. Then explain how you would test the model using both qualitative comparison and at least one quantitative measure.

    ```{dropdown} Suggested considerations
    Choose the behaviour your model should explain and what agents need to sense to produce it. Use a quantitative measure that captures that behaviour and compare it with observations or a known benchmark.
    ```

2. Derive the mean direction of neighbouring headings using complex exponentials. Why can directly averaging angles fail near $0$ and $2\pi$?

    ```{dropdown} Answer
    Map each heading to $e^{\mathrm i\theta_j}=\cos\theta_j+\mathrm i\sin\theta_j$ and take

    $$\bar\theta_i=\operatorname{Arg}\!\left(\sum_{j\in\mathcal N_i}e^{\mathrm i\theta_j}\right).$$

    The ordinary mean of $1^\circ$ and $359^\circ$ is $180^\circ$, while their vector mean points at $0^\circ$. If the vectors cancel exactly, there is no unique mean direction.
    ```

3. Compare angular and vectorial noise mathematically and physically. Give a system for which each is the more defensible representation.

    ```{dropdown} Answer and considerations
    Angular noise adds a turning error after averaging headings,

    $$\theta_i'=\bar\theta_i+\xi_i,\qquad \xi_i\sim U[-\eta/2,\eta/2].$$

    Vectorial noise perturbs the alignment signal before taking its direction,

    $$\theta_i'=\operatorname{Arg}\!\left(\sum_{j\in\mathcal N_i}e^{\mathrm i\theta_j}+\eta n_i e^{\mathrm i\chi_i}\right),\qquad \chi_i\sim U[0,2\pi).$$

    Here $n_i$ is the number of neighbours. For a flock, consider whether uncertainty comes from turning or from sensing neighbours.
    ```

4. Explain why the Vicsek polarisation is an upward move in abstraction. What can two runs with the same polarisation still do differently?

    ```{dropdown} Answer
    Polarisation replaces all agent headings with the magnitude of their mean direction vector. It loses spatial arrangement and individual histories. Runs with the same polarisation can differ in their direction of motion, clusters and density bands.
    ```

5. Design a sweep capable of locating an order–disorder transition. Include ensemble size, parameter spacing, refinement near the transition and system-size checks.

    ```{dropdown} Suggested considerations
    Start with a coarse sweep of noise at fixed density, then add points where the response changes strongly. Use repeated runs to judge uncertainty and choose how much precision is useful. Check the measurement window and compare several system sizes.
    ```

6. Reynolds, Vicsek and Couzin can produce visually similar collective motion. How do their questions change the assumptions, outputs and standards of success?

    ```{dropdown} Answer
    Reynolds uses local steering rules to produce believable, controllable animation. Vicsek isolates alignment and noise to study collective order through polarisation and transition curves. Couzin connects repulsion, alignment and attraction to group shape, motion and sorting observed in animals. Similar-looking motion meets different standards of success in each case.
    ```
