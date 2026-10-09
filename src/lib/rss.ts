import rss from '@astrojs/rss';
import type { APIContext } from 'astro';
import { studio } from '../data/site';
import { localizePath, type Lang } from '../i18n/ui';
import { getPublishedPosts, postPath } from './devlog';

const meta = {
  en: { title: 'Trina Interactive Devlog', description: 'Development notes from Trina Interactive.' },
  tr: { title: 'Trina Interactive Günlüğü', description: 'Trina Interactive’ten geliştirme notları.' },
} as const;

export async function devlogFeed(context: APIContext, lang: Lang) {
  const posts = await getPublishedPosts(lang);
  return rss({
    title: meta[lang].title,
    description: meta[lang].description,
    site: new URL(localizePath('/devlog/', lang), context.site).href,
    trailingSlash: true,
    items: posts.map((post) => ({
      title: post.data.title,
      description: post.data.description,
      pubDate: post.data.date,
      link: postPath(post),
    })),
    customData: `<language>${lang}</language><managingEditor>${studio.email} (${studio.name})</managingEditor>`,
  });
}
