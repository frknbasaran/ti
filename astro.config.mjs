// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import { readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const SITE = 'https://trinainteractive.com';

/**
 * Count published (non-draft) devlog posts per language by reading the
 * frontmatter directly. Used to keep empty devlog index pages out of the
 * sitemap until the first post is published.
 * @returns {Record<string, number>}
 */
function publishedDevlogCounts() {
  /** @type {Record<string, number>} */
  const counts = { en: 0, tr: 0 };
  const root = new URL('./src/content/devlog/', import.meta.url).pathname;
  /** @param {string} dir */
  const walk = (dir) => {
    for (const entry of readdirSync(dir, { withFileTypes: true })) {
      const full = join(dir, entry.name);
      if (entry.isDirectory()) walk(full);
      else if (/\.mdx?$/.test(entry.name)) {
        const fm = readFileSync(full, 'utf8').match(/^---\r?\n([\s\S]*?)\r?\n---/)?.[1] ?? '';
        if (/^draft:\s*true\s*$/m.test(fm)) continue;
        const lang = fm.match(/^lang:\s*['"]?(\w+)/m)?.[1] ?? 'en';
        counts[lang] = (counts[lang] ?? 0) + 1;
      }
    }
  };
  try {
    walk(root);
  } catch {
    /* no devlog folder */
  }
  return counts;
}

const devlogCounts = publishedDevlogCounts();

export default defineConfig({
  site: SITE,
  trailingSlash: 'always',
  build: {
    format: 'directory',
  },
  integrations: [
    sitemap({
      i18n: {
        defaultLocale: 'en',
        locales: { en: 'en', tr: 'tr' },
      },
      filter: (page) => {
        const path = new URL(page).pathname;
        if (path.startsWith('/404')) return false;
        if (path === '/devlog/' && devlogCounts.en === 0) return false;
        if (path === '/tr/devlog/' && devlogCounts.tr === 0) return false;
        return true;
      },
    }),
  ],
});
