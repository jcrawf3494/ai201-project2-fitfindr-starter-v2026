# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**
The input to the search is input by the user and so they may use words or phrases that do not match correctly to what the model would use when creating the fit card. And it needs to return 4/5 times once it has at least one match it should have enough information to move forward. 
---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**
This is important to stop the branching here because if an empty list moves through the loop it will cause the other functions to just give generic responses. So it needs to stop that loop before those occur. Because in a enterprise system in prod those calls to the model with empty lists would add up in cost for no real return. So this is a strict 5/5 one because it is so crucial for the next steps in everything 

---

## 3. Something about state


In 4 out of 5 tries suggest_outfit contains the specific phrases used by the previous step. For example, In suggest_outfit it will either name in the styling guide new_item or it will name an item in the wardrobe. But if it does not for either then it will be a fail. For create_fit_card it should reference back specifically item that it is generating a description for. 


**Why this target:**

This target is important to make sure that the user is recieving the correct information. It also comes in with a built in test. So that the user can tell if the information they are using is incorrect, as it will either reference the correct item, no item, or an incorrect item. And if it references and incorrect item then the user will know that the information that the model is giving is incorrect. I made this 4/5 because since it is a model it can still create a good description without referencing the material from previous steps. But still strict enough to where a tester can see that the majority of the time it is saying information that can be verified by looking at the refereneces. 



---

## 4. Something about the fit card


The fit card will produce a unique description when ran. When it is given information the brand can be a brand name or null. The model should only refer specific brand names given to it or nothing. It should not refer to a brand not mentioned or refer to the brand as null.  In 5 of 5 times ran it will not include brands that are not included in information given to it or refer to a brand called "null" 



**Why this target:**

If the user is looking at a specific item say from Nautica you do not want to create a description with a brand that is not Nautica like J. Crew. The model could also confuse the input "null" as the brand so that needs to be checked for as well as that could cause confusion for the user. I made this a strict one with 5/5 as well because I think it is super important to keep information consistent to make sure that the user is not confused and if you start throwing in other brands or nulls then users especially non tecnical users will quickly be pushed away. 



---

## 5. Your choice



If the user puts a max_price as a filter for input then the search_listings should follow that even if there are now items in that range. In 5 of 5 searches the user follows the max_price input and does not show one outside the range of the input. 



**Why this target:**

This is crucial because many people have a budget or a price range for items they are looking for and if given one outside of that range can become frustrated and leave the site without purchasing. From my own personal experience it is super frustrating when looking for products and the search returns things that do not matcht the criteria. So I made this one 5/5 as I think it is super important. 



---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
