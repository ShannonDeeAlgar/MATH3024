# Practice questions

Unless stated otherwise, use base-2 logarithms, so entropy is measured in bits. Take $0\log_2 0=0$.

## Core questions

1. Define Shannon entropy, joint entropy, conditional entropy and mutual information. Use the information diagram to state and interpret their relationships.

    ~~~{dropdown} Answer
    Shannon entropy measures uncertainty in one variable. Joint entropy is Shannon entropy applied to the combined variable and measures uncertainty in the pair. Conditional entropy averages the Shannon entropy of the relevant conditional distributions. Mutual information measures how much knowing one variable reduces uncertainty about the other.

    $$
    \begin{aligned}
    H(X)&=-\sum_x p(x)\log_2 p(x),\\
    H(X,Y)&=-\sum_{x,y}p(x,y)\log_2 p(x,y),\\
    H(X\mid Y)&=H(X,Y)-H(Y),\\
    I(X;Y)&=H(X)+H(Y)-H(X,Y)\\
    &=H(X)-H(X\mid Y)=H(Y)-H(Y\mid X).
    \end{aligned}
    $$

    The non-overlapping parts are the conditional entropies. The overlap is mutual information. Their union is the joint entropy.
    ~~~

2. Self-information $h(x)$ quantifies the surprise of one outcome. State the six requirements used to define it. What unique form do they produce once the unit is fixed? Why does base 2 give bits, and what changes if we use base $e$ or base 10?

    ~~~{dropdown} Answer
    Surprise depends only on probability, varies continuously, increases as probability falls and is non-negative. Surprises add for independent outcomes. A guaranteed event has zero surprise, while surprise diverges as probability approaches zero. Once the unit is fixed, these requirements give the unique logarithmic form $h(x)=-\log_bP(x)$.

    Base 2 measures information in binary units. An outcome with probability $1/2$ has surprise one bit. Base $e$ gives nats and base 10 gives hartleys. Changing the base changes the unit, not the uncertainty. For $b>1$,

    $$H_b(X)=\frac{H_2(X)}{\log_2 b}.$$

    ~~~

3. Suppose we observe $X$ itself. What is $H(X\mid X)$? Hence evaluate $I(X;X)$. Explain how the result connects entropy as uncertainty with entropy as the information required to resolve that uncertainty.

    ~~~{dropdown} Answer
    Once the state of $X$ is revealed, no uncertainty about $X$ remains.

    $$H(X\mid X)=0.$$

    Therefore,

    $$I(X;X)=H(X)-H(X\mid X)=H(X).$$

    The original entropy is the average information required to resolve all uncertainty about $X$. Entropy can therefore describe both the uncertainty present and the information needed to remove it.
    ~~~

4. For a fixed set of $M$ possible outcomes, explain why the uniform distribution has the greatest entropy. What is the maximum value? Then use $f(p)=-p\log_b p$ and the sign of $f''(p)$ to justify why making unequal probabilities more equal increases entropy.

    ~~~{dropdown} Answer
    Equal probabilities leave no preferred prediction, so uncertainty is greatest when $p_i=1/M$. The maximum is

    $$H_{\max}=\log_b M.$$

    Since

    $$f''(p)=-\frac{1}{p\ln b}<0,$$

    $f$ is concave. Making two unequal probabilities more equal increases their combined contribution to entropy. Repeating this gives the uniform distribution.

    The Jensen's inequality step is optional. Equivalently, Jensen's inequality gives

    $$
    \frac1M\sum_{i=1}^{M}f(p_i)
    \leq f\!\left(\frac1M\right),
    $$

    so $H(X)\leq\log_b M$, with equality only when every $p_i=1/M$.
    ~~~

5. Use the distribution explorer in the Reader to compare distributions within one family and across families. Find two different distributions with the same or similar entropy. Is the distribution family alone enough to determine which distribution has greater entropy? Are the mean and variance enough?

    Compare discrete entropy $H$ for discrete outcomes and differential entropy $H^{\mathrm{dx}}$ for continuous densities. For $H^{\mathrm{dx}}$, use the same measurement units.

    ~~~{dropdown} Suggested considerations
    For a binomial distribution, change $n$ and then $p$. For a Gaussian, change the mean and then the spread; for a uniform distribution, change the location and then the width. Entropy depends on the full probability distribution. Gaussian differential entropy changes with standard deviation and stays fixed under a shift in mean; uniform differential entropy changes with width and stays fixed under a shift in location. Different distributions can have equal entropy. Matching rounded values may only be approximate.
    ~~~

6. Estimate letter probabilities in two English texts from different authors or writing styles. Plot the probabilities and calculate single-letter entropy. Do similar entropy values imply similar letter distributions?

    ~~~{dropdown} Suggested considerations
    Decide how to handle case, spaces and punctuation. Divide each letter count by the total number of counted letters. Use the same choices and similar sample lengths for each text. Different distributions can have similar entropy. Letter frequencies ignore order and dependence between letters.
    ~~~

7. Construct efficient yes/no questions for identifying a letter. How does the strategy change when letters are not equally likely? First use four letters with probabilities $(1/2,1/4,1/8,1/8)$. Then identify one face of a fair die. Compare its entropy with the best achievable average number of questions. Explain why they differ, when equality can hold and why coding blocks of outcomes can approach the bound.

    ~~~{dropdown} Answer
    Label the letters $A,B,C,D$. Ask whether it is $A$, then $B$, then $C$, stopping once it is identified. The question counts are $1,2,3,3$, giving

    $$\tfrac12(1)+\tfrac14(2)+\tfrac18(3)+\tfrac18(3)=1.75.$$

    This equals the entropy, so the strategy is optimal. An outcome reached after $\ell_i$ questions has path length $\ell_i$. Ideally $2^{-\ell_i}=p_i$, giving $\ell_i=-\log_2p_i$. Averaging these ideal lengths gives $H(X)$.

    A valid binary tree cannot have an average length below entropy. Equality is possible here because the probabilities are powers of one half and the ideal lengths are integers.

    A fair die has entropy $\log_2 6\approx2.585$ bits. This fractional value is an average coding rate. An optimal one-roll tree uses two questions for two faces and three questions for four faces, so

    $$L=\frac{2(2)+4(3)}6=\frac83\approx2.667.$$

    The entropy is the ideal average information required. The larger value is the best achievable average for one roll. An optimal one-outcome tree satisfies $H(X)\leq L<H(X)+1$. Coding blocks of $n$ outcomes leaves less than one extra bit per block, so the overhead per outcome is less than $1/n$ and approaches zero.

    For another alphabet, try splitting the remaining probability into roughly equal groups.
    ~~~

8. Use the simplified Schelling focal–neighbour distribution from the Reader, with $p(\text{yellow},\text{yellow})=0.40$, $p(\text{yellow},\text{blue})=0.10$, $p(\text{blue},\text{yellow})=0.10$ and $p(\text{blue},\text{blue})=0.40$. Calculate $H(X)$, $H(Y)$, $H(X,Y)$, both conditional entropies and the mutual information. Compare the result with the Week 1 similarity ratio. Why is the pair table still needed when mutual information is known? How does this local construction differ from $I(X;L)$, where $L$ is a region?

    ~~~{dropdown} Answer
    Sum rows and columns to obtain $p_X=p_Y=(0.5,0.5)$. In bits, rounded to four decimal places,

    $$
    \begin{aligned}
    H(X)&=1,& H(Y)&=1,\\
    H(X,Y)&=1.7219,\\
    H(X\mid Y)&=0.7219,& H(Y\mid X)&=0.7219,\\
    I(X;Y)&=0.2781.
    \end{aligned}
    $$

    The same-group probability is $0.8$, so this corresponds to a mean local similarity of $0.8$ under the stated sampling rule. Mutual information measures dependence strength. The pair table or similarity ratio is still needed to show that the dependence comes from matching neighbours rather than some other reliable pairing pattern.

    $I(X;Y)$ measures association between focal and neighbour groups. $I(X;L)$ measures how much a region reveals about group and is the more common entropy-based segregation construction. Its value depends on how the regions are defined.

    ~~~

9. Sample a fair die 20, 100 and 1000 times. Obviously, do this with code rather than literally rolling a die. Estimate the outcome probabilities and entropy. How does sample length affect the estimates?

    ~~~{dropdown} Suggested considerations
    Repeat each sample length and compare with $\log_2 6$. Keep the die fair throughout. Short samples can miss outcomes and give uneven frequencies, so their entropy can be below $\log_2 6$. Larger samples usually give more stable estimates. Sampling variation produces the differences between repeats.
    ~~~

10. Bin a continuous variable to calculate discrete entropy. Show how the result depends on bin width and state how you would report that choice. Use a uniform variable on $[0,1]$ as one example. Why is this not differential entropy?

    ~~~{dropdown} Answer
    With $M$ equal bins, each has probability $1/M$ and entropy is $\log_2 M$. Halving bin width adds one bit. These are bin probabilities, so the measure is $H$. For fine equal bins of width $\Delta$, $H(B_\Delta)\approx H^{\mathrm{dx}}(X)+\log_2(1/\Delta)$. As the bins narrow, binned entropy includes an increasing resolution term. The continuous uniform variable has $H^{\mathrm{dx}}=0$ while remaining maximally spread over its fixed interval. Use the same bins for comparisons.
    ~~~

11. An AI was asked to describe Shannon entropy using first one word, then two words, and so on up to ten words. It produced the following ladder unchanged:

    | Word limit | AI-generated description |
    |---:|---|
    | 1 | Uncertainty. |
    | 2 | Average surprise. |
    | 3 | Expected information content. |
    | 4 | Average surprise of outcomes. |
    | 5 | Average bits needed per outcome. |
    | 6 | Uncertainty before observing a random outcome. |
    | 7 | Minimum average bits to encode each outcome. |
    | 8 | Expected surprise of outcomes drawn from a distribution. |
    | 9 | Average yes/no questions needed to pin down the outcome. |
    | 10 | Uncertainty in a variable's value, blind to what values mean. |

    Discuss the ladder:

    1. Which descriptions state the mathematical definition, an interpretation or a limitation?
    2. Which require logarithms base 2?
    3. Which are literally correct for one observation, and which are asymptotic coding claims?
    4. What is missing from “uncertainty”?
    5. Which description is most useful for understanding a complex system?
    6. Revise one description without exceeding its word limit.

    ~~~{dropdown} Suggested considerations
    “Average surprise” and “expected surprise of outcomes drawn from a distribution” most directly express the definition. “Uncertainty before observing a random outcome” gives its main probabilistic interpretation. “Expected information content” is equivalent once self-information has been defined.

    “Average bits needed,” “minimum average bits” and “average yes/no questions” assume base-2 logarithms. They describe ideal or asymptotic coding. For one outcome, a code length or literal number of questions must be an integer; entropy is the lower bound approached per outcome by efficient block coding.

    A complete description identifies the variable, its possible outcomes, its probability distribution and the averaging. One six-word revision is “Average uncertainty under a specified probability distribution.”

    The final description states an important limitation. Entropy is unchanged when outcome labels are permuted. It measures uncertainty in the chosen distribution. Meaning, geometry and organisation require additional structure in the variables.

    A concise conclusion is:

    > Shannon entropy is the expected surprise of outcomes under a specified probability distribution. In base 2, it is also the ideal asymptotic average information required per outcome.
    ~~~

12. In the Schelling model, let $K$ be the number of same-group occupied neighbours and let $S$ be the proportion of occupied neighbours in the same group. What do $H(K)$ and $H(S)$ measure? Could either establish that the population is highly segregated without seeing its distribution or mean similarity?

    ~~~{dropdown} Answer
    $H(K)$ measures variation in same-group neighbour counts. $H(S)$ measures variation in local similarity ratios. Either is zero whenever every sampled agent has the same value, whether that value is low or high. A larger entropy means that several values occur with substantial probability. Inspect the distribution and its mean to see whether local similarity is generally low or high. If $S$ is binned, use the same bins for every comparison.
    ~~~

13. Two Schelling grids have the same numbers of yellow, blue and empty sites. One is well mixed and the other is segregated. Let $Z$ be the state of a uniformly sampled site and let $X$ be the group of a sampled occupied agent. Explain why both $H(Z)$ and $H(X)$ are unchanged. What distribution could retain local organisation, and what would independence look like? Why would one information value still be insufficient to describe the spatial pattern completely?

    ~~~{dropdown} Suggested answer
    Movement conserves the numbers of yellow, blue and empty sites, so the site-state distribution $P(Z)$ is unchanged. Conditioning on occupied sites gives the same fixed yellow–blue proportions, so $P(X)$ and $H(X)$ are unchanged as well. Both marginals discard spatial arrangement.

    A focal–neighbour joint distribution $P(X,Y)$ retains one local relationship. Under independence it factorises as $P(x,y)=P(x)P(y)$ for every pair of values and $I(X;Y)=0$; segregation usually makes neighbouring groups dependent.

    The joint distribution records the sampled relationship. Different cluster shapes or arrangements can have the same pair probabilities and mutual information. Region, distance, cluster, geometric or network measures may therefore be needed as well. Information theory measures uncertainty and dependence; complexity requires a broader description.
    ~~~

## Optional extensions

14. Compare the sequences `010101010101` and `001101011100`. Calculate their entropy from individual symbols and overlapping consecutive pairs. What information is retained by the single-symbol frequencies, and what additional information is retained by the pair frequencies?

    ~~~{dropdown} Answer
    Both contain six zeros and six ones, giving entropy one bit. In pair order $(00,01,10,11)$, the counts are $(0,6,5,0)$ and $(2,3,3,3)$. Dividing by 11 gives pair entropies of about $0.994$ and $1.981$ bits per pair. Shuffling preserves single-symbol counts and entropy. Counting consecutive pairs or longer blocks includes some order, but longer blocks need more data.
    ~~~

15. Suppose $X_t$ and $Y_t$ are time series from a proposed leader and follower. State what entropy and mutual information measure. Why does nonzero mutual information not establish that one causes the other? Optionally discuss transfer entropy.

    ~~~{dropdown} Answer
    Entropy describes uncertainty in one signal. Mutual information describes undirected dependence. Transfer entropy measures directed predictive dependence after accounting for the target's own past. Common influences can produce these relationships, so causal claims require separate evidence.
    ~~~

16. Calculate permutation entropy for $(1,3,2,4,5)$ using overlapping windows, lag one and embedding length two. Use $H_{\mathrm{perm}}/\log_2(m!)$ for the normalised value at embedding length $m$. Then try length three. How do the pattern counts and sample size change? The sequence has no ties.

    ~~~{dropdown} Answer
    At length two, three windows rise and one falls. Their probabilities give $H_{\mathrm{perm}}=0.8113$ bits, also the normalised value. At length three, all three windows have different patterns, giving $\log_2 3$ bits and a normalised value of $0.6131$. Longer windows increase the possible patterns while reducing the observations.
    ~~~

17. A box contains either a fair coin or a coin with $P(H)=0.8$. Let $\Theta$ be the unknown coin type and let $D$ be the results of several tosses. What would a Bayesian analysis require and calculate? If the joint distribution $p(\Theta,D)$ is available, what do $H(\Theta)$, $H(\Theta\mid D)$ and $I(\Theta;D)$ measure? If we estimate heads and tails probabilities from counts and calculate their entropy, have we performed Bayesian inference?

    ~~~{dropdown} Suggested answer
    Bayesian inference specifies a prior $p(\theta)$ and a likelihood $p(d\mid\theta)$. Bayes' rule uses the observed data $d$ to calculate the posterior $p(\theta\mid d)$. This updates the probability assigned to each coin type.

    Bayesian updating uses the prior, likelihood and observed data to produce the posterior. Given $p(\Theta,D)$, $H(\Theta)$ measures prior uncertainty about the coin type. $H(\Theta\mid D)$ is the expected posterior uncertainty, averaged over possible datasets. For one observed dataset $d$, $H(\Theta\mid D=d)$ measures the uncertainty in $p(\theta\mid d)$. Mutual information $I(\Theta;D)$ is the expected reduction in uncertainty about the coin type.

    Entropy calculated from heads and tails frequencies concerns uncertainty in a toss outcome. The posterior concerns uncertainty about which coin is in the box. A plug-in entropy calculation summarises toss frequencies; Bayesian updating requires a prior and likelihood. The methods can be combined because a Bayesian analysis provides distributions that information-theoretic quantities can describe.
    ~~~
