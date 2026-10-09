#!/usr/bin/env python3
"""Slots & Skulls wiki extractor.

Reads the Unity project's content data (ScriptableObject .asset files, their .meta
files, localization.csv and a few constants in the C# that consumes them) and
writes one JSON file per wiki category to src/data/wiki/, plus icons to
public/wiki/icons/. Nothing in the output is typed by hand: every number and every
sentence comes from the game. Run it again whenever the game data changes.

Usage:
    python3 -I scripts/wiki/extract.py /path/to/SLOTS_AND_ANVIL [--site /path/to/site]

See scripts/wiki/README.md.
"""
import argparse
import csv
import decimal
import hashlib
import importlib.util
import json
import math
import os
import re
import shutil
import struct
import sys

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit('PyYAML is required: python3 -m pip install pyyaml')

sys.dont_write_bytecode = True  # keep scripts/wiki free of __pycache__
HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location('wiki_aseprite', os.path.join(HERE, 'aseprite.py'))
aseprite = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(aseprite)

# Where icons may come from. Assets/Aseprite is the studio's own art. Assets/Icons
# and Assets/_Project/Art hold the licensed pack art the game shows (RPG Icons Pixel
# Art, Rank Emblems 48x48); the studio chose on 2026-10-09 to show it on the wiki too.
# Each icon is published as the single image the game uses, never as a pack.
# Textures anywhere else are not exported; the page shows a neutral placeholder.
ICON_DIRS = ('Assets/Aseprite/', 'Assets/Icons/', 'Assets/_Project/Art/')

# In-game strings the studio no longer wants repeated outside the game. "No hidden
# RNG" was retired on 2026-07-16 (docs/devlog/plan.md): the reel stop follows the
# press, but crits, the anvil and kill boxes are real rolls.
RETIRED_PHRASES = (re.compile(r'hidden\s+RNG', re.I),)

# --------------------------------------------------------------------------- utils


class DataError(Exception):
    pass


def slugify(value):
    return re.sub(r'[^a-z0-9]+', '-', value.lower()).strip('-')


def export_png(path, out_png):
    """Re-save a PNG sprite at its own size, without the source file's metadata."""
    with aseprite.Image.open(path) as src:
        image = src.convert('RGBA')
    image.info.pop('icc_profile', None)
    image.save(out_png, optimize=True)
    return image.size


def f32(x):
    """Round a Python float to IEEE single precision (C# float arithmetic)."""
    return struct.unpack('<f', struct.pack('<f', float(x)))[0]


def num(value, default=0.0):
    if value is None or value == '':
        return default
    return float(value)


def inum(value, default=0):
    if value is None or value == '':
        return default
    return int(float(value))


def flag(value):
    return str(value).strip() not in ('', '0', 'false', 'False')


def int_array(value):
    """Unity serializes int[] as a little-endian hex blob, float[] as a YAML list."""
    if value in (None, '', '[]'):
        return []
    if isinstance(value, list):
        return [inum(v) for v in value]
    blob = bytes.fromhex(str(value))
    return list(struct.unpack('<%di' % (len(blob) // 4), blob))


def float_array(value):
    if value in (None, '', '[]'):
        return []
    return [num(v) for v in value]


def round_half_even(x):
    return int(round(x))


def round_away(x):
    return int(math.floor(abs(x) + 0.5)) * (1 if x >= 0 else -1)


def shortest_f32(x):
    """Shortest decimal string that round-trips to the same float32."""
    for digits in range(1, 10):
        s = '%.*g' % (digits, x)
        if f32(float(s)) == f32(x):
            return s
    return repr(x)


def fmt(x, decimals):
    """C# ToString("0.#") / ("0.##") of a float."""
    d = decimal.Decimal(shortest_f32(x)).quantize(decimal.Decimal(1).scaleb(-decimals),
                                                  rounding=decimal.ROUND_HALF_UP)
    s = format(d, 'f')
    if '.' in s:
        s = s.rstrip('0').rstrip('.')
    return '0' if s in ('-0', '') else s


def pct(fraction, decimals=0):
    """A fraction as a percent number for prose (0.25 -> "25")."""
    return fmt(fraction * 100, decimals if decimals else 2)


# --------------------------------------------------------------------------- unity io


class Project:
    def __init__(self, root):
        self.root = os.path.abspath(root)
        self.assets = os.path.join(self.root, 'Assets')
        self.data = os.path.join(self.assets, '_Project', 'Data')
        self.scripts = os.path.join(self.assets, '_Project', 'Scripts')
        if not os.path.isdir(self.data):
            raise DataError(f'{self.data} not found: pass the Unity project root')
        self._guids = None
        self._cs = {}

    # -- assets
    def load(self, path):
        with open(path, encoding='utf-8') as fh:
            text = fh.read()
        body = '\n'.join(l for l in text.split('\n') if not l.startswith('%') and not l.startswith('--- '))
        doc = yaml.load(body, Loader=yaml.BaseLoader)
        mono = doc.get('MonoBehaviour') if isinstance(doc, dict) else None
        if mono is None:
            raise DataError(f'{path}: not a MonoBehaviour asset')
        refs = {}
        for ref in ((mono.get('references') or {}).get('RefIds') or []):
            refs[ref['rid']] = (ref['type']['class'], ref.get('data') or {})
        mono['_refs'] = refs
        mono['_path'] = path
        mono['_guid'] = self.guid_of(path)
        return mono

    def effects(self, mono, key):
        out = []
        for entry in mono.get(key) or []:
            rid = entry.get('rid') if isinstance(entry, dict) else None
            if rid in (None, '-2'):
                continue
            if rid not in mono['_refs']:
                raise DataError(f"{mono['_path']}: missing SerializeReference {rid}")
            out.append(mono['_refs'][rid])
        return out

    def folder(self, name):
        folder = os.path.join(self.data, name)
        return [self.load(os.path.join(folder, f)) for f in sorted(os.listdir(folder)) if f.endswith('.asset')]

    # -- guids
    def guid_of(self, path):
        with open(path + '.meta', encoding='utf-8', errors='ignore') as fh:
            for line in fh:
                if line.startswith('guid:'):
                    return line.split()[1]
        raise DataError(f'{path}.meta has no guid')

    def guid_path(self, guid):
        if self._guids is None:
            self._guids = {}
            for dirpath, _dirs, files in os.walk(self.assets):
                for f in files:
                    if f.endswith('.meta'):
                        p = os.path.join(dirpath, f)
                        with open(p, encoding='utf-8', errors='ignore') as fh:
                            for line in fh:
                                if line.startswith('guid:'):
                                    self._guids[line.split()[1]] = p[:-5]
                                    break
        return self._guids.get(guid)

    def ref_path(self, ref):
        if not isinstance(ref, dict) or not ref.get('guid'):
            return None
        return self.guid_path(ref['guid'])

    def rel(self, path):
        return os.path.relpath(path, self.root).replace(os.sep, '/') if path else None

    # -- C# constants
    def cs(self, rel):
        if rel not in self._cs:
            with open(os.path.join(self.scripts, rel), encoding='utf-8') as fh:
                self._cs[rel] = fh.read()
        return self._cs[rel]

    def enum(self, rel, name):
        text = re.sub(r'//[^\n]*', '', self.cs(rel))
        text = re.sub(r'/\*.*?\*/', '', text, flags=re.S)
        m = re.search(r'enum\s+%s\s*\{([^}]*)\}' % re.escape(name), text)
        if not m:
            raise DataError(f'enum {name} not found in {rel}')
        members = [p.strip().split('=')[0].strip() for p in m.group(1).split(',')]
        return [p for p in members if p]

    def const(self, rel, name, kind=float):
        m = re.search(r'\b%s\s*=\s*(-?[\d.]+)f?\s*;' % re.escape(name), self.cs(rel))
        if not m:
            raise DataError(f'constant {name} not found in {rel}')
        return kind(m.group(1))

    def array(self, rel, name, kind=float):
        m = re.search(r'\b%s\s*=\s*(?:new\s*\w*\[\]\s*)?\{([^}]*)\}' % re.escape(name), self.cs(rel))
        if not m:
            raise DataError(f'array {name} not found in {rel}')
        return [kind(v.strip().rstrip('f')) for v in m.group(1).split(',') if v.strip()]


# --------------------------------------------------------------------------- localization


class Loc:
    def __init__(self, path):
        self.en = {}
        with open(path, encoding='utf-8', newline='') as fh:
            rows = csv.reader(fh)
            header = next(rows)
            col = header.index('en')
            for row in rows:
                if row and len(row) > col and row[0] not in self.en:
                    self.en[row[0]] = row[col]

    def has(self, key):
        return key in self.en

    def t(self, key, *args):
        if key not in self.en:
            raise DataError(f'localization key missing: {key}')
        text = self.en[key]
        return re.sub(r'\{(\d+)\}', lambda m: str(args[int(m.group(1))]), text) if args else text

    def td(self, key, fallback):
        return self.en.get(key) or fallback or ''


def clean(text):
    """In-game rich text to plain text: drop <color> tags, split \\n into lines."""
    text = re.sub(r'</?color[^>]*>', '', text or '')
    return text.replace('\\n', '\n').strip()


# --------------------------------------------------------------------------- forge math


class Forge:
    """UpgradeConfig + UpgradeMath, in float32 like the game."""

    def __init__(self, cfg):
        self.success = float_array(cfg['successRatePerPlus'])
        self.cost = int_array(cfg['shardCostPerPlus'])
        self.pity = float_array(cfg['burnPityPerPlus'])
        self.pity_max = num(cfg['burnPityMax'])
        self.gain = f32(num(cfg['gainPerPlus']))
        self.gain_by_rarity = [f32(v) for v in float_array(cfg['gainPerPlusByRarity'])]

    def multiplier(self, plus, rarity_index):
        gain = self.gain_by_rarity[rarity_index] if rarity_index < len(self.gain_by_rarity) else self.gain
        return f32(1.0 + f32(plus * gain))


class Level:
    def __init__(self, plus, mult):
        self.plus = max(0, plus)
        self.mult = f32(mult)

    @staticmethod
    def is_whole(v):
        return abs(v - round(v)) < 0.0005

    def scale(self, base):
        base = f32(base)
        if base == 0:
            return 0.0
        mag, sign = abs(base), (1 if base > 0 else -1)
        if not self.is_whole(mag):
            return f32(base * self.mult)
        growth = math.floor(f32(f32(mag * f32(self.mult - 1.0)) + 0.5))
        if self.plus > 0 and self.mult > 1.0:
            growth = max(growth, self.plus)
        return sign * (round_half_even(mag) + growth)

    def scale_fraction(self, fraction):
        return f32(self.scale(f32(f32(fraction) * 100.0)) / 100.0)


# --------------------------------------------------------------------------- effect text


class Describer:
    """Python port of EffectDef.Describe(): the card text the game shows."""

    def __init__(self, loc, enums, caps, stat_keys):
        self.loc = loc
        self.e = enums
        self.caps = caps
        self.stat_keys = stat_keys

    def name(self, enum, value):
        return self.e[enum][inum(value)]

    def scaled(self, v, lvl):
        return max(0, round_half_even(lvl.scale(num(v))))

    def factor(self, v, lvl):
        return fmt(lvl.scale(num(v)), 2)

    def type_word(self, dtype):
        return self.loc.t('fx.type.magical' if self.name('DamageType', dtype) == 'Magical' else 'fx.type.physical')

    def status_word(self, status):
        return self.loc.t('fx.status.' + self.name('StatusType', status).lower())

    @staticmethod
    def percent_text(fraction):
        percent = f32(fraction * 100.0)
        if abs(percent) < 10:
            return fmt(percent, 1)
        return str(round_half_even(percent))

    def stat_word(self, stat):
        key = self.stat_keys.get(self.name('Stat', stat))
        return self.loc.t(key) if key else self.name('Stat', stat)

    def describe(self, cls, d, lvl):
        fn = getattr(self, 'd_' + cls, None)
        if fn is None:
            raise DataError(f'no description port for effect {cls}')
        return fn(d, lvl)

    def d_DamageEffect(self, d, lvl):
        t = self.loc.t
        amount = d['amount']
        scaling = self.name('ValueScaling', amount['scaling'])
        typ = self.type_word(d['damageType'])
        base, factor = amount['baseValue'], amount['scalingFactor']

        def counter(key):
            return t(key, self.scaled(base, lvl), typ, self.factor(factor, lvl))

        if scaling == 'SkillCheck':
            core = t('fx.damage.skillcheck', self.scaled(base, lvl), typ)
        elif scaling == 'PerSourceCurrentShield':
            core = t('fx.damage.pershield', self.factor(factor, lvl), typ)
        elif scaling == 'PerTargetPoisonStacks':
            core = t('fx.damage.perpoison', self.factor(factor, lvl), typ)
        elif scaling == 'PerCurrentGold':
            core = t('fx.damage.pergold', round_half_even(f32(lvl.scale(num(factor)) * 100.0)), typ)
            if self.caps['gold'] > 0:
                core += t('fx.damage.pergold_cap', self.caps['gold'])
        elif scaling == 'PerPhysicalSymbolsLanded':
            core = t('fx.damage.perphys', self.factor(factor, lvl), typ)
        elif scaling == 'PerSameSymbolsLanded':
            core = counter('fx.damage.perself')
        elif scaling == 'PerAdjacentDamage':
            magic = self.name('DamageType', amount.get('adjacentType', 0)) == 'Magical'
            core = counter('fx.damage.peradjacent_magic' if magic else 'fx.damage.peradjacent_phys')
        elif scaling == 'PerTargetArmor':
            core = counter('fx.damage.perarmor')
        elif scaling == 'PerTargetMissingHP':
            core = counter('fx.damage.permissinghp')
            if self.caps['missing_hp'] > 0:
                core += t('fx.cap.missinghp', self.caps['missing_hp'])
        elif scaling == 'PerTurnNumber':
            core = counter('fx.damage.perturn') + t('fx.perturn.copies')
        elif scaling == 'PerFrozenReel':
            core = counter('fx.damage.perfrozen')
        elif scaling == 'PerPoolSize':
            core = counter('fx.damage.perpool')
        elif scaling == 'PerThinPool':
            core = counter('fx.damage.perthin')
        elif scaling == 'PerTimesLanded':
            core = counter('fx.damage.perlanded')
        elif scaling == 'None':
            core = t('fx.damage.flat', self.scaled(base, lvl), typ)
        else:
            raise DataError(f'DamageEffect scaling {scaling} has no description port')
        if inum(d['hitCount'], 1) > 1:
            core += t('fx.damage.hits', inum(d['hitCount']))
        if num(d['lifeStealPercent']) > 0:
            core += t('fx.damage.lifesteal', round_half_even(f32(min(1.0, lvl.scale_fraction(num(d['lifeStealPercent']))) * 100)))
        if num(d['stunChance']) > 0:
            core += t('fx.damage.stun', self.percent_text(min(1.0, lvl.scale_fraction(num(d['stunChance'])))))
        if num(d['executeBelowFraction']) > 0:
            core += t('fx.execute', fmt(num(d['executeMultiplier']), 1), round_half_even(f32(num(d['executeBelowFraction']) * 100)))
        if num(d['goldPercent']) > 0:
            core += t('fx.damage.gold', round_half_even(f32(min(1.0, lvl.scale_fraction(num(d['goldPercent']))) * 100)))
            if self.caps['damage_gold'] > 0:
                core += t('fx.damage.gold_cap', self.caps['damage_gold'])
        if flag(d['piercesShield']):
            core += t('fx.damage.pierce')
        if flag(d['bounce']):
            core += t('fx.damage.bounce')
        for key, loc_key in (('edgeMultiplier', 'fx.cond.edge'), ('centerMultiplier', 'fx.cond.center'),
                             ('bossMultiplier', 'fx.cond.boss'), ('armorMultiplier', 'fx.cond.armor'),
                             ('lowHPMultiplier', 'fx.cond.low_hp'), ('fullHPMultiplier', 'fx.cond.full_hp'),
                             ('shieldedMultiplier', 'fx.cond.shielded'), ('bareMultiplier', 'fx.cond.bare')):
            if num(d.get(key)) > 0:
                core += t(loc_key, fmt(num(d[key]), 2))
        if flag(d.get('hitsBackTarget')):
            core += t('fx.damage.back')
        if flag(d.get('hitsAllTargets')):
            core += t('fx.damage.all')
        return core

    def d_GainShieldEffect(self, d, lvl):
        t = self.loc.t
        amount = d['amount']
        scaling = self.name('ValueScaling', amount['scaling'])
        if scaling == 'SkillCheck':
            core = t('fx.shield.skillcheck', self.scaled(amount['baseValue'], lvl))
        elif scaling == 'PerTurnNumber':
            core = t('fx.shield.perturn', self.scaled(amount['baseValue'], lvl), self.factor(amount['scalingFactor'], lvl)) + t('fx.perturn.copies')
        elif scaling == 'PerPhysicalSymbolsLanded':
            core = t('fx.shield.perphys', self.factor(amount['scalingFactor'], lvl))
        elif scaling == 'None':
            core = t('fx.shield.flat', self.scaled(amount['baseValue'], lvl))
        else:
            raise DataError(f'GainShieldEffect scaling {scaling} has no description port')
        for key, loc_key in (('edgeMultiplier', 'fx.cond.edge'), ('centerMultiplier', 'fx.cond.center'),
                             ('lowHPMultiplier', 'fx.cond.low_hp'), ('fullHPMultiplier', 'fx.cond.full_hp')):
            if num(d.get(key)) > 0:
                core += t(loc_key, fmt(num(d[key]), 2))
        return core

    def d_HealEffect(self, d, lvl):
        t = self.loc.t
        amount = d['amount']
        scaling = self.name('ValueScaling', amount['scaling'])
        if scaling == 'SkillCheck':
            return t('fx.heal.skillcheck', self.scaled(amount['baseValue'], lvl))
        if scaling == 'PerTargetPoisonStacks':
            return t('fx.heal.perpoison', self.factor(amount['scalingFactor'], lvl))
        if scaling == 'PerSourceMaxHP':
            return t('fx.heal.permaxhp', round_away(lvl.scale(num(amount['scalingFactor'])) * 100.0))
        if scaling == 'None':
            return t('fx.heal', self.scaled(amount['baseValue'], lvl))
        raise DataError(f'HealEffect scaling {scaling} has no description port')

    def gold_text(self, v, lvl):
        return fmt(max(0.0, lvl.scale(num(v))), 1)

    def d_GainGoldEffect(self, d, lvl):
        t = self.loc.t
        amount = d['amount']
        scaling = self.name('ValueScaling', amount['scaling'])
        b, f = amount['baseValue'], amount['scalingFactor']
        if scaling == 'SkillCheck':
            core = t('fx.gold.skillcheck', self.gold_text(b, lvl))
        elif scaling == 'PerSameSymbolsLanded':
            core = t('fx.gold.perself', self.gold_text(b, lvl), self.factor(f, lvl))
        elif scaling == 'PerTargetMissingHP':
            core = t('fx.gold.permissinghp', self.gold_text(b, lvl), self.factor(f, lvl))
            if self.caps['missing_hp'] > 0:
                core += t('fx.cap.missinghp', self.caps['missing_hp'])
        elif scaling == 'PerPoolSize':
            core = t('fx.gold.perpool', self.gold_text(b, lvl), self.factor(f, lvl))
        elif scaling == 'PerTimesLanded':
            core = t('fx.gold.perlanded', self.gold_text(b, lvl), self.factor(f, lvl))
        elif scaling == 'None':
            core = t('fx.gold.gain', self.gold_text(b, lvl))
        else:
            raise DataError(f'GainGoldEffect scaling {scaling} has no description port')
        if num(d.get('executeBelowFraction')) > 0:
            core += t('fx.execute', fmt(num(d['executeMultiplier']), 1), round_half_even(f32(num(d['executeBelowFraction']) * 100)))
        return core

    def d_ApplyStatusEffect(self, d, lvl):
        t = self.loc.t
        if self.name('StatusType', d['status']) == 'Stun':
            text = t('fx.status.apply_stun')
        else:
            sc = self.name('ValueScaling', d['stacks']['scaling'])
            text = t('fx.status.apply_skillcheck' if sc == 'SkillCheck' else 'fx.status.apply',
                     self.scaled(d['stacks']['baseValue'], lvl), self.status_word(d['status']))
        return text + (t('fx.status.nodecay') if flag(d.get('preventDecay')) else '')

    def d_AmplifyStatusEffect(self, d, lvl):
        return self.loc.t('fx.amplify', self.status_word(d['status']),
                          round_half_even(f32(lvl.scale_fraction(num(d['bonusFraction'])) * 100)))

    def d_CleanseEffect(self, d, lvl):
        if flag(d.get('onlyOne')):
            return self.loc.t('fx.cleanse.one', self.status_word(d['only']))
        return self.loc.t('fx.cleanse.all')

    def d_ConsumeShieldEffect(self, d, lvl):
        return self.loc.t('fx.consume.shield', self.factor(d['damagePerShield'], lvl), self.type_word(d['damageType']))

    def d_ConsumeStatusEffect(self, d, lvl):
        t = self.loc.t
        who = t('fx.consume.self') if flag(d.get('fromSelf')) else t('fx.consume.enemy')
        tail = ''
        if num(d.get('damagePerStack')) > 0:
            tail += t('fx.consume.damage', self.factor(d['damagePerStack'], lvl), self.type_word(d['damageType']))
        if num(d.get('healPerStack')) > 0:
            tail += t('fx.consume.heal', self.factor(d['healPerStack'], lvl))
        return t('fx.consume.status', self.status_word(d['status']), who) + tail

    def d_EchoEffect(self, d, lvl):
        fraction = min(1.0, max(0.0, lvl.scale_fraction(min(1.0, max(0.0, num(d['valueFraction']))))))
        return self.loc.t('fx.echo', round_half_even(f32(fraction * 100)))

    def d_GrantModifierEffect(self, d, lvl):
        t = self.loc.t
        mod = d['modifier']
        when = {'ThisTurn': 'fx.when.turn', 'ThisBattle': 'fx.when.battle', 'Run': 'fx.when.run'}.get(
            self.name('ModDuration', d['duration']))
        if self.name('ModOp', mod['op']) == 'Flat':
            flat = self.scaled(mod['value'], lvl) if num(mod['value']) >= 0 else round_half_even(lvl.scale(num(mod['value'])))
            value = t('fx.buff.flat_minus' if flat < 0 else 'fx.buff.flat', abs(flat))
        else:
            fraction = lvl.scale_fraction(num(mod['value']))
            value = t('fx.buff.percent_minus' if fraction < 0 else 'fx.buff.percent', self.percent_text(abs(fraction)))
        return value + ' ' + self.stat_word(mod['stat']) + (t(when) if when else '')

    def d_PayHealthEffect(self, d, lvl):
        return self.loc.t('fx.cost.hp', inum(d['amount'])) + '. ' + self.loc.t('fx.cost.hp_shared')

    def d_SpendGoldEffect(self, d, lvl):
        return self.loc.t('fx.cost.gold', inum(d['amount']))

    def symbol_text(self, effects, lvl):
        return '. '.join(self.describe(cls, d, lvl) for cls, d in effects) + '.'


# --------------------------------------------------------------------------- threats


def enemy_threats(enemy):
    """BossThreats.Kinds(): what an enemy's attacks and armor test."""
    kinds = set()
    rearm = False
    multi_frames = len(enemy.get('attackImpactFrames') or []) > 1
    for a in enemy.get('attackPattern') or []:
        if num(a['poisonChance']) > 0 and inum(a['poisonStacks']) > 0:
            kinds.add('Poison')
        if num(a['stunChance']) > 0:
            kinds.add('Stun')
        if num(a['chillChance']) > 0:
            kinds.add('Chill')
        if num(a['burnChance']) > 0 and inum(a['burnStacks']) > 0:
            kinds.add('Burn')
        if num(a['goldStealChance']) > 0 and inum(a['goldStealAmount']) > 0:
            kinds.add('Theft')
        if inum(a['selfHealAmount']) > 0:
            kinds.add('SelfHeal')
        if inum(a['hitCount'], 1) > 1 or multi_frames:
            kinds.add('MultiHit')
        if inum(a['magicDamage']) > 0:
            kinds.add('Magic')
        if inum(a['physDamage']) > 0:
            kinds.add('Phys')
        if inum(a.get('rearmorAmount')) > 0:
            rearm = True
    if inum(enemy.get('armor')) > 0 or rearm:
        kinds.add('Armor')
    return kinds


EXAM_ORDER = ['Poison', 'Stun', 'Chill', 'Burn', 'Theft', 'SelfHeal', 'Armor', 'MultiHit']


def exam(kinds):
    out = [k for k in EXAM_ORDER if k in kinds]
    if not out:
        out = [k for k in ('Magic', 'Phys') if k in kinds]
    return out


def stat_counters(stat, value, out):
    if value <= 0:
        return
    out.update({'StunResist': ['Stun'], 'GoldTheftResist': ['Theft'], 'Thorns': ['MultiHit'],
                'MagicalResist': ['Magic'], 'PhysicalResist': ['Phys'], 'HPRegenPerTurn': ['Burn'],
                'PhysicalDamageDealt': ['SelfHeal'], 'MagicalDamageDealt': ['SelfHeal']}.get(stat, []))


def effect_counters(cls, d, names, out):
    if cls == 'CleanseEffect':
        only = names['StatusType'][inum(d.get('only'))]
        one = flag(d.get('onlyOne'))
        for status, threat in (('Poison', 'Poison'), ('Burn', 'Burn'), ('Chill', 'Chill')):
            if not one or only == status:
                out.add(threat)
    elif cls == 'HealEffect':
        out.add('Burn')
    elif cls == 'GainShieldEffect':
        out.update(['Phys', 'MultiHit'])
    elif cls == 'GrantModifierEffect':
        stat_counters(names['Stat'][inum(d['modifier']['stat'])], num(d['modifier']['value']), out)
    elif cls == 'DamageEffect':
        if names['DamageType'][inum(d['damageType'])] == 'Magical' or flag(d.get('piercesShield')) or num(d.get('armorMultiplier')) > 1:
            out.add('Armor')
        if num(d.get('executeBelowFraction')) > 0:
            out.add('SelfHeal')


def symbol_group(effects, names):
    """SymbolGroups.Of(): the in-game draft board's grouping."""
    gold = rot = control = shield = heal = phys = magic = False
    for cls, d in effects:
        if cls == 'GainGoldEffect':
            gold = True
        elif cls == 'DamageEffect':
            if num(d.get('goldPercent')) > 0:
                gold = True
            if names['DamageType'][inum(d['damageType'])] == 'Physical':
                phys = True
            else:
                magic = True
        elif cls == 'ApplyStatusEffect':
            if names['StatusType'][inum(d['status'])] in ('Poison', 'Burn'):
                rot = True
            else:
                control = True
        elif cls == 'AmplifyStatusEffect':
            rot = True
        elif cls == 'ConsumeStatusEffect':
            if num(d.get('damagePerStack')) > 0:
                if names['DamageType'][inum(d['damageType'])] == 'Physical':
                    phys = True
                else:
                    magic = True
            elif num(d.get('healPerStack')) > 0:
                heal = True
            else:
                rot = True
        elif cls == 'CleanseEffect':
            control = True
        elif cls == 'GainShieldEffect':
            shield = True
        elif cls == 'ConsumeShieldEffect':
            phys = True
        elif cls == 'HealEffect':
            heal = True
    for cond, group in ((gold, 'Gold'), (rot, 'Rot'), (phys, 'Physical'), (magic, 'Magical'),
                        (shield, 'Shield'), (heal, 'Heal'), (control, 'Control')):
        if cond:
            return group
    return 'Support'


# --------------------------------------------------------------------------- extractor


class Extractor:
    def __init__(self, project_root, site_root):
        self.p = Project(project_root)
        self.site = os.path.abspath(site_root)
        self.out_data = os.path.join(self.site, 'src', 'data', 'wiki')
        self.out_icons = os.path.join(self.site, 'public', 'wiki', 'icons')
        self.loc = Loc(os.path.join(self.p.data, 'localization.csv'))
        self.notes = []  # things worth reporting (left out, uninterpretable)
        self.icon_report = []
        self._enums()

    # -- enums and constants from the C#
    def _enums(self):
        p = self.p
        E = {}
        for rel, names in {
            'Core/Battle/Stats.cs': ['Stat', 'ModOp', 'ModDuration'],
            'Core/Effects/EffectValue.cs': ['ValueScaling'],
            'Core/Battle/BattleEvent.cs': ['DamageType'],
            'Core/Battle/StatusInstance.cs': ['StatusType'],
            'Core/Data/SymbolDef.cs': ['CardRarity'],
            'Core/Data/PowerupDef.cs': ['PowerupKind'],
            'Core/Data/ModifierDef.cs': ['ModifierKind', 'PactRule', 'AbilityKind', 'ModifierSpecial', 'AbilityPhase'],
            'Core/Data/EnemyDef.cs': ['DropKind', 'EnemySpeechTrigger'],
            'Core/Data/ChallengeDef.cs': ['ChallengeKind', 'SymbolMetric', 'ChallengeTier', 'ChallengeRewardKind'],
            'Core/Meta/AnvilLogic.cs': ['GemType'],
            'Core/Run/BossThreats.cs': ['ThreatKind'],
            'Core/Battle/SymbolGroups.cs': ['SymbolGroup'],
        }.items():
            for n in names:
                E[n] = p.enum(rel, n)
        self.E = E
        stats_cs = p.cs('Core/Battle/Stats.cs')
        self.stat_keys = dict(re.findall(r'Stat\.(\w+)\s*=>\s*Loc\.T\("([^"]+)"\)', stats_cs))
        speech = p.cs('Core/Battle/EnemySpeechCues.cs')
        self.speech_keys = dict(re.findall(r'EnemySpeechTrigger\.(\w+)\s*=>\s*"(\w+)"', speech))
        if not self.speech_keys:
            raise DataError('EnemySpeechCues.Key mapping not found')

    def enum_name(self, enum, value):
        return self.E[enum][inum(value)]

    # -- icons
    def icon(self, ref, kind, slug, phase=1):
        """Export an entity's sprite when it lives in ICON_DIRS; else None."""
        path = self.p.ref_path(ref)
        rel = self.p.rel(path)
        info = {'source': rel, 'exported': False}
        if not path:
            return None, info
        if not any(rel.startswith(d) for d in ICON_DIRS):
            info['reason'] = 'unverified source'
            self.icon_report.append((kind, slug, rel))
            return None, info
        out_dir = os.path.join(self.out_icons, kind)
        os.makedirs(out_dir, exist_ok=True)
        out = os.path.join(out_dir, slug + '.png')
        if path.endswith('.aseprite'):
            w, h = aseprite.export(path, out, phase=phase)
        elif path.endswith('.png'):
            w, h = export_png(path, out)
        else:
            raise DataError(f'unsupported icon texture {rel}')
        info['exported'] = True
        return {'src': f'/wiki/icons/{kind}/{slug}.png', 'width': w, 'height': h}, info

    # -- run
    def run(self):
        p, loc = self.p, self.loc
        self.cfg = p.load(os.path.join(p.data, 'GameConfig.asset'))
        self.upcfg = p.load(os.path.join(p.data, 'UpgradeConfig.asset'))
        self.forge = Forge(self.upcfg)
        db = p.load(os.path.join(p.data, 'GameDatabase.asset'))
        self.db_order = {key: [r['guid'] for r in (db.get(key) or []) if isinstance(r, dict) and r.get('guid')]
                         for key in ('symbols', 'enemies', 'levels', 'powerups', 'modifiers', 'cats',
                                     'reinforcements', 'challenges')}
        caps = {'gold': inum(self.cfg['goldScalingGoldCap']), 'damage_gold': inum(self.cfg['damageToGoldCap']),
                'missing_hp': inum(self.cfg['missingHpScalingCap'])}
        self.describer = Describer(loc, self.E, caps, self.stat_keys)
        self.nocaps = Describer(loc, self.E, {'gold': 0, 'damage_gold': 0, 'missing_hp': 0}, self.stat_keys)
        self.demo = self.read_demo()

        if os.path.isdir(self.out_icons):
            shutil.rmtree(self.out_icons)
        os.makedirs(self.out_data, exist_ok=True)

        raw = {name: [m for m in p.folder(folder)] for name, folder in (
            ('symbols', 'Symbols'), ('powerups', 'Powerups'), ('modifiers', 'Modifiers'),
            ('enemies', 'Enemies'), ('cats', 'Cats'), ('challenges', 'Challenges'),
            ('levels', 'Levels'), ('reinforcements', 'Reinforcements'))}
        # Only content registered in GameDatabase ships; anything else is left out.
        for key, items in raw.items():
            order = self.db_order[key]
            shipped = [m for m in items if m['_guid'] in order]
            for m in items:
                if m['_guid'] not in order:
                    self.notes.append(f"left out: {key[:-1]} '{m.get('id')}' ({m.get('displayName')}) is not registered in GameDatabase")
            shipped.sort(key=lambda m: order.index(m['_guid']))
            raw[key] = shipped
        # Spoiler rule (docs/devlog/plan.md, "Spoiler"): the final boss's name and
        # phases stay out. The final boss is the multi-phase enemy; its phase defs
        # used by endless share its animator.
        final = [m for m in raw['enemies'] if inum(m.get('phaseCount'), 1) > 1]
        final_anims = {(m.get('animator') or {}).get('guid') for m in final} - {None}
        self.spoilers = {m['id'] for m in raw['enemies']
                         if m in final or (m.get('animator') or {}).get('guid') in final_anims}
        for sid in sorted(self.spoilers):
            self.notes.append(f"left out (spoiler): enemy '{sid}' (final boss or one of its phases)")
        self.raw = raw
        self.by_id = {m['id']: m for items in raw.values() for m in items}

        levels = self.build_levels()
        enemies = self.build_enemies(levels)
        symbols = self.build_symbols(levels)
        powerups = self.build_powerups()
        modifiers = self.build_modifiers()
        cats = self.build_cats(modifiers)
        challenges = self.build_challenges()
        reinforcements = self.build_reinforcements()
        duels = self.build_duels()
        rules = self.build_rules()
        self.link(levels, enemies, symbols, powerups, cats, challenges)

        for name, payload in (('symbols', symbols), ('powerups', powerups), ('modifiers', modifiers),
                              ('cats', cats), ('enemies', enemies), ('levels', levels),
                              ('challenges', challenges), ('reinforcements', reinforcements),
                              ('duels', duels), ('rules', rules)):
            self.write(name, payload)
        meta = {
            'generatedFrom': os.path.basename(p.root),
            'sourceHash': self.source_hash(),
            'counts': {k: len(v) for k, v in (('symbols', symbols), ('powerups', powerups),
                                             ('enemies', enemies), ('levels', levels),
                                             ('cats', cats), ('reinforcements', reinforcements))},
        }
        self.write('meta', meta)
        # The report names spoilers and third-party sources, so it never goes into
        # the site: stdout, or a file outside the repo via --report.
        return dict(meta, notes=self.notes,
                    iconsNotExported=[{'kind': k, 'id': s, 'source': r} for k, s, r in self.icon_report])

    def write(self, name, payload):
        with open(os.path.join(self.out_data, name + '.json'), 'w', encoding='utf-8') as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=1)
            fh.write('\n')

    def source_hash(self):
        h = hashlib.sha256()
        for dirpath, _dirs, files in sorted(os.walk(self.p.data)):
            for f in sorted(files):
                if f.endswith(('.asset', '.csv')):
                    with open(os.path.join(dirpath, f), 'rb') as fh:
                        h.update(fh.read())
        return h.hexdigest()[:16]

    # -- demo build limits (Game/DemoGate.cs and Core/Pvp/PvpRuleset.cs)
    def read_demo(self):
        p = self.p
        rel = 'Game/DemoGate.cs'
        text = p.cs(rel)
        locked_specials = re.search(r'ModifierLevelCap\(SlotsAnvil\.Core\.ModifierSpecial special\)\s*=>(.*?)\?\s*0', text, re.S)
        if not locked_specials:
            raise DataError('DemoGate.ModifierLevelCap not found')
        specials = re.findall(r'ModifierSpecial\.(\w+)', locked_specials.group(1))
        ids = re.search(r'FullVersionModifierIds\s*=\s*\{([^}]*)\}', text)
        return {
            'maxLevel': p.const(rel, 'MaxLevel', int),
            'maxHeat': p.const(rel, 'MaxHeat', int),
            'maxPlus': p.const(rel, 'MaxPlus', int),
            'maxModifierLevel': p.const(rel, 'MaxModifierLevel', int),
            'maxCats': p.const(rel, 'MaxCats', int),
            'maxAbilities': p.const(rel, 'MaxAbilities', int),
            'lockedSpecials': specials,
            'lockedModifierIds': re.findall(r'"(\w+)"', ids.group(1)) if ids else [],
            'reels': self.base_reels(),
        }

    def base_reels(self):
        m = re.search(r'int reels = (\d+) \+ GetModifierLevel\(meta, ModifierSpecial\.ExtraReel\)',
                      self.p.cs('Core/Run/RunManager.cs'))
        if not m:
            raise DataError('RunManager.ReelCountFor base reel count not found')
        return int(m.group(1))

    # -- builders
    def name(self, m):
        return self.loc.td('def.%s.name' % m['id'], m.get('displayName'))

    def desc(self, m):
        return clean(self.loc.td('def.%s.desc' % m['id'], m.get('description')))

    def rarity(self, m):
        return self.enum_name('CardRarity', m.get('cardRarity', 0)).lower()

    def build_levels(self):
        out = []
        demo_max = self.demo['maxLevel']
        gems = self.E['GemType']
        for m in self.raw['levels']:
            fights = []
            for fi in m.get('fights') or []:
                ids = []
                for ref in fi.get('enemies') or []:
                    path = self.p.ref_path(ref)
                    enemy = next((e for e in self.raw['enemies'] if e['_guid'] == ref.get('guid')), None)
                    if enemy is None:
                        raise DataError(f"{m['id']}: fight enemy {path} not in GameDatabase")
                    ids.append(enemy['id'])
                fights.append(ids)
            rewards = []
            for ref in m.get('firstClearRewards') or []:
                sym = next((s for s in self.raw['symbols'] if s['_guid'] == ref.get('guid')), None)
                if sym is None:
                    raise DataError(f"{m['id']}: first-clear reward not a registered symbol")
                rewards.append(sym['id'])
            first_gems = [gems[g].lower() for g in int_array(m.get('firstClearGems'))]
            idx = inum(m['levelIndex'])
            box = {k: num(m[f'boxChance{k.title()}']) for k in ('common', 'rare', 'epic', 'legendary')}
            out.append({
                'id': m['id'], 'slug': f'level-{idx}', 'index': idx, 'name': self.name(m),
                'fights': [[e if e not in self.spoilers else None for e in group] for group in fights],
                'boss': (fights[-1][0] if fights[-1][0] not in self.spoilers else None) if fights and fights[-1] else None,
                'bossHidden': bool(fights and fights[-1] and fights[-1][0] in self.spoilers),
                'hpMultiplier': num(m['hpMultiplier']), 'damageMultiplier': num(m['damageMultiplier']),
                'goldMultiplier': num(m['goldMultiplier']), 'skullMultiplier': num(m['shardMultiplier']),
                'boxChance': box, 'boxChanceTotal': round(sum(box.values()), 4),
                'firstClearSymbols': rewards, 'firstClearGems': first_gems,
                'inDemo': idx <= demo_max,
            })
        out.sort(key=lambda l: l['index'])
        return out

    def build_enemies(self, levels):
        out = []
        drop_kinds = self.E['DropKind']
        triggers = self.E['EnemySpeechTrigger']
        for m in self.raw['enemies']:
            eid = m['id']
            if eid in self.spoilers:
                continue
            attacks = []
            for a in m.get('attackPattern') or []:
                attacks.append({
                    'physical': inum(a['physDamage']), 'magical': inum(a['magicDamage']),
                    'hits': inum(a['hitCount'], 1),
                    'stunChance': num(a['stunChance']),
                    'burnChance': num(a['burnChance']), 'burnStacks': inum(a['burnStacks']),
                    'chillChance': num(a['chillChance']), 'chillTurns': inum(a['chillTurns']),
                    'poisonChance': num(a['poisonChance']), 'poisonStacks': inum(a['poisonStacks']),
                    'stealChance': num(a['goldStealChance']),
                    'selfHealChance': num(a['selfHealChance']), 'selfHealAmount': inum(a['selfHealAmount']),
                    'rearmor': inum(a.get('rearmorAmount')),
                })
            frames = len(m.get('attackImpactFrames') or [])
            drops = []
            table = [(drop_kinds[inum(d['kind'])], num(d['chance'])) for d in m.get('drops') or []]
            live = [(k, w) for k, w in table if k not in ('Box', 'Scroll', 'Trina') and w > 0]
            total = sum(w for _, w in live)
            for k, w in live:
                drops.append({'kind': k.lower(), 'weight': w, 'share': round(w / total, 4) if total else 0})
            lines = []
            seen = {}
            for line in m.get('speechLines') or []:
                trig = triggers[inum(line['trigger'])]
                n = seen.get(trig, 0)
                seen[trig] = n + 1
                key = 'def.%s.line.%s%s' % (eid, self.speech_keys[trig], '' if n == 0 else str(n + 1))
                if self.loc.has(key):
                    lines.append({'trigger': trig, 'text': clean(self.loc.t(key))})
                else:
                    self.notes.append(f'enemy {eid}: speech line {key} has no English text, skipped')
            appearances = []
            for lvl in levels:
                for fi, group in enumerate(lvl['fights']):
                    if eid in group:
                        appearances.append({'level': lvl['index'], 'fight': fi + 1, 'group': group,
                                            'isBossFight': fi == len(lvl['fights']) - 1})
            kinds = enemy_threats(m)
            slug = slugify(eid.replace('_', '-'))
            icon, src = self.icon(m.get('sprite'), 'enemies', slug, phase=inum(m.get('startPhase'), 1))
            boss_of = [l['index'] for l in levels if l['boss'] == eid]
            out.append({
                'id': eid, 'slug': slug, 'name': self.name(m),
                'hp': inum(m['maxHP']), 'armor': inum(m['armor']), 'magicResist': num(m['magicResist']),
                'attacks': attacks, 'impactFrames': frames, 'rampPercent': num(m['attackRampPercent']),
                'phases': inum(m['phaseCount'], 1), 'startPhase': inum(m.get('startPhase'), 1),
                'gold': inum(m['goldReward']), 'skulls': inum(m['shardReward']),
                'isBoss': flag(m['isBoss']), 'bossOfLevels': boss_of,
                'drops': drops, 'lines': lines,
                'threats': [k for k in self.E['ThreatKind'] if k in kinds], 'exam': exam(kinds),
                'appearances': appearances,
                'endlessPool': inum(m['phaseCount'], 1) <= 1,
                'inDemo': any(a['level'] <= self.demo['maxLevel'] for a in appearances),
                'icon': icon,
            })
        return out

    def build_symbols(self, levels):
        out = []
        forge = self.forge
        names = self.E
        mismatches = []
        for m in self.raw['symbols']:
            effects = self.p.effects(m, 'effects')
            rarity_i = inum(m.get('cardRarity'))
            texts = []
            for plus in range(0, 11):
                lvl = Level(plus, forge.multiplier(plus, rarity_i))
                texts.append(self.describer.symbol_text(effects, lvl))
            base_check = self.nocaps.symbol_text(effects, Level(0, 1.0))
            loc_desc = self.desc(m)
            if loc_desc and base_check != loc_desc:
                mismatches.append((m['id'], base_check, loc_desc))
            counters = set()
            dtypes = []
            for cls, d in effects:
                effect_counters(cls, d, names, counters)
                if cls in ('DamageEffect', 'ConsumeShieldEffect') or (cls == 'ConsumeStatusEffect' and num(d.get('damagePerStack')) > 0):
                    t = self.enum_name('DamageType', d['damageType']).lower()
                    if t not in dtypes:
                        dtypes.append(t)
            unlocked = [l['index'] for l in levels if m['id'] in l['firstClearSymbols']]
            slug = slugify(m['id'])
            out.append({
                'id': m['id'], 'slug': slug, 'name': self.name(m),
                'group': symbol_group(effects, names).lower(),
                'rarity': self.rarity(m),
                'text': texts[0][0].upper() + texts[0][1:],
                'textByPlus': [t[0].upper() + t[1:] for t in texts],
                'shopPrice': inum(m['shopPrice']) or None,
                'starter': flag(m['isStarter']), 'forgeable': flag(m['isForgeable']),
                'inDemo': flag(m.get('availableInDemo')),
                'critMultiplier': num(m['critMultiplier']),
                'skillCheck': flag(m['usesSkillCheck']) or any(
                    isinstance(d.get('amount') or d.get('stacks'), dict) and
                    self.enum_name('ValueScaling', (d.get('amount') or d.get('stacks'))['scaling']) == 'SkillCheck'
                    for _, d in effects),
                'damageTypes': dtypes,
                'answers': [k for k in self.E['ThreatKind'] if k in counters],
                'firstClearOfLevels': unlocked,
                'icon': self.icon(m.get('icon'), 'symbols', slug)[0],
            })
        for sid, ours, theirs in mismatches:
            self.notes.append(f'symbol {sid}: generated +0 text differs from localization.csv '
                              f'(page uses the generated text): ours="{ours}" csv="{theirs}"')
        return out

    def build_powerups(self):
        out = []
        for m in self.raw['powerups']:
            kind = self.enum_name('PowerupKind', m['kind']).lower()
            counters = set()
            passive = []
            for mod in m.get('passiveModifiers') or []:
                stat = self.enum_name('Stat', mod['stat'])
                stat_counters(stat, num(mod['value']), counters)
                passive.append({'stat': stat, 'op': self.enum_name('ModOp', mod['op']), 'value': num(mod['value'])})
            for cls, d in self.p.effects(m, 'activeEffects'):
                effect_counters(cls, d, self.E, counters)
            base = inum(m['goldCostPerUse'])
            growth = num(m['costGrowthPerUse'])
            costs = [max(0, round_away(base * (1 + growth) ** n)) for n in range(5)] if kind == 'active' else []
            slug = slugify(m['id'])
            skill = flag(m['usesSkillCheck']) or any(
                self.enum_name('ValueScaling', (d.get('amount') or {}).get('scaling', 0)) == 'SkillCheck'
                for _, d in self.p.effects(m, 'activeEffects'))
            out.append({
                'id': m['id'], 'slug': slug, 'name': self.name(m), 'kind': kind,
                'text': self.desc(m), 'shopPrice': inum(m['shopPrice']),
                'usesPerTurn': inum(m['usesPerTurn']) if kind == 'active' else None,
                'goldCostPerUse': base if kind == 'active' else None,
                'costGrowthPerUse': growth, 'costByUse': costs,
                'skillCheck': skill, 'duelDamageFraction': num(m['duelDamageFraction']),
                'passive': passive,
                'answers': [k for k in self.E['ThreatKind'] if k in counters],
                'icon': self.icon(m.get('icon'), 'powerups', slug)[0],
            })
        return out

    def build_modifiers(self):
        passives, abilities, pacts = [], [], []
        phase_src = self.p.cs('Core/Data/ModifierDef.cs')
        during = re.search(r'PhaseOf\(AbilityKind kind\)\s*=>\s*kind switch\s*\{(.*?)\}', phase_src, re.S)
        if not during:
            raise DataError('AbilityKinds.PhaseOf not found')
        spin_kinds = set()
        for arm in during.group(1).split(','):
            if 'AbilityPhase.DuringSpin' in arm:
                spin_kinds.update(re.findall(r'AbilityKind\.(\w+)', arm))
        cfg = self.cfg
        ability_rung = 0
        for m in self.raw['modifiers']:
            kind = self.enum_name('ModifierKind', m['kind'])
            costs = int_array(m['levelCosts'])
            stats = [{'stat': self.enum_name('Stat', s['stat']), 'op': self.enum_name('ModOp', s['op']),
                      'value': num(s['value'])} for s in m.get('modifiersPerLevel') or []]
            slug = slugify(m['id'])
            base = {'id': m['id'], 'slug': slug, 'name': self.name(m), 'text': self.desc(m),
                    'icon': self.icon(m.get('icon'), 'modifiers', slug)[0]}
            if kind == 'Passive':
                special = self.enum_name('ModifierSpecial', m['special'])
                cap = 0 if (special in self.demo['lockedSpecials'] or m['id'] in self.demo['lockedModifierIds']) \
                    else self.demo['maxModifierLevel']
                base.update({'maxLevel': inum(m['maxLevel']), 'levelCosts': costs, 'totalCost': sum(costs),
                             'statsPerLevel': stats, 'special': special, 'demoMaxLevel': min(cap, inum(m['maxLevel']))})
                passives.append(base)
            elif kind == 'Ability':
                ability = self.enum_name('AbilityKind', m['ability'])
                base.update({'ability': ability, 'cost': costs[0] if costs else 0, 'ladderIndex': ability_rung,
                             'phase': 'during-spin' if ability in spin_kinds else 'after-stop',
                             'inDemo': ability_rung < self.demo['maxAbilities']})
                ability_rung += 1
                abilities.append(base)
            else:
                rule = self.enum_name('PactRule', m['pactRule'])
                params = {}
                if rule == 'BloodPact':
                    params = {'hpPerSpin': inum(cfg['pactBloodCostPerSpin']), 'forgeBonus': inum(cfg['pactBloodForgeBonus'])}
                elif rule == 'Usury':
                    params = {'interestRate': num(cfg['pactInterestRate']), 'interestCap': inum(cfg['pactInterestCap']),
                              'stealChance': num(cfg['pactUsuryStealChance']),
                              'stealPercent': num(cfg['goldStealPercent']), 'stealMinimum': inum(cfg['goldStealMinimum'])}
                base.update({'rule': rule, 'cost': costs[0] if costs else 0, 'stats': stats,
                             'skullMultiplier': num(m['pactRewardMultiplier']), 'params': params})
                pacts.append(base)
        return {'passives': passives, 'abilities': abilities, 'pacts': pacts}

    def build_cats(self, modifiers):
        out = []
        pacts = {p['id']: p for p in modifiers['pacts']}
        offered = set()
        for rung, m in enumerate(self.raw['cats']):
            pact = pacts.get(m['pactId'])
            if pact is None:
                raise DataError(f"cat {m['id']} offers unknown pact {m['pactId']}")
            offered.add(pact['id'])
            slug = slugify(m['id'])
            icon, src = self.icon(m.get('icon'), 'cats', slug)
            out.append({'id': m['id'], 'slug': slug, 'name': self.name(m), 'flavor': self.desc(m),
                        'cost': inum(m['cost']), 'ladderIndex': rung, 'inDemo': rung < self.demo['maxCats'],
                        'pact': pact, 'icon': icon})
        reserved = [p for p in modifiers['pacts'] if p['id'] not in offered]
        for p in reserved:
            self.notes.append(f"left out: pact '{p['id']}' ({p['name']}) is offered by no cat (held in reserve)")
        modifiers['pacts'] = [p for p in modifiers['pacts'] if p['id'] in offered]
        return out

    def build_challenges(self):
        regular, tasks = [], []
        for m in self.raw['challenges']:
            kind = self.enum_name('ChallengeKind', m['kind'])
            reward_kind = self.enum_name('ChallengeRewardKind', m['rewardKind'])
            amount = inum(m['rewardAmount'])
            if kind == 'SymbolTask':
                metric = self.enum_name('SymbolMetric', m['symbolMetric'])
                share = self.p.const('Core/Meta/ChallengeLogic.cs', 'SymbolTaskSkullShare')
                tasks.append({'id': m['id'], 'symbol': m['param'], 'metric': metric.lower(),
                              'target': inum(m['target']),
                              'rewardSkulls': round_away(amount * share),
                              'text': self.loc.t('challenge.task_' + metric.lower(),
                                                 self.loc.td('def.%s.name' % m['param'], m['param']), inum(m['target']))})
                continue
            reward = {'kind': reward_kind, 'amount': amount}
            if reward_kind == 'Symbol':
                reward['symbol'] = m.get('rewardSymbolId')
            if reward_kind == 'RingStyle':
                reward['style'] = m.get('rewardStyleKey')
                reward['styleName'] = self.loc.t('ring.' + m.get('rewardStyleKey')).capitalize()
            regular.append({'id': m['id'], 'slug': slugify(m['id']), 'name': self.name(m), 'text': self.desc(m),
                            'kind': kind, 'target': inum(m['target']), 'param': m.get('param') or '',
                            'minHeat': inum(m['minHeat']), 'tier': self.enum_name('ChallengeTier', m['tier']).lower(),
                            'endless': kind.startswith('Endless'), 'sortOrder': inum(m['sortOrder']), 'reward': reward})
        regular.sort(key=lambda c: c['sortOrder'])
        logic = 'Core/Meta/ChallengeLogic.cs'
        achievements = self.build_achievements()
        tier_names = {t.lower(): self.loc.t('challenge.tier_' + t.lower()).capitalize() for t in self.E['ChallengeTier']}
        return {'challenges': regular, 'symbolTasks': tasks, 'tierNames': tier_names,
                'taskCycleGrowth': self.p.const(logic, 'CycleGrowth'),
                'taskCycleGrowthCap': self.p.const(logic, 'CycleGrowthCap'),
                'maxTracked': self.p.const(logic, 'MaxActive', int),
                'achievements': achievements}

    def build_achievements(self):
        cat = self.p.cs('Game/Steam/AchievementCatalog.cs')
        ids = dict(re.findall(r'const string (\w+)\s*=\s*"(\w+)"', self.p.cs('Game/Steam/SteamStatIds.cs')))
        demo_block = re.search(r'DemoAchievements\s*=\s*\{([^}]*)\}', self.p.cs('Game/Steam/SteamStatIds.cs'))
        demo = {ids[n] for n in re.findall(r'(\w+)', demo_block.group(1))} if demo_block else set()
        out = []
        for const, group, hidden in re.findall(r'E\(SteamStatIds\.(\w+),\s*AchGroup\.(\w+)(,\s*hidden:\s*true)?\)', cat):
            aid = ids[const]
            name = self.loc.t(f'ach.{aid}.name')
            if hidden:
                self.notes.append(f"left out: hidden achievement '{aid}' ({name})")
                continue
            out.append({'id': aid, 'name': name, 'text': self.loc.t(f'ach.{aid}.desc'),
                        'group': self.loc.t('challenges.ach_group_' + {'FirstSteps': 'first', 'Forge': 'forge', 'Battle': 'battle',
                                                                       'Endless': 'endless', 'Collection': 'collection'}[group]),
                        'inDemo': aid in demo})
        if not out:
            raise DataError('no achievements parsed from AchievementCatalog.cs')
        return out

    def build_reinforcements(self):
        out = []
        for m in self.raw['reinforcements']:
            stat = self.enum_name('Stat', m['stat'])
            op = self.enum_name('ModOp', m['op'])
            value = num(m['value'])
            word = self.loc.t(self.stat_keys[stat])
            text = (self.loc.t('fx.buff.percent', Describer.percent_text(value)) if op == 'PercentAdd'
                    else self.loc.t('fx.buff.flat', fmt(value, 2))) + ' ' + word + self.loc.t('shop.reinforcement_when')
            slug = slugify(m['id'])
            out.append({'id': m['id'], 'slug': slug, 'name': self.name(m), 'stat': stat, 'op': op, 'value': value,
                        'text': text, 'basePrice': inum(m['basePrice']),
                        'icon': self.icon(m.get('icon'), 'reinforcements', slug)[0]})
        return out

    def build_duels(self):
        rel = 'Core/Pvp/DuelRank.cs'
        floors = self.p.array(rel, 'ScoreFloor')
        wins = self.p.array(rel, 'WinsFloor', int)
        tiers = re.search(r'TierKeys\s*=\s*\{([^}]*)\}', self.p.cs(rel))
        tier_keys = re.findall(r'"(\w+)"', tiers.group(1))
        steps = self.p.const(rel, 'StepsPerTier', int)
        numerals = ['I', 'II', 'III', 'IV']
        ranks = []
        for i, (score, won) in enumerate(zip(floors, wins)):
            tier = tier_keys[i // steps]
            ranks.append({'rank': i + 1, 'tier': self.loc.t('rank.tier.' + tier), 'step': numerals[i % steps],
                          'scoreFloor': score, 'winsFloor': won})
        icons = self.p.load(os.path.join(self.p.data, 'DuelRanks.asset')).get('icons') or []
        for r in ranks:
            ref = icons[r['rank'] - 1] if r['rank'] <= len(icons) else None
            r['icon'] = self.icon(ref, 'ranks', f"rank-{r['rank']}")[0]
        pvp = 'Core/Pvp/PvpRuleset.cs'
        rules = {
            'placementDuels': self.p.const(rel, 'PlacementDuels', int), 'z': self.p.const(rel, 'Z'),
            'hpStep': {'3': self.p.const(pvp, 'HPStepThreeReels', int), '4': self.p.const(pvp, 'HPStepFourReels', int),
                       '5': self.p.const(pvp, 'HPStepFiveReels', int)},
            'maxShield': self.p.const(pvp, 'PlayerMaxShield', int),
            'duelHealScale': self.p.const(pvp, 'DuelHealScale'),
            'maxRegenPerTurn': self.p.const(pvp, 'MaxRegenPerTurn'),
            'farmSkullMultiplier': self.p.const(pvp, 'SkullMultiplier'),
            'classicRoundGold': self.p.const(pvp, 'ClassicRoundGold', int),
            'classicRoundSkulls': self.p.const(pvp, 'ClassicRoundSkulls', int),
            'duelOnlyRoundGold': self.p.const(pvp, 'DuelOnlyRoundGold', int),
            'duelOnlyRoundSkulls': self.p.const(pvp, 'DuelOnlyRoundSkulls', int),
            'roundSkullMultipliers': self.p.array(pvp, 'RoundSkullMultipliers'),
            'breakSuccessBonus': self.p.const(pvp, 'AnvilBreakSuccessBonus'),
            'breakOptions': self.p.array(pvp, 'BreakOptions', int),
            'maxPassivePowerups': self.p.const(pvp, 'MaxPassivePowerups', int),
            'maxActivePowerups': self.p.const(pvp, 'MaxActivePowerups', int),
            'gemGreenPrice': self.p.const(pvp, 'GemGreenPrice', int),
            'gemBluePrice': self.p.const(pvp, 'GemBluePrice', int),
            'duelWinYellowGems': self.p.const(pvp, 'DuelWinYellowGems', int),
            'pausesPerPlayer': self.p.const(pvp, 'PausesPerPlayer', int),
            'draftPickSeconds': self.p.const(pvp, 'DraftPickSeconds', int),
            'duelTurnSeconds': self.p.const(pvp, 'DuelTurnSeconds', int),
            'demoMaxRoundsToWin': self.p.const(pvp, 'DemoMaxRoundsToWin', int),
            'demoDraftSymbols': re.findall(r'"(\w+)"', re.search(r'DemoDraftSymbols\s*=\s*new\(\)\s*\{([^}]*)\}',
                                                                self.p.cs(pvp), re.S).group(1)),
        }
        texts = {k: clean(self.loc.t(k)) for k in ('tut.pvp_lobby', 'tut.pvp_mode', 'tut.pvp_draft', 'tut.pvp_farm',
                                                    'tut.pvp_duel', 'tut.pvp_break', 'tut.pvp_rank')}
        return {'ranks': ranks, 'rules': rules, 'texts': texts}

    def build_rules(self):
        c, f, loc = self.cfg, self.forge, self.loc
        rarities = [r.lower() for r in self.E['CardRarity']]
        weights = [inum(c['rarityWeight' + r.title()]) for r in rarities]
        anvil = []
        reach = 1.0
        for plus in range(10):
            chance = min(1.0, f.success[plus])
            reach *= chance
            anvil.append({'from': plus, 'to': plus + 1, 'success': chance, 'skulls': f.cost[plus],
                          'burnPity': f.pity[plus] if plus < len(f.pity) else 0, 'reachFromZero': round(reach, 6)})
        gain = {r: f.gain_by_rarity[i] for i, r in enumerate(rarities)}
        steps = {}
        for key in ('tut.stop_reel', 'tut.resolve', 'tut.crit', 'tut.skillcheck', 'tut.skillcheck_drain',
                    'tut.skillcheck_double', 'tut.vitals', 'tut.enemy_armor', 'tut.telegraph', 'tut.status_burn',
                    'tut.status_chill', 'tut.status_stun_player', 'tut.status_stun_enemy', 'tut.status_poison',
                    'tut.shop', 'tut.shop_lock', 'tut.equipment', 'tut.shards', 'tut.drops', 'tut.anvil',
                    'tut.burn_pity', 'tut.anvil_gems', 'tut.modifiers', 'tut.runsetup', 'tut.terms_abilities',
                    'tut.heat', 'tut.endless_mode', 'tut.early_kill', 'tut.crit_max_hp', 'tut.crit_max_shield',
                    'tut.symbol_position', 'tut.symbol_cost', 'tut.run_buff', 'tut.growth_cap', 'tut.last_word',
                    'tut.momentum', 'tut.stun_fatigue', 'tut.powerup_use', 'tut.auto_mode', 'tut.challenges',
                    'tut.symbol_challenge', 'tut.intro_fight', 'tut.intro_anvil', 'tut.intro_modifier'):
            text = loc.t(key)
            text = re.sub(r'\{0\}', str(inum(c['shopLockCost'])) if key == 'tut.shop_lock' else
                          str(inum(self.p.const('Core/Meta/ChallengeLogic.cs', 'MaxActive', int))) if key == 'tut.challenges' else '{0}', text)
            steps[key] = clean(text)
        tips = []
        for i in range(1, 100):
            if not loc.has(f'tip.{i}'):
                continue
            tip = clean(loc.t(f'tip.{i}'))
            if any(rx.search(tip) for rx in RETIRED_PHRASES):
                self.notes.append(f'left out: tip.{i} uses retired wording: "{tip}"')
                continue
            tips.append(tip)
        exam_texts = {k: loc.t('exam.' + k.lower()) for k in self.E['ThreatKind'] if loc.has('exam.' + k.lower())}
        gem = inum(round_away(num(c['gemGreenSuccessBonus']) * 100))
        groups = {g.lower(): loc.t('group.' + g.lower()).capitalize() for g in self.E['SymbolGroup']}
        return {
            'player': {'maxHP': inum(c['basePlayerMaxHP']), 'maxShield': inum(c['basePlayerMaxShield']),
                       'reels': self.demo['reels'], 'fightsPerLevel': inum(c['fightsPerRun'])},
            'rarity': {'order': rarities, 'weights': dict(zip(rarities, weights)),
                       'unlockLevel': {'rare': inum(c['rarityUnlockLevelRare']), 'epic': inum(c['rarityUnlockLevelEpic']),
                                       'legendary': inum(c['rarityUnlockLevelLegendary'])},
                       'shopPriceGrowth': dict(zip(rarities, float_array(c['shopPriceGrowthByRarity']))),
                       'salvage': dict(zip(rarities, int_array(c['salvageByRarity'])))},
            'groups': groups,
            'statNames': {stat: loc.t(key) for stat, key in self.stat_keys.items()},
            'rarityNames': {r: loc.t('rarity.' + r).capitalize() for r in rarities},
            'anvil': {'steps': anvil, 'burnPityMax': f.pity_max, 'gainPerPlusByRarity': gain,
                      'maxPlus': len(f.success),
                      'critBonusAtMax': self.p.const('Core/Data/UpgradeConfig.cs', 'MaxPlusCritBonus'),
                      'effectArtFromPlus': self.p.const('Core/Data/SymbolDef.cs', 'EffectIconMinPlus', int),
                      'salvagePerPlus': inum(c['salvagePerPlus']),
                      'gemGreenBonus': num(c['gemGreenSuccessBonus']),
                      'gemYellowHeatBossChance': num(c['gemYellowHeatBossChance']),
                      'gemYellowHeatMinimum': inum(c['gemYellowHeatMinimum']),
                      'salvageRightsPerLevel': num(c['salvageRightsChancePerLevel']),
                      'gems': {g: {'name': loc.t(f'gem.{g}.name'), 'text': loc.t(f'gem.{g}.desc', gem) if g == 'green' else loc.t(f'gem.{g}.desc'),
                                   'icon': self.gem_icon(g)} for g in ('green', 'blue', 'yellow')}},
            'combat': {'reelAutoStopSeconds': self.p.const('Core/Slots/ReelClock.cs', 'AutoStopSeconds'),
                       'maxResist': self.p.const('Core/Battle/DamageCalculator.cs', 'MaxResist'),
                       'maxCritChance': num(c['maxCritChance']),
                       'critRaise': self.p.const('Core/Effects/HealEffect.cs', 'CritMaxHPBonus', int),
                       'critRaisesPerRun': inum(c['critCeilingRaisesPerRun']),
                       'lowHpFraction': self.p.const('Core/Effects/EffectDef.cs', 'LowHPFraction'),
                       'burnMinTick': inum(c['burnMinTickDamage']),
                       'maxRegenPerTurn': num(c['maxHpRegenPerTurn']),
                       'runBuffMaxStacks': inum(c['runBuffMaxStacksPerStat']),
                       'symbolMemoryCap': inum(c['symbolMemoryCap']),
                       'freeAtCopies': self.p.const('Core/Effects/PayHealthEffect.cs', 'FreeAtCopies', int),
                       'thinPoolLine': self.p.const('Core/Effects/EffectValue.cs', 'ThinPoolLine', int),
                       'perfectZone': self.p.const('Core/Battle/SkillCheckCurve.cs', 'DefaultPerfectZone'),
                       'skillMinMultiplier': self.p.const('Core/Battle/SkillCheckCurve.cs', 'DefaultMinMultiplier'),
                       'earlyKillFirst': num(c['earlyKillFirstBonus']), 'earlyKillSecond': num(c['earlyKillSecondBonus'])},
            'economy': {'shopSymbolOffers': inum(c['shopSymbolOffers']), 'shopPowerupOffers': inum(c['shopPowerupOffers']),
                        'rerollBase': inum(c['rerollBaseCost']), 'rerollIncrement': inum(c['rerollCostIncrement']),
                        'lockCost': inum(c['shopLockCost']), 'removePrice': inum(c['symbolRemovePrice']),
                        'upgradeOfferMultiplier': num(c['shopUpgradeOfferMultiplier']),
                        'maxShopDiscount': self.p.const('Core/Run/RunManager.cs', 'MaxShopDiscount'),
                        'runEndBonusPerKill': inum(c['runEndBonusPerKill']), 'runEndVictoryBonus': inum(c['runEndVictoryBonus']),
                        'boxGold': [inum(c['boxGoldMin']), inum(c['boxGoldMax'])],
                        'boxSkulls': [inum(c['boxShardMin']), inum(c['boxShardMax'])],
                        'boxTierMultiplier': {'common': 1, 'rare': num(c['boxRewardMultRare']),
                                              'epic': num(c['boxRewardMultEpic']), 'legendary': num(c['boxRewardMultLegendary'])},
                        'boxSymbolTierShare': round(num(c['boxSymbolTierBias']) / (num(c['boxSymbolTierBias']) + 1), 4),
                        'stealPercent': num(c['goldStealPercent']), 'stealMinimum': inum(c['goldStealMinimum']),
                        'goldScalingCap': inum(c['goldScalingGoldCap']), 'damageToGoldCap': inum(c['damageToGoldCap']),
                        'missingHpCap': inum(c['missingHpScalingCap']),
                        'pactRewardCap': num(c['pactRewardCap']),
                        'interestCapFightsEndless': num(c['endlessInterestCapFights'])},
            'heat': {'max': inum(c['maxHeat']), 'enemyMultiplier': float_array(c['heatEnemyMultByTier']),
                     'rewardBonus': float_array(c['heatRewardBonusByTier']),
                     'dropBonusPerHeat': num(c['heatDropBonusPerLevel']),
                     'rarityBonusPerHeat': num(c['heatRarityBonusPerLevel']),
                     'riderChanceFromHeat3': num(c['heatRiderChanceMultiplier']),
                     'rampFromHeat4': num(c['heatRampMultiplier']),
                     'armorAtHeat5': num(c['heatArmorFraction'])},
            'endless': {'poolSize': sum(1 for m in self.raw['enemies'] if inum(m.get('phaseCount'), 1) <= 1),
                        'goldPerKill': num(c['endlessGoldPerKill']), 'goldPerKillGrowth': num(c['endlessGoldPerKillGrowth']),
                        'duoStartFight': inum(c['endlessDuoStartFight']), 'duoChance': num(c['endlessDuoChance']),
                        'duoChanceRamp': num(c['endlessDuoChanceRamp']), 'duoChanceMax': num(c['endlessDuoChanceMax']),
                        'reinforcementOffers': inum(c['endlessShopReinforcementOffers']),
                        'reinforcementGrowth': num(c['endlessReinforcementGrowth']),
                        'reinforcementPriceGrowth': num(c['endlessReinforcementPriceGrowth']),
                        'reinforcementBuysPerShop': inum(c['endlessReinforcementBuysPerShop']),
                        'boxChanceScale': num(c['endlessBoxChanceScale']),
                        'freshnessWindow': inum(c['endlessFreshnessWindow']),
                        'calibrationStartFight': inum(c['endlessCalibrationStartFight']),
                        'calibrationFullFight': inum(c['endlessCalibrationFullFight']),
                        'rewardGrowth': num(c['endlessRewardGrowth']), 'rewardCap': num(c['endlessRewardCap'])},
            'meta': {'momentumPerStack': num(c['momentumPerStack']), 'reviveHealth': num(c['reviveHealthPercent']),
                     'bloodMoneyGoldPerSkull': inum(c['bloodMoneyGoldPerSkull']), 'bloodMoneySkullCap': inum(c['bloodMoneySkullCap']),
                     'demoImportSkullCap': inum(c['demoImportSkullCap'])},
            'demo': self.demo,
            'texts': steps,
            'tips': tips,
            'exam': exam_texts,
        }

    def gem_icon(self, color):
        path = os.path.join(self.p.assets, 'Aseprite', f'{color.title()} Gem.aseprite')
        if not os.path.exists(path):
            return None
        out_dir = os.path.join(self.out_icons, 'gems')
        os.makedirs(out_dir, exist_ok=True)
        w, h = aseprite.export(path, os.path.join(out_dir, color + '.png'), frame=0)
        return {'src': f'/wiki/icons/gems/{color}.png', 'width': w, 'height': h}

    # -- cross references
    def link(self, levels, enemies, symbols, powerups, cats, challenges):
        sym_ids = {s['id'] for s in symbols}
        tasks = {t['symbol']: t for t in challenges['symbolTasks']}
        for s in symbols:
            s['task'] = tasks.get(s['id'])
            s['rewardOf'] = [c['id'] for c in challenges['challenges'] if c['reward'].get('symbol') == s['id']]
        for t in challenges['symbolTasks']:
            if t['symbol'] not in sym_ids:
                raise DataError(f"symbol task {t['id']} names unknown symbol {t['symbol']}")
        by_enemy = {e['id']: e for e in enemies}
        for e in enemies:
            threats = set(e['exam'])  # the boss's distinct tests, as the level select shows them
            e['answeredBySymbols'] = [s['id'] for s in symbols if threats & set(s['answers'])] if e['isBoss'] or e['bossOfLevels'] else []
            e['answeredByPowerups'] = [p['id'] for p in powerups if threats & set(p['answers'])] if e['isBoss'] or e['bossOfLevels'] else []
            e['levelStats'] = []
            for a in e['appearances']:
                lvl = next(l for l in levels if l['index'] == a['level'])
                hp = round_half_even(f32(e['hp'] * f32(lvl['hpMultiplier'])))
                e['levelStats'].append({
                    'level': lvl['index'], 'hp': hp,
                    'armor': min(hp, round_half_even(f32(e['armor'] * f32(lvl['hpMultiplier'])))),
                    'firstAttack': [max(1, round_half_even(f32(t * f32(lvl['damageMultiplier'])))) if t else 0
                                    for t in ((at['physical'] + at['magical']) * at['hits'] for at in e['attacks'])],
                })
        for p in powerups:
            p['answersBosses'] = [e['id'] for e in enemies if e['bossOfLevels'] and set(p['answers']) & set(e['exam'])]
        for lvl in levels:
            boss = by_enemy.get(lvl['boss'])
            lvl['bossExam'] = boss['exam'] if boss else []
        for c in cats:
            c['challenges'] = [ch['id'] for ch in challenges['challenges'] if ch['param'] == c['pact']['id']]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('project', help='Unity project root (the folder that holds Assets/ and ProjectSettings/)')
    parser.add_argument('--site', default=os.path.normpath(os.path.join(HERE, '..', '..')),
                        help='website root (default: two levels above this script)')
    parser.add_argument('--report', help='also write the full report (notes, icons not exported) to this JSON file')
    args = parser.parse_args(argv)
    try:
        meta = Extractor(args.project, args.site).run()
    except DataError as err:
        sys.exit(f'extract.py: {err}')
    if args.report:
        with open(args.report, 'w', encoding='utf-8') as fh:
            json.dump(meta, fh, ensure_ascii=False, indent=1)
    print('wrote', ', '.join(f'{k} {v}' for k, v in meta['counts'].items()))
    for note in meta['notes']:
        print('note:', note)
    print(f"icons not exported (outside ICON_DIRS): {len(meta['iconsNotExported'])}")


if __name__ == '__main__':
    main()
