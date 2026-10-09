import { ORG_ID, SITE_URL, studio } from '../data/site';
import { game, gameCopy } from '../data/slots-and-skulls';

const abs = (p: string) => new URL(p, SITE_URL).href;

export function organizationLd() {
  return {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    '@id': ORG_ID,
    name: studio.name,
    url: studio.url,
    logo: {
      '@type': 'ImageObject',
      url: studio.logo,
      width: 512,
      height: 512,
    },
    email: studio.email,
    contactPoint: {
      '@type': 'ContactPoint',
      contactType: 'customer support',
      email: studio.email,
    },
    sameAs: [studio.steamDeveloper, studio.x],
  };
}

export function websiteLd() {
  return {
    '@context': 'https://schema.org',
    '@type': 'WebSite',
    '@id': `${SITE_URL}/#website`,
    name: studio.name,
    url: studio.url,
    inLanguage: 'en',
    publisher: { '@id': ORG_ID },
  };
}

/** Organization reference that still makes sense on its own page. */
const orgRef = { '@type': 'Organization', '@id': ORG_ID, name: studio.name, url: studio.url };

export function videoGameLd(pagePath: string, images: string[]) {
  return {
    '@context': 'https://schema.org',
    '@type': 'VideoGame',
    '@id': `${SITE_URL}/${game.slug}/#game`,
    name: game.name,
    description: gameCopy.short,
    url: abs(pagePath),
    image: images.map(abs),
    genre: [...game.genres],
    gamePlatform: ['PC'],
    operatingSystem: game.operatingSystems.join(', '),
    applicationCategory: 'Game',
    playMode: ['SinglePlayer', 'MultiPlayer'],
    inLanguage: [...game.languageCodes],
    author: orgRef,
    publisher: orgRef,
    installUrl: game.steamUrl,
    sameAs: [game.steamUrl, studio.x],
  };
}
