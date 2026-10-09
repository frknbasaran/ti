import type { APIContext } from 'astro';
import { devlogFeed } from '../../../lib/rss';

export const GET = (context: APIContext) => devlogFeed(context, 'tr');
