/**
 * Slots & Skulls facts.
 *
 * Sources (do not add anything that is not in one of these):
 * - Steam store page / appdetails API for app 4428910 (English and Turkish)
 * - PRESS_KIT/Information.txt
 *
 * When the game launches, update `release` (status + wording) here.
 */
import type { Lang } from '../i18n/ui';

export const game = {
  slug: 'slots-and-skulls',
  name: 'Slots & Skulls',
  steamUrl: 'https://store.steampowered.com/app/4428910/Slots__Skulls/',
  steamAppId: 4428910,
  demoUrl: 'https://store.steampowered.com/app/4988090/Slots__Skulls_Demo/',
  developer: 'Trina Interactive',
  publisher: 'Trina Interactive',
  /** From Steam: "Coming soon", 4 Nov, 2026. */
  release: {
    comingSoon: true,
    isoDate: '2026-11-04',
  },
  operatingSystems: ['Windows', 'macOS', 'Linux'],
  /** Genre as listed in the press kit (Information.txt). */
  genres: ['Roguelite', 'Turn-Based Strategy'],
  /** Steam genres. */
  steamGenres: ['Indie', 'RPG', 'Strategy'],
  /** Top user-defined tags on the Steam store page. */
  steamTags: [
    'Roguelite',
    'Auto Battler',
    'Turn-Based Combat',
    'Roguelike',
    'Strategy',
    'Gambling',
    'Roguelike Deckbuilder',
    'Pixel Graphics',
    'Deckbuilding',
    'Turn-Based',
    'Procedural Generation',
    'Turn-Based Strategy',
    'Inventory Management',
    'Loot',
    'Perma Death',
    'RPG',
    'Replay Value',
    '2D',
    'Singleplayer',
    'PvP',
  ],
  /** Steam supported languages (interface). */
  languages: [
    'English',
    'Turkish',
    'French',
    'Italian',
    'German',
    'Spanish - Spain',
    'Dutch',
    'Japanese',
    'Korean',
    'Norwegian',
    'Polish',
    'Portuguese - Brazil',
    'Russian',
    'Simplified Chinese',
    'Spanish - Latin America',
    'Traditional Chinese',
    'Ukrainian',
    'Bulgarian',
    'Czech',
    'Danish',
    'Finnish',
    'Greek',
    'Hungarian',
    'Indonesian',
    'Portuguese - Portugal',
    'Romanian',
    'Swedish',
  ],
  /** BCP 47 codes for the languages above (for JSON-LD). */
  languageCodes: [
    'en', 'tr', 'fr', 'it', 'de', 'es-ES', 'nl', 'ja', 'ko', 'no', 'pl', 'pt-BR', 'ru',
    'zh-Hans', 'es-419', 'zh-Hant', 'uk', 'bg', 'cs', 'da', 'fi', 'el', 'hu', 'id', 'pt-PT',
    'ro', 'sv',
  ],
} as const;

type Section = { heading: string; paragraphs: string[] };
type Requirement = { label: string; value: string };

type GameCopy = {
  /** Steam short description (official). */
  short: string;
  /** Press kit one-liner (Information.txt / previous site). */
  tagline: string;
  metaDescription: string;
  releaseLabel: string;
  sections: Section[];
  facts: {
    modes: string;
    controller: string;
    steamFeatures: string;
    languages: string;
    languageList: string;
  };
  requirements: { os: string; rows: Requirement[] }[];
  faq: { q: string; a: string }[];
};

export const gameCopy: Record<Lang, GameCopy> = {
  en: {
    short:
      'A turn-based roguelite built on a slot machine. Stop the machine to attack, win fights for chests, and upgrade what drops at the forge (if you dare). Or invite a friend and fight them.',
    tagline:
      'A turn-based roguelite built on a slot machine. Spin to attack, open chests for new symbols, strike deals with cats, and risk your symbols at the anvil.',
    metaDescription:
      'Slots & Skulls is a turn-based roguelite built on a slot machine. 112 symbols, a merciless forge, cat pacts and 1v1 duels. Windows, macOS and Linux on Steam.',
    releaseLabel: 'November 4, 2026 (coming soon on Steam)',
    sections: [
      {
        heading: 'Your weapon is a slot machine',
        paragraphs: [
          'Slots & Skulls is a turn-based roguelite. Your weapon is a slot machine, and you build the pool of symbols it can land on: blades, spells, poisons, thorns, gold engines. Stop the machine’s wheels one at a time. Whatever luck hands you decides the fate of that turn.',
        ],
      },
      {
        heading: 'In control, but not quite',
        paragraphs: [
          '112 different symbols: common ones that drop easily from kills, and legendary ones that only bosses drop. Every symbol has its own effect. Some boost the symbol next to them, some spend your health, some damage the enemy, some pay you gold. A few call for quick-fingered skill checks.',
          'After every fight the shop opens. Buy new symbols and power-ups, reroll the stock, lock a symbol you cannot afford yet, or remove a symbol you have outgrown to streamline your build. A chart in the shop shows exactly what a purchase does to your attack, defense, gold, pool size and kill speed.',
          'Four active power-ups sit on the d-pad, ready whenever you want them. Up to eight passive power-ups make you readier for the hard fights.',
        ],
      },
      {
        heading: 'More risk, more reward on every level',
        paragraphs: [
          'Ten levels, five fights each, 33 different enemies drawn pixel by pixel. Physical attacks do nothing to armored enemies, but magic goes straight through. Archers can stun you, ice mages can freeze one of your wheels, burn damage keeps eating your health in real time, and thieves lift gold from your purse mid fight.',
          'Replay a level you already beat on raised difficulty modes for more symbols, skulls or gems. The higher the difficulty, the more you earn, and the tougher the enemies.',
        ],
      },
      {
        heading: 'The forge does not joke',
        paragraphs: [
          'At the forge you can raise a symbol from +0 to +10. The higher its level, the lower the chance of reaching the next one, and if the upgrade fails you lose the symbol completely. Gems help: a green gem slightly improves the upgrade chance, a blue gem turns a destroyed symbol into a one-level drop, and the extremely rare yellow gem guarantees the upgrade.',
          'Every fight you win pays skulls, and you keep them even when you die. Spend them at the forge, on modifiers, on adopting a cat, or on abilities.',
        ],
      },
      {
        heading: 'Cats, abilities and modifiers',
        paragraphs: [
          'Before a run you can bring a cat. Every cat comes with a pact that lasts the whole run: one advantage and one disadvantage. Six different abilities, each usable once per fight, change the game from top to bottom. 21 modifiers, activated with skulls, add things like more health, more damage, a last move when you die, or two more wheels on the slot machine.',
        ],
      },
      {
        heading: 'Play with your friends',
        paragraphs: [
          'Invite a friend from your Steam list and play 1v1. A match opens with a draft, then you both beat the same enemies on your own screens, buying symbols from the shop after every fight. After four fights you duel each other. After the duels the anvil opens. First to the set number of rounds wins. Prefer to skip the enemies? Pick Duel Only mode.',
        ],
      },
      {
        heading: 'Auto mode for idle lovers',
        paragraphs: [
          'Turn on Auto Mode and the reels stop themselves; you only step in when a symbol calls for a skill check. Auto 2X Mode makes everything twice as fast. In Endless Mode you can enable Full Auto Mode and test your build without any interaction.',
        ],
      },
    ],
    facts: {
      modes: 'Single-player, online 1v1 PvP',
      controller: 'Full controller support',
      steamFeatures: 'Steam Achievements, Steam Cloud, Steam Leaderboards',
      languageList:
        'English, Turkish, French, Italian, German, Spanish - Spain, Dutch, Japanese, Korean, Norwegian, Polish, Portuguese - Brazil, Russian, Simplified Chinese, Spanish - Latin America, Traditional Chinese, Ukrainian, Bulgarian, Czech, Danish, Finnish, Greek, Hungarian, Indonesian, Portuguese - Portugal, Romanian, Swedish',
      languages: '27 supported languages, including English and Turkish',
    },
    requirements: [
      {
        os: 'Windows (minimum)',
        rows: [
          { label: 'OS', value: 'Windows 10 64-bit' },
          { label: 'Processor', value: '2.0 GHz Dual Core' },
          { label: 'Memory', value: '4 GB RAM' },
          { label: 'Graphics', value: 'DirectX 11 compatible GPU with 1GB VRAM' },
          { label: 'DirectX', value: 'Version 11' },
          { label: 'Storage', value: '1 GB available space' },
        ],
      },
      {
        os: 'macOS (minimum)',
        rows: [
          { label: 'OS', value: 'macOS 10.15 Catalina or newer' },
          { label: 'Processor', value: '2.0 GHz Dual Core (or Apple Silicon)' },
          { label: 'Memory', value: '4 GB RAM' },
          { label: 'Graphics', value: 'Metal compatible GPU' },
          { label: 'Storage', value: '1 GB available space' },
        ],
      },
      {
        os: 'Linux (minimum)',
        rows: [
          { label: 'Processor', value: '2.0 GHz Dual Core' },
          { label: 'Memory', value: '1 GB RAM' },
          { label: 'Graphics', value: 'DirectX 11 compatible GPU with 1GB VRAM' },
          { label: 'Storage', value: '1 GB available space' },
        ],
      },
    ],
    faq: [
      {
        q: 'What is Slots & Skulls?',
        a: 'A turn-based roguelite built on a slot machine. You build the pool of symbols your slot machine can land on, stop its wheels to attack, win chests after fights and upgrade symbols at the forge, where a failed upgrade destroys the symbol.',
      },
      {
        q: 'When does Slots & Skulls come out?',
        a: 'Steam lists the release date as November 4, 2026.',
      },
      {
        q: 'Which platforms is it on?',
        a: 'Windows, macOS and Linux, on Steam.',
      },
      {
        q: 'Is there a demo?',
        a: 'Yes. A free demo is available on Steam.',
      },
      {
        q: 'Does it have multiplayer?',
        a: 'Yes. You can invite a friend from your Steam list and play online 1v1, either with enemies between duels or in Duel Only mode.',
      },
      {
        q: 'Can I play with a controller?',
        a: 'Yes. Steam lists full controller support, including DualShock and DualSense controllers.',
      },
      {
        q: 'Who makes Slots & Skulls?',
        a: 'Trina Interactive, which is both the developer and the publisher.',
      },
    ],
  },
  tr: {
    short:
      'Slot makinesi üzerine kurulu sıra tabanlı bir roguelite. Saldırmak için makineyi durdur, dövüşleri kazanarak sandıklar elde et, sandıklardan çıkan eşyaları demircide yükselt (yiyorsa). Ya da bir arkadaşını davet et, onunla dövüş.',
    tagline:
      'Slot makinesi üzerine kurulu sıra tabanlı bir roguelite. Saldırmak için makineyi durdur, dövüşleri kazanarak sandıklar elde et, sandıklardan çıkan eşyaları demircide yükselt (yiyorsa). Ya da bir arkadaşını davet et, onunla dövüş.',
    metaDescription:
      'Slots & Skulls, slot makinesi üzerine kurulu sıra tabanlı bir roguelite: 112 sembol, acımasız demirci, kedi anlaşmaları ve 1v1 düellolar. Steam’de çok yakında.',
    releaseLabel: '4 Kasım 2026 (Steam’de çok yakında)',
    sections: [
      {
        heading: 'Silahın bir slot makinesi',
        paragraphs: [
          'Slots & Skulls sıra tabanlı bir roguelite. Silahın bir slot makinesi ve gelebilecek sembollerin havuzunu sen oluşturuyorsun: kılıçlar, büyüler, zehirler, dikenler, altın düzenekleri. Makinenin çarklarını tek tek durdur. Şansına ne gelirse o turun kaderini belirler.',
        ],
      },
      {
        heading: 'Kontrol hem sende hem değil',
        paragraphs: [
          'Çeşit çeşit 112 ayrı sembol: düşmanları öldürerek kolayca düşürebileceğin sıradan semboller de var, sadece bosslardan düşen efsanevi semboller de. Her sembolün kendine özel bir etkisi var. Kimi yanındakinin etkisini artırır, kimi canını harcar, kimi düşmana hasar verir, kimi sana altın öder. Birkaçı el çabukluğu gerektiren beceri oyunları içerir.',
          'Her dövüşten sonra dükkân açılır. Yeni semboller ve güçlendirmeler alabilir, stokları yenileyebilir, henüz paran yetmeyen bir sembolü kilitleyebilir ya da artık işine yaramayan bir sembolü havuzdan çıkarıp build’ini sadeleştirebilirsin. Dükkândaki grafik, bir alışverişin saldırına, savunmana, altınına, havuz boyutuna ve öldürme hızına ne yapacağını gösterir.',
          'Dört aktif güçlendirmeyi yön tuşlarıyla dilediğin an kullanabilirsin. Sekize kadar pasif güçlendirmeyle zorlu savaşlara daha hazır girersin.',
        ],
      },
      {
        heading: 'Her seviyede daha fazla risk, daha fazla ödül',
        paragraphs: [
          'On seviye, her birinde beş dövüş, piksel piksel elle tasarlanmış 33 ayrı düşman. Zırhlı düşmanlara fiziksel saldırı işlemez ama büyü içinden geçer. Okçular seni sersemletebilir, buz büyücüleri bir çarkını dondurabilir, yanma hasarı gerçek zamanda sağlığını tüketir, hırsızlar dövüşün ortasında kesenden altın yürütür.',
          'Geçtiğin bir seviyeyi daha fazla sembol, kurukafa ya da cevher için artırılmış zorluk modlarında yeniden oynayabilirsin. Zorluk arttıkça elde edeceklerin artar, düşmanlar da zorlaşır.',
        ],
      },
      {
        heading: 'Demircinin şakası yok',
        paragraphs: [
          'Demircide bir sembolü +0’dan +10’a kadar yükseltebilirsin. Seviye arttıkça bir sonrakine geçme ihtimali düşer ve yükseltme başarısız olursa sembolü tamamen kaybedersin. Cevherler işini kolaylaştırır: yeşil cevher yükselme ihtimalini biraz artırır, mavi cevher başarısızlıkta sembolü yok etmek yerine bir seviye düşürür, aşırı nadir sarı cevher ise yükseltmeyi garanti eder.',
          'Galip geldiğin her dövüşte kurukafa kazanırsın ve ölsen bile kaybetmezsin. Kurukafaları demircide, geliştirmelerde, kedi sahiplenmekte ya da yeteneklerde kullanabilirsin.',
        ],
      },
      {
        heading: 'Kediler, yetenekler ve geliştirmeler',
        paragraphs: [
          'Her run öncesi yanına bir kedi alabilirsin. Her kedi run boyunca geçerli bir anlaşmayla gelir: bir avantaj, bir de dezavantaj. Her dövüşte bir kez kullanılabilen altı ayrı yetenek oynanışı baştan sona değiştirir. Kurukafalarla aktif edilen 21 geliştirme; daha yüksek sağlık, daha fazla hasar, öldüğünde son bir hamle ya da slot makinesine iki çark daha gibi şeyler ekler.',
        ],
      },
      {
        heading: 'Arkadaşlarınla oyna',
        paragraphs: [
          'Steam arkadaş listenden birini davet et ve 1’e 1 oyna. Maç bir seçim turuyla başlar; ikiniz de kendi ekranınızda aynı düşmanları yenersiniz, her dövüşün ardından dükkândan sembol alırsınız. Dört dövüşün sonunda düello yaparsınız. Düellolardan sonra demirci açılır. Belirlenen tur sayısını ilk tamamlayan kazanır. Düşmanlarla uğraşmak istemezseniz Sadece Düello modunu seçin.',
        ],
      },
      {
        heading: 'Idle oyun sevenlere Oto Mod',
        paragraphs: [
          'Oto Modu açtığında çarkları senin yerine o durdurur; sen yalnızca bir sembol beceri testi istediğinde devreye girersin. Oto 2X Mod her şeyi 2 kat hızlandırır. Sonsuz Modda Tam Oto Modu açıp build’inin gücünü hiçbir şeye dokunmadan test edebilirsin.',
        ],
      },
    ],
    facts: {
      modes: 'Tek oyunculu, çevrim içi 1v1 PvP',
      controller: 'Tam kontrolcü desteği',
      steamFeatures: 'Steam Başarımları, Steam Cloud, Steam Sıralama Listeleri',
      languageList:
        'İngilizce, Türkçe, Fransızca, İtalyanca, Almanca, Kastilya İspanyolcası, Felemenkçe, Japonca, Korece, Norveççe, Lehçe, Brezilya Portekizcesi, Rusça, Basitleştirilmiş Çince, Latin Amerika İspanyolcası, Geleneksel Çince, Ukraynaca, Bulgarca, Çekçe, Danca, Fince, Yunanca, Macarca, Endonezce, Portekizce - Portekiz, Rumence, İsveççe',
      languages: 'Türkçe ve İngilizce dahil 27 dil desteği',
    },
    requirements: [
      {
        os: 'Windows (minimum)',
        rows: [
          { label: 'İşletim Sistemi', value: 'Windows 10 64-bit' },
          { label: 'İşlemci', value: '2.0 GHz Çift Çekirdek' },
          { label: 'Bellek', value: '4 GB RAM' },
          { label: 'Ekran Kartı', value: 'DirectX 11 uyumlu, 1GB VRAM’li GPU' },
          { label: 'DirectX', value: 'Sürüm 11' },
          { label: 'Depolama', value: '1 GB kullanılabilir alan' },
        ],
      },
      {
        os: 'macOS (minimum)',
        rows: [
          { label: 'İşletim Sistemi', value: 'macOS 10.15 Catalina veya üzeri' },
          { label: 'İşlemci', value: '2.0 GHz Çift Çekirdek (veya Apple Silicon)' },
          { label: 'Bellek', value: '4 GB RAM' },
          { label: 'Ekran Kartı', value: 'Metal uyumlu GPU' },
          { label: 'Depolama', value: '1 GB kullanılabilir alan' },
        ],
      },
      {
        os: 'Linux (minimum)',
        rows: [
          { label: 'İşlemci', value: '2.0 GHz Çift Çekirdek' },
          { label: 'Bellek', value: '1 GB RAM' },
          { label: 'Ekran Kartı', value: 'DirectX 11 uyumlu, 1GB VRAM’li GPU' },
          { label: 'Depolama', value: '1 GB kullanılabilir alan' },
        ],
      },
    ],
    faq: [
      {
        q: 'Slots & Skulls nedir?',
        a: 'Slot makinesi üzerine kurulu sıra tabanlı bir roguelite. Slot makinenin sembol havuzunu sen kurarsın, saldırmak için çarkları durdurursun, dövüşlerden sonra sandık kazanır ve sembollerini demircide yükseltirsin; yükseltme başarısız olursa sembol yok olur.',
      },
      {
        q: 'Slots & Skulls ne zaman çıkıyor?',
        a: 'Steam’deki çıkış tarihi 4 Kasım 2026.',
      },
      {
        q: 'Hangi platformlarda?',
        a: 'Steam üzerinden Windows, macOS ve Linux.',
      },
      {
        q: 'Demosu var mı?',
        a: 'Evet. Steam’de ücretsiz bir demo var.',
      },
      {
        q: 'Çok oyunculu modu var mı?',
        a: 'Evet. Steam arkadaş listenden birini davet edip çevrim içi 1v1 oynayabilirsin; düellolar arasında düşmanlarla ya da Sadece Düello modunda.',
      },
      {
        q: 'Kontrolcüyle oynanır mı?',
        a: 'Evet. Steam’de DualShock ve DualSense dahil tam kontrolcü desteği listeleniyor.',
      },
      {
        q: 'Slots & Skulls’ı kim yapıyor?',
        a: 'Trina Interactive. Hem geliştirici hem yayıncı.',
      },
    ],
  },
};
