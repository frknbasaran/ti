export const LANGS = ['en', 'tr'] as const;
export type Lang = (typeof LANGS)[number];
export const DEFAULT_LANG: Lang = 'en';

export const htmlLang: Record<Lang, string> = { en: 'en', tr: 'tr' };
export const ogLocale: Record<Lang, string> = { en: 'en_US', tr: 'tr_TR' };

/** Prefix a root-relative path with the language folder (`/tr/...`). */
export function localizePath(path: string, lang: Lang): string {
  const clean = path.startsWith('/') ? path : `/${path}`;
  return lang === DEFAULT_LANG ? clean : `/${lang}${clean}`;
}

export const ui = {
  en: {
    games: 'Games',
    game: 'Game',
    studio: 'Studio',
    pressKit: 'Press Kit',
    devlog: 'Devlog',
    email: 'Email',
    twitter: 'X / Twitter',
    steam: 'Steam',
    platforms: 'Platforms',
    language: 'Türkçe',
    languageLabel: 'Bu sayfanın Türkçesi',
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
  },
  tr: {
    games: 'Oyunlar',
    game: 'Oyun',
    studio: 'Stüdyo',
    pressKit: 'Basın Kiti',
    devlog: 'Günlük',
    email: 'E-posta',
    twitter: 'X / Twitter',
    steam: 'Steam',
    platforms: 'Platformlar',
    language: 'English',
    languageLabel: 'English version of this page',
    mainNav: 'Ana menü',
    homeLink: 'Trina Interactive ana sayfa',
    logoAlt: 'Trina Interactive’in beyaz piksel kedisi Pati',
    wishlist: 'Steam’de istek listene ekle',
    playDemo: 'Ücretsiz demoyu oyna',
    moreAbout: 'Slots & Skulls hakkında',
    videoLabel: 'Slots & Skulls oynanışı: bir iskelete saldırmak için slot makinesinin çarklarını durdurmak',
    noPosts: 'Henüz yazı yok.',
    rss: 'RSS akışı',
    readMore: 'Oku',
    backToDevlog: 'Tüm yazılar',
    published: 'Yayın tarihi',
  },
} as const satisfies Record<Lang, Record<string, string>>;

export function t(lang: Lang) {
  return ui[lang];
}

export function formatDate(date: Date, lang: Lang): string {
  return new Intl.DateTimeFormat(lang === 'tr' ? 'tr-TR' : 'en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    timeZone: 'UTC',
  }).format(date);
}
