/**
 * Steam user reviews of the Slots & Skulls demo (app 4988090).
 *
 * Source: https://store.steampowered.com/appreviews/4988090?json=1&language=all
 * Quotes are verbatim (original spelling kept); "…" marks a cut. Each one links
 * to the review on Steam so it can be checked. Do not edit the wording, do not
 * add review/rating structured data for these (self-serving reviews), and
 * refresh `summary` when you add or change quotes.
 */
import type { Lang } from '../i18n/ui';

const DEMO_APP_ID = 4988090;

export interface DemoReview {
  id: string;
  steamId: string;
  quote: string;
  /** Minutes played when the review was written. */
  playtimeMin: number;
}

export const reviewUrl = (r: DemoReview) =>
  `https://steamcommunity.com/profiles/${r.steamId}/recommended/${DEMO_APP_ID}/`;

export const demoReviewsUrl = `https://steamcommunity.com/app/${DEMO_APP_ID}/reviews/`;

export const summary = {
  positive: 18,
  total: 18,
  asOf: { en: 'October 2026', tr: 'Ekim 2026' } satisfies Record<Lang, string>,
};

export const demoReviews: DemoReview[] = [
  {
    id: '236291786',
    steamId: '76561198061459642',
    quote:
      "JUST. ONE. MORE. PULL. Slots & Skulls was SUPER FUN! The demo gives you just enough that you'll find yourself ripping that lever one more time hoping you've somehow unlocked another level!",
    playtimeMin: 35,
  },
  {
    id: '232198221',
    steamId: '76561198170119190',
    quote:
      'Honestly really fun with the playthrough I had and was a good mix of strategy with item/perk choices and randomness in combat through the slot machine element.',
    playtimeMin: 122,
  },
  {
    id: '231703753',
    steamId: '76561198059939253',
    quote:
      "plays brilliantly on steam deck, like it's made for controller play. … what's here already is a tonne of fun and I'm really looking forward to seeing how it develops.",
    playtimeMin: 84,
  },
  {
    id: '231879826',
    steamId: '76561198835278243',
    quote:
      'Absolutely loved the demo! It takes some thought when building your reels but its not hard to get the hang of and so much fun!',
    playtimeMin: 181,
  },
  {
    id: '231578693',
    steamId: '76561198764851578',
    quote:
      'You took a simple concept, something I’d normally never go near like gambling, and turned it into an absolute blast.',
    playtimeMin: 93,
  },
  {
    id: '235548604',
    steamId: '76561198097861891',
    quote: 'the game is fun until you watch your favorite symbol burn while trying to upgrade it to +8',
    playtimeMin: 404,
  },
];

/** The short quote shown on the home page. */
export const homeQuote = {
  review: demoReviews[0],
  text: 'JUST. ONE. MORE. PULL. Slots & Skulls was SUPER FUN!',
};
