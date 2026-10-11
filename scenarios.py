"""
The runs your test needs. ← UNIT 4, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
the empty-search branch needs an impossible query. One about the fit card needs
the same item run more than once. Working that out is Milestone 3's first step,
and this file is where you write it down.

`run_eval.py` runs everything here five times and writes the run log — five
because your criteria are written out of five.

Three scenarios are filled in to show the shape. Add or change whatever your
own criteria need — these are a starting point, not a fixed set.
"""

SCENARIOS = [
    {
        # A query the data can match. Criterion 1.
        "name": "matching query completes",
        "query": "vintage graphic tee under $30",
        "wardrobe": "example",
        "criterion": 1,
    },
    {
        # A query nothing can match. Criterion 2 — the branch.
        "name": "impossible query stops early",
        "query": "designer ballgown size XXS under $5",
        "wardrobe": "example",
        "criterion": 2,
    },
    {
        # A user with nothing saved. One of unit 4's three failure modes.
        "name": "empty wardrobe",
        "query": "denim jacket under $50",
        "wardrobe": "empty",
        "criterion": None,
    },
    {
        # A matching query checks that the selected item and wardrobe inform
        # the outfit suggestion and fit card. Criterion 3.
        "name": "outfit and fit card use prior state",
        "query": "denim jacket under $50",
        "wardrobe": "example",
        "criterion": 3,
    },
    {
        # This query selects a listing whose brand is null, checking that the
        # fit card does not invent a brand. Five tries test criterion 4.
        "name": "fit card does not invent a brand",
        "query": "2003 tour bootleg tee under $30",
        "wardrobe": "example",
        "criterion": 4,
    },
    {
        # The search must return only listings at or below the requested cap.
        # Criterion 5. Each try uses a DIFFERENT phrasing of a price cap, since
        # the price filter is deterministic and repeating one query five times
        # is one data point. Several phrasings are ones _parse_query has no
        # pattern for, so a miss shows up as max_price None in the report.
        "name": "search results stay within the price cap",
        "query": "graphic tee under $20",
        "queries": [
            "graphic tee under $20",             # baseline: the phrasing the parser knows
            "graphic tee under forty dollars",   # number written out as a word
            "graphic tee $25 or less",           # cap after the number
            "graphic tee, budget of 30",         # no keyword the parser recognises
            "graphic tee under $1",              # cap below every listing: zero results
        ],
        "wardrobe": "example",
        "criterion": 5,
    },
]

WARDROBES = ("example", "empty")


def validate() -> list[str]:
    """Complain about anything malformed, before a long run rather than during."""
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("query", "").strip():
            problems.append(f"scenario {i} has no query")
        for q in scenario.get("queries", []):
            if not str(q).strip():
                problems.append(f"scenario {i} has an empty entry in queries")
        if scenario.get("wardrobe") not in WARDROBES:
            problems.append(
                f"scenario {i} has wardrobe {scenario.get('wardrobe')!r} — "
                f"it should be one of {WARDROBES}"
            )
    return problems
