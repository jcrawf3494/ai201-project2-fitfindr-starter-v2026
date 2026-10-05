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
> The tool implementations and planning loop are built incrementally below.
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

STRETCH FEATURE TOOL



- **What it does:**
  - `suggestions_tool` looks through the listings after a fit card is created and returns two groups of listing recommendations.
  - `suggested_items_based_on_search` contains up to five listings similar to the selected listing, ranked using brand, category, style tags, and descriptive keywords. They exclude listings already returned by the original search and must be within 25% of the selected item's price. If the query included a maximum price, a suggestion must also be at or below that ceiling.
  - `suggested_items_to_help_make_your_outfit` contains five listings whenever at least five other inventory items are available. Outfit-related matches are ranked first, and random inventory listings fill any remaining slots.
- **Inputs:**
  - `new_item: dict | None` — the selected listing from the search, used as the anchor for similar-item recommendations.
  - `outfit: str` — the suggestion returned by `suggest_outfit`, used to look for complementary listings.
  - `search_results: list[dict] | None` — the original search results, excluded from recommendations so the user sees new listings.
  - `max_price: float | None` — the optional price ceiling extracted from the query; it also limits similar-item suggestions.
- **Returns:**
  - A dictionary with two list fields:
    - `suggested_items_based_on_search`: listing dictionaries ranked by similarity to the selected listing.
    - `suggested_items_to_help_make_your_outfit`: five listing dictionaries when at least five eligible inventory items exist, with outfit matches ranked first and random fallback listings filling remaining slots.
  - Each listing dictionary has the fields from the listings dataset: `id`, `title`, `description`, `category`, `style_tags`, `size`, `condition`, `price`, `colors`, `brand`, and `platform`.
- **When it has nothing:**
  - If `new_item` is missing, `suggested_items_based_on_search` is an empty list. The outfit-completion list is padded with random inventory listings to five items when possible, and contains fewer only when the inventory has fewer than five eligible items.
- **Test command** (provided for you to run; not run as part of this change):
  ```powershell
  python -c "from tools import suggestions_tool; from utils.data_loader import load_listings; listings=load_listings(); print(suggestions_tool(listings[0], 'Pair the jeans with a white tank top and chunky sneakers.', listings, 50))"
  ```

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
`agent.py::_parse_query` uses regular expressions to extract a size after `size` (for example, `size M`) and a price ceiling after phrases such as `under $30`, `up to $30`, or `max_price=30`. The remaining text is passed as the description to `search_listings`.

**What moves through the session:** `run_agent` stores the parsed filters and all search results in the session. If results are found, it selects the first listing and passes it with the supplied wardrobe to `suggest_outfit`; that suggestion and listing then go to `create_fit_card`. After the fit card, `suggestions_tool` stores similar listings and outfit-completion listings in the session. An empty search result sets an actionable error and stops before the later tools are called.
---

## Sample Run




**One full query**
This is what is produced when agent.py is run
=== A query the data can match ===
  found:    Graphic Tee — 2003 Tour Bootleg Style — $24.0 on depop
  outfit:   Here are two effortless outfit combinations featuring your new 2003 Tour Bootleg Graphic Tee and pieces from your wardrobe:

### Outfit 1: 90s Streetwear Edge
Lean into the vintage, worn-in vibe of the tee by pairing it with relaxed denim and chunky footwear. 
* **Top:** **Graphic Tee — 2003 Tour Bootleg Style**
* **Bottoms:** Baggy straight-leg jeans (dark wash)
* **Shoes:** Chunky white sneakers
* **Accessories:** Black crossbody bag
* **Styling Tip:** Since the tee has a slightly boxy fit, let it hang naturally over the baggy jeans. Add the black crossbody bag to keep it functional, and let the chunky white sneakers brighten up the dark denim-and-black color palette.

### Outfit 2: High-Low Contrast Grunge
Mix the casual, edgy energy of the graphic tee with tailored trousers to create a cool, high-low textured look.
* **Top:** **Graphic Tee — 2003 Tour Bootleg Style** (tucked in slightly)
* **Bottoms:** Wide-leg khaki trousers
* **Outerwear:** Vintage black denim jacket (worn over the shoulders or unbuttoned)
* **Shoes:** Black combat boots
* **Accessories:** Brown leather belt
* **Styling Tip:** Cinch the khaki trousers with the brown leather belt and do a half-tuck with the graphic tee to define your waist. Layer the vintage black denim jacket on top and finish with the black combat boots to tie the grunge elements together.
  fit card: Found this perfectly faded 2003 tour bootleg tee hiding in the racks and honestly, it’s giving instant 90s streetwear edge. I love wearing it slightly boxy over baggy denim with chunky sneakers, or dressed down with wide-leg trousers and combat boots. Snagged it on depop for $24.0 and it’s already my go-to.

=== A query it can't ===
  stopped: No listings match your search. Try changing the description or size, or raising the maximum price.
  fit_card is None — it should still be None here

The second one should stop before the fit card. If both paths look the same,
the branch isn't doing anything yet.
```
$ python app.py ask '...'

This is a manual ask that will pass: 
python app.py ask 'I want a red sweater under $50'

  Found:    Oversized College Crewneck — Faded Red — $21.0 on thredUp

  Outfit:   Hey there! Great thrift find—that faded red college crewneck has such an effortless, lived-in vintage feel, and the roomy fit makes it super versatile. 

Here are two stylish outfit combinations using your new crewneck and pieces from your wardrobe:

### Look 1: Streetwear Casual
*This look leans into the relaxed, roomy fit of the crewneck and plays with classic streetwear proportions.*
* **Top:** **Oversized College Crewneck — Faded Red** (New Item)
* **Bottoms:** **Baggy straight-leg jeans, dark wash**
* **Shoes:** **Chunky white sneakers**
* **Accessories:** **Black crossbody bag**
* **Styling Tip:** Let the crewneck hang loose over the baggy jeans for an easy, slouchy silhouette. Pair with the chunky white sneakers and throw on the black crossbody bag to keep it hands-free and functional for everyday wear.

### Look 2: Elevated Contrast (Red, Tan & Black)
*This combination balances the sporty, casual vibe of the crewneck with tailored trousers for a cool high-low mix.*
* **Top:** **Oversized College Crewneck — Faded Red** (New Item) worn over the **White ribbed tank top** (let the white hem peek out at the bottom for dimension)
* **Bottoms:** **Wide-leg khaki trousers**
* **Outerwear:** **Vintage black denim jacket**
* **Shoes:** **Black combat boots**
* **Accessories:** **Brown leather belt**
* **Styling Tip:** Tuck the front of the crewneck casually into the khaki trousers, accented with the brown leather belt. Layer the vintage black denim jacket on top and anchor the outfit with the black combat boots to tie the dark accents together. 

Which of these vibes are you feeling most today?

  Fit card: There's nothing quite like the buttery-soft, sun-bleached look of this faded red oversized college crewneck. Snagged on thredUp for $21.0, it’s got that perfect slouchy drape whether you're throwing it on with baggy dark denim or styling it high-low under a black denim jacket. Grab your favorite sneakers and consider your effortless off-duty uniform officially sorted.

2 model calls this session, 939 prompt + 469 output tokens


STRETCH FEATURE TEST ON SAME PROMPT 
  Suggested items based on your search:
    - Oversized Crewneck Sweatshirt — Vintage Navy — $20.0
    - Henley Long Sleeve — Washed Burgundy — $16.0
    - Vintage Polo Shirt — Forest Green — $18.0
    - Graphic Tee — 2003 Tour Bootleg Style — $24.0
    - Vintage Band Tee — Faded Grey — $19.0
  Suggested items to help make your outfit:
    - Straight Leg Black Jeans — Faded — $30.0
    - Vintage Levi's 501 Jeans — Medium Wash — $38.0
    - Baggy Carpenter Jeans — Dark Wash — $36.0
    - Vintage Linen Blazer — Cream — $38.0
    - Denim Jacket — Light Wash, Cropped — $42.0

This is a manual pass that will fail: 

python app.py ask 'I want a puppy'                

  No listings match your search. Try changing the description or size, or raising the maximum price.

0 model calls this session
```

**The tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
[{'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition':'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under agraphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s','streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}]
```

```
$ python -c "from tools import suggest_outfit; ..."

python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"

Here are two outfit combinations featuring your amazing new Vintage Levi's 501 Jeans and pieces from your wardrobe:

### Outfit 1: Casual & Cozy Vintage Streetwear
* **The Look:** Effortless, comfortable, and plays on contrasting proportions with the fitted tank and relaxed denim.
* **Key Pieces:**
  * **New Item:** Vintage Levi's 501 Jeans
  * **Wardrobe Item:** White ribbed tank top
  * **Wardrobe Item:** Oversized grey crewneck sweatshirt (wear layered on top or draped over your shoulders)
  * **Wardrobe Item:** Chunky white sneakers
  * **Wardrobe Item:** Black crossbody bag
* **Why it works:** The crisp white ribbed tank tucked into the medium-wash 501s gives a classic 90s casual vibe. Throwing on the oversized grey crewneck adds a cozy, texturedlayer, while the chunky white sneakers and black crossbody bag tie the streetwear aesthetic together. 

### Outfit 2: Edgy & Classic Grunge
* **The Look:** A nod to retro rock-and-roll styling, utilizing all-black accents to make the medium-wash blue pop.
* **Key Pieces:**
  * **New Item:** Vintage Levi's 501 Jeans
  * **Wardrobe Item:** Black cropped zip hoodie
  * **Wardrobe Item:** Vintage black denim jacket
  * **Wardrobe Item:** Black combat boots
  * **Wardrobe Item:** Brown leather belt
* **Why it works:** Double denim is timeless, especially when mixing washes—the vintage black denim jacket paired with the blue Levi's 501s creates great contrast. Cinching the jeans with the brown leather belt adds a nice grounding earth tone, and the black combat boots and cropped zip hoodie give the whole outfit an edgy, grounded finish.

$ python -c "from tools import create_fit_card; ..."

python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"

These perfectly faded Levi's have that ideal broken-in feel right out of the box. I've been living in them with fresh white sneakers for an effortless, everyday streetwear look. Grab this medium-wash staple for $38.0 on depop before I change my mind.
---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:*
I used AI to write the functions search_listings, suggest_outfit, and create_fit_card. The prompt I used was I copied in what is the directions in the codepath walkthrough and then I also copied the notes from tools.py.
- *What came back:*
It returned 3 functions that were independent of each other and was able to be tested using the command that was included in the notes of each of the functions. Each of them passed those and also passed once they were tested. 
- *What I changed:*
 From the testing that was done it looks like everything is working as intended and it was written well. But changes might need to be done next week after we do a more in depth testing session and try to find ways in which to make it fail. So For this session I did not change anything to the responses that it gave me as everything appears to be working as intended. 

**Moment 2**

- *What I asked for:*
I did the suggestion at the end of milestone 3 "Here are five acceptance criteria for a multi-tool agent. For each one, tell me exactly how you would test it using only what the sentence says. Don't suggest improvements — just tell me what you'd do." 
- *What came back:*
It gave me a walk through of how it would go about testing the criteria that I included in criteria.md, the ones that I had created before using this prompt. 
- *What I changed:*
I went back and changed some of the criteria to be a little clearer so that it was easier to identify what was being tested. Not to make it so that the criteria always passed but rather to make it so that the criteria was actually testable and had a clear path to testing. 

STRETCH FEATURE

- **What it does:**
  - `suggestions_tool` looks through the listings after a fit card is created and returns two groups of listing recommendations.
  - `suggested_items_based_on_search` contains up to five listings similar to the selected listing, ranked using brand, category, style tags, and descriptive keywords. They exclude listings already returned by the original search and must be within 25% of the selected item's price. If the query included a maximum price, a suggestion must also be at or below that ceiling.
  - `suggested_items_to_help_make_your_outfit` contains five listings whenever at least five other inventory items are available. Outfit-related matches are ranked first, and random inventory listings fill any remaining slots.
- **Inputs:**
  - `new_item: dict | None` — the selected listing from the search, used as the anchor for similar-item recommendations.
  - `outfit: str` — the suggestion returned by `suggest_outfit`, used to look for complementary listings.
  - `search_results: list[dict] | None` — the original search results, excluded from recommendations so the user sees new listings.
  - `max_price: float | None` — the optional price ceiling extracted from the query; it also limits similar-item suggestions.
- **Returns:**
  - A dictionary with two list fields:
    - `suggested_items_based_on_search`: listing dictionaries ranked by similarity to the selected listing.
    - `suggested_items_to_help_make_your_outfit`: five listing dictionaries when at least five eligible inventory items exist, with outfit matches ranked first and random fallback listings filling remaining slots.
  - Each listing dictionary has the fields from the listings dataset: `id`, `title`, `description`, `category`, `style_tags`, `size`, `condition`, `price`, `colors`, `brand`, and `platform`.
- **When it has nothing:**
  - If `new_item` is missing, `suggested_items_based_on_search` is an empty list. The outfit-completion list is padded with random inventory listings to five items when possible, and contains fewer only when the inventory has fewer than five eligible items.
- **Test command** (provided for you to run; not run as part of this change):
  ```powershell
  python -c "from tools import suggestions_tool; from utils.data_loader import load_listings; listings=load_listings(); print(suggestions_tool(listings[0], 'Pair the jeans with a white tank top and chunky sneakers.', listings, 5))"

  python -c "from tools import suggestions_tool; from utils.data_loader import load_listings; listings=load_listings(); print(suggestions_tool(listings[0], 'Pair the jeans with a white tank top and chunky sneakers.', listings, 5))"
{'suggested_items_based_on_search': [], 'suggested_items_to_help_make_your_outfit': [{'id': 'lst_035', 'title': 'Low-Top Canvas Sneakers — Off-White', 'description': 'Classic low-top canvas sneakers in off-white. Very minimal. Some light yellowing on the sole edges from age. Size 9.', 'category': 'shoes', 'style_tags': ['classic', 'minimal', 'streetwear', 'basics'], 'size': 'US 9', 'condition': 'good', 'price': 20.0, 'colors': ['off-white', 'cream'], 'brand': None, 'platform': 'poshmark'}, {'id': 'lst_023', 'title': 'Crochet Halter Top — Cream', 'description': 'Handmade-looking crochet halter. Ties at the neck and back. Perfect for layering over a tank in summer.', 'category': 'tops', 'style_tags': ['cottagecore', 'boho', 'crochet', 'summer'], 'size': 'S/M', 'condition': 'excellent', 'price': 22.0, 'colors': ['cream', 'off-white'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_019', 'title': 'Platform Sneakers — White Chunky Sole', 'description': 'White chunky platform sneakers. Very late 90s / early 2000s energy. Velcro straps. True tosize. Some sole yellowing.', 'category': 'shoes', 'style_tags': ['y2k', 'platform', '90s', 'streetwear'], 'size': 'US 8', 'condition': 'good', 'price': 48.0, 'colors': ['white'], 'brand': None, 'platform': 'poshmark'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}]}

   Suggested items based on your search:
    - Oversized Crewneck Sweatshirt — Vintage Navy — $20.0
    - Henley Long Sleeve — Washed Burgundy — $16.0
    - Vintage Polo Shirt — Forest Green — $18.0
    - Graphic Tee — 2003 Tour Bootleg Style — $24.0
    - Vintage Band Tee — Faded Grey — $19.0
  Suggested items to help make your outfit:
    - Straight Leg Black Jeans — Faded — $30.0
    - Vintage Levi's 501 Jeans — Medium Wash — $38.0
    - Baggy Carpenter Jeans — Dark Wash — $36.0
    - Vintage Linen Blazer — Cream — $38.0
    - Denim Jacket — Light Wash, Cropped — $42.0
  ```
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
       [ ] Tool Inventory: all four tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the four per-tool tests, as text
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
