/**
 * High Altitude Auto Spa — Lead, Review, and Follow-up Automation
 * ----------------------------------------------------------------
 * Runs free inside a Google Sheet (Extensions > Apps Script) on Ryan's Google account.
 *
 * WHAT IT DOES
 *  1. Lead intake: the website quote form POSTs here. Every lead is a row in "Leads".
 *     Phone and DM leads can be added by hand (HAAS menu > Add lead from call/DM) and get
 *     the same follow-ups.
 *  2. Owner alert: Ryan gets an email (and a text, if NOTIFY_SMS_EMAIL is set) for every lead.
 *  3. Auto-reply: the customer instantly gets a "got it, here's what happens next" email.
 *  4. Review request: tick "Job complete" on the row. The customer gets a thank-you email with
 *     the Google review link; phone-only customers get a ready-to-paste text in Ryan's inbox.
 *  5. Follow-ups by service, sent from a daily check:
 *       Ceramic coating  -> 6 months: maintenance wash + inspection   -> 12 months: top coat
 *       Full / interior / exterior detail -> 6 months: "it's been a while"
 *       Window tinting   -> 30 days: referral ask
 *       Fleet            -> every 30 days: Ryan gets a "fleet due" reminder
 *  6. Seasonal pushes to past customers: May (tint before summer), October (protect before
 *     mag chloride). Opt-out by replying "stop"; Ryan unticks the box.
 *
 * SETUP: see "HAAS Automation Setup.md". Short version:
 *   - Fill in CONFIG below
 *   - Run setup() once (approve permissions)
 *   - Deploy > New deployment > Web app (Execute as: Me, Access: Anyone)
 *   - Paste the web app URL into FORM_ENDPOINT in the website's js/main.js
 */

const CONFIG = {
  BUSINESS_NAME: 'High Altitude Auto Spa',
  OWNER_FIRST: 'Ryan',
  NOTIFY_EMAIL: 'ryanclark970@gmail.com',       // where new-lead alerts and reminders go
  NOTIFY_SMS_EMAIL: '',                           // optional email-to-text, e.g. 9706230825@vtext.com (Verizon), @txt.att.net, @tmomail.net
  PHONE: '(970) 623-0825',
  ADDRESS: '2912 Hill Ave, Grand Junction',
  REPLY_WITHIN: 'a few hours during shop hours (Mon–Sat 9–5)',
  GOOGLE_REVIEW_LINK: 'https://g.page/r/PASTE-YOUR-REVIEW-LINK/review',  // Business Profile > Ask for reviews
  WEBSITE: 'https://cloudburstt1993-a11y.github.io/HighAltitudeAutoSpa',
  INSTAGRAM: 'https://www.instagram.com/highaltituteautospa/',
  LEADS_SHEET: 'Leads',
  FOLLOWUPS: true,          // service-based follow-ups
  SEASONAL: true,           // May + October pushes
  SEASONAL_MONTHS: { 5: 'summer', 10: 'winter' },
};

const HEADERS = [
  'Received', 'Source', 'Name', 'Phone', 'Email', 'Vehicle', 'Service', 'Shade', 'Details',
  'Status', 'Job complete', 'Completed on', 'Review requested', 'Follow-ups', 'Follow-up log', 'Fleet',
];
const COL = Object.fromEntries(HEADERS.map((h, i) => [h, i + 1]));
const STATUSES = ['New', 'Contacted', 'Quoted', 'Scheduled', 'Won', 'Lost'];
const SERVICES = ['Window tinting', 'Interior detailing', 'Exterior detailing', 'Full detail (inside and out)',
  'Ceramic coating', 'Paint correction', 'Headlight restoration', 'Graphics or vinyl', 'Fleet or work vehicles', 'Not sure yet'];

/* ============================== SETUP ============================== */

/** Run once from the editor. Builds the Leads tab, menu, and triggers. */
function setup() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sh = ss.getSheetByName(CONFIG.LEADS_SHEET);
  if (!sh) sh = ss.insertSheet(CONFIG.LEADS_SHEET);

  sh.getRange(1, 1, 1, HEADERS.length).setValues([HEADERS])
    .setFontWeight('bold').setBackground('#222222').setFontColor('#ffffff');
  sh.setFrozenRows(1);
  sh.setColumnWidth(COL['Details'], 300);
  sh.setColumnWidth(COL['Follow-up log'], 260);

  const rows = sh.getMaxRows() - 1;
  sh.getRange(2, COL['Status'], rows, 1).setDataValidation(
    SpreadsheetApp.newDataValidation().requireValueInList(STATUSES, true).build());
  sh.getRange(2, COL['Service'], rows, 1).setDataValidation(
    SpreadsheetApp.newDataValidation().requireValueInList(SERVICES, true).setAllowInvalid(true).build());
  sh.getRange(2, COL['Job complete'], rows, 1).insertCheckboxes();
  sh.getRange(2, COL['Follow-ups'], rows, 1).insertCheckboxes();
  sh.getRange(2, COL['Fleet'], rows, 1).insertCheckboxes();

  ScriptApp.getProjectTriggers()
    .filter(t => ['onSheetEdit', 'dailyFollowups'].includes(t.getHandlerFunction()))
    .forEach(t => ScriptApp.deleteTrigger(t));
  ScriptApp.newTrigger('onSheetEdit').forSpreadsheet(ss).onEdit().create();   // installable: simple onEdit can't send mail
  ScriptApp.newTrigger('dailyFollowups').timeBased().everyDays(1).atHour(9).create();

  onOpen();
  Logger.log('HAAS setup complete.');
}

/** Adds the HAAS menu to the sheet. */
function onOpen() {
  SpreadsheetApp.getUi().createMenu('HAAS')
    .addItem('Add lead from call/DM', 'addLeadFromCall')
    .addItem('Send follow-ups due today', 'dailyFollowups')
    .addItem('Send me a test lead', 'testLead')
    .addToUi();
}

/* ============================ LEAD INTAKE ============================ */

/** The website quote form POSTs here (JSON or form-encoded). */
function doPost(e) {
  try {
    // The site sends JSON as text/plain (avoids a CORS preflight); plain form posts land in e.parameter.
    let d = {};
    const raw = e && e.postData && e.postData.contents;
    if (raw && raw.trim().startsWith('{')) d = JSON.parse(raw);
    else d = (e && e.parameter) || {};
    if (clean(d._gotcha || d.website)) return json({ ok: true });     // honeypot: bots fill the hidden field

    const lead = {
      source: clean(d.source) || 'Website',
      name: clean(d.name), phone: clean(d.phone), email: clean(d.email),
      vehicle: clean(d.vehicle), service: clean(d.service), shade: clean(d.shade),
      details: clean(d.message || d.details, 2000),
    };
    if (!lead.name && !lead.phone && !lead.email) return json({ ok: false, error: 'empty' });
    addLead(lead);
    return json({ ok: true });
  } catch (err) {
    console.error(err);
    return json({ ok: false, error: String(err) });
  }
}

/** Visiting the web app URL in a browser confirms it's running. */
function doGet() {
  return ContentService.createTextOutput(CONFIG.BUSINESS_NAME + ' lead endpoint is running.');
}

function addLead(lead) {
  const sh = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.LEADS_SHEET);
  const fleet = /fleet|work vehicle/i.test(lead.service);
  sh.appendRow([new Date(), lead.source, lead.name, lead.phone, lead.email, lead.vehicle, lead.service, lead.shade,
    lead.details, 'New', false, '', '', true, '', fleet]);
  const row = sh.getLastRow();
  [COL['Job complete'], COL['Follow-ups'], COL['Fleet']].forEach(c => sh.getRange(row, c).insertCheckboxes());
  sh.getRange(row, COL['Follow-ups']).setValue(true);
  sh.getRange(row, COL['Fleet']).setValue(fleet);
  notifyOwner(lead);
  if (lead.email) autoReply(lead);
}

/** Menu: log a phone or DM lead so it gets the same review request and follow-ups. */
function addLeadFromCall() {
  const ui = SpreadsheetApp.getUi();
  const ask = (q) => { const r = ui.prompt(q); return r.getSelectedButton() === ui.Button.OK ? r.getResponseText().trim() : null; };
  const name = ask('Customer name'); if (name === null) return;
  const phone = ask('Phone'); if (phone === null) return;
  const vehicle = ask('Vehicle (year make model)'); if (vehicle === null) return;
  const service = ask('Service (' + SERVICES.slice(0, 6).join(', ') + '...)'); if (service === null) return;
  const email = ask('Email (leave blank if none)'); if (email === null) return;
  const sh = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.LEADS_SHEET);
  const fleet = /fleet|work vehicle/i.test(service);
  sh.appendRow([new Date(), 'Call/DM', name, phone, email, vehicle, service, '', '', 'Contacted', false, '', '', true, '', fleet]);
  const row = sh.getLastRow();
  [COL['Job complete'], COL['Follow-ups'], COL['Fleet']].forEach(c => sh.getRange(row, c).insertCheckboxes());
  sh.getRange(row, COL['Follow-ups']).setValue(true);
  sh.getRange(row, COL['Fleet']).setValue(fleet);
  ui.alert('Added. Tick "Job complete" when the car leaves and the review request goes out.');
}

function notifyOwner(lead) {
  const who = [lead.name, lead.vehicle].filter(Boolean).join(' — ') || 'Unknown';
  const subject = `New lead: ${who}${lead.service ? ' · ' + lead.service : ''}`;
  const rows = [
    ['Name', lead.name], ['Phone', lead.phone], ['Email', lead.email], ['Vehicle', lead.vehicle],
    ['Service', lead.service], ['Shade', lead.shade], ['Details', lead.details],
  ].filter(r => r[1]);
  const call = lead.phone ? `<p style="margin:16px 0"><a href="tel:${esc(lead.phone.replace(/[^\d+]/g, ''))}" style="background:#f06a1c;color:#161616;padding:12px 22px;text-decoration:none;font-weight:bold">Call ${esc(lead.name || 'them')}</a>
     &nbsp; <a href="sms:${esc(lead.phone.replace(/[^\d+]/g, ''))}" style="background:#222;color:#fff;padding:12px 22px;text-decoration:none;font-weight:bold">Text</a></p>` : '';
  const html =
    `<div style="font-family:Arial,sans-serif;max-width:560px;color:#161616">
      <h2 style="margin:0 0 12px">New lead from the website</h2>
      <table style="border-collapse:collapse;width:100%">${rows.map(([k, v]) =>
        `<tr><td style="padding:6px 10px;background:#eef0f2;font-weight:bold;width:110px;vertical-align:top">${k}</td>
         <td style="padding:6px 10px;border-bottom:1px solid #ddd;white-space:pre-wrap">${esc(v)}</td></tr>`).join('')}
      </table>${call}
      <p style="color:#4e555c;font-size:13px">Logged in the Leads sheet. Customer ${lead.email ? 'got an auto-reply.' : 'left no email, so call or text them.'}</p>
    </div>`;
  MailApp.sendEmail({ to: CONFIG.NOTIFY_EMAIL, subject, htmlBody: html, replyTo: lead.email || undefined });

  if (CONFIG.NOTIFY_SMS_EMAIL) {
    MailApp.sendEmail(CONFIG.NOTIFY_SMS_EMAIL, 'New lead',
      `${lead.name || 'New lead'} ${lead.phone || ''} ${lead.vehicle || ''} ${lead.service || ''}`.replace(/\s+/g, ' ').trim().slice(0, 150));
  }
}

function autoReply(lead) {
  const first = firstName(lead.name);
  const next = /tint/i.test(lead.service)
    ? `<p>Tint jobs usually take 2–3 hours and you can wait or drop off. If you haven't picked a shade yet, the picker on the website shows what each one looks like: <a href="${CONFIG.WEBSITE}/services/window-tinting.html">${CONFIG.WEBSITE}/services/window-tinting.html</a></p>`
    : /ceramic/i.test(lead.service)
    ? `<p>Coatings are a drop-off job: the car needs a day in the shop to prep, coat, and cure. We'll walk you through the options when we call.</p>`
    : `<p>We'll give you a firm price for the vehicle before any work starts, and that's the price you pay.</p>`;
  const html =
    `<div style="font-family:Arial,sans-serif;max-width:560px;color:#161616">
      <p>Hi ${esc(first)},</p>
      <p>Got your request${lead.vehicle ? ' for the <b>' + esc(lead.vehicle) + '</b>' : ''}${lead.service ? ' (' + esc(lead.service.toLowerCase()) + ')' : ''}. I'll get back to you within ${CONFIG.REPLY_WITHIN} with a price.</p>
      ${next}
      <p>Need it sooner? Call or text <b>${CONFIG.PHONE}</b>.</p>
      <p>${CONFIG.OWNER_FIRST}<br>${CONFIG.BUSINESS_NAME}<br>${CONFIG.ADDRESS}</p>
    </div>`;
  MailApp.sendEmail({ to: lead.email, subject: `Got it — ${CONFIG.BUSINESS_NAME}`, htmlBody: html, replyTo: CONFIG.NOTIFY_EMAIL, name: CONFIG.BUSINESS_NAME });
}

/* ========================== REVIEW REQUESTS ========================== */

/** Fires on any edit. Ticking "Job complete" sends the review request once and stamps the date. */
function onSheetEdit(e) {
  const r = e.range, sh = r.getSheet();
  if (sh.getName() !== CONFIG.LEADS_SHEET || r.getRow() < 2) return;
  if (r.getColumn() !== COL['Job complete'] || r.getValue() !== true) return;

  const row = r.getRow();
  const vals = sh.getRange(row, 1, 1, HEADERS.length).getValues()[0];
  if (vals[COL['Review requested'] - 1]) return;

  const name = vals[COL['Name'] - 1], email = vals[COL['Email'] - 1], phone = vals[COL['Phone'] - 1], service = vals[COL['Service'] - 1];
  const today = new Date();
  if (!vals[COL['Completed on'] - 1]) sh.getRange(row, COL['Completed on']).setValue(today);
  const stamp = sh.getRange(row, COL['Review requested']);

  if (email) {
    sendReviewRequest(name, email, service);
    stamp.setValue('Emailed ' + fmt(today));
  } else {
    stamp.setValue('No email — text sent to you');
    MailApp.sendEmail(CONFIG.NOTIFY_EMAIL, `Text a review request to ${name || 'customer'}`,
      `No email on file for ${name || 'this customer'} (${phone || 'no phone'}).\n\nCopy-paste text:\n\n` + reviewText(name, service));
    if (CONFIG.NOTIFY_SMS_EMAIL) MailApp.sendEmail(CONFIG.NOTIFY_SMS_EMAIL, 'Review ask', `Fwd to ${phone}: ` + reviewText(name, service));
  }
  if (vals[COL['Status'] - 1] !== 'Won') sh.getRange(row, COL['Status']).setValue('Won');
}

function sendReviewRequest(name, email, service) {
  const first = firstName(name);
  const html =
    `<div style="font-family:Arial,sans-serif;max-width:560px;color:#161616">
      <p>Hi ${esc(first)},</p>
      <p>Thanks for bringing the car in${service ? ' for ' + esc(String(service).toLowerCase()) : ''}. Hope it looks the way you pictured.</p>
      <p>I'm a one-man shop and Google reviews are most of how people find me. If you've got 30 seconds, this link goes straight to the review box:</p>
      <p style="margin:22px 0"><a href="${CONFIG.GOOGLE_REVIEW_LINK}" style="background:#f06a1c;color:#161616;padding:12px 22px;text-decoration:none;font-weight:bold">Leave a Google review</a></p>
      <p>If anything isn't right, reply to this email or text me at ${CONFIG.PHONE} and I'll fix it.</p>
      <p>${CONFIG.OWNER_FIRST}<br>${CONFIG.BUSINESS_NAME}</p>
    </div>`;
  MailApp.sendEmail({ to: email, subject: `Thanks from ${CONFIG.OWNER_FIRST} at ${CONFIG.BUSINESS_NAME}`, htmlBody: html, replyTo: CONFIG.NOTIFY_EMAIL, name: CONFIG.BUSINESS_NAME });
}

/** Text version for phone-only customers. */
function reviewText(name, service) {
  return `Hey ${firstName(name)}, it's ${CONFIG.OWNER_FIRST} at ${CONFIG.BUSINESS_NAME}. Thanks for bringing the car in! ` +
    `If you've got 30 seconds, a Google review helps a one-man shop more than anything: ${CONFIG.GOOGLE_REVIEW_LINK}`;
}

/* ============================ FOLLOW-UPS ============================= */

/**
 * Daily at 9 AM. For every completed job with "Follow-ups" ticked, sends whichever step is due,
 * once, and logs it. Phone-only customers: Ryan gets the text to forward.
 *   tint:    30d referral
 *   ceramic: 180d maintenance, 365d top coat
 *   detail:  180d nudge
 *   fleet:   every 30d, reminder to Ryan only
 * Seasonal (May/Oct): one email per customer per year, to everyone completed > 30 days ago.
 */
function dailyFollowups() {
  const sh = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.LEADS_SHEET);
  const last = sh.getLastRow(); if (last < 2) return;
  const data = sh.getRange(2, 1, last - 1, HEADERS.length).getValues();
  const today = new Date(), month = today.getMonth() + 1;
  const season = CONFIG.SEASONAL && CONFIG.SEASONAL_MONTHS[month] && today.getDate() <= 7 ? CONFIG.SEASONAL_MONTHS[month] : null;
  const fleetDue = [];

  data.forEach((v, i) => {
    const row = i + 2;
    const done = v[COL['Completed on'] - 1];
    if (!v[COL['Job complete'] - 1] || !(done instanceof Date) || !v[COL['Follow-ups'] - 1]) return;
    const days = Math.floor((today - done) / 864e5);
    const log = String(v[COL['Follow-up log'] - 1] || '');
    const name = v[COL['Name'] - 1], email = v[COL['Email'] - 1], phone = v[COL['Phone'] - 1];
    const service = String(v[COL['Service'] - 1] || ''), vehicle = v[COL['Vehicle'] - 1];
    const sent = [];

    if (v[COL['Fleet'] - 1]) {
      if (days >= 30 && !log.includes('fleet ' + Math.floor(days / 30))) {
        fleetDue.push(`${name} (${vehicle || 'fleet'}) — ${phone || email} — last done ${fmt(done)}`);
        sent.push('fleet ' + Math.floor(days / 30));
      }
    } else if (CONFIG.FOLLOWUPS) {
      const steps = followupSteps(service);
      steps.forEach(s => {
        if (days >= s.days && !log.includes(s.key)) {
          deliver(name, email, phone, s.subject, s.body(firstName(name), vehicle), s.text(firstName(name)));
          sent.push(s.key);
        }
      });
    }
    if (season && days >= 30 && !log.includes(season + ' ' + today.getFullYear()) && !v[COL['Fleet'] - 1]) {
      const s = seasonal(season);
      deliver(name, email, phone, s.subject, s.body(firstName(name)), s.text(firstName(name)));
      sent.push(season + ' ' + today.getFullYear());
    }
    if (sent.length) sh.getRange(row, COL['Follow-up log']).setValue((log ? log + '; ' : '') + sent.map(k => k + ' ' + fmt(today)).join('; '));
  });

  if (fleetDue.length) {
    MailApp.sendEmail(CONFIG.NOTIFY_EMAIL, `Fleet due: ${fleetDue.length} account${fleetDue.length > 1 ? 's' : ''}`,
      `These fleet accounts are 30+ days since their last job. Text them to schedule:\n\n` + fleetDue.join('\n') +
      `\n\nSuggested text: "Hey, it's ${CONFIG.OWNER_FIRST} at High Altitude. The vans are about due for a wash — want me to pencil you in this week?"`);
  }
}

function followupSteps(service) {
  const s = service.toLowerCase();
  const sig = `\n\n${CONFIG.OWNER_FIRST}, ${CONFIG.BUSINESS_NAME} · ${CONFIG.PHONE}`;
  if (s.includes('tint')) return [{
    key: 'tint30', days: 30, subject: `How's the tint holding up?`,
    body: (f, v) => `<p>Hi ${esc(f)},</p><p>It's been a month on the ${esc(v || 'car')}. The film should be fully cured and clear by now; if you see any haze or a bubble, text me a photo and I'll take care of it.</p><p>One ask: if someone you know is sweating through their commute, send them my way. Most of my work is word of mouth, and I take care of people who come in on a referral.</p><p>${CONFIG.OWNER_FIRST}<br>${CONFIG.BUSINESS_NAME} · ${CONFIG.PHONE}</p>`,
    text: (f) => `Hey ${f}, ${CONFIG.OWNER_FIRST} at High Altitude. A month in, the tint should be fully cured. Any haze or bubbles, text me a pic. And if you know anyone who wants tint, send them my way. ${CONFIG.PHONE}`,
  }];
  if (s.includes('ceramic')) return [
    { key: 'ceramic180', days: 180, subject: `Six months on the coating: time for a check`,
      body: (f, v) => `<p>Hi ${esc(f)},</p><p>The coating on the ${esc(v || 'car')} is six months old. A maintenance wash and a quick inspection now keeps it beading the way it did on day one and catches anything the mag chloride started. It's a short visit; drop off or wait.</p><p>Text me a day that works.</p><p>${CONFIG.OWNER_FIRST}<br>${CONFIG.BUSINESS_NAME} · ${CONFIG.PHONE}</p>`,
      text: (f) => `Hey ${f}, ${CONFIG.OWNER_FIRST} at High Altitude. The coating's 6 months old. A maintenance wash + inspection keeps it beading like day one. Text me a day that works. ${CONFIG.PHONE}` },
    { key: 'ceramic365', days: 365, subject: `A year on the coating`,
      body: (f, v) => `<p>Hi ${esc(f)},</p><p>It's been a year since we coated the ${esc(v || 'car')}. A decon wash and a top coat now resets the protection for another year, for a lot less than a full re-coat later.</p><p>Want me to get you on the schedule?</p><p>${CONFIG.OWNER_FIRST}<br>${CONFIG.BUSINESS_NAME} · ${CONFIG.PHONE}</p>`,
      text: (f) => `Hey ${f}, ${CONFIG.OWNER_FIRST} at High Altitude. It's been a year on the coating. A decon wash + top coat resets it for another year. Want on the schedule? ${CONFIG.PHONE}` },
  ];
  if (s.includes('detail')) return [{
    key: 'detail180', days: 180, subject: `It's been six months`,
    body: (f, v) => `<p>Hi ${esc(f)},</p><p>Six months since we detailed the ${esc(v || 'car')}, which around here means a season of dust or a season of mag chloride, depending. If it's due, text me and I'll get you in.</p><p>${CONFIG.OWNER_FIRST}<br>${CONFIG.BUSINESS_NAME} · ${CONFIG.PHONE}</p>`,
    text: (f) => `Hey ${f}, ${CONFIG.OWNER_FIRST} at High Altitude. 6 months since the detail, which here means a season of dust or mag chloride. If it's due, text me and I'll get you in. ${CONFIG.PHONE}`,
  }];
  return [];
}

function seasonal(season) {
  if (season === 'summer') return {
    subject: `Tint before the heat gets here`,
    body: (f) => `<p>Hi ${esc(f)},</p><p>May is when the Grand Junction sun stops being nice. Ceramic tint takes the cabin down by double digits and blocks the UV that cooks dashboards, and I'm booking it now before the June rush. Pick a shade on the site and text me: ${CONFIG.WEBSITE}/services/window-tinting.html</p><p>Reply "stop" if you'd rather not get these.</p><p>${CONFIG.OWNER_FIRST}<br>${CONFIG.BUSINESS_NAME} · ${CONFIG.PHONE}</p>`,
    text: (f) => `Hey ${f}, ${CONFIG.OWNER_FIRST} at High Altitude. Booking tint now before the June heat. Pick a shade and text me: ${CONFIG.WEBSITE}/services/window-tinting.html`,
  };
  return {
    subject: `Protect the paint before mag chloride season`,
    body: (f) => `<p>Hi ${esc(f)},</p><p>The deicer goes down on I-70 in a few weeks and it sits on paint and wheels all winter. A wash, decon, and sealant (or a ceramic coating if you've been thinking about it) now means it rinses off instead of eating in. Text me a day that works.</p><p>Reply "stop" if you'd rather not get these.</p><p>${CONFIG.OWNER_FIRST}<br>${CONFIG.BUSINESS_NAME} · ${CONFIG.PHONE}</p>`,
    text: (f) => `Hey ${f}, ${CONFIG.OWNER_FIRST} at High Altitude. Mag chloride season's a few weeks out. Wash + sealant now means it rinses off instead of eating in. Text me a day. ${CONFIG.PHONE}`,
  };
}

/** Email if there's an address; otherwise hand the text to Ryan to forward. */
function deliver(name, email, phone, subject, html, text) {
  if (email) {
    MailApp.sendEmail({ to: email, subject, htmlBody: `<div style="font-family:Arial,sans-serif;max-width:560px;color:#161616">${html}</div>`, replyTo: CONFIG.NOTIFY_EMAIL, name: CONFIG.BUSINESS_NAME });
  } else {
    MailApp.sendEmail(CONFIG.NOTIFY_EMAIL, `Text ${name || 'customer'}: ${subject}`, `No email for ${name} (${phone}). Copy-paste text:\n\n${text}`);
    if (CONFIG.NOTIFY_SMS_EMAIL) MailApp.sendEmail(CONFIG.NOTIFY_SMS_EMAIL, 'Follow-up', `Fwd to ${phone}: ${text}`.slice(0, 300));
  }
}

/* ============================== HELPERS ============================== */

function clean(v, max) { return String(v == null ? '' : v).trim().slice(0, max || 300); }
function esc(s) { return String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c])); }
function json(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }
function firstName(n) { return String(n || '').trim().split(/\s+/)[0] || 'there'; }
function fmt(d) { return Utilities.formatDate(d, Session.getScriptTimeZone(), 'M/d/yyyy'); }

/** Sends yourself a fake lead to confirm everything works. Delete the row after. */
function testLead() {
  doPost({ postData: { type: 'application/json', contents: JSON.stringify({
    source: 'Test', name: 'Test Customer', phone: '(970) 555-0100', email: CONFIG.NOTIFY_EMAIL,
    vehicle: '2019 Toyota Tacoma', service: 'Window tinting', shade: '20%', message: 'Test lead — delete this row.'
  }) } });
}
