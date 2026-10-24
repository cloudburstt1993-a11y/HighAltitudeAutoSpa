# HAAS Automation Setup — Leads, Reviews, and Follow-ups

Free automation that runs inside a Google Sheet on Ryan's Google account. No
Zapier, no monthly fee. Setup is about 15 minutes. File:
`HAAS-Lead-and-Review-Automation.gs`.

## What it does

- **Lead intake.** Every quote request from the website lands as a row in a
  "Leads" sheet. Phone and DM leads get added with one menu click (HAAS → Add
  lead from call/DM) so they get the same follow-ups.
- **Owner alert.** Ryan gets an email for every lead with one-tap Call and Text
  buttons. Optionally a text message too.
- **Customer auto-reply.** The customer instantly gets a "got it" email with
  what happens next (tint: 2–3 hours, pick a shade on the site; coating: drop-off
  day).
- **Review request.** When the car leaves, tick **Job complete** on the row.
  Customers with an email get a thank-you with a one-tap Google review button.
  Phone-only customers: Ryan gets the text to forward. Sent once, stamped with
  the date.
- **Follow-ups by service.** A daily 9 AM check sends whichever step is due:
  - Window tinting → 30 days: "how's it holding up" plus a referral ask
  - Ceramic coating → 6 months: maintenance wash and inspection → 12 months: top coat
  - Any detail → 6 months: "it's been a season"
  - Fleet accounts → every 30 days, a reminder to Ryan to text them
- **Seasonal pushes.** First week of May (tint before summer) and first week of
  October (protect before mag chloride). One per customer per year; "reply stop"
  is in the email and Ryan unticks **Follow-ups** on that row.
- **Lightweight CRM.** Status dropdown (New, Contacted, Quoted, Scheduled, Won,
  Lost) so nothing gets lost in DMs.

## Before you start

1. **Google review link.** In Google Business Profile, click "Ask for reviews"
   and copy the link. (HAAS already has 88 reviews; this just makes asking
   automatic.)
2. **Optional text alerts.** Ryan's carrier email-to-text address, e.g.
   `9706230825@vtext.com` (Verizon), `@txt.att.net` (AT&T), `@tmomail.net`
   (T-Mobile).

## Setup steps

1. Signed in as ryanclark970@gmail.com, create a new Google Sheet named
   **HAAS Leads**.
2. **Extensions → Apps Script.** Delete the starter code, paste in the full
   `.gs` file.
3. Fill in the `CONFIG` block at the top: review link, optional text address,
   and the website URL once the domain is live.
4. Pick **setup** from the function dropdown and click **Run**. Approve the
   permissions (Google warns "unverified app"; Advanced → Go to project is
   normal for your own scripts). This builds the sheet, the HAAS menu, and the
   two triggers (on-edit for reviews, daily 9 AM for follow-ups).
5. *(Optional)* Run **testLead**. You get an alert email and an auto-reply, and
   a test row appears. Delete the row after.
6. **Deploy → New deployment → Web app.** Execute as: **Me**. Who has access:
   **Anyone**. Deploy, copy the **Web app URL**.
7. In the website repo, open `js/main.js`, paste the URL into
   `FORM_ENDPOINT = ''`, commit, push. The form now sends real leads. (Until
   then it falls back to Formspree if that ID is set, or shows "call us"
   instead.)

## Day-to-day

- A lead comes in → email with Call/Text buttons → Ryan quotes → sets Status.
- Phone or Instagram lead → **HAAS → Add lead from call/DM**, five prompts.
- Car leaves → tick **Job complete**. Review request goes out, Status flips to
  Won, follow-up clock starts.
- Every morning at 9, due follow-ups go out. Phone-only ones arrive in Ryan's
  inbox as "Text <name>: …" with the message ready to paste.
- Fleet: tick **Fleet** on the row (auto-ticked when the service is fleet).
  Ryan gets a "fleet due" email every 30 days with a suggested text.

## Notes and limits

- Gmail sends about 100 automated emails a day. A one-bay shop won't get near it.
- Edit the script later → **Deploy → Manage deployments → Edit → New version**
  keeps the same URL.
- Seasonal pushes only go to customers whose job finished more than 30 days ago,
  so nobody gets a sales email the week after they paid.
- Next upgrade, when Ryan's ready: **missed-call text-back**. The phone rings
  while he's under a car, the caller gets an automatic "I'm mid-job, text me the
  vehicle and I'll quote it" within 30 seconds. Needs OpenPhone (~$15–20/mo) or
  Twilio through n8n; Google Voice can't do it. That's the single highest-value
  add for a one-man shop.
