# Product Pitch — Review Triage Assistant

**Who it's for:** customer support and community-management teams at any
business that collects written customer reviews (e-commerce, restaurants,
apps) and gets more of them than a person can realistically read one by one.

**What it solves:** instead of scrolling through every review in the order
it arrived, a support agent pastes a review in and instantly sees whether
it's a happy customer (no action needed) or an unhappy one (needs attention)
— so the team's limited time goes to the reviews that actually need a human,
not spent reading five positive reviews to find the one angry customer
buried in the middle.

## Before / after

**Before (raw model output — what project 8's API actually returns):**
```json
{
  "text": "This broke after two days and support never replied to my emails.",
  "sentiment": "negative",
  "confidence": 0.869
}
```
Technically correct, but meaningless to someone without an ML background —
what does "confidence: 0.869" mean? Is 0.869 good or bad? Is "negative" a
label a person should trust?

**After (what the product actually shows the user):**
> **Needs attention** — this customer seems unhappy (with high confidence).

Same underlying prediction, translated into a plain sentence a support agent
can act on in one glance, with the raw JSON still available behind an
optional "See the raw output" toggle for anyone who does want the technical
detail underneath.
