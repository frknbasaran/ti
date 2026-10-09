import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

/**
 * Devlog posts live in src/content/devlog/<lang>/<slug>.md.
 * The URL slug is the file name; the folder is only for organisation.
 * Posts in different languages that are translations of each other share
 * the same `translationKey` (used for hreflang alternates).
 */
const devlog = defineCollection({
  loader: glob({
    pattern: '**/*.{md,mdx}',
    base: './src/content/devlog',
    generateId: ({ entry }) => entry.replace(/\.mdx?$/, ''),
  }),
  schema: ({ image }) =>
    z.object({
      title: z.string().max(70),
      description: z.string().max(170),
      date: z.coerce.date(),
      lang: z.enum(['en', 'tr']),
      translationKey: z.string(),
      game: z.enum(['slots-and-skulls']).optional(),
      heroImage: image().optional(),
      heroImageAlt: z.string().optional(),
      draft: z.boolean().default(false),
    }),
});

export const collections = { devlog };
