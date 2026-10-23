import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';
import { game as projectR } from './data/project-r';

/**
 * Devlog posts live in src/content/devlog/en/<slug>.md, Project R's in
 * src/content/devlog/project-r/<slug>.md (left out while it is unlisted, so its
 * images are not built either). The URL slug is the file name.
 */
const devlog = defineCollection({
  loader: glob({
    pattern: projectR.listed ? '**/*.{md,mdx}' : ['**/*.{md,mdx}', '!project-r/**'],
    base: './src/content/devlog',
    generateId: ({ entry }) => entry.replace(/\.mdx?$/, ''),
  }),
  schema: ({ image }) =>
    z.object({
      title: z.string().max(70),
      description: z.string().max(170),
      date: z.coerce.date(),
      game: z.enum(['slots-and-skulls', 'project-r']).optional(),
      heroImage: image().optional(),
      heroImageAlt: z.string().optional(),
      draft: z.boolean().default(false),
    }),
});

export const collections = { devlog };
