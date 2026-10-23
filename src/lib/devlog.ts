import { getCollection, type CollectionEntry } from 'astro:content';
import { game as projectR } from '../data/project-r';

export type DevlogPost = CollectionEntry<'devlog'>;

/**
 * Published posts only. Drafts are excluded everywhere (pages, nav, RSS,
 * sitemap) in production builds; `astro dev` shows them for previewing.
 * Posts of an unlisted game are excluded the same way.
 */
export async function getPublishedPosts(): Promise<DevlogPost[]> {
  const unlisted = (game: string | undefined) => game === projectR.slug && !projectR.listed;
  const posts = await getCollection(
    'devlog',
    ({ data }) => import.meta.env.DEV || (!data.draft && !unlisted(data.game)),
  );
  return posts.sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());
}

/** URL slug = file name without the folder. */
export function postSlug(post: DevlogPost): string {
  return post.id.split('/').pop() ?? post.id;
}

export function postPath(post: DevlogPost): string {
  return `/devlog/${postSlug(post)}/`;
}
