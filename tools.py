"""
The three FitFindr tools.

Each one is a standalone function you can call and test on its own, before any
of them are wired into the loop. Build and test them one at a time — three
untested tools joined by a loop is one problem that looks like six, because you
can't tell which layer is lying to you.

    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)             → str
    create_fit_card(outfit, new_item)              → str

All three are stubs right now. They run and they do nothing — that's the
starting position and it's deliberate.

⚠️ Before you write any of them, fill in the **Tool Inventory** section of your
README (Milestone 2). Four lines per tool: what it does, each input with its
type, exactly what it returns, and what it returns when it has nothing to give.
That last line is what your loop branches on. "Returns a list" earns nothing —
the description has to say what is *in* the list.
"""

import config  # noqa: F401 — you'll use this in search_listings
from generate import generate
from utils.data_loader import load_listings


# ── Tool 1: search_listings ───────────────────────────────────────────────────

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search the listings data for items matching a description, and optionally a
    size and a price ceiling.

    This is the tool that doesn't call the model, which makes it the easiest one
    to test and the one to move onto MCP in unit 4.

    Args:
        description: keywords describing what the user wants
                     (e.g. "vintage graphic tee").
        size:        a size string to filter by, or None to skip size filtering.
                     Match case-insensitively — "M" should match "S/M".

                     ⚠️ Read the sizes in the data before you reach for a plain
                     substring test. `"s" in "us 9"` is True, and so is
                     `"l" in "xl"`. A filter that returns shoes when someone
                     asked for a small top reads like a broken search, and it
                     will quietly cost you in unit 4 when you test criterion 1.
                     What counts as a size match is part of your spec — decide
                     it and write it into your Tool Inventory.
        max_price:   maximum price, inclusive, or None to skip price filtering.

    Returns:
        A list of matching listing dicts, best match first.
        **Returns an empty list when nothing matches — an empty list, not None,
        and not an exception.** Your loop branches on this.

    Each listing dict has these fields:
        id, title, description, category, style_tags (list), size,
        condition, price (float), colors (list), brand (str or None), platform

    Note that `brand` is None for most listings. That is deliberate and
    realistic — thrift listings often have no brand. If something you write
    assumes a brand is always there, you will find out in unit 4.

    TODO:
        1. Load every listing with load_listings().
        2. Filter by max_price and by size, when each is provided.
        3. Score what's left by keyword overlap with `description`.
        4. Drop anything scoring zero.
        5. Sort by score, highest first, and return the listing dicts —
           at most config.SEARCH_RESULT_LIMIT of them.

    Test it from a terminal before you move on:
        python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
    """
    import re

    def _size_tokens(value: str | None) -> set[str]:
        if not value:
            return set()
        cleaned = re.sub(r"[^a-z0-9]+", " ", str(value).lower()).strip()
        tokens: set[str] = set()
        if not cleaned:
            return tokens
        tokens.add(cleaned.replace(" ", ""))
        for token in cleaned.split():
            tokens.add(token)
        return tokens

    def _text_tokens(value: str | None) -> list[str]:
        if not value:
            return []
        return [
            token
            for token in re.findall(r"[a-z0-9]+", str(value).lower())
            if token not in {"a", "an", "the", "for", "with", "and", "or", "of", "on", "in", "to", "from", "it", "is", "at", "as"}
        ]

    def _matches_size(requested_size: str | None, listing_size: str | None) -> bool:
        if requested_size is None:
            return True
        requested_tokens = _size_tokens(requested_size)
        listing_tokens = _size_tokens(listing_size)
        if not requested_tokens or not listing_tokens:
            return False
        return bool(requested_tokens & listing_tokens)

    listings = load_listings()
    query_tokens = [
        token
        for token in _text_tokens(description)
        if token not in {"a", "an", "the", "for", "with", "and", "or", "of", "on", "in", "to", "from", "it", "is", "at", "as", "not", "no", "item", "items", "piece", "pieces", "look", "style", "fit"}
        and len(token) > 1
    ]

    matches: list[tuple[int, dict]] = []
    for listing in listings:
        if max_price is not None and float(listing.get("price", float("inf"))) > float(max_price):
            continue
        if not _matches_size(size, listing.get("size")):
            continue

        searchable = " ".join(
            [
                listing.get("title", ""),
                listing.get("description", ""),
                listing.get("category", ""),
                " ".join(listing.get("style_tags", [])),
                " ".join(listing.get("colors", [])),
                listing.get("brand") or "",
            ]
        )
        score = 0
        if query_tokens:
            counts = {}
            for token in _text_tokens(searchable):
                counts[token] = counts.get(token, 0) + 1
            score = sum(counts.get(token, 0) for token in query_tokens)
        else:
            score = 0

        if score > 0:
            matches.append((score, listing))

    matches.sort(key=lambda item: (-item[0], item[1].get("price", 0.0)))
    results = [listing for _, listing in matches[: config.SEARCH_RESULT_LIMIT]]
    return results


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """
    Given a thrifted item and the user's wardrobe, suggest one or two outfits.

    This one calls the model, through `generate()`. You don't need to think
    about rate limits — the adapter handles pacing for you.

    Args:
        new_item: a listing dict — the item the user is considering.
        wardrobe: a wardrobe dict with an 'items' key holding a list of items.
                  **It may be empty.** Handle that.

    Returns:
        A non-empty string with outfit suggestions.
        With an empty wardrobe, return general styling advice rather than
        raising or returning "". Unit 4 has you trigger the empty wardrobe on
        purpose, so decide now what it should do.

    TODO:
        1. Check whether wardrobe['items'] is empty.
        2. If it is, ask the model for general styling ideas for this item.
        3. If it isn't, format the wardrobe items into the prompt and ask for
           specific combinations naming pieces the user already owns.
        4. Return the model's response.

    Test it from a terminal before you move on:
        python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
    """
    item = new_item or {}
    wardrobe_items = wardrobe.get("items", []) if isinstance(wardrobe, dict) else []

    item_title = item.get("title") or item.get("name") or "this thrifted item"
    item_category = item.get("category") or "unknown category"
    item_colors = ", ".join(item.get("colors", [])) or "no color listed"
    item_brand = item.get("brand") or "no brand listed"
    item_price = item.get("price")
    item_desc = item.get("description") or ""

    if not wardrobe_items:
        prompt = (
            "You are a personal stylist. Suggest 1-2 outfits for a thrifted item.\n\n"
            f"New item: {item_title}\n"
            f"Category: {item_category}\n"
            f"Colors: {item_colors}\n"
            f"Brand: {item_brand}\n"
            f"Price: ${item_price if item_price is not None else 'not listed'}\n"
            f"Description: {item_desc}\n\n"
            "Give practical styling advice using general wardrobe principles. Mention the new item by name and keep it to 2 short outfit ideas with a little detail."
        )
    else:
        wardrobe_lines = []
        for wardrobe_item in wardrobe_items:
            name = wardrobe_item.get("name") or "Unnamed item"
            category = wardrobe_item.get("category") or "unknown category"
            colors = ", ".join(wardrobe_item.get("colors", [])) or "no color listed"
            tags = ", ".join(wardrobe_item.get("style_tags", [])) or "no style tags"
            wardrobe_lines.append(f"- {name} ({category}; colors: {colors}; style tags: {tags})")

        prompt = (
            "You are a personal stylist. Suggest 1-2 outfit combinations using the user's wardrobe and the new thrifted item.\n\n"
            f"New item: {item_title}\n"
            f"Category: {item_category}\n"
            f"Colors: {item_colors}\n"
            f"Brand: {item_brand}\n"
            f"Price: ${item_price if item_price is not None else 'not listed'}\n"
            f"Description: {item_desc}\n\n"
            "User wardrobe:\n" + "\n".join(wardrobe_lines) + "\n\n"
            "Return 1-2 outfit ideas. Explicitly name the new item and at least one wardrobe item in each suggestion."
        )

    return generate(prompt, system="You are a helpful personal stylist.")


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    """
    Write a short caption someone would actually post about the find.

    This calls the model too.

    Args:
        outfit:   the outfit suggestion string from suggest_outfit().
        new_item: the listing dict for the item.

    Returns:
        A two-to-four sentence caption.
        If `outfit` is empty or whitespace, return a descriptive message rather
        than raising.

    The caption should read like a real post rather than a product description,
    mention the item and its price and platform once each, and be specific about
    the vibe.

    It should also come out **differently for different inputs**. If you run
    this three times on the same item and get three word-for-word identical
    strings, it's one of two things, and both are near the top of `config.py`:

        • CACHE_ENABLED — the adapter handed back an answer it already had
        • TEMPERATURE   — at 0.0 the model gives the same words every time

    TODO:
        1. Guard against an empty or whitespace-only `outfit`.
        2. Build a prompt with the item details and the outfit.
        3. Call generate() and return the response.

    Test it from a terminal before you move on:
        python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
    """
    if not outfit or not outfit.strip():
        return "No outfit suggestion is available yet, so a fit card cannot be created."

    item_title = new_item.get("title") or new_item.get("name") or "thrifted find"
    price = new_item.get("price")
    platform = new_item.get("platform") or "platform not listed"
    brand = new_item.get("brand")
    description = new_item.get("description") or ""
    colors = ", ".join(new_item.get("colors", [])) or "not listed"
    style_tags = ", ".join(new_item.get("style_tags", [])) or "not listed"
    brand_detail = f"Brand: {brand}" if brand else "Brand: not listed"

    prompt = (
        "Write a fresh, social-media-ready fit card caption in 2-4 sentences. "
        "Make it sound personal and specific, not like a product listing. "
        "Mention the item, its price, and its platform exactly once each, "
        "and use the outfit details to establish a clear vibe. "
        "Do not invent or imply any brand; only mention a brand if one is "
        "provided below, and never write the word 'null' as a brand.\n\n"
        f"Item: {item_title}\n"
        f"Description: {description}\n"
        f"Colors: {colors}\n"
        f"Style tags: {style_tags}\n"
        f"{brand_detail}\n"
        f"Price: ${price if price is not None else 'not listed'}\n"
        f"Platform: {platform}\n\n"
        f"Outfit suggestion:\n{outfit.strip()}"
    )
    return generate(
        prompt,
        system="You write concise, distinctive thrift-fashion fit card captions.",
        cache=False,
    )
