# Glossary

This glossary records the shared vocabulary of MATH3024. A term is normally **bolded when it is first introduced substantively** in a topic.

The definitions below are deliberately course-sized. They identify how a word is used here without pretending that every field uses it in exactly the same way. Where a term has several meanings, the model under discussion determines the relevant one.

## A

**Adaptation.** A change in an agent, rule or population caused by experience, selection or environmental feedback. Adaptation need not imply biological evolution. *(Weeks 1, 7 and 10)*

**Adaptive network.** A network in which node states and network connections co-evolve, so behaviour changes the network and the changed network alters later behaviour. *(Week 6)*

**Agent.** An individually represented component with its own state and update rule. An agent may be a person, animal, vehicle, particle or abstract decision-maker. *(Weeks 1, 5, 7 and 10)*

**Agent-based model (ABM).** A model constructed from individual agents, their states, their interactions and the world in which they act. *(Weeks 1 and 5)*

**Ant colony optimisation (ACO).** A family of optimisation algorithms in which candidate routes are constructed probabilistically and good routes reinforce shared environmental memory represented by pheromone. *(Week 7)*

**Attractor.** A state or set towards which trajectories approach. In an iterated function system, the attractor is the limiting set produced by repeated application of the maps. *(Week 2; wider dynamical-systems vocabulary)*

**Avalanche.** The complete cascade of topplings triggered by adding a grain to a stable sandpile. Its size, area and duration describe different aspects of the event. *(Week 8)*

## B

**Bifurcation.** A qualitative change in long-term behaviour as a parameter varies. This is useful wider vocabulary for transitions, although formal bifurcation theory is not assessed in this unit. *(Weeks 3, 6 and 8)*

**Boundary condition.** A rule specifying what happens at the edge of a domain, such as periodic wrapping, fixed values, reflection or loss from the system. *(Weeks 3, 4, 7 and 8)*

**Burn-in.** An initial part of a simulation discarded before measurements are collected, allowing the influence of the starting state to diminish. The chosen length is part of the simulation protocol and should be checked rather than assumed sufficient. *(Weeks 6 and 8)*

**Box-counting dimension.** An estimate of how the number of occupied boxes changes as the box size changes. It is one way to quantify multiscale spatial structure. *(Weeks 2 and 8)*

## C

**Calibration.** Using observations to choose or estimate model parameters. Agreement with the data used for calibration does not by itself provide an independent test of the model. *(Course-wide modelling practice)*

**Canonical model.** A deliberately selected model used as the main concrete example for a topic. It is not the only possible model of that phenomenon. *(All weeks)*

**Cellular automaton (CA).** A discrete model on a lattice whose site states are updated from a local rule. *(Week 4)*

**Chaos.** Deterministic dynamics with sensitive dependence on initial conditions, so nearby trajectories separate rapidly. Chaos, randomness and complexity are not synonyms. *(Weeks 0 and 1)*

**Claim.** A statement that an analysis argues is supported. For computational work, keep the claim together with the experiment performed, the evidence obtained and the limitations on its interpretation. *(Course-wide modelling practice)*

**Coarse-graining.** Replacing a fine description by variables that summarise behaviour over space, time or components. Coarse-graining loses detail in order to expose larger-scale structure. *(Weeks 3 and 8)*

**Complementary cumulative distribution function (CCDF).** For a variable $X$, the function $P(X\geq x)$. An empirical CCDF shows the fraction of observations at least as large as $x$ and is useful for inspecting a tail without choosing histogram bins. *(Weeks 2 and 8)*

**Collective intelligence.** Useful problem-solving behaviour produced by a group through interaction, memory or information sharing. Whether a system counts as collectively intelligent depends on what task and evidence are being considered. *(Week 7)*

**Complex system.** A system for which interactions, organisation across levels or history make the behaviour of the whole inadequately described by treating components as independent. This is a working description, not a checklist definition. *(Week 1 and course-wide)*

**Complexity.** The difficulty and structure produced when parts cannot be treated as fully separable or when more than one level of description is useful. In this unit, complexity is not a synonym for complication, randomness, chaos or computational cost, and complexity can occur without classical chaos. *(Week 1 and course-wide)*

**Computational experiment.** A planned use of computation in which relevant inputs or modelling choices are varied, other conditions are controlled, and stochastic conditions are repeated where necessary. Its design determines which comparisons and claims are supported. *(Course-wide modelling practice)*

**Configuration.** The complete assignment of states to all sites or agents at one time. *(Week 4)*

**Conjecture.** A statement suggested by examples, patterns or numerical results but not established by proof. Further computation can test a conjecture without converting finite evidence into a deductive proof. *(Course-wide mathematical practice)*

**Control parameter.** A parameter varied to move a system between macroscopic regimes, such as coupling strength, noise or occupation probability. Calling a parameter a control parameter does not imply that it is controlled by an agent within the model. *(Weeks 5, 6 and 8)*

**Correlation.** A statistical dependence between quantities. Correlation describes association; it does not by itself identify the interaction or causal mechanism that produced it. *(Weeks 5, 6, 8 and 9)*

**Correlation length.** A characteristic distance over which fluctuations remain related. Its growth near a continuous critical point indicates that increasingly distant parts of a system behave collectively. *(Weeks 5 and 8)*

**Critical point.** A parameter value separating macroscopic regimes, often accompanied by long correlations, large fluctuations and scale-free behaviour. *(Week 8)*

**Critical slowing down.** Increasingly slow recovery from perturbations near a critical point. *(Week 8)*

## D

**Density.** A quantity per unit space or a fraction of occupied components. In probability, a density instead describes how probability is distributed; the intended meaning must be stated. *(Weeks 3, 4, 5 and 9)*

**Deterministic model.** A model in which a state and parameter set determine the subsequent evolution exactly. Determinism does not guarantee practical predictability. *(Weeks 0 and 1)*

**Diffusion.** Spatial spreading driven by local differences in concentration or probability density. At a macroscopic level it smooths gradients; microscopically it may arise from random motion. *(Week 3)*

**Discretisation.** Replacing a continuous domain, time variable or equation by finitely many values and update steps that can be computed. The grid spacing and time step belong to the numerical approximation, not automatically to the represented system. *(Week 3)*

**Dynamics.** The rule or equations that change a model state through time. *(All model-building weeks)*

## E

**Emergence.** The appearance of a useful system-level pattern or behaviour that is not evident from one component considered in isolation. An emergent description does not make the component-level account irrelevant. *(Weeks 1 and 5–8)*

**Ensemble.** A collection of comparable runs, usually differing in random seed, initial condition or sampled population. Ensemble summaries show what is typical and how much outcomes vary. *(Weeks 1 and 5–10)*

**Evaluation budget.** A declared limit on how many times an objective function or other costly model output may be evaluated. Holding this budget fixed permits fairer comparisons between algorithms or population sizes. *(Weeks 4 and 7)*

**Entropy.** A measure of uncertainty in a probability distribution. Shannon entropy is the expected self-information of an outcome. *(Week 9)*

**Equilibrium.** A state or distribution that does not change under the relevant dynamics. The precise meaning depends on whether the model is deterministic, stochastic or statistical. *(Weeks 1, 6, 8 and 10)*

**Exploitation.** Using information already acquired to concentrate effort on regions or choices known to perform well. Too much exploitation can make a search converge prematurely. *(Week 7)*

**Exploration.** Searching unfamiliar regions or trying less-tested choices in order to discover alternatives. Too much exploration can prevent a search from making effective use of what it has learned. *(Week 7)*

## F

**Feedback.** A loop in which a system output influences later inputs or dynamics. **Positive feedback** reinforces an initial change or amplifies a difference; **negative feedback** opposes a change and can regulate or stabilise behaviour. “Positive” and “negative” describe the direction of the loop, not whether its outcome is desirable. *(Weeks 1, 6 and 7)*

**Field.** A quantity defined throughout a spatial domain, such as a chemical concentration or density. A field description represents what is present at each location rather than tracking named individuals. *(Weeks 3 and 8)*

**Finite-size effect.** Behaviour caused or modified by simulating a finite population or domain, rather than the large-system limit being discussed. *(Weeks 4–6 and 8)*

**Fitness.** A measure of reproductive success or expected contribution to later generations. In evolutionary games it is commonly derived from payoff, but payoff and fitness are not identical concepts. *(Week 10)*

**Fractal.** A set or pattern with non-trivial structure across scales. Exact self-similarity is sufficient but not necessary for fractal geometry. *(Week 2)*

**Fractal dimension.** A dimension intended to quantify how measured detail changes with scale. Different definitions and estimation procedures need not give identical finite-data results. *(Weeks 2 and 8)*

## G–I

**Garden of Eden configuration.** A cellular-automaton configuration with no predecessor under the global update map. *(Week 4)*

**Hamming distance.** The number of sites at which two discrete configurations differ. *(Week 4)*

**Heavy-tailed distribution.** A distribution that gives relatively substantial probability to unusually large observations. A heavy tail is not automatically a power law. *(Weeks 2 and 8)*

**Heterogeneity.** Variation among components, for example in natural frequencies, preferences, thresholds or responsiveness. *(Weeks 1, 5–7)*

**Information.** In ordinary modelling language, information may mean any state or signal available to a component. In information theory it is defined through probabilities, with self-information measuring surprise and entropy measuring expected uncertainty. State which meaning is intended. *(Weeks 7 and 9)*

**Initial condition.** The state from which a model run begins. In a stochastic model, the initialisation procedure and random seed are also part of a reproducible specification. *(All simulated models)*

**Invariant.** A quantity or property that should remain unchanged under specified updates. Checking an invariant, such as conservation during an interior toppling, is one way to verify an implementation. *(Weeks 4 and 8; course-wide modelling practice)*

**Instability.** Growth of a small perturbation under the dynamics. Instability has to be defined relative to a state and a class of perturbations; it is not another word for randomness, chaos or complexity. *(Weeks 1 and 3)*

**Interaction.** A dependence of one component's update on another component or on shared environmental information. *(Weeks 1 and 4–10)*

**Iterated function system (IFS).** A collection of contraction maps whose repeated application generates a limiting set. *(Week 2)*

## L–M

**Lattice.** A regular discrete arrangement of sites on which states or agents may be placed. *(Weeks 3, 4, 8 and 10)*

**Local rule.** An update determined from a component and a restricted neighbourhood rather than the complete system. *(Weeks 1 and 3–5)*

**Mean-field approximation.** A reduction that replaces detailed interactions or spatial correlations by an average field. Its usefulness depends on whether the omitted correlations matter. *(Weeks 4 and 6)*

**Mechanism.** The represented process proposed to produce a behaviour, not merely a curve or pattern that resembles the observation. *(All weeks)*

**Memory.** Dependence of later behaviour on information retained from the past. Memory may be stored in an agent, a field, a network, a population or an altered environment. *(Weeks 1, 7 and 10)*

**Model.** A purposeful representation that retains selected features of a system in order to answer a question. *(All weeks)*

**Multiscale.** Involving relevant structure or dynamics at more than one spatial, temporal or organisational scale. *(Weeks 1, 2 and 8)*

**Mutual information.** The reduction in uncertainty about one variable obtained by knowing another. It measures statistical dependence, not meaning or causation. *(Week 9)*

## N–O

**Neighbourhood.** The set of components permitted to influence a given component's update. It may be geometric, metric, topological or explicitly network-defined. *(Weeks 1 and 3–6)*

**Nash equilibrium.** A strategy profile in which no player can improve their payoff by changing strategy alone while the other players' strategies remain fixed. It need not maximise collective welfare. *(Week 10)*

**Network.** A collection of nodes and edges used to represent who or what can interact. The network may be fixed, evolving or coupled to node dynamics. *(Weeks 6–8 and 10)*

**Noise.** Random variation included in a model or observation process. Its location, distribution and interpretation are modelling choices; different noise conventions can define different models. *(Weeks 1, 3, 5 and 6)*

**Numerical evidence.** Reproducible computational output connected to a stated question and interpreted through relevant comparisons or alternatives. A simulation output is a consequence of its model, numerical method and initial condition; it does not become evidence for a wider claim merely by being plotted. *(Course-wide modelling practice)*

**Nonlinearity.** A dependence for which effects do not simply add in proportion to causes. Nonlinearity permits interaction effects and multiple regimes but does not by itself imply chaos. *(Weeks 0, 1 and 3)*

**Null model.** A simpler comparison model representing what would be expected without the mechanism or structure of interest. *(Course-wide modelling practice)*

**Observable.** A quantity extracted from a model or system for inspection or comparison. An observable may describe an individual component, a field or the whole system. *(All analysis weeks)*

**Objective function.** A numerical rule used to evaluate a candidate solution. It states what the search treats as better, but need not capture every consideration in the original problem. *(Week 7)*

**Order.** A context-dependent term. It may refer to collective organisation, the order of a phase transition, the order of an equation or the sequence in which updates occur. The intended meaning should be stated rather than inferred from the everyday word. *(Weeks 3–8)*

**Optimum.** A candidate solution with the best objective value over a stated feasible set. A local optimum is best only within a neighbourhood; a global optimum is best over the complete feasible set. *(Week 7)*

**Order parameter.** A macroscopic quantity used to distinguish collective regimes, such as polarisation in the Vicsek model or coherence in the Kuramoto model. *(Weeks 5, 6 and 8)*

## P

**Parameter.** A fixed input controlling a model or experiment during one run. A state variable evolves; a parameter does not unless the model explicitly promotes it to a dynamic variable. *(All weeks)*

**Parameter sweep.** A structured comparison in which one or more parameters are varied and the resulting observables are recorded. *(Weeks 1 and 3–10)*

**Payoff.** The numerical outcome assigned to a player for a combination of strategies. A payoff represents what the model treats as preferable; it is not automatically biological fitness or collective welfare. *(Week 10)*

**Particle swarm optimisation (PSO).** An optimisation method in which candidate solutions update their velocities using retained motion, personal best positions and shared best information. *(Week 7)*

**Path dependence.** Dependence of an outcome on the sequence of earlier events, not only the present state or final inputs. *(Weeks 1, 7 and 10)*

**Percolation threshold.** The occupation probability at which a spanning cluster first appears in the large-system limit. *(Week 8)*

**Phase.** Position within a repeating cycle, usually represented modulo $2\pi$. *(Week 6)*

**Phase locking.** A maintained phase relationship in which the phase difference between oscillators remains constant, not necessarily zero. *(Week 6)*

**Phase space.** A space whose coordinates describe a system's state. Movement in phase space represents changing state, not necessarily physical movement. *(Week 6)*

**Phase transition.** A qualitative change in macroscopic behaviour as a control parameter crosses a threshold. Finite systems may round or shift the apparent transition. *(Weeks 5, 6 and 8)*

**Power law.** A relationship of the form $y=Cx^{-\alpha}$ (or another power of $x$). A straight-looking log–log plot is suggestive but is not sufficient evidence by itself. *(Weeks 2 and 8)*

**Probability distribution.** A rule assigning probabilities to possible outcomes of a random variable. A distribution, rather than one observation, is the input to the information measures used in Week 9. *(Weeks 1, 2 and 5–9)*

**Proof.** A deductive argument establishing a result from stated assumptions. Numerical examples can motivate or test a conjecture, but no finite collection of simulations is a proof of a general mathematical claim. *(Course-wide mathematical practice)*

**Pseudocode.** A precise, language-independent description of an algorithm's logic, update order, stopping rule and returned output. *(All workshops)*

## R

**Random seed.** A value used to initialise a pseudorandom number generator. Recording it makes a stochastic run repeatable; comparing several seeds tests whether a conclusion depends on one random realisation. *(All stochastic workshops)*

**Random variable.** A mapping from possible outcomes to values. Its probability distribution states how likely those values are. *(Week 9)*

**Reaction–diffusion model.** A spatial model combining local reaction terms with diffusion of one or more fields. *(Week 3)*

**Replicator equation.** An equation for strategy frequencies in which strategies grow or decline according to their payoff relative to the population average. *(Week 10)*

**Reproducibility.** The capacity to obtain the stated result again from a complete specification, code, data and random-seed protocol. *(Course-wide modelling practice)*

**Robustness.** Persistence of a conclusion under reasonable changes to seeds, initial conditions, parameters, system size or modelling choices. *(Weeks 4–10)*

**Rule space.** The set of possible update rules within a specified model family. *(Week 4)*

## S

**Scale-free.** Lacking one characteristic scale over a stated range. The term is used differently across literatures, so the measured quantity and range should be given. *(Weeks 2 and 8)*

**Scale invariance.** A property whose mathematical form is preserved under a change of scale, possibly up to a multiplicative factor. *(Weeks 2 and 8)*

**Scaling range.** The finite interval of scales over which a proposed scaling relationship is assessed. Its selection must be stated because fitted exponents and conclusions can depend on it. *(Weeks 2 and 8)*

**Self-information.** The surprise assigned to an outcome of probability $p$, conventionally $-\log p$. *(Week 9)*

**Self-organisation.** The formation or maintenance of macroscopic organisation through interactions among components, without a controller specifying the resulting pattern in detail. *(Weeks 5–8)*

**Self-organised criticality.** The proposal that slow driving and threshold dynamics can bring a system towards a critical-like state without externally tuning a control parameter to a special value. *(Week 8)*

**Self-similarity.** Similar structure appearing under magnification. It may be exact, statistical or approximate over a finite range. *(Week 2)*

**Sensitivity analysis.** A systematic check of how conclusions change when inputs or modelling choices are varied. *(Course-wide modelling practice)*

**Solution space.** The set of candidate solutions that an optimisation method is permitted to search. Its coordinates and feasible bounds are part of the problem representation. *(Week 7)*

**Stability.** The response of a state or pattern to a small perturbation. A stable state remains nearby or returns after the perturbation; the relevant perturbations and notion of distance must be stated. Model stability and numerical stability are different claims. *(Weeks 1, 3, 6 and 8)*

**State.** The information required to continue a model's evolution from the present time. State may belong to one agent, a field or the whole system; its meaning is fixed by the chosen representation. *(All weeks)*

**State space.** The set of all states or configurations allowed by a model. *(Weeks 4 and 6)*

**Steady state.** Behaviour that is constant in time, or statistically unchanged, under the chosen description. It need not mean that every microscopic component is motionless. *(Weeks 3, 5, 6 and 8)*

**Stigmergy.** Indirect coordination through persistent changes to a shared environment, such as pheromone deposited on a network. *(Week 7)*

**Stochastic model.** A model containing explicitly random events or sampled quantities, so repeated runs from the same stated conditions can differ. *(Weeks 1–10)*

**Strategy.** A rule or choice specifying how a player acts. In a repeated game, a strategy may depend on the history of earlier encounters. *(Week 10)*

**Success criterion.** A declared condition used to decide whether a run has achieved an adequate result. It should be chosen before comparing stochastic algorithms and reported alongside the evaluation budget. *(Week 7; course-wide modelling practice)*

**Synchronisation.** The establishment of a maintained timing relationship through interaction. Coincidental alignment without altered dynamics is not sufficient. *(Week 6)*

**System.** The part of the world, mathematical construction or computational process being studied. A model represents selected features of a system; it is not the system itself. *(All weeks)*

## T–V

**Transfer entropy.** A directional information measure comparing prediction of a target from its own past with prediction that also uses another process's past. It does not by itself establish causal mechanism. *(Week 9)*

**Transient.** The non-stationary part of a run before the long-time regime used for analysis has been reached. *(Weeks 3 and 5–8)*

**Universality.** The appearance of the same large-scale behaviour or critical exponents in systems with different microscopic details. A universality claim is stronger than observing vaguely similar plots. *(Weeks 5 and 8)*

**Update order.** The scheduling rule specifying whether components update synchronously, asynchronously, sequentially or in a random order. Different choices can define different models. *(Weeks 1, 4, 7, 8 and 10)*

**Validation.** Assessing whether a model is adequate for its intended question by comparison with observations, accepted behaviour or relevant empirical constraints. *(Course-wide modelling practice)*

**Verification.** Checking that equations or rules have been implemented as intended, using limiting cases, invariants, known results and intermediate states. *(Course-wide modelling practice)*

## Canonical models and named constructions

**Abelian sandpile model.** A driven lattice model in which unstable sites topple and redistribute grains; used here to study avalanches and self-organised criticality. *(Week 8)*

**Cantor set.** A fractal obtained by repeatedly removing the open middle third of each retained interval. *(Week 2)*

**Game of Life.** Conway's two-dimensional cellular automaton with the B3/S23 outer-totalistic rule. *(Week 4)*

**Gray–Scott model.** A two-field reaction–diffusion model used here to connect local chemical kinetics, diffusion and spatial pattern. *(Week 3)*

**Kuramoto model.** A model of heterogeneous phase oscillators coupled through their phase differences. *(Week 6)*

**Prisoner's Dilemma.** A game in which individual incentives favour defection although mutual cooperation gives both players a better outcome than mutual defection. *(Week 10)*

**Schelling segregation model.** An agent-based model in which local similarity preferences can generate population-level segregation. *(Week 1)*

**Sierpiński triangle.** A fractal obtained by repeated triangular subdivision, an iterated function system, a chaos game or several other equivalent constructions. *(Week 2)*

**Vicsek model.** A minimal model of self-propelled agents that align locally in the presence of noise. *(Week 5)*
