# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->



---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** 
     - This returns a a list that contains matches to the user input in description. It ranks the matches in how well they match. The user can also add in an optional size filter and max_price cieling. 

- **Inputs:**  
     - description: str, (required)
          - Description: This is a string input where the user describes the clothing.
     - size: str | None = None, 
          - Description: This is a string input of size that the user can use to filter but it is optional. 
     - max_price: float | None = None
          - Description: This is a float input so the user can put in an input to filter out anything above a certain price threshold. 
- **Returns:**
     A list of matching listing dicts based off of the input strings description and size and uses max_prize as a filter as well as size. It puts the best match first. 
     The return dict has these fields:
          - id
          - title
          - description
          - category 
          - style_tags (list)
          - size
          - condition
          - price (float)
          - colors (list)
          - brand (str or None)
          - platform 
- **When it has nothing:**
     It returns and empty list when nothing matches. NOT None and NOT an exception.

### `suggest_outfit`

- **What it does:**
     - This will look at the thrifted item and the user's wardrobe and then suggest on or two outfits. It will uses generative AI to do this by calling a model. 

- **Inputs:**
     - new_item: dict 
          - Description: it takes the item and all the       information from it in a dictionary format. This is taken from items that the user is currently considering to buy. 
     - wardrobe: dict; 
          - Description: 
               - This can be empty but it is a dict with items key that holds a list of items. 
- **Returns:**
     - a non empty string with outfit suggestions. It will ALWAYS be non-empty
- **When it has nothing:**
     - it will never return nothing, if there is no input then it will just use general styling advice rather than information that is based from input by the user. 

### `create_fit_card`

- **What it does:**
     - It uses the inputs to create a 2-4 sentence description. It uses a model to use generative AI to make the description. 
- **Inputs:**
     - outfit: string
          - Description: this is the outfit suggestion from suggest_outfit() in string format
     - new_item: dict
          - Description: this is the listing dict for the item
- **Returns:**
     - a 2-4 sentence caption about the input variables that were given
- **When it has nothing:**
     - it should return a descptive message rather than raise an exception or say none or null. 

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:**
     If search_listings() from tools.py returns an empty list, put a message in the session, "No listings match your search, please try again" then stop the loop and ask for user input again. If search_listings() returns with a valid list, ie one that is full or not empyt,  then move to suggest_outfit() from tools.py and perform that action of that funtion. This function takes the output from search_listings() which is a dict and uses that to fill new_item dict. Then once those items are considered it moves to wardrobe: dict to create the suggestions and holds those in a dict as well. 
     
     BRANCHING If wardrobe: dict is empty it will just give general advice. if it is not empty then it will format the wardrobe items into the prompt and ask for specific combinations naming pieces the user already owns and then return the models response. 

     Once suggest_outfit() has run it will go to creat_fit_card() and use the output from suggest_outfit to generate a listing description for that product that is unique every time. 
     
     BRANCHING: if outfit is empty it will return a descriptive message rather than raising an exception or an error. 


**Where it lives:** `agent.py::run_agent` the actual functions live in tools.py

**How the query is parsed:** 
To move from search_listings to suggest_outfit 
It will use regex and just look for an empty list. So if the list is empty in search_listings that is how it decides to move forward or not. From there the model will look and decide what to do in suggest_outfit and search_listings since a lot of the work there is done by the model. 

**What moves through the session:** search_listings(description, size, max_price) if not empty moves to suggest_item. new_item comes from the seach_listing and for every new_item added it gets added to the wardrobe: dict. the inputs to search_listing are sent to the model as well and then the output string from suggest_outfit is sent to create_fit_card the inputs to create_fit_card are sent to the model. to and adds it to the new_item dict to create a dictionary of all the new outfits and their descriptions and returns it via a string. 
---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask '...'

```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

```

```
$ python -c "from tools import suggest_outfit; ..."

```

```
$ python -c "from tools import create_fit_card; ..."

```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```

```

**Empty search**

```

```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
