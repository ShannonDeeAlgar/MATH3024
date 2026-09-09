# Reader and slide equations

This release carries the Week 7 entries from the full authoring audit described
below. The manifest explicitly limits checks to Week 7; unchanged earlier-week
notebooks and their committed decks are not replaced by this release.

The reader is the canonical source for course mathematics. Slides may shorten
explanations, but must not silently change symbols, assumptions or equations.

## Audit, 9 September 2026

All ten lecture notebooks were compared. Of the 88 display equations in
slides-only cells, 77 now refer directly to reader equations. The remaining 11
are documented, reviewed variations: selected lines of a derivation, a worked
binary example, an intermediate identity, explicit base-two research measures,
or punctuation/numbering differences. Shared reader/slide cells already have
one source.

Corrections:

- Week 4: removed a stray comma in the exponent of the reader's binomial
  mean-field derivation.
- Week 6: added the deterministic Euler update to the reader, where the slide
  previously supplied mathematics not explicitly developed in the reader.
- Week 7: standardised ACO edge cost to c_e and ant-specific choice notation
  to P_a and A_a; aligned vector notation in the optimisation objective.
  PSO now uses the reader's coordinate-level update on the slide, making the
  independent random draw for each coordinate explicit.
- Week 7: clarified L_a = L(R_a), the cost of the route constructed by ant a.
- Weeks 2, 6 and 8: aligned copied equations and kept explanatory initial
  conditions or prose outside the shared mathematical expression.

The audit distinguishes notation differences from scientific changes.
General-base entropy and explicit base-two information in bits are compatible;
condensing several algebraic lines is also legitimate when the assumptions
and result are retained. These exceptions are recorded individually.

## How equations are maintained

A slides-only cell contains a reader-equation HTML comment identifying a
reader cell and its zero-based display index. The slide builder resolves that
reference into the reader's actual display before rendering. There is no
independent slide copy to edit.

The build check runs for local reader builds, slide generation and the project
deployment workflow. It checks all equation references, exact matches, display
coverage and fingerprints of inline/display mathematics, including notation
footers and MyST containers such as dropdowns and list-tables. Literal code
examples are excluded. Regression tests check both behaviours.
Changes to mathematics require a coordinated review before the audit
manifest is updated; ordinary prose changes do not.

When editing:

1. Change the canonical reader equation.
2. Check all linked slides and their notation footers. Reword or split a slide
   if the revised equation no longer fits.
3. Review any documented shortened derivations that depend on it.
4. Update only the affected entries in tools/equation_consistency.json after
   that review. Do not automatically rebaseline every changed expression.
5. Run tools/check_equation_consistency.py and its tests, then rebuild slides.

Always use generate_slides.sh rather than calling nbconvert directly; direct
nbconvert does not resolve the reader references.

## Scope

This is a consistency safeguard, not a symbolic proof checker. It covers
LaTeX mathematics in lecture Markdown source (including inline notation and
MyST math roles). Equations inside image pixels, arbitrary HTML-only notation,
and executable implementations require separate inspection. A fingerprint
cannot establish that an original equation is scientifically correct.
