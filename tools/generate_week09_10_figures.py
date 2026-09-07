"""Generate course-owned information-theory and game-theory diagrams."""

from pathlib import Path
import shutil

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch
import numpy as np

from figure_style import apply_course_figure_style


ROOT = Path(__file__).resolve().parents[1]
W9 = ROOT / "notebooks/week09/images"
W10 = ROOT / "notebooks/week10/images"
NAVY = "#172A50"
BLUE = "#4A83B5"
YELLOW = "#F2CF4A"
CORAL = "#D96545"
PALE = "#EDF3F9"
GRID = "#CCD8E8"

apply_course_figure_style()


def save(fig, path):
    fig.savefig(path, dpi=240, transparent=True, bbox_inches="tight", pad_inches=.08)
    plt.close(fig)


def binary_entropy():
    p = np.linspace(0, 1, 601)
    h = np.zeros_like(p)
    interior = (p > 0) & (p < 1)
    h[interior] = (
        -p[interior] * np.log2(p[interior])
        - (1 - p[interior]) * np.log2(1 - p[interior])
    )

    fig, ax = plt.subplots(figsize=(6.8, 4.5), constrained_layout=True)
    ax.plot(p, h, color=BLUE, linewidth=3.2)
    ax.scatter([.5], [1], s=72, color=YELLOW, edgecolor=NAVY,
               linewidth=1.2, zorder=3)
    ax.axvline(.5, color=GRID, linewidth=1.2, linestyle="--")
    ax.annotate(
        "maximum uncertainty\n$H_2=1$ bit",
        xy=(.5, 1), xytext=(.68, .89),
        arrowprops={"arrowstyle": "-", "color": NAVY, "linewidth": 1},
        ha="left", va="center", fontsize=11.5,
    )
    ax.text(.025, .055, "certain", transform=ax.transAxes,
            ha="left", va="bottom", fontsize=11.5, color="#596B85")
    ax.text(.975, .055, "certain", transform=ax.transAxes,
            ha="right", va="bottom", fontsize=11.5, color="#596B85")
    ax.set(
        xlabel="Probability of outcome 1, $p=\\Pr(X=1)$",
        ylabel="Binary entropy, $H_2(p)$ (bits)",
        xlim=(0, 1), ylim=(0, 1.08),
        xticks=[0, .25, .5, .75, 1],
        yticks=[0, .25, .5, .75, 1],
    )
    ax.spines[["top","right"]].set_visible(False)
    ax.grid(color=GRID, alpha=.7)
    save(fig, W9 / "Binary_entropy_plot.png")


def entropy_diagram():
    fig, ax = plt.subplots(figsize=(7.2, 3.6), facecolor="white")
    left = Circle((-.62, 0), 1.18, facecolor="#8CB9D8", edgecolor=NAVY,
                  alpha=.82, linewidth=2.2)
    right = Circle((.62, 0), 1.18, facecolor="#F4C542", edgecolor=NAVY,
                   alpha=.72, linewidth=2.2)
    ax.add_patch(left)
    ax.add_patch(right)

    # The circle names sit above the decomposed regions so the hierarchy is
    # visible without repeating the slide title inside the figure.
    ax.text(-1.02, .76, "$H(X)$", ha="center", va="center", fontsize=18)
    ax.text(1.02, .76, "$H(Y)$", ha="center", va="center", fontsize=18)
    ax.text(-.91, -.28, "$H(X\\mid Y)$", ha="center", va="center", fontsize=15)
    ax.text(0, -.05, "$I(X;Y)$", ha="center", va="center", fontsize=16,
            fontweight="bold")
    ax.text(.91, -.28, "$H(Y\\mid X)$", ha="center", va="center", fontsize=15)
    ax.set(xlim=(-1.95, 1.95), ylim=(-1.30, 1.28), aspect="equal")
    ax.axis("off")
    save(fig, W9 / "Entropy_VennDiagram.png")


def payoff_matrix(path, analysed=False):
    fig, ax = plt.subplots(figsize=(7.2, 5.0)); ax.axis("off")
    ax.set(xlim=(0,3.6),ylim=(0,3.2))
    ax.text(2.15,3.02,"Player 2",ha="center",fontsize=15,weight="bold")
    ax.text(.18,1.45,"Player 1",rotation=90,va="center",fontsize=15,weight="bold")
    xs=[.7,1.55,2.4,3.25]; ys=[.35,1.25,2.15,2.85]
    # grid body
    for x in [1.15,2.3,3.45]: ax.plot([x,x],[.2,2.65],color=NAVY,lw=1.5)
    for y in [.2,1.2,2.2,2.65]: ax.plot([1.15,3.45],[y,y],color=NAVY,lw=1.5)
    ax.text(1.72,2.42,"Cooperate",ha="center",weight="bold")
    ax.text(2.87,2.42,"Defect",ha="center",weight="bold")
    ax.text(.68,1.7,"Cooperate",ha="center",weight="bold")
    ax.text(.68,.7,"Defect",ha="center",weight="bold")
    vals={(1.72,1.7):"$(-1,-1)$",(2.87,1.7):"$(-3,0)$",(1.72,.7):"$(0,-3)$",(2.87,.7):"$(-2,-2)$"}
    for (x,y),v in vals.items():
        if analysed and (x,y)==(2.87,.7):
            ax.add_patch(FancyBboxPatch((x-.46,y-.25),.92,.5,boxstyle="round,pad=.05",facecolor=YELLOW,edgecolor=NAVY))
        ax.text(x,y,v,ha="center",va="center",fontsize=16)
    ax.text(2.3,.02,"Each pair is (row payoff, column payoff)",ha="center",fontsize=11,color="#596B85")
    save(fig,path)


def payoff_plane(path, analysed=False):
    pts={"$C,C$":(-1,-1),"$D,C$":(0,-3),"$C,D$":(-3,0),"$D,D$":(-2,-2)}
    fig,ax=plt.subplots(figsize=(5.5,5.2))
    for label,(x,y) in pts.items():
        color=YELLOW if analysed and label=="$D,D$" else BLUE
        ax.scatter(x,y,s=120,color=color,edgecolor=NAVY,zorder=3); ax.annotate(label,(x,y),xytext=(7,7),textcoords="offset points")
    ax.plot([-3,-1,0,-2,-3], [0,-1,-3,-2,0], color=GRID, lw=2)
    ax.set(xlabel="Player 1 utility",ylabel="Player 2 utility",xlim=(-3.4,.4),ylim=(-3.4,.4))
    ax.grid(color=GRID); ax.spines[["top","right"]].set_visible(False)
    save(fig,path)


def strategy_space():
    fig,ax=plt.subplots(figsize=(7.2,3.5)); ax.axis("off")
    items=[("$(C,C)$","mutual cooperation"),("$(C,D)$","P1 cooperates"),("$(D,C)$","P1 defects"),("$(D,D)$","mutual defection")]
    for k,(a,t) in enumerate(items):
        x=.06+k*.235
        ax.add_patch(FancyBboxPatch((x,.25),.2,.5,boxstyle="round,pad=.025",facecolor=PALE,edgecolor=BLUE,linewidth=1.6))
        ax.text(x+.1,.57,a,ha="center",fontsize=16,weight="bold"); ax.text(x+.1,.38,t,ha="center",fontsize=10,wrap=True)
    ax.set(xlim=(0,1.02),ylim=(0,1))
    save(fig,W10/"Strategy_space_PD.png")


def general_pd():
    fig,ax=plt.subplots(figsize=(7.6,4.4)); ax.axis("off")
    ax.text(.5,.9,"Prisoner’s Dilemma payoff ordering",ha="center",fontsize=18,weight="bold",transform=ax.transAxes)
    ax.text(.5,.72,"$T>R>P>S$",ha="center",fontsize=28,transform=ax.transAxes)
    labels=[("$T$","temptation to defect"),("$R$","reward for cooperation"),("$P$","punishment for defection"),("$S$","sucker’s payoff")]
    for i,(s,t) in enumerate(labels):
        y=.53-i*.13; ax.text(.25,y,s,fontsize=16,weight="bold",transform=ax.transAxes); ax.text(.34,y,t,fontsize=13,transform=ax.transAxes)
    save(fig,W10/"General_PD.png")


def repeated_games():
    fig,ax=plt.subplots(figsize=(7.8,4.6)); ax.axis("off")
    ax.text(.5,.92,"Repeated Prisoner’s Dilemma strategies",ha="center",fontsize=18,weight="bold",transform=ax.transAxes)
    rows=[("Always cooperate","C C C C C","forgiving, exploitable"),("Always defect","D D D D D","safe, prevents cooperation"),("Tit for tat","C D D C C","starts cooperatively, then reciprocates"),("Win–stay, lose–shift","C C D D C","repeats successful actions")]
    for i,(name,seq,note) in enumerate(rows):
        y=.73-i*.17
        ax.add_patch(FancyBboxPatch((.04,y-.07),.92,.13,boxstyle="round,pad=.015",facecolor=PALE if i%2==0 else "white",edgecolor=GRID,transform=ax.transAxes))
        ax.text(.07,y,name,weight="bold",va="center",transform=ax.transAxes)
        ax.text(.39,y,seq,fontfamily="monospace",va="center",transform=ax.transAxes)
        ax.text(.62,y,note,va="center",transform=ax.transAxes)
    save(fig,W10/"Iterated_Prisoners_Dilemma_Venn-Diagram.png")


def main():
    W9.mkdir(exist_ok=True); W10.mkdir(exist_ok=True)
    binary_entropy(); entropy_diagram(); strategy_space(); general_pd(); repeated_games()
    payoff_matrix(W10/"Payoff_matrix_pictures_PD.png")
    payoff_matrix(W10/"Payoff_matrix_PD.png", analysed=True)
    payoff_plane(W10/"Payoff_plane_PD.png")
    payoff_plane(W10/"Payoff_plane_analysed_PD.png", analysed=True)
    shutil.copyfile(W10/"Payoff_plane_PD.png",W10/"Payoff_space_PD.png")
    shutil.copyfile(W10/"Payoff_plane_analysed_PD.png",W10/"Payoff_space_analysed_PD.png")


if __name__ == "__main__":
    main()
