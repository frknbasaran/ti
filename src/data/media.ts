/**
 * Press-kit imagery (sources: PRESS_KIT/IMAGES). Astro optimizes these at build time.
 * Alt texts describe only what is visible in each image.
 */
import fightView from '../assets/slots-and-skulls/screenshots/fight_view.jpg';
import lootView from '../assets/slots-and-skulls/screenshots/loot_view.jpg';
import upgradeView from '../assets/slots-and-skulls/screenshots/upgrade_view.jpg';
import modifiersView from '../assets/slots-and-skulls/screenshots/modifiers_view.jpg';
import keyArt from '../assets/slots-and-skulls/art/key_art_with_logo.png';
import keyArtNoLogo from '../assets/slots-and-skulls/art/key_art_without_logo.png';
import logo from '../assets/slots-and-skulls/art/logo_transparent.png';
import biberSlot from '../assets/slots-and-skulls/art/biber_with_slot_machine.png';
import headerCapsule from '../assets/slots-and-skulls/art/header_capsule.png';
import libraryCapsule from '../assets/slots-and-skulls/art/library_capsule.png';
import biber from '../assets/slots-and-skulls/characters/character_biber.png';
import pati from '../assets/slots-and-skulls/characters/character_pati.png';
import ogre from '../assets/slots-and-skulls/characters/character_ogre.png';
import mage from '../assets/slots-and-skulls/characters/character_skeleton_high_mage.png';
import knight from '../assets/slots-and-skulls/characters/character_trina_s_knight.png';

// `?url` imports emit the untouched original file, used for full-size press downloads.
import fightViewFile from '../assets/slots-and-skulls/screenshots/fight_view.jpg?url';
import lootViewFile from '../assets/slots-and-skulls/screenshots/loot_view.jpg?url';
import upgradeViewFile from '../assets/slots-and-skulls/screenshots/upgrade_view.jpg?url';
import modifiersViewFile from '../assets/slots-and-skulls/screenshots/modifiers_view.jpg?url';
import keyArtFile from '../assets/slots-and-skulls/art/key_art_with_logo.png?url';
import keyArtNoLogoFile from '../assets/slots-and-skulls/art/key_art_without_logo.png?url';
import logoFile from '../assets/slots-and-skulls/art/logo_transparent.png?url';
import biberSlotFile from '../assets/slots-and-skulls/art/biber_with_slot_machine.png?url';
import headerCapsuleFile from '../assets/slots-and-skulls/art/header_capsule.png?url';
import libraryCapsuleFile from '../assets/slots-and-skulls/art/library_capsule.png?url';
import biberFile from '../assets/slots-and-skulls/characters/character_biber.png?url';
import patiFile from '../assets/slots-and-skulls/characters/character_pati.png?url';
import ogreFile from '../assets/slots-and-skulls/characters/character_ogre.png?url';
import mageFile from '../assets/slots-and-skulls/characters/character_skeleton_high_mage.png?url';
import knightFile from '../assets/slots-and-skulls/characters/character_trina_s_knight.png?url';

type Alt = { en: string; tr: string };

export const screenshots: { src: ImageMetadata; file: string; alt: Alt; name: string }[] = [
  {
    src: fightView, file: fightViewFile,
    name: 'fight_view',
    alt: {
      en: 'Slots & Skulls boss fight: the slot machine grid with HP and shield bars on the left, the mounted Knight of Trina on the right.',
      tr: 'Slots & Skulls boss dövüşü: solda can ve kalkan çubuklarıyla slot makinesi, sağda atlı Knight of Trina.',
    },
  },
  {
    src: lootView, file: lootViewFile,
    name: 'loot_view',
    alt: {
      en: 'Slots & Skulls loot screen: a 56 gold reward that buys symbols and power-ups in the shop between fights.',
      tr: 'Slots & Skulls ganimet ekranı: dövüşler arasında dükkânda sembol ve güçlendirme almaya yarayan 56 altın ödülü.',
    },
  },
  {
    src: upgradeView, file: upgradeViewFile,
    name: 'upgrade_view',
    alt: {
      en: 'Slots & Skulls anvil screen: upgrading the Executioner’s Coin symbol from +0 to +1 with gems, or smelting it into skulls.',
      tr: 'Slots & Skulls demirci ekranı: Executioner’s Coin sembolünü cevherlerle +0’dan +1’e yükseltme ya da kurukafaya eritme.',
    },
  },
  {
    src: modifiersView, file: modifiersViewFile,
    name: 'modifiers_view',
    alt: {
      en: 'Slots & Skulls modifiers screen: a grid of permanent powers bought with skulls, such as Iron Skin, Vitality and Extra Wheel.',
      tr: 'Slots & Skulls geliştirmeler ekranı: Iron Skin, Vitality ve Extra Wheel gibi kurukafayla alınan kalıcı güçler.',
    },
  },
];

export const art: { src: ImageMetadata; file: string; alt: string; name: string }[] = [
  { src: keyArt, file: keyArtFile, name: 'Key art (with logo)', alt: 'Slots & Skulls key art with logo: a golden slot machine, a cat pulling its lever and a skeleton mage.' },
  { src: keyArtNoLogo, file: keyArtNoLogoFile, name: 'Key art (no logo)', alt: 'Slots & Skulls key art without logo: a golden slot machine, a cat pulling its lever and a skeleton mage.' },
  { src: logo, file: logoFile, name: 'Logo (transparent)', alt: 'Slots & Skulls logo in gold pixel letters.' },
  { src: biberSlot, file: biberSlotFile, name: 'Biber with the slot machine', alt: 'Biber, an orange pixel-art cat, pulling the lever of a golden slot machine.' },
  { src: headerCapsule, file: headerCapsuleFile, name: 'Steam header capsule', alt: 'Slots & Skulls Steam header capsule: the gold logo next to a golden slot machine and Biber the cat.' },
  { src: libraryCapsule, file: libraryCapsuleFile, name: 'Steam library capsule', alt: 'Slots & Skulls vertical Steam library capsule: the gold logo above a golden slot machine and Biber the cat.' },
];

export const characters: { src: ImageMetadata; file: string; alt: string; name: string }[] = [
  { src: knight, file: knightFile, name: 'Knight of Trina', alt: 'Knight of Trina: an armored pixel-art knight with a lance, riding an armored horse.' },
  { src: mage, file: mageFile, name: 'Skeleton High Mage', alt: 'Skeleton High Mage: a hooded pixel-art skeleton holding a skull-topped staff.' },
  { src: ogre, file: ogreFile, name: 'Ogre', alt: 'Ogre: a two-headed pixel-art ogre in a red loincloth.' },
  { src: biber, file: biberFile, name: 'Biber', alt: 'Biber: a sitting orange pixel-art cat.' },
  { src: pati, file: patiFile, name: 'Pati', alt: 'Pati: a sitting white pixel-art cat.' },
];
