import grayboxImage from '../assets/project-r/haydarpasa_blockout.png';

/**
 * Project R facts. Unannounced: the name, this line and the graybox image are
 * all the site says about it.
 */
export const game = {
  slug: 'project-r',
  name: 'Project R',
} as const;

export const gameCopy = {
  tagline: 'The second game from Trina Interactive, in development.',
  /** Same platforms as Slots & Skulls; no store link until the Steam page is public. */
  platforms: 'Steam (Windows, macOS, Linux)',
  releaseLabel: 'Q1 2027',
  image: grayboxImage,
  imageAlt: 'A graybox model from Project R: plain grey blocks of a large stone building with two towers.',
} as const;
