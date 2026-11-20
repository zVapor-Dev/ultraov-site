"""Builds the legal and support pages: wraps src/pages/*.html in the homepage header/footer.
Run after editing a page or the homepage layout: python3 tools/build.py

Wraps page bodies in the shared header/footer. Output is plain static HTML committed to the repo."""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
G = ROOT / 'src' / 'pages'
SITE = ROOT / 'public'
# The homepage is the layout source: header = everything before <main>, footer = from </main>.
_index = (SITE / 'index.html').read_text()
header = _index[: _index.index('<main id="inhoud">')]
footer = _index[_index.index('</main>') :]

EN_NAV = """<ul>
          <li><a href="/#functies">Features</a></li>
          <li><a href="/en/privacy">Privacy</a></li>
          <li><a href="/en/terms">Terms</a></li>
          <li><a href="/en/support">Support</a></li>
        </ul>"""


def page(out, body_file, title, desc, lang='nl'):
    h = header
    h = re.sub(r'<title>.*?</title>', f'<title>{title} · Ultra OV NL</title>', h)
    h = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{desc}">', h)
    h = re.sub(r'<meta property="og:title" content=".*?">', f'<meta property="og:title" content="{title} · Ultra OV NL">', h)
    f = footer
    if lang == 'en':
        h = h.replace('<html lang="nl">', '<html lang="en">')
        h = h.replace('Naar de inhoud', 'Skip to content')
        h = h.replace('aria-label="Ultra OV NL, naar de startpagina"', 'aria-label="Ultra OV NL, home"')
        h = h.replace('aria-label="Hoofdmenu"', 'aria-label="Main menu"')
        h = re.sub(r'<ul>\s*<li><a href="/#functies">.*?</ul>', EN_NAV, h, flags=re.S)
        f = f.replace('<li><a href="/en/privacy" hreflang="en" lang="en">English</a></li>', '<li><a href="/NLPRIV" hreflang="nl" lang="nl">Nederlands</a></li>')
        f = f.replace('<h2>Informatie</h2>', '<h2>Information</h2>')
        f = f.replace('Support en contact', 'Support and contact').replace('/support"', '/en/support"')
        f = f.replace('Privacybeleid', 'Privacy policy').replace('/privacy"', '/en/privacy"')
        f = f.replace('Gebruiksvoorwaarden', 'Terms of use').replace('/voorwaarden"', '/en/terms"')
        f = f.replace('Account verwijderen</a>', 'Delete your account</a>').replace('/account-verwijderen"', '/en/delete-account"')
        f = f.replace('<h2>Databronnen</h2>', '<h2>Data sources</h2>')
        f = f.replace('Reisinformatie op basis van open OV-gegevens, waaronder NDOV Loket, OVapi en NS. Gegevens kunnen afwijken van de werkelijkheid.',
                      'Travel information based on open Dutch public transport data, including NDOV Loket, OVapi and NS. Data may differ from reality.')
        f = f.replace('Niet verbonden aan NS of andere vervoerders.', 'Not affiliated with NS or any other transport operator.')
        f = f.replace('/NLPRIV"', '/privacy"')
        f = f.replace('Jouw reis. Het OV in detail.', 'Your journey. Public transport in detail.')
    body = (G / body_file).read_text()
    dest = SITE / out / 'index.html' if out else SITE / '404.html'
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(h + '<main id="inhoud">\n' + body + '\n  ' + f)
    print('wrote', dest)


page('', '404.html', 'Pagina niet gevonden', 'Deze pagina bestaat niet.')
page('privacy', 'privacy-nl.html', 'Privacybeleid', 'Hoe Ultra OV NL met je gegevens omgaat.')
page('voorwaarden', 'terms-nl.html', 'Gebruiksvoorwaarden', 'De voorwaarden voor het gebruik van Ultra OV NL.')
page('account-verwijderen', 'account-nl.html', 'Account verwijderen', 'Zo verwijder je je Ultra OV NL-account en bijbehorende gegevens.')
page('support', 'support-nl.html', 'Support en contact', 'Hulp, contact en het verwijderen van je gegevens bij Ultra OV NL.')
for f, o, t, d in [
    ('privacy-en.html', 'en/privacy', 'Privacy policy', 'How Ultra OV NL handles your data.'),
    ('terms-en.html', 'en/terms', 'Terms of use', 'The terms for using Ultra OV NL.'),
    ('account-en.html', 'en/delete-account', 'Delete your account', 'How to delete your Ultra OV NL account and its data.'),
    ('support-en.html', 'en/support', 'Support and contact', 'Help, contact and deleting your data at Ultra OV NL.'),
]:
    if (G / f).exists():
        page(o, f, t, d, 'en')
