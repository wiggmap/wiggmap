// data/share.js
(function () {
  // prevents double binding
  if (window.__WM_SHARE_LOADED__) return;
  window.__WM_SHARE_LOADED__ = true;

  function toast(msg) {
    // mini toast simple (pas besoin de CSS global)
    let t = document.getElementById("wmShareToast");
    if (!t) {
      t = document.createElement("div");
      t.id = "wmShareToast";
      t.style.position = "fixed";
      t.style.left = "50%";
      t.style.bottom = "18px";
      t.style.transform = "translateX(-50%)";
      t.style.background = "rgba(20,24,22,.92)";
      t.style.color = "#fff";
      t.style.padding = "10px 12px";
      t.style.borderRadius = "999px";
      t.style.fontWeight = "900";
      t.style.fontSize = "13px";
      t.style.boxShadow = "0 12px 30px rgba(0,0,0,.25)";
      t.style.display = "none";
      t.style.zIndex = "99999";
      document.body.appendChild(t);
    }
    t.textContent = msg;
    t.style.display = "block";
    clearTimeout(window.__WM_SHARE_TOAST_TIMER__);
    window.__WM_SHARE_TOAST_TIMER__ = setTimeout(() => {
      t.style.display = "none";
    }, 2000);
  }

  async function copy(text) {
    try {
      await navigator.clipboard.writeText(text);
      return true;
    } catch (e) {
      // fallback old school
      try {
        const ta = document.createElement("textarea");
        ta.value = text;
        ta.style.position = "fixed";
        ta.style.opacity = "0";
        document.body.appendChild(ta);
        ta.focus();
        ta.select();
        const ok = document.execCommand("copy");
        document.body.removeChild(ta);
        return ok;
      } catch (err) {
        return false;
      }
    }
  }

  async function doShare() {
    const url = window.location.href;
    const title = document.title || "WiggMap";

    // Mobile share if available
    if (navigator.share) {
      try {
        await navigator.share({ title, url });
        return;
      } catch (e) {
        // user cancelled -> do nothing
        return;
      }
    }

    // Desktop fallback = copy
    const ok = await copy(url);
    toast(ok ? "Link copied ✅" : "Copy failed ❌");
  }

  // Bind ALL share buttons if multiple exist (safe)
  function bind() {
    const buttons = document.querySelectorAll("#btnShare");
    if (!buttons.length) return;
    buttons.forEach((btn) => {
      if (btn.__wm_bound__) return;
      btn.__wm_bound__ = true;
      btn.addEventListener("click", (e) => {
        e.preventDefault();
        doShare();
      });
    });
  }

  // Run now + after DOM ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bind);
  } else {
    bind();
  }
})();
