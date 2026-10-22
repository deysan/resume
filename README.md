# Andrii Deisan · Resume

Personal resume website built with Astro, with professional experience, skills, education, and a downloadable PDF.

[Web resume](https://deysan.github.io/resume/) · [Download CV](https://deysan.github.io/resume/Andrii_Deisan_CV.pdf)

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

- `src/data/resume.json` — content shared by the website and PDF. The `pdf` field contains the PDF summary, skill grouping, and web resume URL.
- `src/pages/index.astro` — page structure.
- `src/styles/global.css` — styles and responsive layout.
- `src/assets/andrii-deisan.jpg` — original website portrait. Astro generates responsive WebP images during the build.
- `assets/cv-portrait.jpg` — optimized 400 × 400 JPEG portrait for the PDF.
- `public/Andrii_Deisan_CV.pdf` — downloadable CV. Regenerate it after updating resume content.

### Regenerate the PDF

Requires Python 3, ReportLab, and the Arial and Georgia Bold fonts.

```sh
python3 -m venv .venv
.venv/bin/pip install -r scripts/requirements.txt
.venv/bin/python scripts/build_cv.py
```

The generator uses macOS system fonts by default. For another font directory, pass `--font-dir /path/to/fonts` containing `Arial.ttf`, `Arial Bold.ttf`, and `Georgia Bold.ttf`. Review both pages and commit the generated PDF.

## GitHub Pages

Astro uses `https://deysan.github.io` as the site origin and `/resume/` as the base path. Asset links use Astro's `BASE_URL`.

`.github/workflows/pages.yml` checks formatting and builds pull requests. Pushes to `main` publish `dist/` to GitHub Pages, including the committed PDF. The workflow can also be run manually from `main`. In repository Settings → Pages, select GitHub Actions as the source.
