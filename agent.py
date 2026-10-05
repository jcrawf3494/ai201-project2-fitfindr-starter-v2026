"""
The FitFindr planning loop.

This is the file that makes FitFindr an agent rather than a script. It decides
which tool to run next based on what the last one returned.

If your loop calls every tool no matter what comes back, you have a list
of function calls. A loop looks at the last result before it picks the next
step. **That branch is the graded part of this unit.**

Build and test the tools in `tools.py` first. Then come here.

    python agent.py          runs both example paths below
"""

import re

import config
import trace
from tools import (
    search_listings,
    suggest_outfit,
    create_fit_card,
    suggestions_tool,
)
from generate import ModelUnavailable


# ── session state ─────────────────────────────────────────────────────────────

def new_session(query: str, wardrobe: dict) -> dict:
    """
    A fresh session for one user interaction.

    The session is the single source of truth for a run. Every tool result goes
    in here, and the next tool reads it back out.

    You could pass values straight from one call to the next. It would work,
    and you would not be able to test it — you can't print a variable you have
    already overwritten. Going through the session is what makes the state
    visible, and unit 4 has you write a criterion about exactly that.

    Add fields if you need them.
    """
    return {
        "query": query,              # what the user typed
        "parsed": {},                # description / size / max_price you pulled out of it
        "search_results": [],        # everything search_listings returned
        "selected_item": None,       # the one you chose — goes into suggest_outfit
        "wardrobe": wardrobe,        # the user's wardrobe
        "outfit_suggestion": None,   # what suggest_outfit returned
        "fit_card": None,            # what create_fit_card returned
        "suggestions": None,         # similar listings and outfit-completion picks
        "error": None,               # set when the run ended early
    }


def _parse_query(query: str) -> dict:
    """Extract a description, a size, and an optional price ceiling with regex."""
    description = query
    size = None
    max_price = None

    size_match = re.search(
        r"\bsize\s+(one\s+size(?:\s*/\s*oversized)?|us\s+\d+(?:\.\d+)?|"
        r"w\d+(?:\s+l\d+)?|[xsml]{1,3}(?:\s*/\s*[xsml]{1,3})?)"
        r"(?:\s*\([^)]*\))?",
        query,
        flags=re.IGNORECASE,
    )
    if size_match:
        size = re.sub(r"\s+", " ", size_match.group(1)).strip()
        description = description.replace(size_match.group(0), " ")

    price_pattern = (
        r"\b(?:under|below|less\s+than|at\s+most|up\s+to|max(?:imum)?"
        r"(?:\s+price)?|max_price\s*=|<=)\s*\$?\s*(\d+(?:\.\d+)?)"
    )
    price_match = re.search(price_pattern, description, flags=re.IGNORECASE)
    if price_match:
        max_price = float(price_match.group(1))
        description = description[:price_match.start()] + " " + description[price_match.end():]

    description = re.sub(r"\s+", " ", description)
    description = re.sub(r"^(?:and|with)\s+|\s+(?:and|with)\s*$", "", description, flags=re.IGNORECASE)
    description = description.strip(" ,.-")

    return {
        "description": description,
        "size": size,
        "max_price": max_price,
    }


# ── planning loop ─────────────────────────────────────────────────────────────

def run_agent(query: str, wardrobe: dict) -> dict:
    """
    Run the loop once and return the finished session.

    Args:
        query:    what the user asked for, in plain language
                  (e.g. "vintage graphic tee under $30, size M").
        wardrobe: a wardrobe dict — get_example_wardrobe() or
                  get_empty_wardrobe() from utils/data_loader.py.

    Returns:
        The session dict. **Check session["error"] first** — if it isn't None,
        the run ended early and the later fields will still be None.

    ─────────────────────────────────────────────────────────────────────────
    TODO — build this, following the branch rule you wrote in Milestone 2.

      1. Start a session with new_session().

      2. Count the times round the loop, and call trace.check_iterations(count)
         on each one before you go again. It raises when the count passes
         MAX_ITERATIONS in config.py — see trace.py.

      3. Parse the query into a description, a size, and a max_price. Regex,
         string splitting, or asking the model are all fine — say which you
         chose in your README. Put the result in session["parsed"].

      4. Call search_listings() with what you parsed.
         Put the results in session["search_results"].

         ⚠️ THIS IS THE BRANCH. If nothing came back:
              - put a message in session["error"] saying what the user could
                change — "No results" is not that message
              - return the session
              - do NOT call suggest_outfit with nothing

      5. Choose an item — the first result is fine. Put it in
         session["selected_item"].

      6. Call suggest_outfit() with the selected item and the wardrobe.
         Put the result in session["outfit_suggestion"].

      7. Call create_fit_card() with the outfit and the item.
         Put the result in session["fit_card"].

      8. Call suggestions_tool() after the fit card, passing the selected item,
         outfit, original search results, and optional max_price. Store the two
         suggestion groups in session["suggestions"].

      9. Return the session.

    ─────────────────────────────────────────────────────────────────────────
    IN UNIT 4 you come back and add two things:

      • Trace calls. One per step. `trace.step("search_listings", inputs=...,
        returned=...)` — see trace.py. Your README needs the output.

      • A handler for ModelUnavailable, so a bad key produces a message rather
        than a stack trace. The import is already at the top of this file.

        **Branch rule:**
     If search_listings() from tools.py returns an empty list, put a message in the session, "No listings match your search, please try again" then stop the loop and ask for user input again. If search_listings() returns with a valid list, ie one that is full or not empyt,  then move to suggest_outfit() from tools.py and perform that action of that funtion. This function takes the output from search_listings() which is a dict and uses that to fill new_item dict. Then once those items are considered it moves to wardrobe: dict to create the suggestions and holds those in a dict as well. 
     
     BRANCHING If wardrobe: dict is empty it will just give general advice. if it is not empty then it will format the wardrobe items into the prompt and ask for specific combinations naming pieces the user already owns and then return the models response. 

     Once suggest_outfit() has run it will go to creat_fit_card() and use the output from suggest_outfit to generate a listing description for that product that is unique every time. 
     
     BRANCHING: if outfit is empty it will return a descriptive message rather than raising an exception or an error. 

    """
    session = new_session(query, wardrobe)

    iteration = 0
    while True:
        iteration += 1
        trace.check_iterations(iteration)

        parsed = _parse_query(query)
        session["parsed"] = parsed
        results = search_listings(
            parsed["description"],
            size=parsed["size"],
            max_price=parsed["max_price"],
        )
        session["search_results"] = results

        if not results:
            session["error"] = (
                "No listings match your search. Try changing the description or "
                "size, or raising the maximum price."
            )
            return session

        selected_item = results[0]
        session["selected_item"] = selected_item
        session["outfit_suggestion"] = suggest_outfit(selected_item, wardrobe)
        session["fit_card"] = create_fit_card(
            session["outfit_suggestion"],
            selected_item,
        )
        session["suggestions"] = suggestions_tool(
            selected_item,
            session["outfit_suggestion"],
            search_results=results,
            max_price=parsed["max_price"],
        )
        return session


# ── running it directly ───────────────────────────────────────────────────────

def _show(session: dict) -> None:
    if session["error"]:
        print(f"  stopped: {session['error']}")
        print(f"  fit_card is {session['fit_card']!r} — it should still be None here")
        return

    item = session["selected_item"] or {}
    print(f"  found:    {item.get('title')} — ${item.get('price')} on {item.get('platform')}")
    print(f"  outfit:   {session['outfit_suggestion']}")
    print(f"  fit card: {session['fit_card']}")
    suggestions = session["suggestions"] or {}
    print(f"  similar items: {suggestions.get('suggested_items_based_on_search', [])}")
    print(
        "  outfit additions: "
        f"{suggestions.get('suggested_items_to_help_make_your_outfit', [])}"
    )


if __name__ == "__main__":
    from utils.data_loader import get_example_wardrobe

    print("=== A query the data can match ===")
    _show(run_agent(
        query="looking for a vintage graphic tee under $30",
        wardrobe=get_example_wardrobe(),
    ))

    print("\n=== A query it can't ===")
    _show(run_agent(
        query="designer ballgown size XXS under $5",
        wardrobe=get_example_wardrobe(),
    ))

    print(
        "\nThe second one should stop before the fit card. If both paths look "
        "the same,\nthe branch isn't doing anything yet."
    )
