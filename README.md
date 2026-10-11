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



<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

FitFindr helps users discover secondhand clothing by searching listings with a description and optional size or maximum price. It selects a matching item and suggests outfit combinations based on the user’s wardrobe, or gives general styling advice if the wardrobe is empty. The app creates a shareable fit-card caption for the item, then recommends similar listings and additional pieces that could complete the outfit. The user enters in a search in a string and then adds in the rest 



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
     It returns and empty list when nothing matches.  NOT None and NOT an exceptions. Now the logic is added that when it sees none it also says a message prompting the user on how to get a response by suggesting the user changes the description or size or price 

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
     - it should return a descriptive message rather than raise an exception or say none or null. 

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



**Branch rule:**
     If search_listings() from tools.py returns an empty list, put a message in the session, "No listings match your search, please try again" then stop the loop and ask for user input again. If search_listings() returns with a valid list, ie one that is full or not empyt,  then move to suggest_outfit() from tools.py and perform that action of that funtion. This function takes the output from search_listings() which is a dict and uses that to fill new_item dict. Then once those items are considered it moves to wardrobe: dict to create the suggestions and holds those in a dict as well. 
     
     BRANCHING If wardrobe: dict is empty it will just give general advice. if it is not empty then it will format the wardrobe items into the prompt and ask for specific combinations naming pieces the user already owns and then return the models response. 

     Once suggest_outfit() has run it will go to create_fit_card() and use the output from suggest_outfit to generate a listing description for that product that is unique every time. 
     
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

**Stretch features were added in this unit.** Details are in [STRETCH FEATURES](#stretch-features) below:

- A second tool moved onto MCP (`suggestions_tool`).
- Retry with looser constraints: an empty search retries once without the size filter and says what it dropped.
- A second improvement from the diagnosis, measured the same way: a stronger test for criterion 4.

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

- Produced by: `run_eval.py::main`
- Loop: `agent.py::run_agent` · tools: `tools.py`
- Tries per scenario: 5, caching off
- Temperature: 0.9
- When: 2026-10-11 15:55

The table below scores the five criteria from `criteria.md` against the
five recorded tries for each scenario.

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. A matching query completes all three tools | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. An impossible query stops before the second tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Outfit suggestion and fit card use prior state | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card does not invent a brand | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Search results stay within the price cap | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

---

**Real output from one try**, pasted as text, naming the file and function
that produced it:

Produced by `run_eval.py::main` (which calls `run_once`, which calls `agent.py::run_agent`) and written to `results/run_2026-10-11_1555_before.md`. This is Try 1 of the "search results stay within the price cap" scenario. The trace lines come from the `trace.step()` calls in `agent.py::run_agent`.

````
### search results stay within the price cap

- Query: `graphic tee under $20`
- Wardrobe: example

**Try 1**

- stopped early: no
- selected_item: Vintage Band Tee — Faded Grey ($19.0, depop)
- search_results: 3

Outfit suggestion:

```
Here are two distinct outfit combinations using your new vintage band tee and pieces from your wardrobe:

### Look 1: 90s Streetwear Edge
*This look leans into the boxy, well-loved feel of the tee, pairing it with dark denim and chunky sneakers for an effortless, casual vibe.*

* **Top:** Vintage Band Tee (Faded Grey)
* **Bottoms:** Baggy straight-leg jeans, dark wash
* **Outerwear (Optional):** Vintage black denim jacket (worn open for a layered, double-denim-adjacent texture play)
* **Shoes:** Chunky white sneakers
* **Accessories:** Black crossbody bag

### Look 2: High-Low Grunge Minimalist
*This combination plays with proportions by pairing the boxy, distressed tee with tailored trousers, finished off with classic grunge footwear.*

* **Top:** Vintage Band Tee (Faded Grey) - *Tuck it in slightly or let it hang loose over the waistband.*
* **Bottoms:** Wide-leg khaki trousers
* **Accessory:** Brown leather belt (to add a touch of structure and break up the tones)
* **Shoes:** Black combat boots (to anchor the slouchy silhouette of the trousers)
* **Outerwear (Layering option):** Black cropped zip hoodie (tied around the waist or thrown over the shoulders)
```

Fit card:

```
This boxy, charcoal band tee has that perfect sun-bleached fade you hunt years for. I've been living in it with slouchy khaki trousers and combat boots for an effortless grunge silhouette. Grab it on depop for $19.0.
```

Trace:

```
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 3 items: Vintage Band Tee — Faded Grey, Y2K Baby Tee — Butterfly Print, Mesh Long-Sleeve Top — Black
[2] suggest_outfit
      in:  dict with keys: new_item, wardrobe
      out: Here are two distinct outfit combinations using your new vintage band tee and pieces from your wardrobe:  ### …
[3] create_fit_card
      in:  dict with keys: outfit, new_item
      out: This boxy, charcoal band tee has that perfect sun-bleached fade you hunt years for. I've been living in it wit…
[4] suggestions_tool
      in:  dict with keys: new_item, outfit, search_results, max_price
      out: dict with keys: suggested_items_based_on_search, suggested_items_to_help_make_your_outfit
```

**Try 2**

- stopped early: no
- selected_item: Vintage Band Tee — Faded Grey ($19.0, depop)
- search_results: 3

Outfit suggestion:

```
Here are two distinct outfit combinations using your new vintage band tee and pieces from your wardrobe:

### Look 1: 90s Streetwear Edge
This look leans into the boxy, well-loved vibe of the tee, pairing it with dark denim and chunky footwear for an effortless, casual aesthetic. 

*   **Top:** Vintage Band Tee (Faded Grey)
*   **Bottoms:** Baggy straight-leg jeans (dark wash)
*   **Shoes:** Chunky white sneakers
*   **Bag:** Black crossbody bag
*   **Styling Tip:** Since the band tee has a boxy fit, let it hang naturally over the baggy jeans. Add the black crossbody bag and chunky white sneakers to tie the streetwear look together.

---

### Look 2: High-Low Grunge Contrast
This combination plays with proportions and styles by pairing the grungy, distressed band tee with tailored trousers, finished off with classic combat boots for an edgy, put-together finish.

*   **Top:** Vintage Band Tee (Faded Grey)
*   **Bottoms:** Wide-leg khaki trousers
*   **Outerwear:** Vintage black denim jacket
*   **Shoes:** Black combat boots
*   **Accessory:** Brown leather belt
*   **Styling Tip:** Tuck the band tee loosely into the wide-leg khaki trousers and cinch with the brown leather belt to define your waist against the wider silhouettes. Throw the vintage black denim jacket over your shoulders and lace up your black combat boots to complete the grunge-meets-minimalist aesthetic.
```

Fit card:

```
Threw this charcoal boxy band tee into heavy rotation with baggy denim and combat boots for that effortless 90s grunge edge. Snagged it on depop for just $19.0—the faded, well-loved wash is everything.
```

Trace:

```
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 3 items: Vintage Band Tee — Faded Grey, Y2K Baby Tee — Butterfly Print, Mesh Long-Sleeve Top — Black
[2] suggest_outfit
      in:  dict with keys: new_item, wardrobe
      out: Here are two distinct outfit combinations using your new vintage band tee and pieces from your wardrobe:  ### …
[3] create_fit_card
      in:  dict with keys: outfit, new_item
      out: Threw this charcoal boxy band tee into heavy rotation with baggy denim and combat boots for that effortless 90…
[4] suggestions_tool
      in:  dict with keys: new_item, outfit, search_results, max_price
      out: dict with keys: suggested_items_based_on_search, suggested_items_to_help_make_your_outfit
```

**Try 3**

- stopped early: no
- selected_item: Vintage Band Tee — Faded Grey ($19.0, depop)
- search_results: 3

Outfit suggestion:

```
Hey! Great find on that vintage band tee—a faded grey boxy tee is a timeless streetwear staple, and at $19, that's a total steal. 

Here are two effortless ways to style your new **Vintage Band Tee** using pieces right from your wardrobe:

### Look 1: 90s Grunge Streetwear
*This look leans into the relaxed, distressed vibe of the tee by pairing it with denim and chunky footwear.*

* **Top:** Vintage Band Tee (Faded Grey)
* **Bottoms:** Baggy straight-leg jeans (dark blue/indigo)
* **Outerwear:** Vintage black denim jacket
* **Shoes:** Chunky white sneakers
* **Accessories:** Black crossbody bag

**Why it works:** Double denim is having a major moment, and throwing the vintage black denim jacket over your new faded grey tee creates a cool, tonal contrast. The boxy fit of the shirt will drape nicely over the baggy dark-wash jeans, and the chunky white sneakers add a fresh, balanced finish.

---

### Look 2: High-Low Smart Casual
*This outfit mixes the edgy, well-loved character of the band tee with clean, tailored earth tones for an elevated, effortless look.*

* **Top:** Vintage Band Tee (Faded Grey)
* **Bottoms:** Wide-leg khaki trousers (khaki/tan)
* **Shoes:** Black combat boots
* **Accessories:** Brown leather belt, Black crossbody bag
* **Layering option (optional):** Black cropped zip hoodie worn over the shoulders or unzipped on hand if it gets chilly.

**Why it works:** Juxtaposing a casual graphic tee with tailored wide-leg trousers is one of my favorite styling tricks—it instantly looks intentional and fashion-forward. Tucking the band tee into the trousers and defining the waist with the brown leather belt pulls the whole outfit together, while the black combat boots add a subtle edge that ties back to the tee's graphics.
```

Fit card:

```
Tossed on this perfectly sun-bleached grey band tee with baggy dark denim and chunky white sneakers for a heavy 90s grunge look. It's got that heavy, lived-in feel you spend years trying to thrift, but I snagged it on depop for just $19.0.
```

Trace:

```
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 3 items: Vintage Band Tee — Faded Grey, Y2K Baby Tee — Butterfly Print, Mesh Long-Sleeve Top — Black
[2] suggest_outfit
      in:  dict with keys: new_item, wardrobe
      out: Hey! Great find on that vintage band tee—a faded grey boxy tee is a timeless streetwear staple, and at $19, th…
[3] create_fit_card
      in:  dict with keys: outfit, new_item
      out: Tossed on this perfectly sun-bleached grey band tee with baggy dark denim and chunky white sneakers for a heav…
[4] suggestions_tool
      in:  dict with keys: new_item, outfit, search_results, max_price
      out: dict with keys: suggested_items_based_on_search, suggested_items_to_help_make_your_outfit
```

**Try 4**

- stopped early: no
- selected_item: Vintage Band Tee — Faded Grey ($19.0, depop)
- search_results: 3

Outfit suggestion:

```
Hey! That vintage band tee is an amazing find—the boxy fit and faded wash give it so much character. Here are two effortless ways to style it using pieces from your wardrobe:

### Outfit 1: Effortless Streetwear Edge
*Play up the relaxed, vintage vibe of the tee with a full denim-on-denim moment and chunky kicks.*

*   **Top:** Vintage Band Tee — Faded Grey *(New Item)*
*   **Outerwear:** Vintage black denim jacket
*   **Bottoms:** Baggy straight-leg jeans, dark wash
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag

**Why it works:** Pairing the faded grey tee with the dark wash baggy jeans creates a great tonal contrast. Tossing the vintage black denim jacket over the top leans into that 90s streetwear aesthetic, while the chunky white sneakers keep the lower half feeling balanced and fresh. 

***

### Outfit 2: High-Low Contrast
*Mix the grungy, distressed feel of the band tee with polished, earthy tailoring for a cool, unexpected look.*

*   **Top:** Vintage Band Tee — Faded Grey *(New Item)* (tucked in slightly)
*   **Bottoms:** Wide-leg khaki trousers
*   **Accessories:** Brown leather belt
*   **Shoes:** Black combat boots
*   **Bag:** Black crossbody bag

**Why it works:** This is all about playing with proportions and styles. The wide-leg khaki trousers bring a minimal, structured element, which is instantly grounded by the edgy black combat boots. Adding the brown leather belt pulls the earth tones together and lets you do a casual half-tuck with the band tee to define your waist.
```

Fit card:

```
Wore this perfectly faded grey band tee with baggy dark wash denim and chunky white kicks for instant 90s streetwear energy. It’s got that ideal boxy, well-loved drape that only comes with age. Snag it on depop for $19.0 to instantly level up your rotation.
```

Trace:

```
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 3 items: Vintage Band Tee — Faded Grey, Y2K Baby Tee — Butterfly Print, Mesh Long-Sleeve Top — Black
[2] suggest_outfit
      in:  dict with keys: new_item, wardrobe
      out: Hey! That vintage band tee is an amazing find—the boxy fit and faded wash give it so much character. Here are …
[3] create_fit_card
      in:  dict with keys: outfit, new_item
      out: Wore this perfectly faded grey band tee with baggy dark wash denim and chunky white kicks for instant 90s stre…
[4] suggestions_tool
      in:  dict with keys: new_item, outfit, search_results, max_price
      out: dict with keys: suggested_items_based_on_search, suggested_items_to_help_make_your_outfit
```

**Try 5**

- stopped early: no
- selected_item: Vintage Band Tee — Faded Grey ($19.0, depop)
- search_results: 3

Outfit suggestion:

```
Hey there! That vintage faded grey band tee is an amazing find—the boxy fit and distressed graphic give it so much character. Since it has a cool, effortless grunge and streetwear vibe, I’ve put together two distinct outfit combinations utilizing pieces right from your wardrobe:

### Outfit 1: 90s Streetwear Edge
*Play up the boxy, relaxed fit of the band tee by pairing it with rich dark denim and chunky footwear.*

* **Top:** Vintage Band Tee — Faded Grey (New Item!)
* **Bottoms:** Baggy straight-leg jeans, dark wash
* **Outerwear:** Vintage black denim jacket (worn over the tee for a double-denim moment)
* **Shoes:** Chunky white sneakers
* **Accessories:** Black crossbody bag

**Styling Tip:** Let the tee hang loose over the baggy jeans for an effortless, skate-inspired silhouette. Layer the black denim jacket on top, leaving it unbuttoned to let the graphic peek through. 

***

### Outfit 2: High-Low Contrast
*Balance the worn-in, grunge aesthetic of the band tee with clean, tailored earth tones for a stylish juxtaposition.*

* **Top:** Vintage Band Tee — Faded Grey (New Item!)
* **Bottoms:** Wide-leg khaki trousers
* **Accessories:** Brown leather belt + Black crossbody bag
* **Shoes:** Black combat boots

**Styling Tip:** Tuck the band tee loosely into the wide-leg khaki trousers and define your waist with the brown leather belt. Finish the look with the black combat boots to anchor the outfit and tie in the dark tones of the tee's graphic.
```

Fit card:

```
This charcoal faded grey band tee has that perfect, lived-in drape that’s impossible to fake. I love wearing it loose over baggy dark denim with chunky sneakers for an effortless streetwear edge. Snag it on depop for $19.0 to instantly ground your rotation in 90s grunge.
```

Trace:

```
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 3 items: Vintage Band Tee — Faded Grey, Y2K Baby Tee — Butterfly Print, Mesh Long-Sleeve Top — Black
[2] suggest_outfit
      in:  dict with keys: new_item, wardrobe
      out: Hey there! That vintage faded grey band tee is an amazing find—the boxy fit and distressed graphic give it so …
[3] create_fit_card
      in:  dict with keys: outfit, new_item
      out: This charcoal faded grey band tee has that perfect, lived-in drape that’s impossible to fake. I love wearing i…
[4] suggestions_tool
      in:  dict with keys: new_item, outfit, search_results, max_price
      out: dict with keys: suggested_items_based_on_search, suggested_items_to_help_make_your_outfit
```

````

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
| 1 | 1. A matching query completes all three tools | 4 of 5 | Met | All of the tests that had a matching query for the initial tool, like the search, continued on and completed all three tools |
| 2 | 2. An impossible query stops before the second tool  | 5 of 5 | Met | This is an extension of the previous criteria to where it needs to stop if there is no matching criteria before moving on to the next state. This did that.  |
| 3 | 3. Outfit suggestion and fit card use prior state |4 of 5  | Met | In this one  I made sure that there was mention of the previous state in the outfit card to make sure that it matched and it did.  |
| 4 | 4. Fit card does not invent a brand | 5 of 5 | Met | Checked to see if there were none or null or if it invented a brand when a specific brand or none was mentioned.  |
| 5 | 5. Search results stay within the price cap | 5 of 5   | Met  | Gave a price point and then had to return results less than that or up to that, but could not go over.  |

**Diagnoses**

So all of the evals that I ran passed with perfect scores of 5/5 on each of the different criteria. This can be just as much of a red flag when doing testing and evaluations as multiple failures would be, because it usually means that something is wrong with the tests or with the criteria. So I ran a second eval. The first one was run_2026-10-07_2002_before.md and the most recent one was run_2026-10-11_1555_before.md. Both run_eval.py results showed the same results. So I initially looked at the criteria and the tests to see if I had specifically designed them to be passed. The criteria looked okay, but the issue did turn out to be the tests. For each of the tests or evaluations, it was using the same input for each try. For example, for every try it gave:

- Query: `graphic tee under $20`
- Wardrobe: example

This caused the model to pull the same information for every try, which was:

- selected_item: Vintage Band Tee — Faded Grey ($19.0, depop)
- search_results: 3

I then looked at the other tries for the evals that were run, and it did the same thing for every one. For some of the criteria this is needed. For example, the fit card needs the same item run more than once. But the criteria that check things like staying under pricing limits need multiple different inputs tested, including edge cases like using "forty" instead of "40" or spelling issues. So while the tests technically passed, they were not set up correctly and will need to be run again with updates to the testing, to get a good idea of whether the application actually meets the criterion or not.

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
python app.py ask 'I want a shirt that is under $20.' --trace         
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 1 items: Vintage Polo Shirt — Forest Green
[2] suggest_outfit
      in:  dict with keys: new_item, wardrobe
      out: Hey there! That forest green Ralph Lauren polo is an incredible find—classic, versatile, and that slightly box…
[3] create_fit_card
      in:  dict with keys: outfit, new_item
      out: This forest green Ralph Lauren polo brings the ultimate low-effort, high-reward energy to my rotation. Tucked …
[4] suggestions_tool
      in:  dict with keys: new_item, outfit, search_results, max_price
      out: dict with keys: suggested_items_based_on_search, suggested_items_to_help_make_your_outfit

  Found:    Vintage Polo Shirt — Forest Green — $18.0 on thredUp

  Outfit:   Hey there! That forest green Ralph Lauren polo is an incredible find—classic, versatile, and that slightly boxy fit gives it such a cool, effortless vibe. 

Here are two ways to style your new vintage polo using pieces from your wardrobe:

### Outfit 1: Streetwear Edge
*Play up the boxy fit of the polo with relaxed denim and chunky sneakers for an effortless, cool-girl street style look.*

*   **Top:** Vintage Polo Shirt — Forest Green (New item!)
*   **Bottoms:** Baggy straight-leg jeans, dark wash
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag
*   **Styling Tip:** Leave the polo unbuttoned for a relaxed feel, and let it drape naturally over the baggy jeans. Add the black crossbody bag to pull the monochromatic black-and-white accents together.

### Outfit 2: Elevated Earth Tones
*Lean into the rich forest green by pairing it with warm neutrals for a minimal, sophisticated look that still feels super comfortable.*

*   **Top:** Vintage Polo Shirt — Forest Green (New item!)
*   **Bottoms:** Wide-leg khaki trousers
*   **Accessories:** Brown leather belt, Black crossbody bag
*   **Shoes:** Chunky white sneakers (or swap for black combat boots for a grunge contrast)
*   **Styling Tip:** Tuck the polo loosely into the wide-leg khaki trousers and cinch your waist with the brown leather belt to anchor the earth tones. It’s a polished outfit that works for brunch, errands, or casual hangouts.

  Fit card: This forest green Ralph Lauren polo brings the ultimate low-effort, high-reward energy to my rotation. Tucked into wide-leg khakis with a brown leather belt, it’s giving rich earth tones and timeless prep. Snagged this gem on thredUp for just $18.0.

  Suggested items based on your search:
    - Henley Long Sleeve — Washed Burgundy — $16.0
    - Oversized Crewneck Sweatshirt — Vintage Navy — $20.0
    - Vintage Band Tee — Faded Grey — $19.0
    - Y2K Baby Tee — Butterfly Print — $18.0
    - Tie-Dye Long Sleeve — Pastel — $17.0
  Suggested items to help make your outfit:
    - Straight Leg Khaki Trousers — Olive — $29.0
    - Straight Leg Black Jeans — Faded — $30.0
    - Leather Belt — Brown, Braided — $12.0
    - Wide-Leg Linen Trousers — Natural — $34.0
    - Vintage Levi's 501 Jeans — Medium Wash — $38.0

1 model calls this session, 1 served from cache, 518 prompt + 63 output tokens

```

**Empty search**

```
python app.py ask 'How does a MCP work?' --trace             
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)
      →    branch: empty, stopping

  The search found no matching listings. Try using different description keywords, changing the size, or raising the maximum price.

0 model calls this session
```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->

I moved one tool, `search_listings`, behind MCP. It is the one tool that doesn't call the model.

What changed in the code:

- `mcp_server.py` now registers `search_listings` with `@mcp.tool()`. It takes `description: str`, an optional `size: str | None` and an optional `max_price: float | None`, and returns `list[dict]`. Its docstring is the tool description and states the empty case: no match returns an empty list. The function wraps the real implementation in `tools.py`, which is imported under the alias `_search_listings_impl` so the registered tool doesn't call itself.
- `agent.py::run_agent` no longer imports or calls `search_listings` directly. It builds a `search_inputs` dict from the parsed query and calls `call_tool("search_listings", search_inputs)` from `mcp_client.py`.
- I added a `trace.step("search_listings (via MCP)", ...)` call right after it, so the MCP call shows up in the trace (see the Loop Trace above).

Whether anything behaved differently afterwards:

- The return value did not change. The call still comes back as a list of listing dicts, and the empty-list branch still fires: an impossible query stops with `branch: empty, stopping` and no model calls (see the Empty search trace above).
- Search results were the same kind of data as before, with the same fields, and all five criteria ran through the MCP path in the run logs.
- `mcp_client.py` starts the server, makes the call and stops the server on every call, so each search spawns a subprocess. I did not time it, but that is the design and it is slower than a direct function call.



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

What I changed

So I decided to just focus on making a better test for criterion 5 since the instruction said to focus on just one change. So the changes I made were in scenarios.py and run_eval.py to change how the tests were actually run. 

The criterion 5 scenario now has a queries list, so each of the five tries gets a different query:
graphic tee under $20 is the baseline, using the phrasing the parser knows.
graphic tee under forty dollars writes the number as a word.
graphic tee $25 or less puts the cap after the number.
graphic tee, budget of 30 uses no keyword the parser recognizes.
graphic tee under $1 sets a cap below every listing, so it should return zero results.
validate() now rejects an empty entry in queries.
run_eval.py

A new query_for(scenario, attempt) picks the query for each try. A scenario with queries uses a different one per try. Every other scenario still repeats its single query, so criteria 1–4 behave exactly as before.
run_once takes the attempt number and stores the query it used.
The console output shows the query for each try on scenarios that have a queries list.
The report now logs, for every try, the query used, the parsed values (including max_price), and the prices of all returned results.


**Which failure it was meant to fix:**

So based of the testing there were not "failures" of the criteria  or criterion that needed fixing but rather the test for those actually needed to be updated. So the failure was a test that was not extensive and basically to perfect for the scenario that it was given. So I tried to create a better test. 

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. A matching query completes all three tools | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. An impossible query stops before the second tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Outfit suggestion and fit card use prior state | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card does not invent a brand | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Search results stay within the price cap | 5 of 5 | PASS | PASS | FAIL | PASS | PASS | MISSED (4/5) |




**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->

It did "help" by causing fails. Here is the diagnosis for each run 
Criterion 5, per try (query → parsed max_price → result prices):

- Try 1 `graphic tee under $20` → 20.0 → [19.0, 18.0, 15.0]: all within the cap. PASS
- Try 2 `graphic tee under forty dollars` → **None** → [24.0, 19.0, 18.0, 15.0, 26.0, 27.0]: the cap was never parsed, but every result happens to be under $40. PASS by outcome only.
- Try 3 `graphic tee $25 or less` → **None** → [24.0, 19.0, 18.0, 26.0, 15.0, 27.0]: 26.0 and 27.0 are over the $25 cap. FAIL
- Try 4 `graphic tee, budget of 30` → **None** → [24.0, 19.0, 18.0, 26.0, 15.0, 27.0]: the cap was never parsed, but every result happens to be under $30. PASS by outcome only.
- Try 5 `graphic tee under $1` → 1.0 → []: nothing over the cap, and the loop stopped early. PASS

Tries 2 and 4 are passes by luck, not by the cap being applied. If the criterion is read as "the cap is applied", they are FAILs and the row is 2/5. Either reading is MISSED.

**Diagnosis of the criterion 5 miss**

- **Place:** the loop's query parsing, `_parse_query` in `agent.py`. It is not the search tool.
- **Mechanism:** the price regex in `_parse_query` only matches a keyword followed by a number: `under`, `below`, `less than`, `at most`, `up to`, `max`, `max_price=` or `<=`, then an optional `$` and digits. A cap phrased any other way (`under forty dollars`, `$25 or less`, `budget of 30`) matches nothing, so `parsed["max_price"]` is `None`. `None` is then passed to `search_listings` through the MCP call, and `search_listings` skips price filtering when `max_price` is `None`. The cap is dropped without any error or notice, and the search runs unfiltered.
- **Why the tool is not at fault:** when the cap is parsed correctly (`under $20`, `under $1`), `search_listings` applies it correctly. Try 1 returned only prices at or below 20 and Try 5 returned nothing.
- **Pattern:** Tries 2, 3 and 4 are one problem, not three. Only Try 3 produced a visible violation (26.0 and 27.0 against a $25 cap), because the other two caps happened to sit above every matching listing.
- **Fix I would make, not done in this unit:** extend the price pattern in `_parse_query` to cover number words, `or less` and `budget of`. Better still, when a query contains a price word or `$` but `max_price` comes back `None`, set `session["notice"]` so the user is told the cap was not understood.

## Failure Modes

Three failure modes, each triggered on purpose.

**1. Empty search.** The query `designer ballgown size XXS under $5` matches nothing. The loop stops before `suggest_outfit` and tells the user what to change. From `results/run_2026-10-11_1810_after.md`, scenario "impossible query stops early", produced by `agent.py::run_agent`:

```
- query used: `designer ballgown size XXS under $5`
- parsed: {'description': 'designer ballgown', 'size': 'XXS', 'max_price': 5.0}
- stopped early: yes — The search found no matching listings. Try using different description keywords, changing the size, or raising the maximum price.
- selected_item: (none)
- search_results: 0

[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)
      →    branch: empty, stopping
```

**2. Empty wardrobe.** `suggest_outfit` is handed a wardrobe with no items. `agent.py::run_agent` sets `session["notice"]` saying general advice will be used, and `tools.py::suggest_outfit` switches to a general-styling prompt. From `results/run_2026-10-11_1810_after.md`, scenario "empty wardrobe" (`denim jacket under $50`), Try 1. It returned advice, with no crash and no empty string:

```
Outfit suggestion:

That Wrangler cropped denim jacket is a fantastic find—the structured shoulders give it a great 80s edge, and the light wash makes it super versatile. 

Here are 2 outfit ideas using general wardrobe principles of balance and proportion:

**1. High-Contrast & Proportion Play**
* **The Look:** Pair the **Wrangler Light Wash Cropped Denim Jacket** with a sleek black or charcoal ribbed midi dress and chunky black combat boots. 
* **Why it works:** Because the jacket is cropped, it naturally defines your waist and balances the length of the midi dress. The dark, fitted dress creates a sharp contrast against the boxy, light-wash denim, adding instant edge.

**2. Playful Textures (Double Denim)**
* **The Look:** Layer the **Wrangler Light Wash Cropped Denim Jacket** over a crisp white cotton tee and wide-leg trousers in an olive green or camel color, finished off with retro sneakers.
* **Why it works:** Pairing light-wash denim with earthy tones creates a grounded, effortless look. The relaxed, wide-leg pants balance out the structured, cropped silhouette of the jacket for an easy, balanced daytime outfit.

Fit card:

Shoulder pads doing all the heavy lifting in this vintage Wrangler cropped denim jacket. I love throwing it over an olive wide-leg trouser and crisp tee for that effortless daytime proportion play. Snagged this blank-canvas vintage layer on Poshmark for $42.0.
```

**3. Model unavailable.** `agent.py::run_agent` wraps both model calls, `suggest_outfit` and `create_fit_card`, in `try/except ModelUnavailable`. On a failure it records a `trace.step(...)` and sets `session["error"]` instead of raising. I changed one character of `GEMINI_API_KEY` in `.env`, ran the command below, then restored the key. The run did not hang and did not show a stack trace. It ended with a readable message that names the cause and the fix:

```
python app.py ask 'I want a shirt that is under $20.'
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 1 items: Vintage Polo Shirt — Forest Green
[2] suggest_outfit
      in:  dict with keys: new_item, wardrobe
      out: Hey there! That forest green Ralph Lauren polo is an incredible find—classic, versatile, and that slightly box…
[3] create_fit_card
      in:  dict with keys: outfit, new_item
      out: ModelUnavailable: The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh k…

  The model is unavailable, so the fit card could not be generated. The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com. Fix the model access issue and try again.

1 model calls this session, 1 served from cache
```

The error came from the `create_fit_card` handler in `agent.py::run_agent`. Step 2 still shows an outfit because I had already asked this query, so `suggest_outfit` was answered from the build cache (the last line says "1 served from cache"). `create_fit_card` always calls the model with the cache off, so it was the first call to reach the API and it was rejected. The `suggest_outfit` handler was not exercised in this run, only the `create_fit_card` one.


---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->

The other tests that seem to still need to be re worked are as follows: 

Criterion 2: weak test

The impossible query has two causes, size XXS and under $5. Either one alone empties the results, so you can't tell which one triggered the stop.
The error text in agent.py:195 is a fixed string, so it is identical on every try. The criterion requires a message that names what to change, and the test never checks that it fits the query.

Criterion 3: mostly measures the prompt

The prompt tells the model to name the new item and a wardrobe item, so it nearly always does.
On the empty-wardrobe path only the item name is required, which is easier.
A substring match is a loose check. Decide whether a partial title like "denim jacket" counts.

Criterion 4: depends on the data

The test only means something if the selected listing has a null brand. Check that in the log, because the model isn't responsible for it.
The prompt already says "never write null" and "don't invent a brand", which pushes the model toward passing.
A stronger test would add:
a listing that does have a brand, with a check that the card names exactly that brand
a scan of the card for brand names the model might add on its own, such as "Levi's" or "Nike"
Criterion 1: easy target

The scenario query matches clearly, and the loop has no random branches. The only failures would be a model outage or a crash, so 5 of 5 is almost certain.
Your "why" says user phrasing is the risk, but the test uses a clean query. It doesn't exercise that risk.
Fixes that stay within the testing

Criterion 2: split it into two scenarios, one with only an impossible size and one with only an impossible price. Then check that the message matches the cause.
Criterion 3: require an exact item title, or at least the key words, and score the empty-wardrobe path separately.
Criterion 4: add one branded and one unbranded listing, and scan the cards for outside brand names.
Criterion 1: use messier queries, such as typos, extra words and different sizes.

So if there was more time I would go in and update the testing for these to offer a more robust testing and diagnosis of where the application actually is at. Right now it is almost like a "false positive" for how good the results are but after a deep dive it is obvious this is would not be an application that would be ready for production. Though depending on if I have time I might fix one more for the stretch feature. 



---

## STRETCH FEATURES

Three stretch features were added. None of them changes `criteria.md`.

### 1. A second tool moved onto MCP

I moved suggestions_tool onto MCP as the second tool. Like search_listings, it doesn't call the model, so moving it only changes where it runs and not what it returns.

In mcp_server.py I registered suggestions_tool as a tool. It takes the selected item (or nothing), the outfit text, the original search results and an optional max price, and it returns the two lists of suggested listings. I wrote the description so someone who never sees my code could still use it. It says that max price is in whole dollars, what the two lists are, and what happens when there is no selected item. The real function in tools.py is imported under a different name so the registered tool doesn't end up calling itself.

In agent.py, run_agent no longer imports suggestions_tool from tools. It now calls it through call_tool, and the trace step is labelled "suggestions_tool (via MCP)". Nothing should look different to the user. The suggestions in the session should still be a dict with the same two keys.

To check it, run python app.py ask 'I want a shirt that is under $20.' --trace. Step 4 of the trace should say suggestions_tool (via MCP) and both suggestion lists should still print.

Here is the output from that run, which is the proof that the second tool is connected. Step 4 now says suggestions_tool (via MCP), and it returned a dict with the same two keys as before, suggested_items_based_on_search and suggested_items_to_help_make_your_outfit. Both lists printed at the end with five items each, so what comes back did not change when the call moved behind MCP. The trace was produced by the trace.step calls in agent.py::run_agent, and the call itself goes through call_tool in mcp_client.py to the server in mcp_server.py.

```
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 1 items: Vintage Polo Shirt — Forest Green
[2] suggest_outfit
      in:  dict with keys: new_item, wardrobe
      out: Hey there! That forest green Ralph Lauren polo is an incredible find—classic, versatile, and that slightly box…
[3] create_fit_card
      in:  dict with keys: outfit, new_item
      out: Scored this forest green Ralph Lauren vintage polo on thredUp for just $18.0. I love leaning into the boxy fit…
[4] suggestions_tool (via MCP)
      in:  dict with keys: new_item, outfit, search_results, max_price
      out: dict with keys: suggested_items_based_on_search, suggested_items_to_help_make_your_outfit

  Found:    Vintage Polo Shirt — Forest Green — $18.0 on thredUp

  Outfit:   Hey there! That forest green Ralph Lauren polo is an incredible find—classic, versatile, and that slightly boxy fit gives it such a cool, effortless vibe. 

Here are two ways to style your new vintage polo using pieces from your wardrobe:

### Outfit 1: Streetwear Edge
*Play up the boxy fit of the polo with relaxed denim and chunky sneakers for an effortless, cool-girl street style look.*

*   **Top:** Vintage Polo Shirt — Forest Green (New item!)
*   **Bottoms:** Baggy straight-leg jeans, dark wash
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag
*   **Styling Tip:** Leave the polo unbuttoned for a relaxed feel, and let it drape naturally over the baggy jeans. Add the black crossbody bag to pull the monochromatic black-and-white accents together.

### Outfit 2: Elevated Earth Tones
*Lean into the rich forest green by pairing it with warm neutrals for a minimal, sophisticated look that still feels super comfortable.*

*   **Top:** Vintage Polo Shirt — Forest Green (New item!)
*   **Bottoms:** Wide-leg khaki trousers
*   **Accessories:** Brown leather belt, Black crossbody bag
*   **Shoes:** Chunky white sneakers (or swap for black combat boots for a grunge contrast)
*   **Styling Tip:** Tuck the polo loosely into the wide-leg khaki trousers and cinch your waist with the brown leather belt to anchor the earth tones. It’s a polished outfit that works for brunch, errands, or casual hangouts.

  Fit card: Scored this forest green Ralph Lauren vintage polo on thredUp for just $18.0. I love leaning into the boxy fit by tucking it into wide-leg khaki trousers with a brown belt for an effortless earth-tone moment. It’s that ultimate classic piece you can dress up or down without even trying.

  Suggested items based on your search:
    - Henley Long Sleeve — Washed Burgundy — $16.0
    - Oversized Crewneck Sweatshirt — Vintage Navy — $20.0
    - Vintage Band Tee — Faded Grey — $19.0
    - Y2K Baby Tee — Butterfly Print — $18.0
    - Tie-Dye Long Sleeve — Pastel — $17.0
  Suggested items to help make your outfit:
    - Straight Leg Khaki Trousers — Olive — $29.0
    - Straight Leg Black Jeans — Faded — $30.0
    - Leather Belt — Brown, Braided — $12.0
    - Wide-Leg Linen Trousers — Natural — $34.0
    - Vintage Levi's 501 Jeans — Medium Wash — $38.0

1 model calls this session, 1 served from cache, 518 prompt + 68 output tokens
```

2. Retry with looser constraints

When the first search comes back empty and the query asked for a size, run_agent now searches one more time without the size filter, then tells the user what it dropped. For example: "No listings matched size XXS, so the search was repeated once without the size filter."

I only drop the size. The price cap and the description are never loosened, and it only retries once. If the retry is also empty, the loop stops with the same "no matching listings" message as before.

The retry shows up in three places. The session records what was dropped, the notice carries the message to the user (app.py already prints notices), and the trace gets a second search step labelled "retry without size" with a note saying whether it found anything.

This shouldn't affect criterion 2. The impossible query (designer ballgown size XXS under $5) still finds nothing on the retry, because no listing costs $5 or less, so it still stops before suggest_outfit. The only difference is that its trace now has two search steps instead of one.

I also added a diagnostic scenario to scenarios.py, "empty search retries without size", which searches for a graphic tee in size XXS. None of the tees come in XXS, so it should take the retry path. It isn't one of the five criteria. I haven't measured this yet, since I haven't run the evals since making the change.

3. A second improvement: a stronger test for criterion 4

This came straight from my own diagnosis in What's Still Broken, where I said the criterion 4 test was weak. The scenario used one listing with a null brand five times, so all it could show was that the model didn't invent a brand for that one item. The prompt also already tells the model not to invent a brand, so it was set up to pass.

I only changed the testing, not the criterion. In scenarios.py, the criterion 4 scenario now has a list of queries so each try picks a different listing. Two of the five use listings with no brand: the original bootleg tee, and a color block windbreaker, which is the kind of item a model might label Nike or Adidas on its own. The other three use listings that have a real brand: the Ralph Lauren polo, the Wrangler denim jacket and the Champion track jacket. For those, the fit card has to name the right brand and nothing else.

In run_eval.py I added a brand check that writes one extra line for every try in the log. It shows the brand on the listing, any brand names found in the fit card, and whether the word "null" shows up. The list of brands it looks for is every brand in the listings data plus a short list of well-known ones like Nike, Adidas and Gucci. It doesn't score anything. I still read the log and decide pass or fail myself.

I think this is a better test because a pass on the branded listings now means the card used the right brand, not just that it avoided one, and the windbreaker is there to catch the model bringing in a brand from its own knowledge.

There are two caveats. The search always picks the first result, so each query only tests the listing it selects, and the selected_item line in the log shows which one that was. Also, a word like "Champion" can show up in a card as an ordinary word, so a hit in the brand check has to be read in context.

### Results

I ran python run_eval.py --label stretch (results/run_2026-10-11_1854_stretch.md), five tries per scenario with caching off, using the same format as the other run logs.

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. A matching query completes all three tools | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. An impossible query stops before the second tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Outfit suggestion and fit card use prior state | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card does not invent a brand | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Search results stay within the price cap | 5 of 5 | PASS | PASS | FAIL | PASS | PASS | MISSED (4/5) |

The two diagnostic scenarios are not part of the five criteria, so they are not in the table. Both ran five tries with no crashes.

Did the stronger criterion 4 test help? It did not find a failure, and I think that result is more trustworthy than the first one. Before, a 5/5 only meant the model didn't invent a brand for one listing with no brand. Now the five tries use five different listings and the log shows the evidence for each. Both of the null-brand listings came back with no brand in the card, and that includes the color block windbreaker, which I picked because it is the kind of item a model might call a Nike or Adidas. The three branded listings (Ralph Lauren, Wrangler and Champion) each came back with exactly that brand named in the card and no other. The word "null" never showed up. So I'm fairly confident criterion 4 is actually being met and not just passing because of a weak test. The honest limit is that it is still five listings out of forty, and the search picks the first result, so a different item could still behave differently.

Criterion 5 is still missed at 4 of 5, the same as the earlier after run. Try 3 (graphic tee $25 or less) returned a $26 and a $27 listing over the cap. Tries 2 and 4 only passed because every result happened to be under the cap I meant, since the cap was never parsed. That is still the _parse_query problem in agent.py I described in the diagnosis, and I did not fix it in this unit.

The retry worked as intended. For graphic tee size XXS, all five tries found nothing on the first search, searched again without the size, found six listings, and showed the notice saying the size was dropped. The trace shows the second search step with the note "retry: dropped size XXS". Criterion 2 is not affected, because the impossible query still stops before suggest_outfit in all five tries. The only change is that its trace now shows two search steps, and the second one ends with "retry: still empty, stopping".



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
