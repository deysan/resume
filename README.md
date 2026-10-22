# Andrii Deisan · Resume

A static CV website built with Astro. Content reflects the October 2026 resume: Product Engineer with a frontend focus, experience at Promova, Memcrab, HolyWater, and Lumi-Dent. No project showcase is included.

The layout follows the supplied Figma reference: black canvas, electric blue accents, white and pale blue rounded cards, oversized typography, and pill-shaped contact links. It adapts to desktop, tablet, and mobile screens without client-side JavaScript.

## Local development

Use Node.js 24 LTS (`nvm use`), then:

```sh
npm ci
npm run dev
```

Open the local URL printed by Astro. For a production preview:

```sh
npm run build
npm run preview
```

`npm run build` runs Astro's type checks and writes a static site to `dist/`. `npm run format:check` checks formatting.

## Updating the content

- `src/data/resume.json` is the shared source for the webpage and downloadable CV. Keep dates, role names, and attribution of team-reported results accurate.
- `src/pages/index.astro` defines the page sections; `src/styles/global.css` contains design tokens and responsive styles.
- `public/andrii-deisan.jpg` is Andrii's public GitHub portrait.
- `public/Andrii_Deisan_CV.pdf` is the downloadable, two-page CV. Regenerate it whenever the shared data changes.

### Regenerate the PDF

The PDF generator is optional for normal web development. It requires Python 3, ReportLab, and Arial font files (installed by default on macOS).

```sh
python3 -m venv .venv
.venv/bin/pip install -r scripts/requirements.txt
.venv/bin/python scripts/build_cv.py
```

On another platform, pass `--font-dir /path/to/fonts` containing `Arial.ttf` and `Arial Bold.ttf`. The script reads the shared JSON and writes the PDF into `public/`. Check both rendered pages after changing the text.

## Deployment status

GitHub Pages is not configured or enabled by this change. There is no deployment workflow. The default build uses the root path for local preview. When publication is approved, configure Astro's `site` and `base` for the chosen GitHub Pages URL, then add the deployment workflow. Asset links already use Astro's `BASE_URL`.
