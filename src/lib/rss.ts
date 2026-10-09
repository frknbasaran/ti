import rss from '@astrojs/rss';
import type { APIContext } from 'astro';
import { studio } from '../data/site';
import { getPublishedPosts, postPath } from './devlog';

export async function devlogFeed(context: APIContext) {
  const posts = await getPublishedPosts();
  return rss({
    title: 'Trina Interactive Devlog',
    description: 'Development notes from Trina Interactive.',
    site: new URL('/devlog/', context.site).href,
    trailingSlash: true,
    items: posts.map((post) => ({
      title: post.data.title,
      description: post.data.description,
      pubDate: post.data.date,
      link: postPath(post),
    })),
    customData: `<language>en</language><managingEditor>${studio.email} (${studio.name})</managingEditor>`,
  });
}
