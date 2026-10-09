import { getCollection, type CollectionEntry } from 'astro:content';
import { localizePath, type Lang } from '../i18n/ui';

export type DevlogPost = CollectionEntry<'devlog'>;

/**
 * Published posts only. Drafts are excluded everywhere (pages, nav, RSS,
 * sitemap) in production builds; `astro dev` shows them for previewing.
 */
export async function getPublishedPosts(lang?: Lang): Promise<DevlogPost[]> {
  const posts = await getCollection(
    'devlog',
    ({ data }) => (import.meta.env.DEV || !data.draft) && (!lang || data.lang === lang),
  );
  return posts.sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());
}

/** URL slug = file name without the language folder. */
export function postSlug(post: DevlogPost): string {
  return post.id.split('/').pop() ?? post.id;
}

export function postPath(post: DevlogPost): string {
  return localizePath(`/devlog/${postSlug(post)}/`, post.data.lang);
}

/** Paths of the same post in other languages, keyed by language. */
export async function postAlternates(post: DevlogPost): Promise<Partial<Record<Lang, string>>> {
  const all = await getPublishedPosts();
  const out: Partial<Record<Lang, string>> = {};
  for (const p of all) {
    if (p.data.translationKey === post.data.translationKey) out[p.data.lang] = postPath(p);
  }
  return out;
}
