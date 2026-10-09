// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import { readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const SITE = 'https://trinainteractive.com';

/**
 * Count published (non-draft) devlog posts by reading the frontmatter
 * directly. Used to keep the empty devlog index page out of the sitemap
 * until the first post is published.
 * @returns {number}
 */
function publishedDevlogCount() {
  let count = 0;
  const root = new URL('./src/content/devlog/', import.meta.url).pathname;
  /** @param {string} dir */
  const walk = (dir) => {
    for (const entry of readdirSync(dir, { withFileTypes: true })) {
      const full = join(dir, entry.name);
      if (entry.isDirectory()) walk(full);
      else if (/\.mdx?$/.test(entry.name)) {
        const fm = readFileSync(full, 'utf8').match(/^---\r?\n([\s\S]*?)\r?\n---/)?.[1] ?? '';
        if (!/^draft:\s*true\s*$/m.test(fm)) count++;
      }
    }
  };
  try {
    walk(root);
  } catch {
    /* no devlog folder */
  }
  return count;
}

const devlogCount = publishedDevlogCount();

export default defineConfig({
  site: SITE,
  trailingSlash: 'always',
  build: {
    format: 'directory',
  },
  integrations: [
    sitemap({
      filter: (page) => {
        const path = new URL(page).pathname;
        if (path.startsWith('/404')) return false;
        if (path === '/devlog/' && devlogCount === 0) return false;
        return true;
      },
    }),
  ],
});
