# Practice questions

1. Write one stencil matrix for a discrete Laplacian using a Moore neighbourhood. State its weights and grid spacing. When might it be preferred to the five-point stencil?

    ```{dropdown} Answer and considerations
    For square grid spacing $h$, one weighted nine-point approximation is

    $$L_h=\frac{1}{6h^2}\begin{bmatrix}1&4&1\\4&-20&4\\1&4&1\end{bmatrix}.$$

    The weights sum to zero, so a constant field gives zero. Including diagonals with suitable weights can reduce grid-direction artefacts. Check whether diagonal interactions fit the intended process, or whether the aim is a better approximation to continuous diffusion.
    ```

2. Construct a reaction–diffusion system with two reacting and diffusing fields. Identify the reaction and diffusion terms.

    ```{dropdown} Suggested considerations
    Choose local reactions $f(u,v)$ and $g(u,v)$, then add $D_u\nabla^2u$ and $D_v\nabla^2v$. Which feedback could reinforce a difference, and which could limit it?
    ```

3. Reaction–diffusion equations are continuous, yet simulations use discrete arrays. Explain how the choice of representation changes what can be implemented and observed.

    ```{dropdown} Answer
    Arrays sample continuous concentration fields at finitely many positions and times. Their values can still be real numbers. Grid spacing and time step limit the detail represented and introduce approximation error.
    ```

4. Are fingerprints Turing patterns? State what evidence would be needed rather than deciding from visual resemblance alone.

    ```{dropdown} Suggested considerations
    Look for evidence of the proposed local feedback and spatial transport during development. Perturbing those processes and measuring the resulting pattern would test the mechanism more directly than comparing images.
    ```

5. Read Duran-Nebreda et al. (2021), [*Synthetic Lateral Inhibition in Periodic Pattern Forming Microbial Colonies*](https://doi.org/10.1021/acssynbio.0c00318), and summarise one result that changes how you think about reaction–diffusion models.

    ```{dropdown} Suggested considerations
    Choose one experimental result and explain what the model helps account for. Consider how cell growth and movement affect the interpretation of the reacting and diffusing fields.
    ```

6. Derive a forward-Euler update for a two-field reaction–diffusion system. State $\Delta t$, grid spacing, boundary treatment and update ordering.

    ```{dropdown} Answer
    Let $L_h$ approximate the Laplacian on a grid of spacing $h$, with local reactions $f,g$. Forward Euler gives

    $$u^{n+1}_{i,j}=u^n_{i,j}+\Delta t\left[f(u^n_{i,j},v^n_{i,j})+D_u(L_hu^n)_{i,j}\right],$$

    $$v^{n+1}_{i,j}=v^n_{i,j}+\Delta t\left[g(u^n_{i,j},v^n_{i,j})+D_v(L_hv^n)_{i,j}\right].$$

    Both fields use the same old state. Apply the chosen boundary conditions and check stability as $h$ and $\Delta t$ change.
    ```

7. A pattern changes when the grid spacing is halved. Give three possible explanations and a test for each.

    ```{dropdown} Suggested considerations
    Check spatial approximation error, time-step stability and whether the physical domain or parameters changed accidentally. Compare refinements with the same physical setup, reducing the time step separately.
    ```

8. Separate verification from validation for a Gray–Scott implementation. Give two checks of each kind.

    ```{dropdown} Answer and considerations
    Verification could check one update by hand and test convergence as the grid and time step shrink. Validation could compare a measured wavelength and its response to a parameter change with data from the system being modelled. Choose checks relevant to the intended application and its assumptions.
    ```

9. Choose one pattern-level summary and one field-level summary. What question does each answer, and what information does each discard?

    ```{dropdown} Suggested considerations
    A pattern summary might describe spot spacing; a field summary might describe mean concentration. Choose a question for each and identify changes that would leave its value unchanged.
    ```
