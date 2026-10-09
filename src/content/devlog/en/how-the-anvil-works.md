---
title: How the anvil works, with the real odds
description: Every upgrade chance from +0 to +10, what a failed strike takes from you, the gems, and what changes at the anvil between 1v1 rounds.
date: 2026-10-09
game: slots-and-skulls
heroImage: ../../../assets/slots-and-skulls/screenshots/anvil_grid.jpg
heroImageAlt: The anvil screen in Slots & Skulls, with the skull counter and a grid of symbols waiting to be upgraded.
draft: false
---

Hi,

The anvil comes up in almost every demo review, and some of them quote numbers: "+0 95%, +4 80% / 20% break". Those were right when the demo launched. They aren't anymore. I've changed the curve three times since, so here's how it works in the current build, with my reasons where I actually wrote them down.

## Where you meet it

The ANVIL is a row in the main menu, run by Garrick the blacksmith. You use it between runs, never during one.

A new save doesn't see it at first. It opens after your first death. The game was throwing too much at new players up front, so the meta screens now arrive one at a time, as you lose. The first visit hands you 50 skulls (and a spare Rusty Dagger if you don't own a fourth symbol), so you never meet a new system with an empty wallet.

Skulls come from kills and you keep them when you die. Inside a run the shop can sell you an owned symbol one level higher, but that only lasts for the run. Permanent levels only come from the anvil.

## One strike

Pick a symbol and press UPGRADE. It costs skulls, 3 for the first strike and up to 50 for the last. If every strike landed, +0 to +10 would cost 209 skulls. They won't all land.

If it works, the symbol goes up one level. If it fails, the symbol burns. It doesn't drop a level, it's gone, and so are the skulls. That's the old Knight Online upgrade rule, which is where this whole system comes from. I kept it on purpose: the risk of losing the symbol is exactly what makes a successful strike feel that good.

Each level multiplies the symbol's numbers. Commons and rares gain 18% of their base per level, epics 19%, legendaries 20%, so a +10 common sits at 2.8x and a +10 legendary at 3x. And every whole number grows by at least one per level, so no strike is wasted. Coin pays 2 gold at +0 and 12 at +10.

Both rules are from September. Coin was showing "2.4 gold" at +1 and "2.7" at +2, and I didn't want fractions on any card. The rarity gains also used to run backwards (commons grew fastest), so a +10 Hammer, a rare, out-damaged a +10 Shackle, a legendary. Now a +10 epic stays above a +10 rare.

Costs never scale, so a symbol that costs gold or health to use costs the same at +10. Life steal and thorns stop at 100%, and damage to gold never pays more than 100 gold at once. And +10 has its own bonus: the symbol crits one tier harder, x3 becomes x4.

## The odds

| Strike | Success | Cost (skulls) | Consolation if it burns |
|---|---|---|---|
| +0 → +1 | 100% | 3 | none |
| +1 → +2 | 95% | 5 | +1% |
| +2 → +3 | 85% | 8 | +3% |
| +3 → +4 | 75% | 12 | +4% |
| +4 → +5 | 65% | 16 | +5% |
| +5 → +6 | 55% | 20 | +6% |
| +6 → +7 | 45% | 25 | +7% |
| +7 → +8 | 35% | 30 | +8% |
| +8 → +9 | 25% | 40 | +10% |
| +9 → +10 | 15% | 50 | +15% |

The chance on screen is the base number for that step plus your bonuses, added as flat points and capped at 100%. So 75% plus 8 is 83%. The bonuses are the Anvil Blessing modifier (2% per level, two levels), a Green Gem (+8%) and the CONSOLATION BONUS from the last column. The number you see is the number the game rolls. Even with everything stacked, +9 to +10 tops out at 52%. Only a Yellow Gem makes it certain.

The demo stops at +3. It was +5 until mid-September, when I lowered it. Three is enough for everyone to see how the anvil works, and it still leaves you a reason to push further in the full game. Whatever you forge in the demo carries over.

Now the history, since that's where the review numbers come from. The demo launched with 95 / 90 / 85 / 80 / 72 / 65 / 58 / 52 / 46 / 40. Around September 20 I made the first strike a sure thing and the back half much harsher: 100 / 95 / 85 / 75 / 65 / 55 / 25 / 15 / 10, then 50% for the very last step. That 50 looked like a typo, and I left it anyway. On September 29 a player reported seeing 50% at +9, and my note that day was basically "this is nonsense, make it 5%". In early October I eased the back half to what's in the table, for two reasons. I had just added fusion, which needs two +10s, and with fusion in the game it made more sense for +10 to be something you can actually reach. And the feedback was pretty clear that the old tail was brutal.

One of my playtesters, who has also played the full game, put it better than I can in their demo review: "the game is fun until you watch your favorite symbol burn while trying to upgrade it to +8". A player writing in Turkish said they'd wanted something to play in 5 to 10 minutes while still taking the risk of "+ basma" on items (Turkish MMO slang for pushing gear up a level), and that this game was exactly that.

## What softens it

Gems. One per strike, used up whether it lands or not. Green adds 8%. Blue turns a fail into a one level drop instead of a burn. Yellow skips the roll. Yellows come from the first clear of the hardest levels and from bosses at Heat 4 or higher, and the Gem Fusion modifier turns three greens into a blue and four blues into a yellow. The demo only has green.

The CONSOLATION BONUS. Every burn makes your next strike more likely, by the last column above, stacking up to 25% and resetting on any success. It's an old Knight Online superstition made real, the "yakmalık item": burn some junk first and the thing you care about will land. One catch: close the game and it's gone. That one is simply a design call.

The keep rule. You can't upgrade the last copy of a symbol type if losing it would leave fewer types than your machine has reels (three, more with Extra Wheel). A failed strike should never leave you unable to fill your reels. A Blue or Yellow Gem lifts the rule, and so does any strike at 100%, since none of those can burn anything.

The rest is smaller. Salvage Rights gives a burned symbol a 25% chance per level to leave a Green Gem. SMELT melts a spare into skulls, on a hold, because there's no undo. LOCK protects a copy from both. UPGRADE ALL strikes every copy at one level once each, because late saves end up with 25 copies of one symbol. Two different +10s can be fused into one new +1 symbol with both effects, and fusion never fails. The idea came from BALL x PIT. No cat changes the odds.

And Garrick talks. I wanted him to needle you a little. Burn something high and he asks, "Happy now? Couldn't stop while it was good, could you?"

## The 1v1 break

In a 1v1 match it's the same anvil screen, between rounds, with different rules around it.

My first multiplayer notes in August had you bringing your campaign symbols into duels. In September I decided against it. A match is its own sandbox: both players draft at +0, earn skulls inside the match and forge at the break. Nothing comes in from your save, and no gold, symbols or skulls go back. The thinking was that a +10 collection would flatten a new player, and "a fail destroys it" is only fair when both sides started from zero.

- Same base odds. No Anvil Blessing and no CONSOLATION BONUS. (For a while the bonus was shared by both seats by mistake, so one player's burn made the other's strike easier.)
- Every break after the first adds 5 points at every level, shown as EASIER TO UPGRADE.
- Every match shop deals one gem card (Green for 25 gold or Blue for 50), and the duel winner gets a Yellow Gem.
- The strike plays at double speed, because both players share one break clock.
- Your rival sees OPPONENT FORGED or OPPONENT BURNED IT only after you've seen your own result.
- Demo matches stop at +3 too.

The [demo is free on Steam](https://store.steampowered.com/app/4988090/Slots__Skulls_Demo/) if you want to try your luck up to +3. The full game, with seven more levels to burn things at, comes out on November 4. If that sounds like your kind of bad idea, [a wishlist](https://store.steampowered.com/app/4428910/Slots__Skulls/) helps a lot.
