/**
 * Project R facts. Unannounced: the name, this line and the graybox image are
 * all the site says about it.
 *
 * `listed: false` takes Project R off the site: no /project-r/ page, no home or
 * footer entry, and its devlog posts are left out of every page, the RSS and
 * the sitemap, and its posts (src/content/devlog/project-r/) and images are not
 * built at all. To bring it back, set it to true, rename
 * src/pages/project-r/_index.astro to index.astro (an underscore page is not
 * built, so its graybox image does not ship) and move the cover video
 * (src/assets/project-r/cover/) back to public/media/.
 *
 * No image import here: everything imports this file, and an imported image
 * ships with the site even when nothing shows it.
 */
export const game = {
  slug: 'project-r',
  name: 'Project R',
  listed: false,
} as const;

export const gameCopy = {
  tagline: 'The second game from Trina Interactive, in development.',
  /** Same platforms as Slots & Skulls; no store link until the Steam page is public. */
  platforms: 'Steam (Windows, macOS, Linux)',
  releaseLabel: 'Q1 2027',
  imageAlt: 'A graybox model from Project R: plain grey blocks of a large stone building with two towers.',
  coverAlt: 'A large stone building with two towers, shown as a plain graybox, then a detailed graybox, then textured.',
} as const;
