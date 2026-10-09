/**
 * Slots & Skulls wiki: data access, paths, labels and structured data.
 *
 * Every fact comes from src/data/wiki/*.json, which scripts/wiki/extract.py
 * generates from the game's own data. Do not edit those files by hand.
 */
import symbolsData from '../data/wiki/symbols.json';
import powerupsData from '../data/wiki/powerups.json';
import modifiersData from '../data/wiki/modifiers.json';
import catsData from '../data/wiki/cats.json';
import enemiesData from '../data/wiki/enemies.json';
import levelsData from '../data/wiki/levels.json';
import challengesData from '../data/wiki/challenges.json';
import reinforcementsData from '../data/wiki/reinforcements.json';
import duelsData from '../data/wiki/duels.json';
import rulesData from '../data/wiki/rules.json';
import { SITE_URL } from '../data/site';

export const symbols = symbolsData;
export const powerups = powerupsData;
export const modifiers = modifiersData;
export const cats = catsData;
export const enemies = enemiesData;
export const levels = levelsData;
export const challenges = challengesData;
export const reinforcements = reinforcementsData;
export const duels = duelsData;
export const rules = rulesData;

export type Symbol = (typeof symbols)[number];
export type Powerup = (typeof powerups)[number];
export type Cat = (typeof cats)[number];
export type Enemy = (typeof enemies)[number];
export type Level = (typeof levels)[number];
export type WikiIcon = { src: string; width: number; height: number } | null;

export const GAME = '/slots-and-skulls/';
export const WIKI = '/slots-and-skulls/wiki/';
export const WIKI_NAME = 'Slots & Skulls Wiki';

/** A boss gets its own page; every other enemy is a section of the enemies page. */
export const hasEnemyPage = (e: Enemy) => e.isBoss || e.bossOfLevels.length > 0;

export const paths = {
  hub: WIKI,
  symbols: `${WIKI}symbols/`,
  powerups: `${WIKI}powerups/`,
  cats: `${WIKI}cats/`,
  modifiers: `${WIKI}modifiers/`,
  enemies: `${WIKI}enemies/`,
  levels: `${WIKI}levels/`,
  challenges: `${WIKI}challenges/`,
  endless: `${WIKI}endless/`,
  duels: `${WIKI}duels/`,
  symbol: (slug: string) => `${WIKI}symbols/#${slug}`,
  powerup: (slug: string) => `${WIKI}powerups/${slug}/`,
  cat: (slug: string) => `${WIKI}cats/${slug}/`,
  ability: (slug: string) => `${WIKI}cats/#${slug}`,
  modifier: (slug: string) => `${WIKI}modifiers/#${slug}`,
  enemy: (e: Enemy) => (hasEnemyPage(e) ? `${WIKI}enemies/${e.slug}/` : `${WIKI}enemies/#${e.slug}`),
  level: (index: number) => `${WIKI}levels/#level-${index}`,
};

/** The wiki's sections, in reading order (hub list and the nav under every page). */
export const sections = [
  { key: 'symbols', title: 'Symbols', href: paths.symbols, count: symbols.length },
  { key: 'powerups', title: 'Powerups', href: paths.powerups, count: powerups.length },
  { key: 'cats', title: 'Cats and abilities', href: paths.cats, count: cats.length + modifiers.abilities.length },
  { key: 'modifiers', title: 'Modifiers', href: paths.modifiers, count: modifiers.passives.length },
  { key: 'enemies', title: 'Enemies and bosses', href: paths.enemies, count: enemies.length },
  { key: 'levels', title: 'Levels', href: paths.levels, count: levels.length },
  { key: 'challenges', title: 'Challenges', href: paths.challenges, count: challenges.challenges.length + challenges.symbolTasks.length },
  { key: 'endless', title: 'Endless mode', href: paths.endless, count: reinforcements.length },
  { key: 'duels', title: '1v1 duels', href: paths.duels, count: duels.ranks.length },
] as const;

export type SectionKey = (typeof sections)[number]['key'];

// ---- lookups

export const symbolById = new Map(symbols.map((s) => [s.id, s]));
export const powerupById = new Map(powerups.map((p) => [p.id, p]));
export const enemyById = new Map(enemies.map((e) => [e.id, e]));
export const levelByIndex = new Map(levels.map((l) => [l.index, l]));

// ---- labels (UI words; the facts they label come from the data)

export const rarityName = (r: string) => (rules.rarityNames as Record<string, string>)[r] ?? r;
export const groupName = (g: string) => (rules.groups as Record<string, string>)[g] ?? g;
export const statName = (s: string) => (rules.statNames as Record<string, string>)[s] ?? s;

export const threatName: Record<string, string> = {
  Poison: 'Poison',
  Stun: 'Stun',
  Chill: 'Chill',
  Burn: 'Burn',
  Theft: 'Gold theft',
  SelfHeal: 'Self-heal',
  Armor: 'Armor',
  MultiHit: 'Multi-hit',
  Magic: 'Magic damage',
  Phys: 'Physical damage',
};

export const metricName: Record<string, string> = {
  landings: 'Landings',
  damage: 'Damage',
  kills: 'Kills',
  crits: 'Crits',
  shield: 'Shield',
  heal: 'Healing',
  gold: 'Gold',
  status: 'Status stacks',
};

// ---- number formatting

/** 0.25 -> "25%", 0.025 -> "2.5%". */
export function pct(fraction: number, digits = 1): string {
  const v = Math.round(fraction * 100 * 10 ** digits) / 10 ** digits;
  return `${v}%`;
}

export function signedPct(fraction: number): string {
  return `${fraction >= 0 ? '+' : '-'}${pct(Math.abs(fraction))}`;
}

export function mult(x: number): string {
  return `x${Math.round(x * 100) / 100}`;
}

export const join = (items: string[]) =>
  items.length <= 1 ? items.join('') : `${items.slice(0, -1).join(', ')} and ${items[items.length - 1]}`;

/** A stat modifier as a short phrase: "+25% physical damage", "+50 max shield". */
export function statPhrase(m: { stat: string; op: string; value: number }, times = 1): string {
  const v = m.value * times;
  const flatPercentStats = ['PhysicalResist', 'MagicalResist', 'HPRegenPerTurn', 'GoldGain', 'CritChance', 'PowerupUseCost', 'ShopPrice', 'SkillCheckZone', 'StunResist', 'Thorns', 'GoldTheftResist'];
  const isPercent = m.op === 'PercentAdd' || flatPercentStats.includes(m.stat);
  const sign = v < 0 ? '-' : '+';
  return isPercent ? `${sign}${pct(Math.abs(v))} ${statName(m.stat)}` : `${sign}${Math.abs(v)} ${statName(m.stat)}`;
}

// ---- structured data

export type Crumb = { name: string; href: string };

export const abs = (p: string) => new URL(p, SITE_URL).href;

export function breadcrumbLd(crumbs: Crumb[]) {
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: crumbs.map((c, i) => ({
      '@type': 'ListItem',
      position: i + 1,
      name: c.name,
      item: abs(c.href),
    })),
  };
}

export function itemListLd(name: string, items: { name: string; href: string }[]) {
  return {
    '@context': 'https://schema.org',
    '@type': 'ItemList',
    name,
    numberOfItems: items.length,
    itemListElement: items.map((it, i) => ({
      '@type': 'ListItem',
      position: i + 1,
      name: it.name,
      url: abs(it.href),
    })),
  };
}

export const baseCrumbs: Crumb[] = [
  { name: 'Slots & Skulls', href: GAME },
  { name: 'Wiki', href: WIKI },
];

// ---- small HTML helpers for Meta rows (values rendered with set:html)

export const esc = (s: string | number) =>
  String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

export const a = (href: string, text: string) => `<a href="${esc(href)}">${esc(text)}</a>`;

export const symbolLink = (id: string) => {
  const s = symbolById.get(id);
  return s ? a(paths.symbol(s.slug), s.name) : esc(id);
};

export const powerupLink = (id: string) => {
  const p = powerupById.get(id);
  return p ? a(paths.powerup(p.slug), p.name) : esc(id);
};

export const enemyLink = (id: string) => {
  const e = enemyById.get(id);
  return e ? a(paths.enemy(e), e.name) : esc(id);
};

export const levelLink = (index: number) => {
  const l = levelByIndex.get(index);
  return l ? a(paths.level(index), `Level ${index}: ${l.name}`) : `Level ${index}`;
};
