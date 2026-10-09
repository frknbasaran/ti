import { pct, rules, statPhrase, type Cat } from '../../../../lib/wiki';

/** The pact's terms as plain sentences, built from the pact's data. */
export function pactTerms(cat: Cat): string[] {
  const p = cat.pact;
  const out: string[] = [];
  for (const s of p.stats) out.push(`${statPhrase(s)} for the whole run.`);
  const params = p.params as Record<string, number>;
  if (p.rule === 'BloodPact') {
    out.push(`Every spin costs ${params.hpPerSpin} HP.`);
    out.push(`Every symbol acts as if it were ${params.forgeBonus} forge levels higher, up to +${rules.anvil.maxPlus}.`);
  }
  if (p.rule === 'Usury') {
    out.push(`After every won fight your gold grows by ${pct(params.interestRate)}.`);
    out.push(
      `Every enemy gets a ${pct(params.stealChance)} chance per attack to steal ${pct(params.stealPercent)} of your gold (at least ${params.stealMinimum}). Theft resist, such as the Golden Padlock, blocks it.`,
    );
  }
  if (p.rule === 'NoHeal') out.push('You are not healed to full between fights.');
  if (p.rule === 'VowOfPoverty') out.push('The shop never opens.');
  if (p.skullMultiplier !== 1) {
    out.push(
      `Skull rewards are multiplied by ${p.skullMultiplier}. Together with heat the skull multiplier is capped at x${rules.economy.pactRewardCap}.`,
    );
  }
  return out;
}
