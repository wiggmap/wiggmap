// data/correction-form.js
// Netlify Forms modal (NO fetch). Works from any page.
(function () {
  const FORM_NAME = "wiggmap-corrections";

  function countryFromTitle() {
    const t = (document.title || "").split("—")[0].trim();
    return t || "Country";
  }

  // Prevent double-injection if script is loaded twice
  if (window.__WM_CORRECTION_LOADED__) return;
  window.__WM_CORRECTION_LOADED__ = true;

  const css = `
  .wm-backdrop{position:fixed;inset:0;background:rgba(0,0,0,.45);display:none;align-items:center;justify-content:center;padding:18px;z-index:9999}
  .wm-modal{width:min(560px,100%);background:#fff;border-radius:16px;border:1px solid rgba(0,0,0,.10);box-shadow:0 18px 60px rgba(0,0,0,.25);overflow:hidden;font-family: Arial, Helvetica, sans-serif}
  .wm-head{padding:14px 16px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid rgba(0,0,0,.10)}
  .wm-head strong{font-size:15px}
  .wm-body{padding:14px 16px}
  .wm-body p{margin:0 0 12px;color:#5b6b62;font-weight:700;font-size:13px;line-height:1.4}
  .wm-body label{display:block;font-weight:900;font-size:12px;color:#2a3a32;margin:10px 0 6px}
  .wm-body input,.wm-body textarea{width:100%;padding:10px 12px;border-radius:12px;border:1px solid rgba(0,0,0,.12);font-size:14px;outline:none}
  .wm-body textarea{min-height:90px;resize:vertical}
  .wm-actions{display:flex;justify-content:flex-end;gap:10px;padding:14px 16px;border-top:1px solid rgba(0,0,0,.10);background:#fafbfa}
  .wm-btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;padding:10px 12px;border-radius:12px;font-weight:900;border:1px solid rgba(0,0,0,.12);background:#fff;cursor:pointer}
  .wm-btn:hover{background:rgba(0,0,0,.04)}
  .wm-btn.primary{background:#2ecc71;color:#fff;border-color:transparent}
  .wm-btn.primary:hover{background:#27ae60}
  .wm-req{color:#ff5a5f;font-weight:900;margin-left:4px}
  .wm-toast{position:fixed;left:50%;bottom:18px;transform:translateX(-50%);background:rgba(20,24,22,.92);color:#fff;padding:10px 12px;border-radius:999px;font-weight:900;font-size:13px;box-shadow:0 12px 30px rgba(0,0,0,.25);display:none;z-index:10000}
  `;

  const style = document.createElement("style");
  style.textContent = css;
  document.head.appendChild(style);

  const backdrop = document.createElement("div");
  backdrop.className = "wm-backdrop";
  backdrop.id = "wmBackdrop";

  // action "/" = Netlify handles it; we keep user on same page (no redirect)
  backdrop.innerHTML = `
    <div class="wm-modal" role="dialog" aria-modal="true" aria-label="Suggest correction">
      <div class="wm-head">
        <strong>Suggest a correction</strong>
        <button class="wm-btn" type="button" id="wmCloseTop">Close</button>
      </div>

      <form class="wm-body"
            id="wmForm"
            name="${FORM_NAME}"
            method="POST"
            data-netlify="true"
            data-netlify-honeypot="bot-field"
            action="/">
        <input type="hidden" name="form-name" value="${FORM_NAME}" />
        <input type="hidden" name="country" id="wmCountry" value="" />

        <p style="display:none;">
          <label>Don’t fill this out: <input name="bot-field" /></label>
        </p>

        <p id="wmIntro"></p>

        <label>Field <span class="wm-req">*</span></label>
        <input id="wmField" name="field" type="text" placeholder="e.g., Electricity / month" required />

        <label>Your suggested value <span class="wm-req">*</span></label>
        <input id="wmValue" name="value" type="text" placeholder="e.g., $30" required />

        <label>Your email <span class="wm-req">*</span></label>
        <input id="wmEmail" name="email" type="email" placeholder="name@email.com" required />

        <label>Notes / Source (optional)</label>
        <textarea id="wmNotes" name="notes" placeholder="City/region, source link, date…"></textarea>
      </form>

      <div class="wm-actions">
        <button class="wm-btn" type="button" id="wmCancel">Cancel</button>
        <button class="wm-btn primary" type="button" id="wmSend">Send</button>
      </div>
    </div>
  `;

  document.body.appendChild(backdrop);

  const toast = document.createElement("div");
  toast.className = "wm-toast";
  toast.id = "wmToast";
  toast.textContent = "Sent ✅ Thank you!";
  document.body.appendChild(toast);

  function showToast() {
    toast.style.display = "block";
    setTimeout(() => (toast.style.display = "none"), 2200);
  }

  function hide() {
    backdrop.style.display = "none";
  }

  function show(prefillField) {
    const country = countryFromTitle();
    document.getElementById("wmIntro").innerHTML =
      `Suggest an update for <strong>${country}</strong>.`;
    document.getElementById("wmCountry").value = country;

    document.getElementById("wmField").value = prefillField || "";
    document.getElementById("wmValue").value = "";
    document.getElementById("wmEmail").value = "";
    document.getElementById("wmNotes").value = "";

    backdrop.style.display = "flex";
    setTimeout(() => document.getElementById("wmField").focus(), 0);
  }

  function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  function send() {
    const form = document.getElementById("wmForm");

    // Required checks
    const field = (document.getElementById("wmField").value || "").trim();
    const value = (document.getElementById("wmValue").value || "").trim();
    const email = (document.getElementById("wmEmail").value || "").trim();

    if (!field || !value || !email) {
      alert("Please fill Field + Suggested value + Email.");
      return;
    }
    if (!isValidEmail(email)) {
      alert("Please enter a valid email address.");
      return;
    }

    // UX first
    hide();
    showToast();

    // Netlify native submit (no fetch)
    try {
      form.submit();
    } catch (e) {
      console.warn(e);
      alert("Could not send right now. Please try again.");
    }
  }

  // Close handlers
  backdrop.addEventListener("click", (e) => { if (e.target === backdrop) hide(); });
  document.getElementById("wmCloseTop").addEventListener("click", hide);
  document.getElementById("wmCancel").addEventListener("click", hide);
  document.getElementById("wmSend").addEventListener("click", send);

  // Public API used by header
  window.openCorrection = function (fieldLabel) {
    show(fieldLabel || "");
  };
})();

// Compatibility: existing pencils call openModal('electricity')
window.openModal = function (fieldKey) {
  const MAP = {
    general: "General / multiple fields",
    min_wage: "Minimum wage (net / month)",
    avg_salary: "Average salary (net / month)",
    doctor_salary: "Doctor (GP, net / month)",
    rent_studio: "Studio rent / month",
    electricity: "Electricity / month",
    water: "Water / month",
    mobile: "Mobile plan / month",
    beer: "Beer (pint 0.5L)",
    coffee: "Coffee",
    dish: "Main dish",
    gas: "Gasoline (per L)",
    vat: "VAT (%)",
    income_tax: "Income tax (typical worker, %)",
    smallbiz: "Small business taxes (%)",
    iphone: "iPhone price (latest, 256GB)",
    samsung: "Galaxy S price (latest, 256GB)",
    immigration: "Immigration-friendly score (0–10)",
    happiness: "Happiness score (/10)",
    sun: "Sunny days / year",
    health: "Public healthcare",
    insurance: "Private insurance / month",
    crime: "Crime index",
    pp: "Purchasing power index",
    religion: "Religion %"
  };

  const label = MAP[fieldKey] || fieldKey || "";
  if (typeof window.openCorrection === "function") {
    window.openCorrection(label);
  } else {
    alert("Correction form not loaded.");
  }
};
