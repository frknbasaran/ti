import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

/**
 * Devlog posts live in src/content/devlog/en/<slug>.md.
 * The URL slug is the file name; the folder is only for organisation.
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
      game: z.enum(['slots-and-skulls']).optional(),
      heroImage: image().optional(),
      heroImageAlt: z.string().optional(),
      draft: z.boolean().default(false),
    }),
});

export const collections = { devlog };
