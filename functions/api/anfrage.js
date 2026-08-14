/**
 * Cloudflare Pages Function für das Anfrageformular auf /kontakt/.
 *
 * Nimmt die Formular-POST-Daten entgegen, prüft sie serverseitig und
 * verschickt sie per Cloudflare Email Routing (send_email-Binding) als
 * E-Mail an die feste Zieladresse. Kein Drittanbieter, keine Datenbank,
 * keine Speicherung – die Daten laufen einmalig durch diese Function durch
 * und landen als E-Mail im Postfach.
 *
 * Setup-Voraussetzungen (siehe README.md):
 *   1. Domain strandbad-gerlebogk.de liegt bei Cloudflare.
 *   2. Cloudflare Email Routing ist für die Domain aktiviert.
 *   3. fischerparty@web.de ist dort als Zieladresse verifiziert.
 *   4. Das send_email-Binding "ANFRAGE_MAIL" ist im Pages-Projekt mit
 *      genau dieser Zieladresse verknüpft (wrangler.toml oder Dashboard).
 *
 * Ohne dieses Binding schlägt der E-Mail-Versand fehl; das Formular zeigt
 * dann die Fehlerseite statt der Danke-Seite.
 */

import { EmailMessage } from "cloudflare:email";

const ZIEL_ADRESSE = "fischerparty@web.de";
const ABSENDER_ADRESSE = "anfrage@strandbad-gerlebogk.de";

const ANLASS_LABELS = {
  hochzeit: "Hochzeit",
  catering: "Catering & Buffet",
  feiern: "Feiern (Geburtstag, Firmen, Schulklasse)",
  camping: "Camping",
  sonstiges: "Sonstiges",
};

function escapeForHeader(value) {
  // Verhindert Header-Injection über Zeilenumbrüche in Formularfeldern.
  return value.replace(/[\r\n]/g, " ").trim();
}

function fehlerSeite(nachricht) {
  // Nutzt main.css statt eines inline <style>-Blocks: die Seite läuft unter
  // derselben strikten CSP (style-src 'self') wie der Rest der Website, ein
  // <style>-Block wäre dort blockiert.
  const html = `<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Anfrage konnte nicht gesendet werden – Strandbad Gerlebogk</title>
<meta name="robots" content="noindex">
<link rel="stylesheet" href="/assets/css/main.css">
</head>
<body>
<main id="inhalt">
  <section class="section">
    <div class="wrap prosa">
      <div class="fakten">
        <h1>Anfrage konnte nicht gesendet werden</h1>
        <p>${nachricht}</p>
      </div>
      <p class="mt-l"><a class="btn btn--anfrage" href="/kontakt/">Zurück zum Formular</a></p>
    </div>
  </section>
</main>
</body>
</html>`;
  return new Response(html, {
    status: 400,
    headers: { "content-type": "text/html; charset=utf-8" },
  });
}

export async function onRequestPost(context) {
  const { request, env } = context;

  let form;
  try {
    form = await request.formData();
  } catch {
    return fehlerSeite("Das Formular konnte nicht gelesen werden. Bitte versucht es erneut.");
  }

  // Honeypot: unsichtbares Feld, das nur Bots ausfüllen.
  if ((form.get("website") || "").toString().trim() !== "") {
    // Für Bots sieht das wie ein Erfolg aus, es passiert aber nichts.
    return Response.redirect(new URL("/kontakt/danke/", request.url), 303);
  }

  const name = escapeForHeader((form.get("name") || "").toString());
  const email = escapeForHeader((form.get("email") || "").toString());
  const telefon = escapeForHeader((form.get("telefon") || "").toString());
  const anlassKey = (form.get("anlass") || "").toString();
  const termin = (form.get("termin") || "").toString().trim();
  const personen = (form.get("personen") || "").toString().trim();
  const nachricht = (form.get("nachricht") || "").toString().trim();
  const datenschutz = form.get("datenschutz");

  if (!name || !email || !anlassKey || !nachricht) {
    return fehlerSeite("Bitte füllt Name, E-Mail, Art der Anfrage und eine kurze Nachricht aus – das sind Pflichtfelder.");
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return fehlerSeite("Die E-Mail-Adresse sieht nicht gültig aus. Bitte prüft die Eingabe.");
  }
  if (!datenschutz) {
    return fehlerSeite("Bitte bestätigt die Datenschutzhinweise, damit wir eure Anfrage bearbeiten dürfen.");
  }

  const anlass = ANLASS_LABELS[anlassKey] || anlassKey;

  const zeilen = [
    `Neue Anfrage über strandbad-gerlebogk.de`,
    ``,
    `Art der Anfrage: ${anlass}`,
    `Name: ${name}`,
    `E-Mail: ${email}`,
    telefon ? `Telefon: ${telefon}` : null,
    termin ? `Wunschtermin: ${termin}` : `Wunschtermin: (nicht angegeben)`,
    personen ? `Anzahl Personen: ${personen}` : null,
    ``,
    `Nachricht:`,
    nachricht,
  ].filter((zeile) => zeile !== null);

  const textBody = zeilen.join("\r\n");

  const raw =
    `From: Anfrageformular Strandbad Gerlebogk <${ABSENDER_ADRESSE}>\r\n` +
    `To: ${ZIEL_ADRESSE}\r\n` +
    `Reply-To: ${name} <${email}>\r\n` +
    `Subject: Anfrage (${anlass}) von ${name}\r\n` +
    `MIME-Version: 1.0\r\n` +
    `Content-Type: text/plain; charset="UTF-8"\r\n` +
    `Content-Transfer-Encoding: 8bit\r\n` +
    `\r\n` +
    textBody;

  try {
    const message = new EmailMessage(ABSENDER_ADRESSE, ZIEL_ADRESSE, raw);
    await env.ANFRAGE_MAIL.send(message);
  } catch (err) {
    return fehlerSeite(
      "Der E-Mail-Versand ist gerade nicht möglich. Bitte schreibt uns in der Zwischenzeit direkt an " +
      `<a href="mailto:info@party-company.de">info@party-company.de</a>.`
    );
  }

  return Response.redirect(new URL("/kontakt/danke/", request.url), 303);
}

export async function onRequestGet() {
  return new Response("Diese Adresse verarbeitet nur Formular-Anfragen (POST).", { status: 405 });
}
