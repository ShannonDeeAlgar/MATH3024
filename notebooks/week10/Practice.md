# Practice questions

1. What dilemma is captured by the Prisoner's Dilemma? Distinguish individually rational choices from outcomes preferred by both players.

    ~~~{dropdown} Answer
    Defection gives each player a higher payoff for either action of the other player. Both receive less from mutual defection than from mutual cooperation. Each player therefore defects, even though both would prefer mutual cooperation.
    ~~~

2. Consider the symmetric relative payoff rankings (a) $T>R>P>S$, (b) $R>T>P>S$ and (c) $T>R>S>P$. Which defines a Prisoner's Dilemma? Explain using the incentives to cooperate or defect rather than a story attached to the game.

    ~~~{dropdown} Answer
    Only (a) is a Prisoner's Dilemma. Defection is better against cooperation because $T>R$, and against defection because $P>S$, while both prefer mutual cooperation to mutual defection. In (b), cooperation is better against cooperation; in (c), cooperation is better against defection.
    ~~~

3. Extend the Prisoner's Dilemma to three players. Specify actions, payoffs and any dominant strategy. What would the normal form look like for a three-player game? Sketch the payoff table as slices, one for each action of Player 3. How could the same payoffs be represented as a **payoff tensor**?

    ~~~{dropdown} Answer
    Let each player choose $C$ or $D$. Give a cooperator payoff $3,1,0$ when the other two players contain two, one or zero cooperators, and give a defector payoff $4,2,1$ in the same cases. Defection is then strictly dominant for every player, while $(C,C,C)$ gives everyone $3$ and $(D,D,D)$ gives everyone $1$.

    The normal form has two $2\times2$ slices. Rows are Player 1's action, columns are Player 2's action, and each cell is $(u_1,u_2,u_3)$:

    Together, these slices form a $2\times2\times2$ payoff tensor: fixing the third index selects one matrix slice, and each entry still contains a payoff triple.

    **Player 3 chooses $C$**

    $$
    \begin{array}{c|cc}
      & C & D \\
      \hline
      C & (3,3,3) & (1,4,1) \\
      D & (4,1,1) & (2,2,0)
    \end{array}
    $$

    **Player 3 chooses $D$**

    $$
    \begin{array}{c|cc}
      & C & D \\
      \hline
      C & (1,1,4) & (0,2,2) \\
      D & (2,0,2) & (1,1,1)
    \end{array}
    $$
    ~~~

4. Keep the two-player Prisoner's Dilemma, but give each player three actions. Add a third action such as costly punishment or withdrawal. What would the $3\times3$ normal form look like? Choose payoffs, then check whether defection remains dominant and whether mutual cooperation is still better than mutual defection. Draw the best-response graph on the $3\times3$ grid of action profiles.

    ~~~{dropdown} Example solution
    Let the third action be $W$ (withdraw). One possible symmetric normal form is

    $$
    \begin{array}{c|ccc}
      & C & D & W \\
      \hline
      C & (-1,-1) & (-3,0) & (-2,-2) \\
      D & (0,-3) & (-2,-2) & (-1,-1) \\
      W & (-2,-2) & (-1,-1) & (-2,-2)
    \end{array}
    $$

    Against $C$, Player 1 prefers $D$; against $D$, Player 1 prefers $W$; against $W$, Player 1 prefers $D$. Thus $D$ is no longer dominant. Mutual cooperation still gives $(-1,-1)$, which is better for both than mutual defection $(-2,-2)$. Drawing the improvement arrows gives pure equilibria at $(D,W)$ and $(W,D)$ for this particular choice. Other third actions and payoffs can produce different arrows and equilibria.
    ~~~

5. Analyse either Stag Hunt or Chicken. Define its scenario, ordinal payoff ranking and equilibrium structure. Choose numerical payoffs if calculating mixed-strategy probabilities.

    ~~~{dropdown} Answer
    Stag Hunt has $R>T>P>S$ and pure Nash equilibria at mutual cooperation and mutual defection. Chicken has $T>R>S>P$ and two pure equilibria, with one player cooperating and the other defecting. Each also has a symmetric mixed equilibrium whose probabilities depend on the numerical payoffs. For example, $(R,T,P,S)=(4,3,2,0)$ for Stag Hunt or $(3,4,0,2)$ for Chicken gives cooperation probability $2/3$ for each player in that mixed equilibrium.

    ~~~

6. Explain why Tit for Tat performed well in Axelrod's tournaments. Give an environment or error process under which it may cease to do so.

    ~~~{dropdown} Suggested answer
    Tit for Tat cooperates first, then copies the opponent's previous action. It supports mutual cooperation, responds to defection and resumes cooperation after the opponent cooperates. Action errors can trigger repeated retaliation. A forgiving strategy can rank higher when errors are common, while Always Defect can rank higher against mostly defecting opponents.
    ~~~

7. Can you exploit a predictable rock–paper–scissors player?

    One claim is that men open with rock more often. Treat this as a hypothesis about observed play. You can explore it as a thought experiment or design and implement a study. Earlier work has examined departures from uniform play and responses to previous outcomes or information about opponents ([Wang, Xu and Zhou, 2014](https://doi.org/10.1038/srep05830); [Batzilis et al., 2019](https://doi.org/10.3390/g10020018)).

    For the calculations below, suppose an opponent independently chooses rock, paper and scissors with probabilities

    $$
    (q_R,q_P,q_S)=(0.50,0.30,0.20).
    $$

    Use payoffs of $+1$ for a win, $0$ for a draw and $-1$ for a loss.

    1. Calculate your expected payoff from each pure action. Which is the best response? Compare it with choosing each action with probability $1/3$.
    2. Does exploiting this opponent change the payoff matrix or the mixed Nash equilibrium of the original game? Distinguish a best response to a fixed opponent from an equilibrium in which both players can adjust.
    3. Your opponent notices that you always choose your best response. What should they do next? Explain why the initial advantage need not persist.
    4. Is knowing only that an opponent chooses rock more often than paper enough to identify your best response? Test the alternative distribution $(q_R,q_P,q_S)=(0.35,0.20,0.45)$, and explain why the full distribution matters.
    5. Design a study of the opening-move claim. Distinguish “men choose rock more often than paper” from “men choose rock more often than women”. What observations, comparison groups and uncertainty estimates would you need? Why are self-reported preferences not the same as observed throws, and why should first throws be analysed separately from later rounds? Explain why repeated throws from one person are not independent participants, and why a group average need not predict a particular opponent.

    ~~~{dropdown} Answer
    Against a fixed mixture, expected payoffs are

    $$
    \mathbb E[u(R)]=q_S-q_P,\qquad
    \mathbb E[u(P)]=q_R-q_S,\qquad
    \mathbb E[u(S)]=q_P-q_R.
    $$

    For the first distribution these are $-0.10$, $0.30$ and $-0.20$, so paper is best. Uniform randomisation gives expected payoff zero against any fixed mixture.

    The payoff matrix and uniform mixed Nash equilibrium are unchanged. If you become predictably paper, an adapting opponent can choose scissors.

    For the alternative distribution the payoffs are $0.25$, $-0.10$ and $-0.15$, so rock is best. The inequality $q_R>q_P$ alone is insufficient.

    ~~~

    ~~~{dropdown} Suggested considerations
    For the study, compare observed first throws from independent people, separating the within-group claim from the between-group claim. Estimate uncertainty across people; analyse later rounds and repeated throws separately. Group frequencies describe a population pattern, not every individual opponent.
    ~~~

## Optional extensions

These questions extend the material to population and evolutionary models.

1. Equation (8) uses four distinct ranks for the four outcomes usually labelled $T$, $R$, $P$ and $S$. Assign ranks 1–4 in all $4!=24$ ways. For each assignment, draw the payoff plane, mark the best responses and identify the pure Nash equilibria. Which assignments give dominance, coordination or anti-coordination? Do any produce a cyclic or matching-pennies pattern with no pure Nash equilibrium? Which one is the Prisoner’s Dilemma?

    ~~~{dropdown} Suggested answer
    All 24 permutations are mathematically valid strict ordinal symmetric two-player games, but they are not all Prisoner’s Dilemmas. The labels $T$, $R$, $P$ and $S$ refer to particular action profiles only when the usual Prisoner’s Dilemma interpretation is being used; after a permutation, do not assume that the highest rank is still “temptation”.

    Test the defining conditions directly: defection is dominant when $T>R$ and $P>S$, and mutual cooperation is better than mutual defection when $R>P$. Together these give $T>R>P>S$. Other permutations produce dominance, coordination or anti-coordination. None of these 24 symmetric cases produces a cyclic or matching-pennies pattern with no pure Nash equilibrium; that requires asymmetric player preferences.

    The atlas is broader: it includes all strict ordinal $2\times2$ games, including asymmetric games. The 24 cases here are its symmetric subset, with some equivalent after relabelling the actions.
    ~~~

2. Figure 10.4 places action profiles at the corners of a rectangle, while Figure 10.2 gives a parallelogram from numerical Prisoner's Dilemma utilities. Which geometric features carry information in each figure? What restrictions follow from strict ordinal rankings, zero-sum payoffs or symmetric payoffs?

    ~~~{dropdown} Suggested answer
    The rectangle in Figure 10.4 is a schematic action-profile grid: only adjacency and arrow directions matter. Figure 10.2 uses actual utility values, so its shape reflects those numbers; a different payoff assignment can give a different quadrilateral. Strict ordinal rankings require four distinct values on each player's payoff axis, so ties in either coordinate are excluded. Zero-sum payoffs put all points on a line, while symmetric payoffs make the set of points mirror across the line $u_1=u_2$.
    ~~~


3. Write pseudocode for an evolutionary iterated-Prisoner's-Dilemma tournament in which strategies are inherited, payoff determines fitness and mutation is possible. State how success will be measured.

    ~~~{dropdown} Suggested considerations
    Separate match scoring from producing the next generation. Choose a payoff-to-fitness rule and mutation process, then track payoff and strategy frequencies.
    ~~~

4. Distinguish one-shot play, repeated play, tournament success and evolutionary success. Why can the same strategy rank differently under each?

    ~~~{dropdown} Answer
    One-shot play has one simultaneous choice; repeated play allows responses to earlier actions. Tournament success means scoring well against the included opponents. Evolutionary success means becoming more common under the reproduction or copying rule. Changing the opponents, match length or population rule can change which strategy succeeds.
    ~~~

5. Rock–paper–scissors is a game in the game-theoretic sense. Write its payoff matrix, then explain what new assumptions are introduced when many agents reproduce or replace neighbours. Compare well-mixed and networked populations: who interacts, who imitates and how do strategies spread?

    ~~~{dropdown} Answer
    With rows and columns ordered rock, paper, scissors, row-player payoffs are

    $$
    A=\begin{pmatrix}0&-1&1\\1&0&-1\\-1&1&0\end{pmatrix}.
    $$

    The column player's payoff is its negative. A population model must also state who meets whom, how encounters affect replacement and when updates occur. In a well-mixed population, encounters follow the overall mixture; in a networked population, agents meet specified neighbours. Boundaries, starting frequencies and chance then affect the population history.
    ~~~

6. Replace rock–paper–scissors with rock–paper–scissors–lizard–Spock. Construct the $5\times5$ payoff matrix using $+1$ for a win, $-1$ for a loss and $0$ for a draw. Identify its zero-sum, symmetric and cyclic structure.

    ~~~{dropdown} Answer
    Order rows and columns as rock, paper, scissors, lizard, Spock. The row player's payoff matrix is

    $$
    A=
    \begin{pmatrix}
    0&-1&1&1&-1\\
    1&0&-1&-1&1\\
    -1&1&0&1&-1\\
    -1&1&-1&0&1\\
    1&-1&1&-1&0
    \end{pmatrix}.
    $$

    The column player's payoff is $-A$. The game is zero-sum and symmetric. Its dominance graph is cyclic: each action defeats two alternatives and loses to two, producing several overlapping cycles rather than one three-action loop.
    ~~~
