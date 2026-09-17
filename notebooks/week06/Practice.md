# Practice questions

1. Distinguish in-phase synchronisation, frequency entrainment and phase locking. Give an example in which two of these occur without the third.

    ```{dropdown} Answer
    In-phase synchronisation means equal phases modulo $2\pi$. Frequency entrainment means equal long-time average frequencies; phase locking means a constant phase difference. An anti-phase pair has phase difference $\pi$, so it is phase locked and frequency entrained without being in phase.
    ```

2. For two uncoupled oscillators, derive the evolution of their phase difference. What changes with the one-way coupling $\dot\theta_1=\omega_1+K\sin(\theta_2-\theta_1)$ and $\dot\theta_2=\omega_2$?

    ```{dropdown} Answer
    Set $\phi=\theta_1-\theta_2$ and $\Delta\omega=\omega_1-\omega_2$. Without coupling,

    $$\phi(t)=\phi(0)+\Delta\omega t.$$

    The stated coupling gives $\dot\phi=\Delta\omega-K\sin\phi$. A locked phase difference satisfies $\sin\phi=\Delta\omega/K$, which is possible when $|\Delta\omega|\leq K$ for positive $K$.
    ```

3. Explain every term in the Kuramoto model, including how $\omega_i$ is initialised and what all-to-all coupling means.

    ```{dropdown} Answer
    In

    $$\dot\theta_i=\omega_i+\frac{K}{N}\sum_{j=1}^{N}\sin(\theta_j-\theta_i),$$

    $\theta_i$ is phase, $\omega_i$ is natural angular frequency, $K$ is coupling strength and $N$ is population size. Each $\omega_i$ is sampled once from a prescribed distribution and stays fixed. Every oscillator interacts with every other through their phase differences; $1/N$ keeps the total influence comparable across population sizes.
    ```

4. Starting from $r e^{i\psi}=N^{-1}\sum_j e^{i\theta_j}$, explain geometrically why $r\approx0$ indicates cancellation and $r\approx1$ indicates coherence.

    ```{dropdown} Answer
    Each oscillator contributes a unit vector on the phase circle. Vectors spread around the circle largely cancel, giving $r\approx0$. Aligned vectors add in nearly the same direction, giving $r\approx1$.
    ```

5. Natural frequencies are drawn from a normal distribution with fixed mean and increasing standard deviation while $K$ is fixed. Predict and then explain the effect on long-time coherence, time to synchrony and the number of drifting oscillators.

    ```{dropdown} Answer and considerations
    A wider frequency distribution generally lowers long-time coherence and increases the drifting fraction because the same coupling must overcome larger frequency differences. Some runs never reach a chosen synchrony criterion, and time to synchrony need not increase steadily with width. Define that criterion before comparing times and include runs that do not reach it.
    ```

6. How would you choose and test when to measure long-time coherence? Compare equal-duration windows, different initial phases and coupling strengths. What changes when measuring time to synchrony?

    ```{dropdown} Suggested considerations
    Compare equal-duration windows starting later and extend the run when their summaries still change. Hold the frequency sample fixed while comparing initial phases, then recheck at other coupling strengths. Time to synchrony measures the initial adjustment, so count from the original start.
    ```

7. Fireflies flash in physical space, while standard Kuramoto oscillators do not occupy a spatial domain. Identify what the model represents, omits and would need to add for spatial visibility.

    ```{dropdown} Answer and considerations
    Phase represents position within a cycle, and coupling represents how other oscillators affect its timing. Standard Kuramoto omits positions, viewing directions and limited visibility. Consider adding positions and a visibility-dependent interaction network if those details matter to the question.
    ```

8. Write one calculation question, one interpretation question and one model-criticism question. Exchange them with another student, answer theirs, and revise any question that admits an unintended interpretation.
