import { getCollection, type CollectionEntry } from 'astro:content';

export type DevlogPost = CollectionEntry<'devlog'>;

/**
 * Published posts only. Drafts are excluded everywhere (pages, nav, RSS,
 * sitemap) in production builds; `astro dev` shows them for previewing.
 */
export async function getPublishedPosts(): Promise<DevlogPost[]> {
  const posts = await getCollection('devlog', ({ data }) => import.meta.env.DEV || !data.draft);
  return posts.sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());
}

/** URL slug = file name without the folder. */
export function postSlug(post: DevlogPost): string {
  return post.id.split('/').pop() ?? post.id;
}

export function postPath(post: DevlogPost): string {
  return `/devlog/${postSlug(post)}/`;
}
