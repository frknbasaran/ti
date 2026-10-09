/**
 * Slots & Skulls facts.
 *
 * Sources (do not add anything that is not in one of these):
 * - Steam store page / appdetails API for app 4428910 (English)
 * - PRESS_KIT/Information.txt
 *
 * When the game launches, update `release` (status + wording) here.
 */
export const game = {
  slug: 'slots-and-skulls',
  wikiPath: '/slots-and-skulls/wiki/',
  name: 'Slots & Skulls',
  steamUrl: 'https://store.steampowered.com/app/4428910/Slots__Skulls/',
  steamAppId: 4428910,
  demoUrl: 'https://store.steampowered.com/app/4988090/Slots__Skulls_Demo/',
  developer: 'Trina Interactive',
  publisher: 'Trina Interactive',
  /** From Steam: "Coming soon", 4 Nov, 2026. */
  release: {
    comingSoon: true,
    isoDate: '2026-11-04',
  },
  operatingSystems: ['Windows', 'macOS', 'Linux'],
  /** Genre as listed in the press kit (Information.txt). */
  genres: ['Roguelite', 'Turn-Based Strategy'],
  /** Steam genres. */
  steamGenres: ['Indie', 'RPG', 'Strategy'],
  /** Top user-defined tags on the Steam store page. */
  steamTags: [
    'Roguelite',
    'Auto Battler',
    'Turn-Based Combat',
    'Roguelike',
    'Strategy',
    'Gambling',
    'Roguelike Deckbuilder',
    'Pixel Graphics',
    'Deckbuilding',
    'Turn-Based',
    'Procedural Generation',
    'Turn-Based Strategy',
    'Inventory Management',
    'Loot',
    'Perma Death',
    'RPG',
    'Replay Value',
    '2D',
    'Singleplayer',
    'PvP',
  ],
  /** Steam supported languages (interface). */
  languages: [
    'English',
    'Turkish',
    'French',
    'Italian',
    'German',
    'Spanish - Spain',
    'Dutch',
    'Japanese',
    'Korean',
    'Norwegian',
    'Polish',
    'Portuguese - Brazil',
    'Russian',
    'Simplified Chinese',
    'Spanish - Latin America',
    'Traditional Chinese',
    'Ukrainian',
    'Bulgarian',
    'Czech',
    'Danish',
    'Finnish',
    'Greek',
    'Hungarian',
    'Indonesian',
    'Portuguese - Portugal',
    'Romanian',
    'Swedish',
  ],
  /** BCP 47 codes for the languages above (for JSON-LD). */
  languageCodes: [
    'en', 'tr', 'fr', 'it', 'de', 'es-ES', 'nl', 'ja', 'ko', 'no', 'pl', 'pt-BR', 'ru',
    'zh-Hans', 'es-419', 'zh-Hant', 'uk', 'bg', 'cs', 'da', 'fi', 'el', 'hu', 'id', 'pt-PT',
    'ro', 'sv',
  ],
} as const;

type Section = { heading: string; paragraphs: string[] };
type Requirement = { label: string; value: string };

type GameCopy = {
  /** Steam short description (official). */
  short: string;
  /** Press kit one-liner (Information.txt / previous site). */
  tagline: string;
  metaDescription: string;
  releaseLabel: string;
  sections: Section[];
  facts: {
    modes: string;
    controller: string;
    steamFeatures: string;
    languages: string;
    languageList: string;
  };
  requirements: { os: string; rows: Requirement[] }[];
  faq: { q: string; a: string }[];
};

export const gameCopy: GameCopy = {
  short:
    'A turn-based roguelite built on a slot machine. Stop the machine to attack, win fights for chests, and upgrade what drops at the forge (if you dare). Or invite a friend and fight them.',
  tagline:
    'A turn-based roguelite built on a slot machine. Spin to attack, open chests for new symbols, strike deals with cats, and risk your symbols at the anvil.',
  metaDescription:
    'Slots & Skulls is a turn-based roguelite built on a slot machine. 112 symbols, a merciless forge, cat pacts and 1v1 duels. Windows, macOS and Linux on Steam.',
  releaseLabel: 'November 4, 2026 (coming soon on Steam)',
  sections: [
    {
      heading: 'Your weapon is a slot machine',
      paragraphs: [
        'Slots & Skulls is a turn-based roguelite. Your weapon is a slot machine, and you build the pool of symbols it can land on: blades, spells, poisons, thorns, gold engines. Stop the machine’s wheels one at a time. Whatever luck hands you decides the fate of that turn.',
      ],
    },
    {
      heading: 'In control, but not quite',
      paragraphs: [
        '112 different symbols: common ones that drop easily from kills, and legendary ones that only bosses drop. Every symbol has its own effect. Some boost the symbol next to them, some spend your health, some damage the enemy, some pay you gold. A few call for quick-fingered skill checks.',
        'After every fight the shop opens. Buy new symbols and power-ups, reroll the stock, lock a symbol you cannot afford yet, or remove a symbol you have outgrown to streamline your build. A chart in the shop shows exactly what a purchase does to your attack, defense, gold, pool size and kill speed.',
        'Four active power-ups sit on the d-pad, ready whenever you want them. Up to eight passive power-ups make you readier for the hard fights.',
      ],
    },
    {
      heading: 'More risk, more reward on every level',
      paragraphs: [
        'Ten levels, five fights each, 33 different enemies drawn pixel by pixel. Physical attacks do nothing to armored enemies, but magic goes straight through. Archers can stun you, ice mages can freeze one of your wheels, burn damage keeps eating your health in real time, and thieves lift gold from your purse mid fight.',
        'Replay a level you already beat on raised difficulty modes for more symbols, skulls or gems. The higher the difficulty, the more you earn, and the tougher the enemies.',
      ],
    },
    {
      heading: 'The forge does not joke',
      paragraphs: [
        'At the forge you can raise a symbol from +0 to +10. The higher its level, the lower the chance of reaching the next one, and if the upgrade fails you lose the symbol completely. Gems help: a green gem slightly improves the upgrade chance, a blue gem turns a destroyed symbol into a one-level drop, and the extremely rare yellow gem guarantees the upgrade.',
        'Every fight you win pays skulls, and you keep them even when you die. Spend them at the forge, on modifiers, on adopting a cat, or on abilities.',
      ],
    },
    {
      heading: 'Cats, abilities and modifiers',
      paragraphs: [
        'Before a run you can bring a cat. Every cat comes with a pact that lasts the whole run: one advantage and one disadvantage. Six different abilities, each usable once per fight, change the game from top to bottom. 21 modifiers, activated with skulls, add things like more health, more damage, a last move when you die, or two more wheels on the slot machine.',
      ],
    },
    {
      heading: 'Play with your friends',
      paragraphs: [
        'Invite a friend from your Steam list and play 1v1. A match opens with a draft, then you both beat the same enemies on your own screens, buying symbols from the shop after every fight. After four fights you duel each other. After the duels the anvil opens. First to the set number of rounds wins. Prefer to skip the enemies? Pick Duel Only mode.',
      ],
    },
    {
      heading: 'Auto mode for idle lovers',
      paragraphs: [
        'Turn on Auto Mode and the reels stop themselves; you only step in when a symbol calls for a skill check. Auto 2X Mode makes everything twice as fast. In Endless Mode you can enable Full Auto Mode and test your build without any interaction.',
      ],
    },
  ],
  facts: {
    modes: 'Single-player, online 1v1 PvP',
    controller: 'Full controller support',
    steamFeatures: 'Steam Achievements, Steam Cloud, Steam Leaderboards',
    languageList:
      'English, Turkish, French, Italian, German, Spanish - Spain, Dutch, Japanese, Korean, Norwegian, Polish, Portuguese - Brazil, Russian, Simplified Chinese, Spanish - Latin America, Traditional Chinese, Ukrainian, Bulgarian, Czech, Danish, Finnish, Greek, Hungarian, Indonesian, Portuguese - Portugal, Romanian, Swedish',
    languages: '27 supported languages, including English and Turkish',
  },
  requirements: [
    {
      os: 'Windows (minimum)',
      rows: [
        { label: 'OS', value: 'Windows 10 64-bit' },
        { label: 'Processor', value: '2.0 GHz Dual Core' },
        { label: 'Memory', value: '4 GB RAM' },
        { label: 'Graphics', value: 'DirectX 11 compatible GPU with 1GB VRAM' },
        { label: 'DirectX', value: 'Version 11' },
        { label: 'Storage', value: '1 GB available space' },
      ],
    },
    {
      os: 'macOS (minimum)',
      rows: [
        { label: 'OS', value: 'macOS 10.15 Catalina or newer' },
        { label: 'Processor', value: '2.0 GHz Dual Core (or Apple Silicon)' },
        { label: 'Memory', value: '4 GB RAM' },
        { label: 'Graphics', value: 'Metal compatible GPU' },
        { label: 'Storage', value: '1 GB available space' },
      ],
    },
    {
      os: 'Linux (minimum)',
      rows: [
        { label: 'Processor', value: '2.0 GHz Dual Core' },
        { label: 'Memory', value: '1 GB RAM' },
        { label: 'Graphics', value: 'DirectX 11 compatible GPU with 1GB VRAM' },
        { label: 'Storage', value: '1 GB available space' },
      ],
    },
  ],
  faq: [
    {
      q: 'What is Slots & Skulls?',
      a: 'A turn-based roguelite built on a slot machine. You build the pool of symbols your slot machine can land on, stop its wheels to attack, win chests after fights and upgrade symbols at the forge, where a failed upgrade destroys the symbol.',
    },
    {
      q: 'When does Slots & Skulls come out?',
      a: 'Steam lists the release date as November 4, 2026.',
    },
    {
      q: 'Which platforms is it on?',
      a: 'Windows, macOS and Linux, on Steam.',
    },
    {
      q: 'Is there a demo?',
      a: 'Yes. A free demo is available on Steam.',
    },
    {
      q: 'Does it have multiplayer?',
      a: 'Yes. You can invite a friend from your Steam list and play online 1v1, either with enemies between duels or in Duel Only mode.',
    },
    {
      q: 'Can I play with a controller?',
      a: 'Yes. Steam lists full controller support, including DualShock and DualSense controllers.',
    },
    {
      q: 'Who makes Slots & Skulls?',
      a: 'Trina Interactive, which is both the developer and the publisher.',
    },
  ],
};
