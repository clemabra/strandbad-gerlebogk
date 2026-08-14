# Strandbad & Campingplatz Gerlebogk – Website

Statische Website, kein Build-Framework. Reines HTML5 + CSS, 0 Byte JavaScript,
0 externe Requests. Schwesterseite zu [party-company.de](https://party-company.de) –
gleiche Typografie, gleiche Bausteine, gleiche Akzentfarbe, gespiegeltes Farbschema
(hell statt dunkel).

## Struktur

```
/
├── index.html                Startseite
├── hochzeit/index.html       Hochzeit am See (wichtigste Unterseite)
├── catering/index.html       Catering & Buffet, organisiert mit der Partycompany
├── feiern/index.html         Event-Location: Geburtstage, Firmen & Teams, Schulklassen
├── strandbad/index.html      Badebetrieb, Öffnungszeiten, Preise, Baderegeln, FAQ
├── camping/index.html        Campingplatz (Gerüst, siehe TODOs)
├── kontakt/index.html        Kontakt & Anfrage
├── impressum/index.html
├── datenschutz/index.html
├── 404.html
├── assets/css/main.css       Ein Stylesheet, keine @import-Ketten
├── assets/fonts/             Alfa Slab One (woff2, selbst gehostet)
├── assets/img/                Ausgelieferte Bilder (WebP + JPG-Fallback)
├── assets/img/src/            Quellbilder (Originale + geraderichtete Zwischenstufen) – nicht ausliefern, siehe robots.txt/.htaccess
├── tools/                     Build-Skripte für den Bild-Workflow (siehe unten)
├── functions/api/anfrage.js   Cloudflare Pages Function: Anfrageformular → E-Mail
├── wrangler.toml               send_email-Binding für das Anfrageformular (siehe unten)
├── robots.txt, sitemap.xml, llms.txt
├── .htaccess                  Apache-Konfiguration (falls nicht Cloudflare Pages)
├── _headers                   Header-Konfiguration für Cloudflare Pages / Netlify
└── _redirects                 Cloudflare Pages: 404 für /assets/img/src/ und /tools/
```

Die Website selbst bleibt bei 0 Byte JavaScript im Browser und 0 externen Requests
vom Client aus. Das Anfrageformular ist ein normales HTML-`<form>` (funktioniert
ohne JavaScript), das serverseitig von einer Cloudflare Pages Function verarbeitet
wird – die läuft bei Cloudflare selbst, nicht bei einem Drittanbieter.

## Deployment (Cloudflare Pages)

1. Repository/Ordner an Cloudflare Pages anbinden (Build-Command: keiner, Output-Verzeichnis: `/`).
2. Cloudflare Pages liest `_headers` automatisch aus – die `.htaccess` wird dort **nicht** ausgewertet, die liegt nur für alternative Apache-Hosts bereit.
3. Domain `strandbad-gerlebogk.de` (TODO: Registrierung bestätigen) als Custom Domain in Cloudflare Pages hinterlegen, DNS auf Cloudflare zeigen lassen.
4. Nach dem ersten Deploy: `sitemap.xml` bei der Google Search Console einreichen.

## Anfrageformular einrichten (wichtig, sonst schlägt der Versand fehl)

Das Formular auf `/kontakt/` sendet per POST an `/functions/api/anfrage.js`.
Diese Cloudflare Pages Function verschickt die Anfrage per **Cloudflare Email
Routing** – keine Datenbank, kein Drittanbieter, alles bleibt bei Cloudflare.
Damit das funktioniert, sind einmalig ein paar Schritte im Cloudflare-Dashboard
nötig (kann ich als Claude Code nicht selbst erledigen, da das Zugriff auf euer
Cloudflare-Konto braucht):

1. Domain `strandbad-gerlebogk.de` muss bei Cloudflare liegen (siehe Deployment oben).
2. Im Dashboard: **Email** → **Email Routing** → aktivieren, falls noch nicht geschehen.
3. Unter **Destination addresses**: `fischerparty@web.de` hinzufügen und über
   den Bestätigungslink in der Mail verifizieren – ohne diese Verifizierung
   kann Cloudflare dorthin keine E-Mails zustellen.
4. Im Pages-Projekt: **Settings** → **Functions** → **Email Bindings** (falls
   diese Oberfläche bei euch anders heißt oder die `wrangler.toml` im Repo-Root
   automatisch gegriffen hat, ist dieser Schritt schon erledigt) → Binding mit
   Name `ANFRAGE_MAIL` anlegen, Zieladresse `fischerparty@web.de`.
5. Neu deployen, danach das Formular auf `/kontakt/` einmal testweise ausfüllen
   und prüfen, ob die Mail bei fischerparty@web.de ankommt (ggf. Spam-Ordner
   prüfen, gerade beim allerersten Testversand).

**Wichtig:** Ich habe dieses Setup nicht live gegen ein echtes Cloudflare-Konto
getestet, da ich dafür keinen Zugriff habe – die Function folgt Cloudflares
dokumentiertem Vorgehen für `send_email`-Bindings, aber der erste Testversand
nach dem Deploy ist Pflicht, nicht optional. Schlägt er fehl, zeigt das
Formular eine Fehlerseite mit Ausweich-Kontaktdaten statt der Danke-Seite –
schaut in dem Fall in die Function-Logs im Cloudflare-Dashboard.

## Bild-Workflow

14 Quellfotos lagen als JPG mit Facebook-Dateinamen vor (`assets/img/src/`, dort
umbenannt gemäß der Motiv-Tabelle unten). Workflow, reproduzierbar über
`tools/build-images.py` (Python 3 + Pillow + `cwebp`):

1. **Umbenennen** – Quelldateien nach Motiv benannt (siehe Tabelle).
2. **Geraderichten** – `traubogen-see` und `trauung-strand` waren stark schräg
   fotografiert. Begradigt mit `tools/straighten.py <in> <out> <winkel>`
   (Rotation + Zuschnitt auf das größte unverzerrte Rechteck):
   - `traubogen-see`: 40° Rotation, Ergebnis 1002×1194
   - `trauung-strand`: 20° Rotation, Ergebnis 970×1826
   - Winkel wurden visuell durch Vergleich mit der Wasserlinie ermittelt und
     iterativ geprüft – kein automatisches Horizont-Tracking. Bei Bedarf mit
     echter Fotosoftware nachschärfen.
3. **WebP-Konvertierung** – `python3 tools/build-images.py` erzeugt aus jedem
   Quellbild mehrere Zielbreiten als WebP (`cwebp -q 82`) und JPG-Fallback
   (Pillow, `quality=82`, progressive). Zielbreiten stehen im `MANIFEST` am
   Anfang des Skripts.
4. **OG-Bilder** – `og-default.jpg` (aus `luftaufnahme-strandbad`) und
   `og-hochzeit.jpg` (aus `traubogen-see`), je 1200×630, center-cropped.

| Quelldatei (Original) | Zielname | Einsatz |
|---|---|---|
| `486629678_…` | `luftaufnahme-strandbad` | Startseite, neben Faktenabsatz |
| `485729486_…` | `sonnenuntergang-see` | Hero Startseite |
| `488602981_…` | `see-blaue-stunde` | Camping-Seite, Sektionstrenner |
| `704148249_…` | `strandbar-liegestuehle` | Strandbad-Seite (Hero) |
| `495773711_…` | `lounge-deck-nacht` | Feiern-Seite (Hero) |
| `495796302_…` | `terrasse-abendsonne` | Feiern-Seite |
| `485041185_…` | `zeltanlage-terrasse` | Feiern-/Hochzeit-Seite |
| `497461515_…` | `festzelt-hochzeitstafel` | Hochzeit-Seite, Startseite |
| `486576197_…` | `traubogen-see` | **geraderichtet**, Hero Hochzeit-Seite |
| `487123129_…` | `trauung-strand` | **geraderichtet**, Hochzeit-Seite |
| `496944330_…` | `tischdeko-detail` | Hochzeit-Seite, Startseite |
| `487382859_…` | `ruderboot-daemmerung` | klein, Startseite (Bildstrecke) |
| `494698507_…` | `catering-fingerfood` | klein, aktuell ungenutzt – TODO Einsatzort |
| `495576236_…` | `catering-buffet` | klein, aktuell ungenutzt – TODO Einsatzort |

Die drei kleinen Motive (414×414) sind nur bis ~380px Anzeigebreite eingesetzt,
wie gefordert. `catering-fingerfood` ist jetzt in der Bildstrecke der
Catering-Seite verbaut; `catering-buffet` ist weiterhin ungenutzt (durch die
zweite Lieferung gibt es davon inzwischen hochauflösende Alternativen).

### Zweite Lieferung ("Strandbad Assets", nach Kategorien sortiert)

Zweiter Foto-Ordner, bereits vom Betreiber in Unterordner (`See/`, `Party/`,
`Deko/`, `Team/`, `Hochzeit/`, `Strand/`, `Buffet/`, `Umgebung/`, `logo/`)
sortiert. Ausgewählt, umbenannt und mit demselben `build-images.py`-Workflow
verarbeitet:

| Zielname | Quellordner | Einsatz |
|---|---|---|
| `ruderboot-tag` | See | Startseite/Camping, Bildstrecke |
| `abenddaemmerung-baum` | See | Sektionstrenner |
| `wolken-spiegelung-see` | See | Startseite/Strandbad |
| `sonnenuntergang-allee` | See | Bildstrecke |
| `nachtfeier-lichter` | Party | Feiern-Seite |
| `deck-abend-schirme` | Party | Feiern-Seite |
| `campingplatz-wohnwagen` | Deko | **beschnitten** (Aschenbecher/Notizzettel im Vordergrund entfernt), Camping-Seite |
| `hochzeitstafel-kerzen` | Hochzeit | Hochzeit-Seite |
| `deck-sonnensegel-tag` | Hochzeit | Feiern-/Hochzeit-Seite |
| `deko-kiste-laterne` | Hochzeit | Hochzeit-Seite, Detail |
| `festzelt-tafel-innen` | Hochzeit | Hochzeit-Seite, Festzelt-Innenansicht |
| `festzelt-tischdeko-palme` | Hochzeit | Hochzeit-Seite |
| `mondaufgang-strand` | Strand | Startseite/Strandbad |
| `team-shirt` | Team | Kontakt-Seite, Team-Abschnitt |
| `team-grillen` | Team | Kontakt-Seite, Team-Abschnitt |
| `catering-tafel-uebersicht` | Buffet | Catering-Seite (Hero) |
| `catering-fruchtsalat`, `-kaesebrett`, `-grillspiesse`, `-braten`, `-dessert`, `-salat-bluete`, `-haehnchen`, `-krautsalat` | Buffet | Catering-Seite, Bildstrecke |

Nicht verwendet: `Umgebung/` (nur herbstliche/kahle Bäume, passt nicht zur
Sommer-Saison der Seite), die meisten `Deko/`-Nahaufnahmen (redundant zu
bereits vorhandenen Detailbildern), einzelne `Party/`- und `Buffet/`-Fotos mit
störendem Fremdbranding oder unruhigem Hintergrund. `Bilder Ivonne/` war leer.
Der `logo/`-Ordner enthält die in der Konversation abgestimmten Logo-Entwürfe
(Festzelt-Motiv) – noch nicht final gewählt/eingebaut.

### Logo & Wellenkante – austauschen, sobald finale Assets vorliegen

- **Logo**: Aktuell ein bewusst als Platzhalter erkennbares SVG-artiges PNG
  (gestrichelter Kreis, "LOGO"-Schriftzug), erzeugt mit `tools/build-placeholder-logo.py`.
  Sobald das finale Logo vorliegt: Datei in `assets/img/src/` legen, mit
  Pillow/`cwebp` in `logo-96/192/384.{png,webp}` und `favicon-32.png`/`favicon-180.png`
  umwandeln (gleiches Muster wie `build-placeholder-logo.py`), `alt`-Text in
  allen 8 Seiten + `404.html` von "Platzhalter-Logo … finales Logo folgt" auf
  eine echte Bildbeschreibung ändern.
- **Wellenkante** (Signature-Element, Pendant zur Lichterketten-Girlande der
  Partycompany – ursprünglich als "Segelkante"/Sonnensegel-Motiv geplant,
  nach Rückmeldung auf drei ineinander verschlungene Wellenlinien geändert):
  ein von Hand geschriebenes SVG, direkt als CSS-Variable `--wellen` in
  `assets/css/main.css` eingebettet (kein Bild-Request). Die Kachel ist exakt
  eine Wellenperiode breit (160×64, Seitenverhältnis 2,5:1) und dadurch
  mathematisch nahtlos wiederholbar. Wichtig beim Anpassen: `background-size`
  bei `.wellen`/`.wellen--kopf` muss immer im Verhältnis 2,5:1 bleiben, sonst
  verzerrt sich die Wiederholung (das war der Bug in der ersten Segelkante-Version).
  Falls später ein Rasterbild verwendet werden soll: auf
  `background-image: url(...)` mit eigener Bilddatei umstellen, Seitenverhältnis
  der neuen Grafik beibehalten.

## Event-Teaser austauschen

Ganz oben im `<body>` von `index.html` und `feiern/index.html` liegt ein
auskommentierter Block:

```html
<!-- EVENT-TEASER (Partycompany): ... -->
<section class="section section--schmal section--nacht" aria-labelledby="event-titel">
  ...
</section>
-->
```

Titel, Datum und Link eintragen, Kommentarzeichen (`<!--` / `-->`) entfernen –
fertig. Datum/Line-up bewusst nicht vorab eingebaut, da der Termin des
nächsten Open Airs laut Auftraggeber gerade verschoben wird.

## Auf "Saison beendet" umstellen

Kein automatischer Mechanismus (keine JS-Datumslogik, um die 0-Byte-JS-Vorgabe
einzuhalten). Manuell umzustellen, sobald die Saison (15.9.) endet:

1. `index.html` und `strandbad/index.html`: `.hero__aktion`/`.hero__unter` um
   einen Hinweis "Saison beendet, wir sind ab 15. Mai wieder da" ergänzen
   (`.hinweis`-Klasse in `main.css` vorhanden, gleiche Optik wie der
   Baderegel-Hinweis).
2. Primäre CTAs, die auf Tagesgast-Besuch abzielen, auf Camping-/Hochzeit-Anfragen
   umlenken (die außerhalb der Saison weiterhin sinnvoll sind).
3. JSON-LD `openingHoursSpecification` in `index.html` unverändert lassen – das
   Feld beschreibt die reguläre Saison, nicht den aktuellen Status.

## Offene TODOs (gesammelt)

- **Öffnungstage**: Widerspruch in den Unterlagen (Mo–So vs. Di–So), 10–20 Uhr
  unbestritten. Sichtbar als `<span class="todo">` auf Start- und Strandbad-Seite.
- **Preise**: Eintritt Tagesgäste/Kinder/Liegewiese, Feiern-Locationmiete,
  Camping-Stellplätze – Preistabellen mit Platzhaltern angelegt (Start,
  Strandbad, Feiern, Camping).
- **Camping-Details**: Stellplatzarten, Strom/Wasser/Sanitär, An-/Abreisezeiten,
  Buchungsweg – Gerüst auf `/camping/` angelegt.
- **Hochzeit-FAQ**: 4 von 5 Fragen ohne Antwort (freie Trauung, Schlechtwetter,
  Gästezahl, Vorlaufzeit für Buchung) – nur "Übernachtung vor Ort" ist aus
  bestehendem Partycompany-Material belegt und beantwortet.
- **Strandbad-FAQ**: Hunde erlaubt?, Duschen vorhanden? – unbeantwortet.
- **Logo**: Platzhalter aktiv, s. o.
- **Domain-Registrierung** `strandbad-gerlebogk.de`: zu bestätigen (Hinweis in
  der Datenschutzerklärung).
- **Bilder in höherer Auflösung**: `ruderboot-daemmerung`, `catering-fingerfood`,
  `catering-buffet` (aktuell 414×414, nur klein einsetzbar).
- **Nächstes Event** (Termin/Line-up Partycompany-Open-Air): bewusst nicht
  eingebaut, siehe "Event-Teaser austauschen" oben.
- **Anfrageformular-Versand testen**: Cloudflare Email Routing + send_email-
  Binding einrichten (siehe "Anfrageformular einrichten" oben) und nach dem
  Deploy einmal live durchtesten – von mir ungetestet, da kein Zugriff aufs
  Cloudflare-Konto.

Impressum, Kontakt und USt-IdNr. wurden **nicht** als TODO gelassen: Auftraggeber
hat bestätigt, dass Strandbad dieselben Kontakt-/Impressumsdaten wie die
Partycompany nutzt (Inhaberin Martina Wachsmuth, Am Gemeindebackhaus 4a, 06406
Bernburg, USt-IdNr. DE315511872), ergänzt um die Betriebsstätte Gröbziger
Straße 25, 06420 Könnern OT Gerlebogk.

## Selbstprüfung gegen die Anforderungsliste

**Stack**
- ✅ Reines HTML5 + CSS, kein Framework/Build-Tool/npm-Runtime-Paket.
- ✅ 0 Byte JavaScript im Browser (kein `<script>` außer `type="application/ld+json"`,
  das ist kein ausführbarer Code). Das Anfrageformular ist ein normales
  HTML-`<form>`, funktioniert ohne JavaScript; die Verarbeitung läuft
  serverseitig in einer Cloudflare Pages Function (`functions/api/anfrage.js`),
  nicht im Browser.
- ✅ Keine externen Requests: kein CDN, keine Google Fonts, kein Maps-iFrame,
  keine Analytics/Social-Widgets. Geprüft per Grep über alle `<link>`/`<script>`/
  `<img>`-Quellen – alle zeigen auf `/…` oder sind reine `<a>`-Links (OSM,
  Google Maps als Linkziel, party-company.de, wa.me). Font selbst gehostet
  (woff2, `font-display: swap`, preload). Das Anfrageformular sendet nur an
  die eigene Cloudflare Pages Function (`form-action 'self'` in der CSP),
  nicht an einen Formular-Drittanbieter.
- ✅ Keine Cookies/localStorage/sessionStorage/Fingerprinting.

**Bilder**
- ✅ WebP über `<picture>` mit `srcset`/`sizes` + JPG-Fallback.
- ✅ `width`/`height` überall gesetzt, `loading="lazy"` außer Hero-Bildern,
  Hero mit `fetchpriority="high"` + Preload.
- ✅ Alt-Texte beschreiben das Motiv (automatisiert geprüft: kein `<img>` ohne
  `alt`). Kein Keyword-Stuffing.
- ✅ Workflow, Zielgrößen und Crop-Befehle in diesem README dokumentiert.

**Performance**
- ⚠️ Lighthouse nicht in dieser Umgebung gemessen (kein echter Browser-Audit
  verfügbar) – strukturell auf 100/100/100/100 ausgelegt: keine
  Render-Blocker, ein CSS ohne `@import`, Hero-Bild + Font vorgeladen.
- ⚠️ "Critical CSS inline im `<head>`" wurde **nicht** wörtlich umgesetzt –
  wie bei der Partycompany-Seite (Referenzimplementierung) liegt das gesamte
  CSS in einer verlinkten, gzip-komprimierten Datei (main.css: 22,4 KB roh /
  6,2 KB gzip). Das vermeidet Render-Blocking bereits ausreichend bei dieser
  Dateigröße; ein separater Inline-Block hätte Inhalte dupliziert. Abweichung
  bewusst analog zur Schwesterseite.
- ✅/⚠️ "Gesamtgewicht jeder Seite ohne Bilder unter 50 KB": als **komprimierte
  Transfergröße** (Cloudflare liefert automatisch gzip/brotli) klar erfüllt –
  schwerste Seite (Startseite) 5,1 KB HTML + 6,2 KB CSS gzip ≈ 11,3 KB, Font
  einmalig 11,6 KB (danach `immutable` gecacht). Als **unkomprimierte
  Rohgröße** liegt die Startseite beim allerersten Laden (HTML+CSS+Font) bei
  rund 53 KB, knapp über der 50-KB-Marke – bei jedem Folgebesuch bzw. jeder
  weiteren Seite entfällt CSS+Font aus dem Cache. Transparent gemessen und
  hier dokumentiert statt stillschweigend gerundet.
- ✅ `.htaccess` und `_headers` mit Security-Headern (CSP ohne `unsafe-inline`,
  HSTS, X-Content-Type-Options, Referrer-Policy, weitere) mitgeliefert.

**SEO**
- ✅ Genau eine `<h1>` pro Seite (automatisiert geprüft).
- ✅ `<title>` / Meta-Description / Canonical / `lang="de"` / OG + Twitter Cards
  mit eigenem OG-Bild (1200×630) auf jeder Seite.
- ✅ JSON-LD: `LocalBusiness`+`BeachResort` (Startseite), `Campground`
  (Camping), `Service` (Hochzeit, Feiern), `FAQPage` (wo echte Antworten
  vorliegen), `BreadcrumbList` (Unterseiten), `ContactPage` (Kontakt).
  `isRelatedTo`/`sameAs` verweist auf party-company.de. Alle Blöcke als
  valides JSON geprüft (automatisiert, Python `json.loads`).
- ✅ `sitemap.xml`, `robots.txt`.
- ✅ Regionale Keywords natürlich eingebaut (Strandbad Gerlebogk, Badesee
  Könnern, Campingplatz Salzlandkreis, Hochzeit am See Sachsen-Anhalt,
  Firmenfeier am See, Klassenfahrt Badesee).

**GEO**
- ✅ Faktendichter Absatz direkt unter jedem Hero (Adresse, Saison, Angebot).
- ✅ FAQ-Blöcke in echter Frage-Antwort-Form; unbelegte Antworten sind sichtbar
  als TODO markiert, nicht erfunden oder in JSON-LD strukturiert (nur belegte
  Antworten sind Teil des `FAQPage`-Markups, damit keine leeren/TODO-Antworten
  in Suchergebnissen landen).
- ✅ `llms.txt` im Root mit Betrieb, Saison, Angebot, Verhältnis zur
  Partycompany, offenen TODOs.
- ✅ Eckdaten als Definitionslisten/Tabellen statt Fließtext.

**Barrierefreiheit**
- ✅ `#F07A16` nur als Fläche (Buttons, Ösen-Akzent, Randlinie) verwendet, nie
  als Fließtext/Link-Farbe – Textlinks laufen in Navy (`--nacht`).
- ✅ Sichtbarer Fokus-Stil (`:focus-visible`), `prefers-reduced-motion`
  respektiert (Wellenkante-Animation + `scroll-behavior` deaktiviert), responsiv
  ab 320px getestet (Breakpoint bei 22.5rem), Skip-Link vorhanden.

**Rechtliches**
- ✅ Impressum und Datenschutz als eigene Seiten mit klar markierten TODOs.
- ✅ Datenschutzerklärung dokumentiert explizit: keine Cookies, keine
  Drittanbieter außer verlinkten (nicht eingebetteten) Zielen.
- ✅ Kein Kontaktformular – `mailto:`, `tel:`, WhatsApp-Link (`wa.me`).

**Keine Anfragen an fremde Domains**: geprüft per Grep über alle `href`/`src`-
Attribute in `<link>`/`<script>`/`<img>`; einzige externen `<a>`-Linkziele sind
`party-company.de`, `openstreetmap.org`, `google.com/maps`, `wa.me` und (nur im
Fließtext der Datenschutzerklärung) `cloudflare.com` – alles reine, vom Nutzer
angeklickte Links, keine automatisch geladenen Ressourcen.
