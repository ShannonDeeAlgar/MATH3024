# Week 10 workshop · instructor guide

The workshop is open-ended. Students choose a question, so their assumptions, observables and experiments will differ. Assess the modelling process rather than reproduction of one canonical ranking.

## Minimum requirements

Ask students to complete one of the following:

1. implement and check a single repeated match;
2. compare at least two conditions while changing one declared factor;
3. report the observable, the comparison and one limitation.

Students who get further can implement a round-robin tournament or a simple population update.

## Checks for the baseline implementation

With \((T,R,P,S)=(5,3,1,0)\), 50 rounds and no noise:

- Always Cooperate against Always Cooperate gives payoff \((3,3)\) every round;
- Always Defect against Always Cooperate gives payoff \((5,0)\) every round;
- Always Defect against Always Defect gives payoff \((1,1)\) every round;
- Tit for Tat against Always Defect gives Tit for Tat one initial sucker payoff and then mutual punishment. Over 50 rounds the totals are \((49,54)\), with Tit for Tat first and Always Defect second;
- both strategies choose before either history is updated in a round.

The exact numbers should change if students choose another horizon or payoff matrix. The invariants are the simultaneity, the payoff lookup and the declared history rule.

## What to look for in the model specification

Students should be able to identify:

- the question and the factor being changed;
- the interaction rule and what each strategy can observe;
- whether the comparison is a match, fixed-field tournament or changing population;
- the observable and why it addresses the question;
- the repetition or seed policy;
- at least one limitation or alternative explanation.

Common problems are changing several factors at once, treating a tournament rank as a property of a strategy in general, and describing a population process while only simulating a fixed tournament.

## Suggested discussion answers

**Does forgiveness help?** It can protect cooperation after noise, but may be exploitable by persistent defectors. The answer depends on the opponent field, error rate and how forgiveness is defined.

**Does longer play change the ranking?** It can change the weight of opening moves and the value of recovering from mistakes. There is no general direction without specifying the strategies and opponent field.

**Does the opponent field matter?** Yes. A strategy’s score is an average over its opponents, so changing the field changes what “successful” means.

**Does tournament success imply evolutionary success?** No. Evolution changes strategy frequencies, which changes the opponents encountered. A fixed tournament and a population process answer different questions.

## Reference implementation

The previous long notebook is retained as `Axelrod_tournament_reference.ipynb`, and the compact engine is also available in `axelrod_tournament.py`. Use these to check student implementations after they have written their own pseudocode and model specification. Do not make the reference ranking the expected answer for every student question.
