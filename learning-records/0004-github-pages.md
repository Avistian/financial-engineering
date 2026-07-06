# GitHub Pages enabled

Static site deploys via `.github/workflows/pages.yml`: on every push to `main` it stamps
`index.html` with the manifest version (cache-bust), assembles `public/` from `index.html`,
`.nojekyll`, `assets/`, `lessons/`, `reference/`, and the lab notebook sources + README, then
publishes through GitHub Actions. `.nojekyll` disables Jekyll so the plain `assets/`/`lessons/`
folders serve as-is.

Target URL: **https://avistian.github.io/financial-engineering/** — requires (1) a push to `main`
and (2) repo **Settings → Pages → Build and deployment → Source = GitHub Actions** (one-time).
The manifest-driven home nav needs HTTP (it `fetch()`es `lessons/manifest.json`), which Pages
provides; opening files via `file://` locally still shows the fallback link.
