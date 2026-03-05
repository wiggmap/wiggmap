// /data/footer.js
(function () {
  // prevent duplicates
  if (document.getElementById("wmSiteFooter")) return;

  const year = new Date().getFullYear();

  const footerHTML = `
    <footer id="wmSiteFooter" class="wm-footer" role="contentinfo">
      <div class="wm-footer__inner">
        <div class="wm-footer__row">
          <div class="wm-footer__copy">© ${year} WiggMap. All rights reserved.</div>

          <nav class="wm-footer__links" aria-label="Legal">
            <a href="/terms.html">Terms</a>
            <span class="wm-footer__sep">•</span>
            <a href="/privacy.html">Privacy</a>
          </nav>
        </div>
      </div>
    </footer>

    <style>
      .wm-footer{
        margin-top: 18px;
        padding: 18px 14px 22px;
        text-align: center;
        font-family: "Poppins", system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
        color: rgba(0,0,0,.62);
      }
      .wm-footer__inner{
        max-width: 1100px;
        margin: 0 auto;
        border-top: 1px solid rgba(0,0,0,.10);
        padding-top: 12px;
      }
      .wm-footer__row{
        display:flex;
        align-items:center;
        justify-content:center;
        gap: 12px;
        flex-wrap: wrap;
      }
      .wm-footer__copy{
        font-size: 13px;
        opacity: .9;
      }
      .wm-footer__links{
        display:flex;
        align-items:center;
        gap: 10px;
        flex-wrap: wrap;
        justify-content:center;
        font-size: 13px;
      }
      .wm-footer a{
        color: rgba(0,0,0,.62);
        text-decoration: none;
        font-weight: 700;
      }
      .wm-footer a:hover{
        text-decoration: underline;
      }
      .wm-footer__sep{
        opacity: .55;
        font-weight: 900;
      }
    </style>
  `;

  document.body.insertAdjacentHTML("beforeend", footerHTML);
})();
