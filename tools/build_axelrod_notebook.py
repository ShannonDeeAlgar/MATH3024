"""Generate the self-contained teaching notebook from the tested match engine.

Print an apply_patch patch; do not overwrite a student notebook silently.
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
cells = []


def md(id, text):
    cells.append({'cell_type':'markdown','id':id,'metadata':{},'source':text.strip().splitlines(keepends=True)})


def code(id, text):
    cells.append({'cell_type':'code','id':id,'metadata':{},'source':text.strip().splitlines(keepends=True),
                  'execution_count':None,'outputs':[]})


md('title', '''# Week 10 optional workshop · Repeated games and an Axelrod-style tournament

<span class="workshop-download-enabled" aria-hidden="true"></span>

This optional workshop asks three questions: which strategies score well against this field, does winning individual matches predict tournament success, and how robust are the results to the simulation conditions? Use it if time allows.

This is a small teaching tournament, not a reproduction of Axelrod’s historical entrants or rankings. It includes later strategies as well as familiar early ones. We implement the rules directly so that every decision can be inspected. NumPy and Matplotlib are the only dependencies; run the notebook from top to bottom.

The sequence is one match → repeated round-robin tournaments → opponent-level explanation → controlled sensitivity tests. There is no reproduction, selection or mutation of strategies here. Those belong to the subsequent evolutionary model.''')
md('conditions','''## Specify the experiment before running it

| Choice | Baseline |
|---|---|
| Payoffs | temptation 5, mutual-cooperation reward 3, mutual-defection punishment 1, sucker’s payoff 0; higher is better |
| Match | 200 simultaneous rounds, all rounds weighted equally; strategies do not receive the stopping round |
| Opponents | seven named strategies, equally weighted |
| Self-play | included, using two separate copies; their scores are averaged into one opponent contribution |
| Repetitions | 30 complete tournaments, with independently seeded matches |
| Noise | zero in the baseline; extensions independently flip each intended action with a stated probability |
| Memory | realised actions from the current match only; reset between matches |
| Ranking | median across repetitions of each strategy’s mean payoff per round across opponents |
| Wins | fraction of non-self matches in which the focal player strictly outscores its opponent; draws are not wins |

These positive payoffs are the conventional tournament example, not a change of sign in the reader’s prison sentences. Both matrices satisfy the prisoner’s-dilemma ordering, but their numerical incentives differ. The fixed horizon is a simulation budget, not a claim that these rules are equilibrium strategies for a known finite-horizon game.

A tournament repetition is one independent realisation of all matches. The middle-50% intervals below describe variation between repetitions, not confidence intervals for a mean and not variation between agents within one match.''')
md('rules','''### Strategies

| Strategy | Rule |
|---|---|
| Always Cooperate | always C |
| Always Defect | always D |
| Tit for Tat | start C, then copy the opponent’s previous realised action |
| Grudger | start C; after any opponent defection, defect for the rest of this match |
| Tit for Two Tats | defect only after two consecutive opponent defections; otherwise C |
| Random | independently choose C or D with equal probability each round |
| Win-Stay Lose-Shift | start C; keep the previous action after reward 3 or temptation 5, otherwise switch |

Both choices use the same completed history. Only after both choices are made do we apply action errors, assign payoffs and append the realised actions. This prevents the player processed second from seeing the opponent’s current choice. Action errors are not observation errors: both players see what actually happened.''')
code('engine',(ROOT/'notebooks/week10/axelrod_tournament.py').read_text())
md('checks','''## Check familiar encounters first

Tit for Tat against Always Defect is exploited once, then both defect. Over 200 rounds their total scores should be 199 and 204. A single forced error in Tit for Tat self-play should be followed by alternating retaliation; this is a check of timing, not tournament evidence.''')
code('known-answers','''assert np.allclose(play_match('Always Cooperate', 'Always Cooperate')['mean_scores'], (3,3))
assert np.allclose(play_match('Always Defect', 'Always Cooperate')['mean_scores'], (5,0))
assert np.allclose(play_match('Tit for Tat', 'Always Defect')['mean_scores'] * 200, (199,204))
check = play_match('Tit for Tat', 'Tit for Tat', rounds=5, forced_flips=((1,0),))
assert np.array_equal(check['actions'], [[0,0],[1,0],[0,1],[1,0],[0,1]])
print('Known-answer and simultaneous-update checks passed.')''')
code('plot-setup','''import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
plt.rcParams.update({'font.size': 11, 'axes.spines.top': False, 'axes.spines.right': False,
                     'figure.dpi': 110, 'savefig.bbox': 'tight'})
colours = ['#347eaf', '#dc603d', '#17294f', '#239a83', '#8650af', '#b68b22', '#667585']
short = ['Always C', 'Always D', 'Tit for Tat', 'Grudger', 'Two Tats', 'Random', 'Win-Stay Lose-Shift']''')
md('inspect-one','''## Inspect one match

The top panels show realised actions, one row per player. The lower panels show accumulated payoff. The second match has exactly one imposed error in round 5 (player 1), not continuing random noise. Read the action histories to explain the score curves before interpreting a tournament average.''')
code('match-history','''examples = [
    ('Tit for Tat vs Always Defect', play_match('Tit for Tat','Always Defect',rounds=30)),
    ('Tit for Tat self-play: one error in round 5',
     play_match('Tit for Tat','Tit for Tat',rounds=30,forced_flips=((4,0),))),
]
fig, axes = plt.subplots(2,2,figsize=(11,5.2),layout='constrained',gridspec_kw={'height_ratios':[1,2]})
for col, (title, match) in enumerate(examples):
    axes[0,col].imshow(match['actions'].T, cmap=ListedColormap(colours[:2]),
                       vmin=0,vmax=1,aspect='auto',extent=(.5,30.5,2.5,.5))
    axes[0,col].set(title=title,yticks=[1,2],yticklabels=['Player 1','Player 2'],xlabel='Round')
    for seat in (0,1):
        axes[1,col].plot(np.arange(31),np.r_[0,match['cumulative_scores'][:,seat]],
                         color=colours[seat],label=f'Player {seat+1}')
    axes[1,col].set(xlabel='Completed rounds',ylabel='Accumulated payoff')
    axes[1,col].legend(frameon=False)
fig.suptitle('One match at a time · blue = C; orange = D')
plt.show()''')
md('tournament','''## Repeat the round robin

Each pair meets once per repetition. Seven entrants with self-play give 28 matches per repetition, or 840 matches in the baseline. Each match evaluates both players for the same number of rounds. All observations are retained in the arrays returned by `run_tournament`.

Rank by payoff, not by the number of opponents beaten. When comparing repetitions, keep the field and opponent weights fixed.''')
code('baseline','''baseline = run_tournament(rounds=200,repetitions=30,noise=0,seed=3024)
rows = summarise(baseline)
print(f"{'Rank':<5} {'Strategy':<23} {'Median':>7} {'Middle 50%':>17} {'Coop.':>7} {'Wins':>7}")
for row in rows:
    print(f"{row['rank']:<5} {row['strategy']:<23} {row['median_score']:7.3f} "
          f"[{row['q25']:.3f}, {row['q75']:.3f}] {row['cooperation']:10.3f} {row['win_fraction']:7.3f}")''')
code('ranking','''order = [baseline['players'].index(row['strategy']) for row in rows]
fig, axes = plt.subplots(1,2,figsize=(11,4.8),layout='constrained',sharey=True)
for y,i in enumerate(order):
    q1,med,q3 = np.quantile(baseline['scores'][:,i],[.25,.5,.75])
    axes[0].scatter(baseline['scores'][:,i],y-.20+np.linspace(-.06,.06,30),s=14,alpha=.4,color=colours[i])
    axes[0].plot([q1,q3],[y+.10,y+.10],lw=3,color='#172b4d',solid_capstyle='butt',zorder=3)
    axes[0].vlines([q1,q3],y+.02,y+.18,color='#172b4d',lw=2,zorder=3)
    axes[0].scatter(med,y+.10,facecolor='white',edgecolor='#172b4d',linewidth=1.5,s=32,zorder=4)
    axes[1].barh(y,baseline['win_fraction'][:,i].mean(),color=colours[i])
axes[0].set(yticks=range(7),yticklabels=[short[i] for i in order],xlabel='Payoff per round',
            title='Dots above: repetitions\\nCapped line below: middle 50% · circle: median')
axes[0].invert_yaxis()
axes[1].set(xlabel='Fraction of non-self matches won',xlim=(0,1),title='Winning matches is a different measurement')
plt.show()''')
md('pair-explanation','''## Explain the ranking opponent by opponent

Rows are focal strategies; columns are opponents. The left matrix is the mean payoff per round across repetitions. The right matrix is the fraction of the focal player’s realised actions that were cooperative, averaged over repetitions. It is not the fraction of rounds in which both players cooperated. The diagonal averages the two copies in self-play.

Use these matrices to find out who supplies each strategy’s high scores and who exploits it. An overall ranking hides this structure.''')
code('pair-matrices','''fig, axes = plt.subplots(1,2,figsize=(12,5),layout='constrained')
for ax, data, title, upper in zip(axes,
    [baseline['pair_payoff'].mean(axis=0), baseline['pair_cooperation'].mean(axis=0)],
    ['Payoff of row strategy', 'Cooperation by row strategy'], [5,1]):
    im=ax.imshow(data,cmap='Blues',vmin=0,vmax=upper)
    ax.set(xticks=range(7),yticks=range(7),xticklabels=short,yticklabels=short,
           xlabel='Opponent',ylabel='Focal strategy',title=title)
    plt.setp(ax.get_xticklabels(),rotation=55,ha='right')
    for i in range(7):
        for j in range(7):ax.text(j,i,f'{data[i,j]:.2f}',ha='center',va='center',fontsize=8,
                                  color='white' if data[i,j]>.6*upper else '#17294f')
    fig.colorbar(im,ax=ax,shrink=.7)
plt.show()''')
md('sensitivity','''## Test sensitivity, one choice at a time

Before running these comparisons, predict which strategies will be damaged by a mistaken defection and which can recover. Keep the entrant field, payoff matrix and scoring convention fixed. First vary match length without noise; then vary action-error probability at 200 rounds. The curves retain four contrasting strategies for readability; all seven remain in every tournament and in the saved arrays.

Each point summarises 30 complete repetitions. Shading is the middle 50% of tournament scores, not uncertainty in a mean. Pair seeds are matched between conditions, so a paired difference—not an independent-samples calculation—is appropriate if quantifying the change.''')
code('sweeps','''lengths = [10,30,100,200]
noises = [0,.01,.05,.10]
length_results = [run_tournament(rounds=n,repetitions=30,seed=3024) for n in lengths]
noise_results = [run_tournament(rounds=200,repetitions=30,noise=e,seed=3024) for e in noises]
fig, axes=plt.subplots(1,2,figsize=(11,4),layout='constrained')
for ax,x,results,label in zip(axes,[lengths,noises],[length_results,noise_results],
                             ['Rounds per match (noise = 0)','Action-error probability (200 rounds)']):
    for i in [1,2,3,6]:
        q=np.array([np.quantile(r['scores'][:,i],[.25,.5,.75]) for r in results])
        ax.plot(x,q[:,1],'o-',color=colours[i],label=short[i])
        ax.fill_between(x,q[:,0],q[:,2],color=colours[i],alpha=.13)
    ax.set(xlabel=label,ylabel='Payoff per round',ylim=(0,5))
axes[1].legend(frameon=False,fontsize=9)
plt.show()''')
md('field','''### Change the opponent field

Remove Always Cooperate and rerun the tournament. This changes the opponents, not the rules of the remaining strategies. With equal weights the remaining opponents also receive greater weight. Excluding self-play is a separate comparison.

The seed scheme preserves each surviving pair’s match history. This isolates the field/scoring change rather than introducing a new random sample of those encounters. Report the field whenever reporting a winner.''')
code('field-comparison','''without_cooperator = run_tournament(players=STRATEGIES[1:],seed=3024)
without_self = run_tournament(self_play=False,seed=3024)
for label,result in [('Baseline',baseline),('No Always Cooperate',without_cooperator),('No self-play',without_self)]:
    print(label)
    print(', '.join(f"{r['rank']}: {r['strategy']} ({r['median_score']:.3f})" for r in summarise(result)))
for epsilon,result in zip(noises,noise_results):
    i=result['players'].index('Tit for Tat')
    differences=result['scores'][:,i]-baseline['scores'][:,i]
    print(f'Noise {epsilon:.2f}: median paired change for Tit for Tat = {np.median(differences):+.3f}')''')
md('interpret','''## What does the experiment support?

- Explain a high or low tournament score using the pairwise matrices and a specific match history.
- Distinguish a median-score ranking from head-to-head wins. Preserve ties; small observed differences do not establish a robust ordering.
- State whether changing match length, noise or the entrant field changes your conclusion. More repetitions address simulation variability; they do not fix an unrepresentative opponent field.
- A tournament keeps the strategy field fixed. It does not show invasion, evolutionary stability or which strategy becomes common.

The baseline includes deterministic and stochastic encounters. Repeating an entirely deterministic, noise-free field produces identical results; more identical repetitions would add no evidence about robustness.

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>Can a strategy score well without beating its opponents? Which opponent-level results explain your answer, and would the conclusion survive a different field?</span></div>''')
md('export','''## Retain the evidence

The following cell saves the complete per-repetition payoff and cooperation matrices, strategy scores, sensitivity arrays, settings and ranking tables in a local `tournament_results` folder. No data are sent elsewhere. The match seed is determined by the master seed, repetition and stable pair identifiers; record the NumPy version as well as the seed.''')
code('save-evidence','''import csv, json
from pathlib import Path
out=Path('tournament_results')
out.mkdir(exist_ok=True)
settings={k:baseline[k] for k in ['players','rounds','repetitions','noise','seed','self_play','payoffs']}
settings.update(numpy_version=np.__version__,lengths=lengths,noises=noises,
                ranking='median across repetitions of mean payoff per round; equal opponent weights',
                self_play_weight='one opponent contribution, average of both seats',
                wins='non-self strict wins; draws count as zero',
                historical_reproduction=False)
(out/'settings.json').write_text(json.dumps(settings,indent=2))
np.savez_compressed(out/'results.npz',**{k:baseline[k] for k in
    ['pair_payoff','pair_cooperation','scores','cooperation','win_fraction']},
    length_scores=np.stack([r['scores'] for r in length_results]),
    noise_scores=np.stack([r['scores'] for r in noise_results]),
    no_cooperator_scores=without_cooperator['scores'],no_self_scores=without_self['scores'])
with (out/'ranking.csv').open('w',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=rows[0].keys()); writer.writeheader(); writer.writerows(rows)
print(out.resolve())''')
md('sources','''## Sources and relation to standard practice

The [Axelrod-Python tournament summaries](https://axelrod.readthedocs.io/en/stable/tutorials/new_to_game_theory_and_or_python/summarising_tournaments.html) report median scores, cooperation and wins. Its [noise example](https://axelrod.readthedocs.io/en/dev/how-to/include_noise.html) defines noise as independent action flips. We use these measurements, state the weighting and self-play conventions explicitly, and add controlled match-length and opponent-field checks.

The library’s [first-tournament reconstruction](https://axelrod.readthedocs.io/en/stable/tutorials/running_axelrods_first_tournament/) uses 200 turns and five repetitions with the historical strategy descriptions. It cautions that some original descriptions are ambiguous and reconstructed rankings can differ. Our seven-entry example is deliberately not that reconstruction; it uses 30 repetitions for its stochastic comparisons. Win-Stay Lose-Shift and Tit for Two Tats are included for comparison, not presented as original first-tournament entrants.

For the historical result, see Axelrod and Hamilton, [*The evolution of cooperation*](https://doi.org/10.1126/science.7466396).''')
notebook={'cells':cells,'metadata':{'kernelspec':{'display_name':'Python 3 (ipykernel)','language':'python','name':'python3'},
                                   'language_info':{'name':'python'}},'nbformat':4,'nbformat_minor':5}
path=ROOT/'notebooks/week10/Axelrod_tournament.ipynb'
print('*** Begin Patch\n*** Add File: '+str(path))
print('\n'.join('+'+line for line in (json.dumps(notebook,ensure_ascii=False,indent=1)+'\n').splitlines()))
print('*** End Patch')
