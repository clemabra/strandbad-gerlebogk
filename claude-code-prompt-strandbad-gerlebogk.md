# Prompt für Claude Code – Website „Strandbad & Campingplatz Gerlebogk"

> Alles ab hier kopieren und in Claude Code einfügen.

---

## Auftrag

Baue die Website für das **Strandbad & Campingplatz Gerlebogk** – eine statische, extrem schnelle Website ohne Build-Framework. Arbeite in zwei Phasen: **erst Designplan vorlegen, dann bauen.**

Es handelt sich um die **Schwesterseite** zu `https://party-company.de` (Die Partycompany). Beide Seiten gehören zusammen und verlinken sich gegenseitig. Sie sollen erkennbar aus einer Familie stammen – gleiche Typografie, gleiche Bausteine, gleiche Akzentfarbe – aber deutlich unterschiedlich wirken.

**Der entscheidende Unterschied:**

| | Partycompany | Strandbad Gerlebogk |
|---|---|---|
| Grundstimmung | dunkel, Party, Nacht, laut | hell, Sommer, Wasser, Ruhe |
| Hintergrund | Navy `#293742` | Weiß `#FDFDFD` als dominante Fläche |
| Akzentfarbe | Orange `#EF760C` | **dieselbe** Orange `#EF760C` |
| Hauptaufgabe | Tickets verkaufen | Anfragen erzeugen + Gäste informieren |

Weiß ist hier nicht „der Hintergrund, den man halt nimmt", sondern das gestalterische Mittel: viel Luft, große Bildflächen, wenig Farbfläche. Orange kommt nur an wenigen, gezielten Stellen vor (CTA, Hover, Marker, ein Signature-Element). Navy darf sparsam als Textfarbe / Fußzeile weiterlaufen, damit die Verwandtschaft sichtbar bleibt.

Wenn dir das Farbsystem der Partycompany-Seite zugänglich ist (CSS-Variablen, `main.css`), lies es aus und übernimm Variablennamen und Schriften **wörtlich**, statt sie neu zu erfinden. Falls nicht: frag mich nach der `main.css`, bevor du den Designplan schreibst.

## Über den Betrieb

- **Name:** Strandbad & Campingplatz Gerlebogk
- **Adresse:** Gröbziger Str. 25, OT Gerlebogk, 06420 Könnern (Sachsen-Anhalt, Salzlandkreis)
- **Was es ist:** Naturbadesee mit Sandstrand und Liegewiese, Campingplatz, Gastronomie/Strandbar und Eventlocation – alles auf einem Gelände
- **Saison:** 15. Mai bis 15. September
- **Öffnungszeiten:** `[TODO: Widerspruch klären – in meinen Unterlagen steht einmal „Montag–Sonntag 10:00–20:00" und einmal „Dienstag–Sonntag 10:00–20:00". Bis zur Klärung als sichtbares TODO im Code stehen lassen, NICHT raten.]`
- **Schwesterfirma:** Die Partycompany (Events, Eventcatering, Gastronomie) – `https://party-company.de`
- **Catering:** läuft über die Partycompany / Grill & BBQ – auf der Strandbad-Seite erwähnen und verlinken, nicht doppelt ausführlich beschreiben
- **Kontakt:** `[TODO: eigene Telefonnummer/E-Mail des Strandbads – oder soll alles über die Partycompany-Kontakte laufen?]`
- **Impressumsdaten:** `[TODO: Das Strandbad ist eine eigene Firma, nicht die Partycompany. Firmierung, Inhaber, Rechtsform, USt-IdNr. nachliefern. Nichts von der Partycompany übernehmen.]`
- **Domain:** `strandbad-gerlebogk.de` `[TODO: bestätigen]`
- **Hosting:** Cloudflare Pages (wie die Partycompany-Seite) – Deployment entsprechend vorbereiten

## Ziele der Seite, in dieser Reihenfolge

1. **Anfragen erzeugen** für Hochzeiten, Firmenfeiern, Geburtstage, Klassenfahrten. Das ist der Umsatz mit Marge – hier darf die Seite am meisten Raum bekommen.
2. **Tagesgäste informieren:** Wann offen? Was kostet es? Wo parken? Kann man baden? Diese Leute suchen mobil, oft direkt am Auto, und wollen in 5 Sekunden eine Antwort.
3. **Camping-Anfragen** aufnehmen.
4. **Auf die Veranstaltung der Partycompany verweisen.**

Zu Punkt 4 wichtig: Die Eventseite lebt auf `party-company.de`, nicht hier. Auf der Strandbad-Seite gibt es nur einen kompakten Teaser-Block „Was ist bei uns los" mit Verlinkung. **Datum und Line-up nicht hier fest einbauen** – der Termin des nächsten Open Airs wird gerade verschoben. Baue den Block so, dass Titel, Datum und Link in **einem** klar markierten Abschnitt am Anfang der HTML-Datei stehen und in 30 Sekunden austauschbar sind.

## Seitenstruktur

```
/                                  Startseite
/hochzeit/                         Hochzeit am See (wichtigste Unterseite)
/feiern/                           Event-Location: Geburtstage, Firmen & Teams, Schulklassen
/strandbad/                        Badebetrieb, Öffnungszeiten, Preise, Anfahrt, Regeln
/camping/                          Campingplatz
/kontakt/                          Kontakt & Anfrage
/impressum/  /datenschutz/
```

Sprechende URLs mit Ordnerstruktur, jeweils `index.html`.

**Startseite:** Hero mit Seebild + einem Satz, der sagt, was das hier ist. Direkt darunter der faktendichte Absatz (siehe GEO). Dann: Öffnungszeiten/Saison als Karte, die drei Nutzungsarten (Badetag / Feiern / Camping) als drei Einstiege, Bildstrecke, Event-Teaser, Anfahrt, Kontakt.

**`/hochzeit/`** ist die kommerziell wichtigste Seite und bekommt die stärksten Bilder, mehrere Anfrage-CTAs und den ausführlichsten Text.

## Texte

Die folgenden Texte stammen vom Betreiber. Übernimm **Tonfall und Inhalt**, du darfst sprachlich glätten, kürzen, in Zwischenüberschriften gliedern und für SEO/GEO ergänzen – aber **keine neuen Fakten erfinden** (keine Preise, keine Kapazitäten, keine Personenzahlen, keine Ausstattung, die nicht dasteht). Ansprache: Hochzeit „ihr", alles andere „du". Das ist bewusst so und bleibt so.

### Hochzeit am See

> **Strandbad Hochzeit am See**
> Romantische Hochzeiten am See mit umfassendem Service und unvergesslichem Ausblick.
>
> **Für alle, die sich das Ja-Wort am See unter freiem Himmel wünschen**
> Stellt euch vor: Eine sanfte Brise weht über den See, eure Gäste sitzen barfuß im Sand und vor euch liegt ein liebevoll geschmückter Traubogen mit Blick auf das Wasser. Im Strandbad Gerlebogk wird eure Hochzeit zu einem unvergesslichen Moment voller Romantik, Natur und Leichtigkeit. Ob intime Zeremonie oder große Feier mit Freunden und Familie – wir bieten euch den perfekten Rahmen für euren großen Tag und unterstützen euch bei jedem Schritt der Planung.
>
> **All-Inclusive Hochzeitspaket** – alles, was ihr für euren großen Tag braucht, stilvoll geplant und liebevoll umgesetzt am See:
>
> - **Zeremonie am Seeufer** – liebevoll dekorierte Traufläche direkt am See, mit stilvoller Bestuhlung, Blumenarrangements und natürlichem Panorama als Kulisse.
> - **Hochzeits-Catering** – im Grill- & BBQ-Style, passend zu eurem Stil und Geschmack.
> - **Live-Musik & DJs** – ob romantische Liveband zur Trauung oder energiegeladene Beats für die Party, wir sorgen für die passende Stimmung.
> - **Und noch mehr** – Dekoration, Fotografen, Feuerwerk und viele weitere Services, um euren Tag einzigartig zu machen.
>
> **Plant jetzt euren großen Tag.** Erzählt uns von eurer Traumhochzeit – wir setzen sie für euch um. Lasst uns gemeinsam eure persönliche Traumkulisse am See gestalten: Romantik, Emotionen und ein unvergessliches Erlebnis für euch und eure Gäste.

Ergänze auf dieser Seite einen FAQ-Block mit echten Fragen (freie Trauung möglich? Schlechtwetter-Alternative? Wie viele Gäste? Ab wann buchbar? Übernachtung vor Ort?). Antworten, die du nicht aus dem Material belegen kannst, als `TODO` markieren statt sie zu erfinden – lieber sechs echte Fragen als zwölf erfundene Antworten.

### Event-Location

> **Event Location** – für unvergessliche Feiern am Wasser, von Firmenfest bis Geburtstag.
>
> **Geburtstagsfeiern – feier deinen Tag mit Stil am See**
> Mach deinen Geburtstag unvergesslich: eine Feier direkt am Wasser, individuell gestaltet mit Musik, Catering, Deko und vielen Extras für Gäste jeden Alters. Genieße die entspannte Atmosphäre im Strandbad und feier, wie du willst.
>
> **Schulklassen – sichere und spaßige Klassenausflüge**
> Plant einen unvergesslichen Tag mit Outdoor-Aktivitäten, viel Platz zum Spielen, leckeren Verpflegungsoptionen und einem sicheren Umfeld – perfekt für Wandertage, Abschlussfahrten oder Klassengemeinschaftstage.
>
> **Firmen & Teams – Workshops. Teambuilding. Feiern. Alles am See.**
> Raus aus dem Büro, rein ins Erlebnis: Im Strandbad Gerlebogk wird jedes Firmenevent zum echten Highlight – egal ob lockerer Teamtag, kreativer Workshop oder stilvolle Sommerfeier. Euch erwarten exklusive Flächen, sportliche Action, entspannte Atmosphäre und individuelle Betreuung – perfekt für starke Verbindungen und frische Impulse.
>
> **Bereit für deinen Moment am See?**
> Ob Event, Hochzeit oder entspannter Sommertag – schreib uns und sichere dir deinen Platz im Strandbad Gerlebogk. Wir freuen uns auf deine Anfrage!

### Strandbad

> **Strandbad & Campingplatz Gerlebogk**
> Entspann am See mit kühlen Drinks, leckerem Essen, Sonne und guter Laune – perfekt für Familien, Badegäste und alle, die den Sommer lieben.
>
> **Öffnungszeiten & Saison**
> Die Saison beginnt am 15. Mai und endet am 15. September. `[TODO Öffnungstage/-zeiten]`
> Genieße entspannte Stunden am See mit kühlen Drinks, am Strand und auf unserer Liegewiese. Unsere großzügigen Öffnungszeiten bieten dir den perfekten Rahmen für einen entspannten Tag oder eine Abendentspannung am Wasser.
>
> **Badespaß – abtauchen, entspannen und den Sommer genießen**
> Ob morgens zum ersten Sprung ins kühle Nass oder am Nachmittag mit der Familie auf der Liegewiese – unser Naturbad macht jeden Sommertag zum kleinen Urlaub. Mit schattigen Plätzen unter alten Bäumen und unseren Sonnensegeln.
>
> **Baden auf eigene Gefahr.** Parkplätze stehen ausreichend zur Verfügung.

Der Hinweis „Baden auf eigene Gefahr" gehört sichtbar und nicht kleingedruckt auf die Strandbad-Seite. Preise: `[TODO: Eintritt Tagesgäste, Kinder, Liegewiese – Preistabelle als Gerüst mit Platzhaltern anlegen]`.

### Camping

Eigene Seite mit dem, was gesichert ist: Camping direkt am See, auf demselben Gelände wie Strandbad und Gastronomie. Alles Weitere – Stellplatzarten, Preise, Strom/Wasser/Sanitär, An- und Abreisezeiten, Buchung – als `TODO`-Gerüst anlegen. `[TODO: Campingdetails nachliefern]`

## Bildmaterial

14 Fotos liegen vor. Benenne sie beim Import um, konvertiere nach WebP und dokumentiere den Workflow in der README.

| Quelldatei (Original) | Zielname | Motiv | Einsatz |
|---|---|---|---|
| `486629678_…` (1600×1066) | `luftaufnahme-strandbad` | Luftbild: See, Sandstrand, Liegewiese mit Sonnensegeln, Camping, Parkplätze | Startseite – bestes Bild zum Erklären der Anlage, ideal neben dem Faktenabsatz |
| `485729486_…` (1536×2048) | `sonnenuntergang-see` | Sonnenuntergang über dem See, Schilf, kräftiges Pink/Orange | Hero-Kandidat Startseite (Orange harmoniert mit der Akzentfarbe) |
| `488602981_…` (1200×1600) | `see-blaue-stunde` | See in der blauen Stunde, Baumsilhouette | Sektionstrenner, Camping-Seite |
| `704148249_…` (2048×1536) | `strandbar-liegestuehle` | Sandfläche mit Liegestühlen, Sonnenschirmen, Kabeltrommel-Tischen | Strandbad-Seite, Gastronomie |
| `495773711_…` (1536×2048) | `lounge-deck-nacht` | Holzdeck mit Sonnensegel, Lichterketten, lila LED, Nacht | Feiern-Seite – stärkstes Stimmungsbild |
| `495796302_…` (1536×2048) | `terrasse-abendsonne` | Holzterrasse im Abendlicht, Olivenbäume, Zelt | Feiern-Seite, Event-Location |
| `485041185_…` (2048×1366) | `zeltanlage-terrasse` | Pagodenzelt + Festzelt auf Holzterrasse, Außenansicht | Feiern-Seite – zeigt die Kapazität |
| `497461515_…` (2048×1536) | `festzelt-hochzeitstafel` | Festzelt innen, lange gedeckte Tafel, Hussen, Ballons | Hochzeit-Seite |
| `486576197_…` (1536×2048) | `traubogen-see` | Birken-Traubogen mit weißen Rosen und Pampasgras am Wasser | Hochzeit-Seite, Hero |
| `487123129_…` (1536×2048) | `trauung-strand` | Traubogen + Stehtische mit weißen Hussen am Strand | Hochzeit-Seite |
| `496944330_…` (1536×2048) | `tischdeko-detail` | Tischdeko-Detail: Pampasgras, Namenskarte, Menükarte, Abendlicht | Hochzeit-Seite, Detailreihe |
| `487382859_…` (414×414) | `ruderboot-daemmerung` | Ruderboot auf dem See in der Dämmerung | nur klein einsetzbar |
| `494698507_…` (414×414) | `catering-fingerfood` | Fingerfood-Platten, Canapés | nur klein einsetzbar |
| `495576236_…` (414×414) | `catering-buffet` | Buffetplatten und Dessertgläser | nur klein einsetzbar |

Drei Hinweise, die du beim Einbau beachten musst:

1. **Die letzten drei Bilder sind nur 414×414 Pixel.** Nicht als Hero oder großflächig verwenden – sie zerfallen sofort. Entweder klein einsetzen (max. ~380 px Anzeigebreite) oder als `TODO: Bild in höherer Auflösung nachliefern` markieren.
2. **`486576197_…` und `487123129_…` (Traubogen) sind stark schräg fotografiert** – die Horizontlinie läuft diagonal durchs Bild. Vor dem Einsatz geraderichten und beschneiden; dokumentiere den Crop-Befehl in der README.
3. **Hochformate dominieren.** Plane das Layout so, dass 3:4- und 4:3-Bilder nebeneinander funktionieren (feste `aspect-ratio` pro Bildslot, `object-fit: cover`), sonst wird die Seite zum Zickzack.

Logo: `[TODO: Strandbad-Logo liefern – blau mit Sonnenschirm]`. Bis dahin Platzhalter mit korrekter Größe einbauen, kein Fantasie-Logo zeichnen.

## Technische Vorgaben (harte Anforderungen)

**Stack**
- Reines, valides HTML5 + CSS. Kein Framework, kein Build-Tool, kein npm-Runtime-Paket.
- JavaScript nur wenn zwingend nötig, dann Vanilla, inline oder eine Datei, insgesamt < 5 KB. Die Seite muss ohne JS vollständig funktionieren.
- **Keine externen Requests:** keine CDNs, kein Google Fonts, kein Google Maps iFrame, keine Analytics, keine Social-Widgets. Fonts selbst hosten (WOFF2, `font-display: swap`, preload) oder System-Font-Stack.
- **Keine Cookies, kein localStorage, kein sessionStorage, kein Fingerprinting** – die Seite muss ohne Cookie-Banner rechtlich sauber sein. Karte: statisches WebP mit Link zu Google Maps / OSM statt eingebettetem iFrame.

**Bilder**
- Auslieferung als WebP (optional zusätzlich AVIF) über `<picture>` mit `srcset`/`sizes` und JPG-Fallback.
- Immer `width`/`height` gesetzt (kein Layout Shift), `loading="lazy"` außer Hero, Hero mit `fetchpriority="high"` und Preload.
- Aussagekräftige `alt`-Texte, die das Motiv beschreiben – nicht „Strandbad Gerlebogk Hochzeit See Event" (Keyword-Stuffing im Alt-Attribut ist ein Barrierefreiheits-Problem, kein SEO-Trick).
- `assets/img/`, Konvertierungsbefehle und Zielgrößen in der README dokumentieren.

**Performance**
- Lighthouse Mobile 100/100/100/100 anstreben, LCP < 1,5 s, CLS 0, kein Render-Blocking.
- Critical CSS inline im `<head>`, Rest als eine CSS-Datei. Keine `@import`-Ketten.
- Gesamtgewicht jeder Seite ohne Bilder unter 50 KB.
- `.htaccess` und `_headers` (Cloudflare/Netlify) mitliefern, inkl. Security-Header (CSP möglichst ohne `unsafe-inline`, HSTS, X-Content-Type-Options, Referrer-Policy).

**SEO**
- Semantisches HTML, genau eine `<h1>` pro Seite, saubere Überschriftenhierarchie.
- Pro Seite: `<title>` (< 60 Zeichen), Meta-Description (< 155 Zeichen), Canonical, `lang="de"`, Open Graph + Twitter Cards mit eigenem OG-Bild (1200×630).
- JSON-LD nach Schema.org: `LocalBusiness` bzw. `Campground` und `BeachResort` für das Gelände (mit `PostalAddress`, `geo`, `openingHoursSpecification` inkl. Saisonzeitraum), `Service` für Hochzeit/Event-Angebote, `FAQPage` je FAQ-Block, `BreadcrumbList`. Auf `party-company.de` per `sameAs`/`isRelatedTo` verweisen.
- `sitemap.xml`, `robots.txt`.
- Regionaler Keyword-Fokus, natürlich eingebaut: „Strandbad Gerlebogk", „Badesee Könnern", „Campingplatz Salzlandkreis", „Hochzeit am See Sachsen-Anhalt", „Firmenfeier am See Bernburg", „Klassenfahrt Badesee".

**GEO (Auffindbarkeit in KI-Suchen)**
- Alle Fakten im sichtbaren Text ausschreiben, nie nur im Bild: Adresse, Saison, Öffnungszeiten, Preise, was es vor Ort gibt, Baderegeln, Parkplätze.
- Direkt unter dem Hero ein faktendichter Absatz in 2–3 Sätzen: Was ist das, wo liegt es, wann offen, was kann man dort machen.
- FAQ-Blöcke in echter Frage-Antwort-Form, jede Antwort eigenständig verständlich (Ist der Eintritt kostenpflichtig? Sind Hunde erlaubt? Gibt es Duschen? Kann man vor Ort essen? Ist der See bewacht? Wie komme ich hin?). Was nicht belegt ist: `TODO`, nicht raten.
- `llms.txt` im Root mit strukturierter Zusammenfassung von Betrieb, Saison, Leistungen und Verhältnis zur Partycompany.
- Eckdaten als Tabellen/Definitionslisten statt Werbefließtext.

**Barrierefreiheit**
- Kontrast mindestens 4,5:1 – bei weißem Hintergrund mit Orange besonders prüfen: `#EF760C` auf Weiß liegt **unter** 4,5:1 und darf nicht für Fließtext oder kleine Schrift verwendet werden. Orange nur als Fläche mit dunkler oder weißer Schrift darauf, als Rahmen oder für große Elemente. Textlinks in Navy.
- Sichtbarer Fokus-Stil, volle Tastaturbedienbarkeit, `prefers-reduced-motion` respektieren, responsiv ab 320 px.

**Rechtliches**
- Impressum und Datenschutz als eigene Seiten, mit klar markierten Platzhaltern. Nichts erfinden, nichts von der Partycompany kopieren.
- In der Datenschutzerklärung dokumentieren, dass keine Cookies gesetzt und keine Drittanbieter eingebunden werden.
- Kein Kontaktformular im ersten Wurf: `mailto:`, `tel:` und WhatsApp-Link. Das spart Backend und Datenschutzaufwand; Formular später optional.

## Design

Zielgruppe: Familien und Tagesgäste aus der Region (Bernburg, Könnern, Halle, Aschersleben) sowie Brautpaare und Firmenkunden aus Sachsen-Anhalt. Die Seite soll nach Sommer, Wasser und Luft aussehen – ruhig, hell, einladend – und trotzdem als Geschwister der Partycompany-Seite erkennbar sein.

Bevor du Code schreibst, leg mir einen **kurzen Designplan** vor:

- **Farbpalette** (4–6 benannte Hex-Werte), ausgehend von Weiß `#FDFDFD`, Orange `#EF760C` und Navy `#293742`. Wenn du eine weitere Farbe brauchst (z. B. ein Wasserton), begründe sie in einem Satz.
- **Typografie** – Display- und Body-Schrift, identisch zur Partycompany-Seite, wenn möglich. Falls du abweichst: begründen.
- **Layoutkonzept** als ASCII-Wireframe für Startseite und Hochzeitsseite.
- **Ein „Signature-Element"**, an das man sich erinnert – und das erkennbar mit dem der Partycompany-Seite verwandt ist, ohne es zu kopieren.

Prüfe deinen eigenen Plan kritisch. Wenn ein Teil davon so aussieht, wie du jede beliebige Location-Website bauen würdest, ersetze ihn und sag mir warum. Die üblichen Verdächtigen, die ich nicht sehen will: ganzflächiges Hero-Foto mit zentriertem weißem Text und dunklem Overlay; Karten-Grid mit abgerundeten Ecken und Schlagschatten; „Unsere Leistungen" mit drei Outline-Icons. Setz die Mutigkeit an genau einer Stelle ein und halt den Rest ruhig. Animationen sparsam und nur CSS.

**Warte auf meine Freigabe des Designplans, bevor du die Seiten baust.**

## Lieferumfang

```
/
├── index.html
├── hochzeit/index.html
├── feiern/index.html
├── strandbad/index.html
├── camping/index.html
├── kontakt/index.html
├── impressum/index.html
├── datenschutz/index.html
├── assets/css/main.css
├── assets/img/
├── assets/fonts/
├── robots.txt
├── sitemap.xml
├── llms.txt
├── .htaccess
├── _headers
└── README.md
```

README mit: Deployment auf Cloudflare Pages, Bild-Workflow (Quellformat → WebP, Zielgrößen, Crop-Hinweise), Liste aller offenen `TODO`-Platzhalter, Anleitung zum Austauschen des Event-Teasers und zum Umstellen auf „Saison beendet" außerhalb der Öffnungszeit.

Zum Schluss: Selbstprüfung gegen die harte Anforderungsliste – Punkt für Punkt bestätigen oder Abweichung benennen. Prüfe insbesondere, dass **kein einziger Request an eine fremde Domain** geht, und gib alle `TODO`-Platzhalter gesammelt aus.

## Was ich noch nachliefere

- Öffnungstage (Mo–So oder Di–So?)
- Eintritts- und Campingpreise
- Kontaktdaten und Impressumsdaten des Strandbads
- Strandbad-Logo
- Bilder in höherer Auflösung für die drei kleinen Motive
- Termin und Line-up der nächsten Veranstaltung
