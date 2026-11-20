# Ultra OV NL website

Public website for Ultra OV NL: the Dutch homepage plus the privacy policy, terms of use, support and account-deletion pages that Google Play and the App Store link to. Live at https://ultraov.nl.

Plain HTML and CSS, no framework and no build step to serve it. No cookies, analytics or third-party requests.

## Structure

| Path | What |
|---|---|
| `public/` | Everything that is served. `public/index.html` is the homepage and the layout source. |
| `src/pages/` | Bodies of the legal and support pages (`*-nl.html`, `*-en.html`, `404.html`). |
| `tools/build.py` | Wraps `src/pages/*` in the homepage header and footer and writes them into `public/`. |
| `server.js` | Zero-dependency Node static server with clean URLs, security headers and a 404 page. |

## Editing

- Homepage: edit `public/index.html` directly.
- Legal/support pages: edit the file in `src/pages/`, then run `python3 tools/build.py` and commit both.
- Changing the header or footer: edit it in `public/index.html`, then run `python3 tools/build.py`.
- Update the "Laatst bijgewerkt / Last updated" date when the privacy policy or terms change, in both languages.

## Run locally

```bash
npm start            # serves public/ on http://localhost:8080
PORT=3000 npm start  # another port
```

Requires Node 18 or newer. `SERVER_PORT` (set by the hosting panel) takes precedence over `PORT`.

## URLs for the store listings

| Store field | URL |
|---|---|
| Privacy policy | https://ultraov.nl/privacy |
| Account deletion (Google Play) | https://ultraov.nl/account-verwijderen |
| Support / contact | https://ultraov.nl/support |
| Website | https://ultraov.nl |

English versions live under `/en/` (`/en/privacy`, `/en/terms`, `/en/support`, `/en/delete-account`).

## Brand

Colours, logo and tone follow the Ultra OV NL brand guide (November 2026): gold `#EEA614`, navy `#0B1530`, peach `#FAD8BA`, system font stack, light and dark themes via `prefers-color-scheme`. Example data on the homepage is labelled "Voorbeeldgegevens - niet live".

The legal texts are templates written to match the app's actual data handling. They are not legal advice.
