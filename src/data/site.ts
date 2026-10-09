/**
 * Studio-level facts. Keep this to verifiable facts only.
 */
export const SITE_URL = 'https://trinainteractive.com';

export const studio = {
  name: 'Trina Interactive',
  url: `${SITE_URL}/`,
  email: 'hi@trinainteractive.com',
  logo: `${SITE_URL}/logo.png`,
  steamDeveloper: 'https://store.steampowered.com/developer/trinainteractive',
  x: 'https://x.com/slotsandskulls',
  xHandle: '@slotsandskulls',
  pressKitDrive:
    'https://drive.google.com/drive/folders/1GrIPkeUNpGxxJZ_NxcIazyq4cZ637Iu0?usp=sharing',
} as const;

export const ORG_ID = `${SITE_URL}/#organization`;

/** Default social share image (1200x630, generated from the key art). */
export const DEFAULT_OG_IMAGE = {
  url: '/og/slots-and-skulls.png',
  width: 1200,
  height: 630,
  alt: 'Slots & Skulls key art: a golden slot machine, a cat pulling its lever and a skeleton mage, on black.',
};
