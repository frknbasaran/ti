export const ui = {
  games: 'Games',
  game: 'Game',
  studio: 'Studio',
  pressKit: 'Press Kit',
  devlog: 'Devlog',
  wiki: 'Wiki',
  wikiText: 'Symbols, enemies and rules',
  email: 'Email',
  twitter: 'X / Twitter',
  steam: 'Steam',
  platforms: 'Platforms',
  mainNav: 'Main',
  homeLink: 'Trina Interactive home',
  logoAlt: 'Pati, the white pixel-art cat of Trina Interactive',
  wishlist: 'Wishlist on Steam',
  playDemo: 'Play the free demo',
  moreAbout: 'More about Slots & Skulls',
  videoLabel: 'Slots & Skulls gameplay: stopping the slot machine’s wheels to attack a skeleton',
  noPosts: 'No posts yet.',
  rss: 'RSS feed',
  readMore: 'Read',
  backToDevlog: 'All devlog posts',
  published: 'Published',
} as const;

export function formatDate(date: Date): string {
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    timeZone: 'UTC',
  }).format(date);
}
