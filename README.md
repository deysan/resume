# Andrii Deisan · Resume

A static CV website built with Astro. Content reflects the October 2026 resume: Product Engineer with a frontend focus, experience at Promova, Memcrab, HolyWater, and Lumi-Dent. No project showcase is included.

The layout follows the supplied Figma reference: black canvas, electric blue accents, white and pale blue rounded cards, oversized typography, and pill-shaped contact links. It adapts to desktop, tablet, and mobile screens without client-side JavaScript.

## Local development

Use Node.js 24 LTS (`nvm use`), then:

```sh
npm ci
npm run dev
```

Open the local URL printed by Astro with the `/resume/` path. For a production preview:

```sh
npm run build
npm run preview
```

`npm run build` runs Astro's type checks and writes a static site to `dist/`. `npm run format:check` checks formatting.

## Updating the content

- `src/data/resume.json` is the shared source for the webpage and downloadable CV. Keep dates, role names, and attribution of team-reported results accurate. The `pdf` field preserves the original resume summary and two-column skill grouping; experience and learning are shared.
- `src/pages/index.astro` defines the page sections; `src/styles/global.css` contains design tokens and responsive styles.
- `public/andrii-deisan.jpg` is the original 2000 × 2000 portrait supplied by Andrii.
- `assets/cv-portrait.png` is the separate photo supplied for the PDF; it does not replace the website portrait.
- `public/Andrii_Deisan_CV.pdf` is the downloadable, two-page CV, styled after the user’s resume.io reference (serif blue headings, photo header, and two-column skills). Regenerate it whenever the shared data changes.

### Regenerate the PDF

The PDF generator is optional for normal web development. It requires Python 3, ReportLab, and Arial / Georgia Bold font files (installed by default on macOS).

```sh
python3 -m venv .venv
.venv/bin/pip install -r scripts/requirements.txt
.venv/bin/python scripts/build_cv.py
```

On another platform, pass `--font-dir /path/to/fonts` containing `Arial.ttf`, `Arial Bold.ttf`, and `Georgia Bold.ttf`. The script reads the shared JSON and writes the PDF into `public/`. Check both rendered pages after changing the text.

## GitHub Pages

The public website is hosted at [deysan.github.io/resume](https://deysan.github.io/resume/). Astro uses this site origin and the `/resume/` base path; asset links use Astro's `BASE_URL`.

`.github/workflows/pages.yml` checks formatting and builds pull requests. Pushes to `main` also publish the static `dist/` output through GitHub Actions. The workflow can be run manually from `main`. Repository Settings → Pages must use GitHub Actions as its source.

The PDF includes this address as a separate Web resume link on page two, configured by `pdf.webResumeUrl` in `src/data/resume.json`. Regenerate and commit the PDF when its content changes; deployment serves the committed file without requiring fonts or Python in CI.
