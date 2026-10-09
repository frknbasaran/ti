import { pct, type Enemy } from '../../../../lib/wiki';

/** One attack in the enemy's cycle as a sentence. */
export function attackText(at: Enemy['attacks'][number]): string {
  const parts: string[] = [];
  const dmg: string[] = [];
  if (at.physical) dmg.push(`${at.physical} physical`);
  if (at.magical) dmg.push(`${at.magical} magical`);
  parts.push(`${dmg.join(' + ')} damage${at.hits > 1 ? `, ${at.hits} times` : ''}`);
  if (at.stunChance) parts.push(`${pct(at.stunChance)} stun chance`);
  if (at.burnChance) parts.push(`${pct(at.burnChance)} chance to burn (${at.burnStacks})`);
  if (at.chillChance) parts.push(`${pct(at.chillChance)} chance to chill (${at.chillTurns} ${at.chillTurns === 1 ? 'turn' : 'turns'})`);
  if (at.poisonChance) parts.push(`${pct(at.poisonChance)} chance to poison (${at.poisonStacks})`);
  if (at.stealChance) parts.push(`${pct(at.stealChance)} chance to steal gold`);
  if (at.selfHealAmount) parts.push(`heals itself for ${at.selfHealAmount}${at.selfHealChance ? ` (${pct(at.selfHealChance)} chance)` : ''}`);
  if (at.rearmor) parts.push(`regains ${at.rearmor} armor first`);
  return parts.join(', ') + '.';
}

export const dropName: Record<string, string> = {
  weapon: 'Symbol',
  gemgreen: 'Green Gem',
  gemblue: 'Blue Gem',
  gemyellow: 'Yellow Gem',
  gold: 'Gold',
  shard: 'Skulls',
};

export const triggerName: Record<string, string> = {
  Enter: 'When the fight starts',
  FirstDamageDealt: 'After its first hit',
  FirstDamageTaken: 'When first hit',
  BeforeDeath: 'On death',
  KilledPlayer: 'When it kills you',
};
