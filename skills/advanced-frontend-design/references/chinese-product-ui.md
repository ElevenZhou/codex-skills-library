# Chinese-Language Product UI

Guidance for products whose primary audience reads Chinese (zh-CN first; zh-TW/HK noted where different). This overrides the generic "avoid system font stacks" default for body text: for CJK, a good system stack is often the right answer. Baseline rules for CJK typography are in [states-and-a11y.md](states-and-a11y.md) section 6; do not repeat them here.

## 1. Font Stacks

Principle: put the Latin/numeral face you want first, then Chinese fallbacks. The browser picks glyphs per character, so a Latin display font in front costs nothing for Chinese text.

```css
:root {
  /* Sans: system first, zero download, matches the OS */
  --font-sans: "Your Latin Face", -apple-system, BlinkMacSystemFont, "PingFang SC",
    "HarmonyOS Sans SC", "Noto Sans SC", "Source Han Sans SC", "Microsoft YaHei UI",
    "Microsoft YaHei", "Hiragino Sans GB", sans-serif;
  /* Serif: editorial / long-form */
  --font-serif: "Your Latin Serif", "Noto Serif SC", "Source Han Serif SC", "Songti SC",
    "STSong", "SimSun", serif;
  --font-mono: "JetBrains Mono", "SF Mono", Menlo, Consolas, "Noto Sans Mono CJK SC", monospace;
}
html { font-family: var(--font-sans); }
html:lang(zh-TW) { font-family: "PingFang TC", "Noto Sans TC", "Microsoft JhengHei", sans-serif; }
```

Free, open-licensed Chinese fonts (confirm each license before shipping; these are commonly SIL OFL, which allows commercial use and embedding):

| Font | Character | Source |
| --- | --- | --- |
| Noto Sans SC / Noto Serif SC | Neutral, complete weights, same design as Source Han | Google Fonts; npm `@fontsource/noto-sans-sc` |
| Source Han Sans / Serif (思源黑体/宋体) | Adobe/Google open release of the same family | GitHub releases |
| LXGW WenKai (霞鹜文楷) | Humanist kai-style, warm, good for editorial and cultural brands | GitHub, community-maintained web builds |
| ZCOOL KuaiLe / XiaoWei / QingKe HuangYou | Display and playful headline faces | Google Fonts |

Other popular free-for-commercial families (HarmonyOS Sans, MiSans, Alibaba PuHuiTi) have their own license terms; read them rather than assuming OFL.

**Delivery cost is the real problem.** A full CJK font is 4-20 MB. Rules:

- Prefer system fonts for body text and long UI. Use a web font only for the display layer (headings, brand, numerals).
- Subset to the characters used (pyftsubset from fonttools, or `unicode-range` slices as Google Fonts and Fontsource do) and serve WOFF2 with `font-display: swap`.
- **Self-host.** Google Fonts and other foreign CDNs can be slow or blocked from mainland China, and the free-first rule in `free-toolkit.md` already prefers local files. `verify_frontend.py` flags remote font hosts.
- Weights: Chinese body at 400, emphasis at 500-600; avoid 300 on small text (thin strokes break up at 12-14px on low-DPI screens).

## 2. Density and Size Norms

- Chinese consumer apps (e-commerce, content, super-apps) accept and expect higher information density than Western equivalents: tighter spacing, more modules per screen, visible price/promotion/social-proof. Density is not disorder: keep one clear primary action and a stable grid.
- Mobile body 14-16px, secondary 12-13px, never below 11px. Desktop admin tools: 14px base (Ant Design default) with 8px-based spacing; 13px in dense tables is acceptable.
- Headings are rarely above 28-32px on mobile; hierarchy comes from weight and color more than scale.
- 适老化 (senior-friendly) mode: base 17-18px+, 48px targets, high contrast, fewer simultaneous choices. Required in practice for public-service, banking, and health products.
- Red/green semantics are reversed relative to Western finance: in mainland A-share/fund products, **red = up/gain, green = down/loss**. Match the audience convention, add arrows and signs so the meaning never depends on color.

## 3. Mobile-First: H5 and Mini Programs (小程序)

- Design on a 375pt (iPhone) or 750px (2x) artboard. In WeChat mini programs, `rpx` makes 750rpx equal the screen width; use `rpx` for layout, `px` for hairlines.
- Reserve safe areas: `env(safe-area-inset-top/bottom)` for notch and home indicator. In a WeChat mini program, the top-right capsule button sits beside the status bar and varies by device; do not put actions under it. Use the platform API to read its rect rather than hard-coding.
- Navigation: bottom tab bar with 3-5 destinations (WeChat limits the native tabBar to 5), page title in the top bar, back at top-left. Avoid hamburger menus for primary destinations.
- Primary action fixed at the bottom within thumb reach, above the safe-area inset (e.g. "立即购买", "提交"). Keep bottom bars under ~64px plus inset.
- Sharing is a first-class feature: define the share card (title, 5:4 image) per page. Design the post-payment and result pages as shareable moments.
- Authorization: ask for login/phone/location at the moment of need, with a one-line reason, not on first launch. Provide a visible refuse path.
- No hover-only affordances; use pull-to-refresh and bottom-sheet patterns that users already know from WeChat/Alipay.
- In-app browsers (WeChat, Alipay, Douyin) behave differently from Safari/Chrome: test fixed positioning, viewport height (`dvh`), file upload, and back-button behavior in the actual host. Not verifiable by the static script; test on device.
- Compliance surfaces that must exist: privacy policy and user agreement links before sign-in, and for websites the ICP filing number in the footer. Treat as layout elements, not afterthoughts.

## 4. Number, Date, and Currency Formats

| Item | Convention |
| --- | --- |
| Date | `2026年11月12日` in prose; `2026-11-12` or `2026/11/12` in dense UI; order year-month-day always |
| Time | 24-hour `14:05` is standard; avoid AM/PM |
| Weekday | `周四` (or `星期四` in formal copy); week starts Monday in most Chinese products |
| Relative | `刚刚`, `5分钟前`, `昨天 18:30`, then absolute dates; use `Intl.RelativeTimeFormat('zh-CN')` |
| Currency | `¥1,234.50` (prefix, 2 decimals); `元` in prose/table headers; label currency when mixed |
| Large numbers | Consumer: `1.2万`, `3.4亿` (units at 10^4 and 10^8); B2B/finance: full digits with thousands separators; never mix both on one screen |
| Percent / delta | `+12.3%` with sign; fixed decimals per column |
| Phone | `138 0013 8000` grouping; validate 11 digits starting with 1 |
| Names | Single `姓名` field; surname-first; do not split into first/last |
| Address | Largest to smallest: province, city, district, street, unit; offer region pickers |

Use `Intl.NumberFormat('zh-CN', { style: 'currency', currency: 'CNY' })` and `Intl.DateTimeFormat('zh-CN', ...)`, and verify their output against the table.

## 5. Brand Color Without the Clichés

Overused defaults to challenge: "tech blue" (#1677ff-family) everywhere, blue-purple gradients, red-gold for everything festive or official, WeChat green, Taobao orange, and dark navy with neon cyan for any "AI" product. These are fine only when they are the actual brand.

Method: derive the accent from the subject, then test it against category neighbors.

- Pull from the material world of the product: tea (茶青, 黛), ink (墨 + 宣纸 off-white), lacquer and cinnabar (朱砂, a warm red that is not "festival red"), porcelain (月白, 天青), turmeric/gamboge (藤黄), bamboo (竹青). Use as an accent role, not as costume; avoid dragon/cloud/seal motifs unless the brand is about heritage.
- Keep one accent plus neutrals. Chinese UIs often carry many promotional colors; restrain them to one "promotion" role (usually red or orange) and keep the rest calm.
- Check cultural semantics: white and black are not forbidden in modern UI; red means gain and good fortune (but also an error in forms: pair with icon and text); gold implies luxury or official.
- Verify contrast on the chosen accent for text on white and for white-on-accent buttons (4.5:1).

## 6. Review Questions for Chinese UI

- Is `lang="zh-CN"` set and does the Latin/CJK mix look balanced (baseline, size)?
- Is a CJK web font used where a system font would do, and is it subset and self-hosted?
- Do text blocks have 1.7+ line-height and zero letter-spacing on Chinese?
- Are red/green and 万/亿 conventions consistent with the audience?
- On mobile: safe areas, capsule overlap, thumb-reach primary action, share card?
