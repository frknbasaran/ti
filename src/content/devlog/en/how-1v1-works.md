---
title: How 1v1 works, from the draft to the duel ranks
description: The two modes, the draft, the fights before each duel, health that grows every round, equal pay for both players, and how the duel rank reads your record.
date: 2026-10-10
game: slots-and-skulls
heroImage: ../../../assets/slots-and-skulls/screenshots/fight_view.jpg
heroImageAlt: A fight in Slots & Skulls, with the slot machine and its stop button on the left and an enemy with its health and shield bars on the right.
draft: false
---

Hi,

1v1 went into the demo in the middle of September. Back then there was no ranking at all. By October 1 there was, and nearly every number in a match has moved since. Here's the match as it ships, and the notes I kept along the way.

## Getting into a match

1v1 is a row on the main menu, and unlike the anvil it's open from your first launch. You can invite a friend from your Steam list.

In the lobby each player picks a skin, any of 35, which is every enemy in the game, bosses included (no two alike), and that's what you look like on the other screen during the duel. The host sets the rest: rounds to win (1 to 5, two by default), reels (3 to 5, which is also how many symbols each of you drafts), the break between rounds (60 seconds to six minutes, 90 by default) and the mode.

CLASSIC is the whole thing. Every round you both fight four enemies on your own, then you duel. DUEL ONLY drops the enemies, so every round is just the duel.

The demo has 1v1 too: Classic only, best of three, three reels, two skins, the shortest break and ten symbols to draft. My note at the time was that the demo was already very generous, so ten would do. The rest of the board is still there, dimmed.

## Everyone starts level

Nothing from your save comes into a match, and no gold, symbols or skulls go back out. Both players start with no gold, no modifiers, no gems and nothing forged. I went through why in [the anvil post](/devlog/how-the-anvil-works/#the-1v1-break).

## The draft

In the full game every symbol is on the draft board, grouped by what they do. You pick one, your opponent picks one, back and forth until you each have one per reel, and who goes first is random. What you take is gone for the other side, and you can watch their cursor while they decide.

The first version used a snake order like a Dota hero pick, and I changed it the same day to one pick each. A pick gets 30 seconds (20 until the end of September), and when the clock runs out the game picks at random.

## A round

In Classic, a round starts with the farm: the same four enemies for both of you, each on your own screen, at your own pace. Round one borrows level 1's fights, round two level 2's, and so on, never the boss. After an early playtest my note was that players were dying too often, so in round one the farm enemies have 90% of their campaign health and 85% of their damage. From round two they get tougher on top of that. Kills pay gold and five times the usual skulls, and a shop opens after every fight for 30 seconds.

Die in the farm and the round ends on the spot: your opponent takes the point and nobody gets paid for that round. Finish first and a waiting screen shows which fight the other player is on, with a button back into the shop.

Then the duel. You walk in at full health, a coin flip decides who spins first (a fresh flip every duel), and turns alternate. Your reels hit your opponent, theirs hit you, and their symbols appear one at a time as each of their reels lands. You have 25 seconds to start a spin, and each reel stops itself after 9. Whoever hits zero loses the round.

There's no typing. You get four preset lines for the fight and four replies for the anvil, and a fight line is delivered by a cat walking onto the other screen. I wanted them translated into every language the game has, so each side reads them in their own.

## Health, healing and pay

Max health comes in steps set by the reel count and grows one step every round for both players. The duel pays both of you the same: gold, plus skulls that climb with the round.

| Round | Max health (3 / 4 / 5 reels) | Classic duel pay (gold / skulls) | Duel Only pay (gold / skulls) |
|---|---|---|---|
| 1 | 350 / 500 / 750 | 150 / 75 | 300 / 60 |
| 2 | 700 / 1,000 / 1,500 | 150 / 113 | 300 / 90 |
| 3 | 1,050 / 1,500 / 2,250 | 150 / 188 | 300 / 150 |
| 4 | 1,400 / 2,000 / 3,000 | 150 / 300 | 300 / 240 |
| 5 | 1,750 / 2,500 / 3,750 | 150 / 450 | 300 / 360 |

Past round five the skulls stay at the round five number and health keeps climbing.

Shields start at zero in every fight and cap at 250. My note on that one was basically "keep the max the same, but both of them start at 0."

In an early match Ember Heart, a heal that also gives regen, kept one player standing so long that my note just says "it made the guy almost immortal." So against a player, heals, regen and life steal work at half strength, and in a match regen never gives back more than 6% of your max health per turn.

Two more duel-only rules. Your opponent counts as a boss, so symbols with a bonus against bosses get it. The Explosion powerup normally hits for a fixed amount. In a duel it does up to 15% of your opponent's max health instead, because my note on the old version was that it "hits flat right now and there's no point to it."

## Equal pay, and the break

In the first version the round's winner took the loser's gold, and the menu line for the mode said "BRING A FRIEND. LEAVE WITH THEIR GOLD." I cut it a day later, and the line now says "LEAVE WITH THE SKULLS." Then for a day the winner was paid more than the loser. After a playtest on September 16 my note was that the winner's bigger purse was snowballing the match, so now both get the same and a win only buys the point, plus a Yellow Gem that lives as long as the match does.

The climbing skulls came later. I asked for something like 100, 150, 250, 400 and 600 over five rounds, and the game uses that curve on a smaller base.

Between rounds there's one clock for the shop and the anvil together, split however you like, and it ends early once you both press I'M READY. The match shop sells symbols, powerups (four passive and four active at most) and one gem card. It started as two separate timers, and my note was that both players should simply get 90 seconds for the two. At the end of September it became the lobby setting. The break's anvil rules, including the odds getting easier every break, are in [the anvil post](/devlog/how-the-anvil-works/#the-1v1-break).

Each player gets two 60-second pauses per match, which stop the clock for both of you. Leaving hands your opponent the match, and so does dropping out for more than a minute.

When someone takes the last round, a match report puts both of you side by side: rounds, kills, damage, gold and skulls. CONTINUE takes you both back to the same lobby, so a rematch is one READY away.

## Duel ranks

Every duel you finish goes on your record, won or lost. A round lost in the farm doesn't count, and leaving a match counts as a lost duel.

You're unranked until your third duel is on record. After that you hold one of 16 ranks, four tiers of four: Bronze, Silver, Gold and Obsidian. The purple tier was nearly called Skull. I picked Obsidian.

The rank isn't your raw win rate. I wanted it to work like Steam's review scores, which need a lot of reviews before they say anything big, and I didn't want someone at one win out of one sitting at the top. So the game asks a more careful question: with this many duels on record, how low could your real win rate plausibly be? (It's the lower bound of a Wilson score interval at about 80% confidence, if you want the name.) A short record gets a cautious number that grows as you play, and each rank past the first also asks for a number of wins.

In practice, winning your first three puts you at Bronze IV. Ten out of ten is Silver II, good but not much proof yet. Win exactly half and you reach Silver I after sixty-odd duels. Obsidian IV asks for 190 wins and roughly a 96% win rate over about 500 duels. Because the higher ranks count wins and not duels played, a loss can only move you down and a win can only move you up. Every rank's numbers are on [the duels page of the wiki](/slots-and-skulls/wiki/duels/#ranks).

Your rank shows on your lobby seat, your opponent's emblem sits next to their name in the duel, and a RANK UP or RANK DOWN card follows the match when it moves. In the full game the main menu scoreboard also has a 1v1 page, ordered by duels won.

No gold, symbols or skulls come home from a match, so your record, your rank and that board are what you take with you.

The demo has 1v1 with the limits above, including upgrades up to +3. The full game comes out on November 4, with every symbol in the draft, Duel Only, four and five reels and matches up to five rounds to win. If you play a few duels in the demo, tell me what rank you landed on and whether it felt fair. [A wishlist](https://store.steampowered.com/app/4428910/Slots__Skulls/) helps a lot.
