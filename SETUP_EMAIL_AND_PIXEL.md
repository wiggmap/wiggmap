# 📋 Setup Email + Meta Pixel — 15 minutes

Quick setup guide for the two missing pieces:
1. **Meta Pixel** (Facebook/Instagram retargeting)
2. **Email service** (Buttondown for newsletter)

Both are **free** to start.

---

## 1. Meta Pixel (5 min)

### Step 1 — Create the pixel
1. Go to https://business.facebook.com/events_manager/
2. If you don't have a Business account, create one (free)
3. Click **"Connect data sources"** → **Web** → **Meta Pixel**
4. Name it **WiggMap** → Continue
5. Choose **"Set up the pixel manually"** (not partner integration)
6. **Copy the Pixel ID** — it's a 15-16 digit number like `123456789012345`

### Step 2 — Drop the ID into the code
Open `data/header.js`. At the top of the file, find this line:

```javascript
var META_PIXEL_ID = 'YOUR_PIXEL_ID'; // ← REPLACE WITH REAL ID
```

Replace `YOUR_PIXEL_ID` with the number you copied. Save. Push to Netlify.

### Step 3 — Verify it's working
1. Install **Meta Pixel Helper** Chrome extension
2. Visit https://wiggmap.com/
3. The extension should turn green and show "PageView fired"

⚠️ Note: the pixel only fires after the user accepts cookies (GDPR-compliant). Test in incognito and accept the cookie banner first.

### Step 4 — Set up the conversion event
The form already fires a `Lead` event when someone signs up to the newsletter (handled in `data/footer.js`). After 7 days you should see "Lead" events in your Meta Events Manager.

---

## 2. Email service — Buttondown (10 min)

We use **Buttondown** because:
- Free up to 100 subscribers, $9/month after
- Simple API that works with any HTML form (no plugin)
- Good deliverability
- GDPR-friendly

### Step 1 — Create account
1. Go to https://buttondown.email
2. Sign up with your email
3. Pick a username — this becomes your **public newsletter URL** (e.g., `wiggmap` → `buttondown.email/wiggmap`)
4. Set the newsletter name to **WiggMap Weekly** (or whatever)
5. Skip the paid tiers — start free

### Step 2 — Drop the username into the code
Open `data/footer.js`. Find this line:

```javascript
var BUTTONDOWN_USERNAME = ''; // ← e.g. 'wiggmap'
```

Replace `''` with your Buttondown username, like:
```javascript
var BUTTONDOWN_USERNAME = 'wiggmap';
```

Save. Push to Netlify.

### Step 3 — Test
1. Go to https://wiggmap.com/
2. Scroll to the newsletter form at the bottom
3. Enter a test email
4. Check Buttondown dashboard → **Subscribers** — your test email should appear

That's it. Every newsletter signup is now **dual-stored**:
- **Netlify Forms** (your backup, accessible in Netlify dashboard → Forms)
- **Buttondown** (your sending tool)

### Step 4 — Send your first email
In Buttondown:
1. **Emails** → **New email**
2. Subject: `Welcome to WiggMap`
3. Body: short intro + link to your top 3 chronicles
4. **Send to all subscribers**

Repeat once a week with a new chronicle highlight. Keep it short (300 words max).

---

## 3. Quick checklist before going live

- [ ] Meta Pixel ID added to `data/header.js`
- [ ] Buttondown username added to `data/footer.js`
- [ ] Tested newsletter signup → email appears in both Netlify Forms and Buttondown
- [ ] Tested Meta Pixel → green helper extension on the home page
- [ ] First welcome email drafted in Buttondown
- [ ] Both files pushed to Netlify

---

## 4. Alternatives if Buttondown isn't right

| Service | Free tier | Best for |
|---|---|---|
| **Buttondown** | 100 subs, then $9/mo | Simplest, best for starting |
| **ConvertKit (Kit)** | 1000 subs free | More features, automation |
| **Resend** | 3000 emails/mo free | Developer-friendly, transactional + newsletter |
| **Beehiiv** | 2500 subs free | Built-in monetization (sponsorship marketplace) |

To switch from Buttondown to one of these, you'd need to change the form `action` URL in `data/footer.js`. The code structure supports any of them with a small tweak — ping me if you want help.

---

## 5. After 30 days

Once you have:
- 50+ newsletter subscribers
- 500+ pixel-tracked visitors
- 1+ Lead conversion in Meta Events Manager

You're ready to launch:
1. **Brand search Google** — bid on "wiggmap" (~30€/mo)
2. **Retargeting Meta** — show ads to people who visited but didn't subscribe (~70€/mo)

Without these two prerequisites, paid acquisition is wasted budget. With them, every euro works 5-10x harder.
