import { game as slotsAndSkulls } from './slots-and-skulls';
import { game as projectR } from './project-r';

/** Every game a devlog post can belong to (the `game` field), keyed by slug. */
export const games = {
  [slotsAndSkulls.slug]: { name: slotsAndSkulls.name, path: `/${slotsAndSkulls.slug}/` },
  [projectR.slug]: { name: projectR.name, path: `/${projectR.slug}/` },
} as const;

export type GameSlug = keyof typeof games;
