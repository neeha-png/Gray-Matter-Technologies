# Insights — Titanic Passenger Data

Plain-English takeaways from `notebooks/eda.ipynb`. Full charts and code are in
the notebook; this is the "just tell me what it means" summary.

- **891 passengers, 12 columns of information.** Most columns are clean; the
  gaps are in `Age` (~20% missing), `Cabin` (~77% missing), and `Embarked`
  (2 missing — which port someone boarded at).
- **Ticket class mattered a lot.** 1st-class passengers survived about 63% of
  the time, 2nd-class about 47%, 3rd-class about 24% — roughly a 2.6x gap
  between the top and bottom class.
- **Sex mattered even more than class.** Splitting survival by class *and*
  sex shows women survived at far higher rates than men in every class (e.g.
  97% of 1st-class women survived vs. 37% of 1st-class men) — consistent with
  a "women and children first" evacuation pattern.
- **Fare and class are closely linked, but not identical** (a moderate
  negative correlation of about -0.55) — people who paid more tended to be in
  better classes, but the two aren't telling exactly the same story.
- **A handful of passengers paid extreme, outlier-level fares**, far above
  everyone else, while `Age` had no similarly dramatic outliers — just a
  small number of elderly passengers above ~65.
- **Only a minority of passengers survived overall** (about 38%), so raw
  survivor counts alone would be misleading without looking at rates.
- **Bottom line:** on the Titanic, *where you could afford to be, and whether
  you were a woman or a man,* mattered more to your odds of survival than
  almost anything else in this data.
