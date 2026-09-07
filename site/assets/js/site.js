/* ==========================================================================
   Momentum Link Professionals — site behaviour
   Progressive enhancement only: every page is readable and navigable with
   this file removed. Nothing here is required to reach the content.
   ========================================================================== */
(function () {
  "use strict";

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var finePointer = window.matchMedia("(hover: hover) and (pointer: fine)").matches;

  function $(sel, root) { return (root || document).querySelector(sel); }
  function $$(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }
  function clamp01(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
  function seg(p, a, b) { return clamp01((p - a) / (b - a)); }
  function ease(t) { return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }
  function lerp(a, b, t) { return a + (b - a) * t; }

  /* ── Mobile navigation ─────────────────────────────────────────────── */

  function initNav() {
    var toggle = $("[data-nav-toggle]");
    var nav = $("#site-nav");
    if (!toggle || !nav) return;

    var mq = window.matchMedia("(max-width: 900px)");

    function apply() {
      if (mq.matches) {
        nav.hidden = toggle.getAttribute("aria-expanded") !== "true";
      } else {
        nav.hidden = false;
        toggle.setAttribute("aria-expanded", "false");
      }
    }

    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", open ? "false" : "true");
      apply();
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && mq.matches && toggle.getAttribute("aria-expanded") === "true") {
        toggle.setAttribute("aria-expanded", "false");
        apply();
        toggle.focus();
      }
    });

    if (mq.addEventListener) mq.addEventListener("change", apply);
    else if (mq.addListener) mq.addListener(apply);
    apply();
  }

  /* ── Reading-progress bar ──────────────────────────────────────────── */

  function initProgress() {
    var bar = $("[data-progress]");
    if (!bar) return;
    return function () {
      var max = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.width = (max > 0 ? Math.min(100, (window.scrollY / max) * 100) : 0) + "%";
    };
  }

  /* ── Pinned scroll stage on the home page ──────────────────────────── */

  function initStage() {
    var stage = $("[data-stage]");
    if (!stage) return;

    // The choreography is scroll-driven; with reduced motion it would never
    // resolve, so fall back to the flat hero the stylesheet already defines.
    if (reduced) {
      stage.classList.add("is-static");
      return;
    }

    var l1 = $("[data-stage-l1]", stage);
    var l2 = $("[data-stage-l2]", stage);
    var l2img = l2 && l2.querySelector("img");
    var tint = $("[data-stage-tint]", stage);
    var blockA = $("[data-stage-a]", stage);
    var blockB = $("[data-stage-b]", stage);
    var bar = $("[data-stage-bar]", stage);
    var count = $("[data-stage-count]", stage);
    var cue = $("[data-stage-cue]", stage);

    return function () {
      var rect = stage.getBoundingClientRect();
      var total = stage.offsetHeight - window.innerHeight;
      var p = clamp01(total > 0 ? -rect.top / total : 0);

      if (l1) {
        var a = ease(seg(p, 0, 0.24));
        var b = ease(seg(p, 0.42, 0.78));
        l1.style.opacity = String(lerp(0.92, 1, ease(seg(p, 0, 0.12))));
        l1.style.borderRadius = lerp(30, 0, a) + "px";
        l1.style.transform = "translate(-50%,-50%) scale(" + lerp(0.3, 1, a) * lerp(1, 1.14, b) + ")";
      }
      if (l2) {
        var c = ease(seg(p, 0.52, 0.84));
        l2.style.clipPath = "inset(" + lerp(100, 0, c) + "% 0 0 0)";
        if (l2img) l2img.style.transform = "scale(" + lerp(1.16, 1, c) + ") translateY(" + lerp(5, 0, c) + "%)";
      }
      if (tint) tint.style.opacity = String(lerp(0.15, 1, ease(seg(p, 0.08, 0.34))));

      if (blockA) {
        var inA = ease(seg(p, 0.16, 0.34));
        var outA = ease(seg(p, 0.44, 0.56));
        blockA.style.opacity = String(inA * (1 - outA));
        blockA.style.transform = "translateY(" + (lerp(48, 0, inA) + lerp(0, -46, outA)) + "px)";
        blockA.style.filter = "blur(" + lerp(8, 0, inA) + "px)";
        blockA.style.pointerEvents = inA * (1 - outA) > 0.6 ? "auto" : "none";
      }
      if (blockB) {
        var inB = ease(seg(p, 0.7, 0.9));
        blockB.style.opacity = String(inB);
        blockB.style.transform = "translateY(" + lerp(52, 0, inB) + "px)";
        blockB.style.filter = "blur(" + lerp(8, 0, inB) + "px)";
        blockB.style.pointerEvents = inB > 0.6 ? "auto" : "none";
      }
      if (bar) bar.style.transform = "scaleX(" + p + ")";
      if (count) count.textContent = (p > 0.6 ? "02" : "01") + " / 02";
      if (cue) cue.style.opacity = String(1 - ease(seg(p, 0, 0.14)));
    };
  }

  /* ── Scroll reveal ─────────────────────────────────────────────────── */

  function initReveal() {
    var targets = $$("[data-reveal]");
    if (!targets.length) return;

    if (reduced || !("IntersectionObserver" in window)) {
      targets.forEach(function (el) { el.classList.add("is-visible"); });
      return;
    }

    function show(el, index) {
      el.style.transitionDelay = Math.min(index * 70, 350) + "ms";
      el.classList.add("is-visible");
    }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        var index = el.parentNode ? Array.prototype.indexOf.call(el.parentNode.children, el) : 0;
        show(el, index);
        io.unobserve(el);
      });
    }, { rootMargin: "0px 0px -6% 0px", threshold: 0.06 });

    targets.forEach(function (el) { io.observe(el); });

    // Observer callbacks are throttled while a tab is backgrounded, so anything
    // already inside the viewport is swept in directly. Content must never be
    // left sitting at opacity 0 because a notification did not arrive.
    var pending = targets.slice();

    function sweep() {
      pending = pending.filter(function (el) {
        if (el.classList.contains("is-visible")) return false;
        if (el.getBoundingClientRect().top >= window.innerHeight * 1.05) return true;
        show(el, targets.indexOf(el));
        io.unobserve(el);
        return false;
      });
      if (!pending.length) window.removeEventListener("scroll", sweep);
    }

    window.addEventListener("load", sweep);
    window.addEventListener("scroll", sweep, { passive: true });
    window.setTimeout(sweep, 1200);
    document.addEventListener("visibilitychange", function () {
      if (document.visibilityState === "visible") sweep();
    });
  }

  /* ── Card blurbs open on hover, but only where hovering exists ─────── */

  function initCards() {
    if (!finePointer || reduced) return;
    $$("[data-card]").forEach(function (card) { card.classList.add("is-collapsible"); });
  }

  /* ── Sector rail on the home page ──────────────────────────────────── */

  function initPanels() {
    var panels = $$("[data-panel]");
    if (!panels.length) return;

    function open(panel) {
      panels.forEach(function (p) { p.classList.toggle("is-open", p === panel); });
    }

    panels.forEach(function (panel) {
      panel.addEventListener("mouseenter", function () { if (finePointer) open(panel); });
      panel.addEventListener("focus", function () { open(panel); });

      // Without hover there is nothing to expand a panel, and the panel is a
      // link — so the first tap expands it and only a second tap follows it.
      panel.addEventListener("click", function (e) {
        if (finePointer) return;
        if (!panel.classList.contains("is-open")) {
          e.preventDefault();
          open(panel);
        }
      });
    });
  }

  /* ── Presentation overlay ──────────────────────────────────────────── */

  var SLIDE_MS = 5600;

  var SLIDES = [
    ["31-technology-complexity-to-clarity", "From complexity to a clear system", "Most operations do not need more software. They need the software they already have to make sense together."],
    ["01-practice-understand-business-workflow", "We start on the floor, not in a demo", "Weeks spent tracing the real path of an order, a job, or a tenancy — including every exception that happens often enough to be the rule."],
    ["07-industry-smart-manufacturing", "Manufacturing", "Production monitoring, scheduling, and true product cost answering to one set of numbers."],
    ["09-industry-construction-project-management", "Construction", "Preconstruction through final billing, with the change orders that decide whether a job made money."],
    ["11-industry-wholesale-distribution", "Wholesale distribution", "Ordering, fulfilment, inventory and both sides of the ledger at transaction density."],
    ["13-industry-multi-property-management", "Property", "Leasing, maintenance and owner reporting that reconcile every month without heroics."],
    ["15-industry-premium-retail-website", "Retail and commerce", "Storefronts that stay fast under load, findable in search, and worth returning to."],
    ["19-technology-api-integration", "Integration before replacement", "A governed service coordinating accounting, routing, monitoring and commerce into one dependable truth."],
    ["27-technology-digital-twin", "Test the change before you commit", "Simulation of an operational change, run against real data, before a single process is disturbed."],
    ["34-technology-secure-data-journey", "Secure from capture to report", "Encrypted, auditable movement of every record, with identity-first access at each hop."],
    ["30-technology-connected-ecosystem", "One network, many sites", "Plants, depots, offices and storefronts operating as a single connected system."],
    ["06-practice-long-term-technology-care", "Then we stay", "Version history kept, improvements delivered continuously, accountability years after go-live."]
  ].map(function (s, i) {
    return {
      stem: s[0],
      title: s[1],
      sub: s[2],
      num: String(i + 1).padStart(2, "0") + " / 12"
    };
  });

  function initPresentation() {
    var triggers = $$("[data-open-pres]");
    if (!triggers.length) return;

    var base = document.documentElement.getAttribute("data-media-base") || "media/";
    var root = null;
    var slideEls = [];
    var tickFills = [];
    var numEl, titleEl, subEl, playBtn, closeBtn;
    var index = 0;
    var previous = -1;
    var playing = true;
    var timer = null;
    var parity = 0;
    var lastFocus = null;

    function media(stem, width, ext) {
      return base + stem + (width === 768 ? "-768" : "") + "." + ext;
    }

    function build() {
      root = document.createElement("div");
      root.className = "pres";
      root.setAttribute("role", "dialog");
      root.setAttribute("aria-modal", "true");
      root.setAttribute("aria-label", "Momentum Link presentation");
      root.hidden = true;

      var html = "";
      SLIDES.forEach(function (s) {
        html +=
          '<div class="pres__slide">' +
            '<picture>' +
              '<source type="image/webp" srcset="' + media(s.stem, 768, "webp") + ' 768w, ' + media(s.stem, 1536, "webp") + ' 1536w" sizes="100vw">' +
              '<img src="' + media(s.stem, 1536, "jpg") + '" alt="' + s.title + '" loading="lazy" decoding="async">' +
            '</picture>' +
          '</div>';
      });

      html +=
        '<div class="pres__brand"><span class="pres__brand-mark"></span><span class="pres__brand-name">Momentum Link</span></div>' +
        '<div class="pres__caption">' +
          '<p class="pres__num" data-pres-num></p>' +
          '<p class="pres__title" data-pres-title></p>' +
          '<p class="pres__sub" data-pres-sub></p>' +
        '</div>' +
        '<div class="pres__controls">' +
          '<button type="button" class="pres__btn" data-pres-play>&#10073;&#10073; Pause</button>' +
          '<button type="button" class="pres__btn pres__btn--close" data-pres-close>Esc &#10005;</button>' +
        '</div>' +
        '<div class="pres__ticks">' +
          SLIDES.map(function (s, i) {
            return '<button type="button" class="pres__tick" data-pres-jump="' + i + '" aria-label="Slide ' + (i + 1) + ': ' + s.title + '"><span><i></i></span></button>';
          }).join("") +
        '</div>' +
        '<button type="button" class="pres__edge pres__edge--prev" data-pres-prev aria-label="Previous slide"></button>' +
        '<button type="button" class="pres__edge pres__edge--next" data-pres-next aria-label="Next slide"></button>';

      root.innerHTML = html;
      document.body.appendChild(root);

      slideEls = $$(".pres__slide", root);
      tickFills = $$(".pres__tick i", root);
      numEl = $("[data-pres-num]", root);
      titleEl = $("[data-pres-title]", root);
      subEl = $("[data-pres-sub]", root);
      playBtn = $("[data-pres-play]", root);
      closeBtn = $("[data-pres-close]", root);

      $("[data-pres-prev]", root).addEventListener("click", function () { step(-1); });
      $("[data-pres-next]", root).addEventListener("click", function () { step(1); });
      closeBtn.addEventListener("click", close);
      playBtn.addEventListener("click", togglePlay);
      $$("[data-pres-jump]", root).forEach(function (btn) {
        btn.addEventListener("click", function () { go(Number(btn.getAttribute("data-pres-jump"))); });
      });

      root.addEventListener("keydown", trapFocus);
    }

    function trapFocus(e) {
      if (e.key !== "Tab") return;
      var focusable = $$("button", root).filter(function (el) { return el.offsetParent !== null; });
      if (!focusable.length) return;
      var first = focusable[0];
      var last = focusable[focusable.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }

    function paint() {
      var slide = SLIDES[index];
      parity = (parity + 1) % 2;

      slideEls.forEach(function (el, i) {
        el.classList.toggle("is-active", i === index);
        el.classList.toggle("is-prev", i === previous && i !== index);

        var img = el.querySelector("img");
        if (i === index) {
          // Restart the wipe and the slow pan; the parity flip forces a
          // fresh animation even when the same keyframes are reused.
          if (!reduced) {
            el.style.animation = "none";
            void el.offsetWidth;
            el.style.animation = "mlWipe" + (index % 5) + " 1.15s cubic-bezier(.76,0,.24,1) both";
            if (img) {
              img.style.animation = "none";
              void img.offsetWidth;
              img.style.animation = "mlKen" + (parity ? "A" : "B") + " 12s linear forwards";
            }
          }
          if (img && img.getAttribute("loading") === "lazy") img.setAttribute("loading", "eager");
        } else {
          el.style.animation = "none";
          if (img) img.style.animation = "none";
        }
      });

      // Warm the neighbouring slides so a click never waits on a download.
      [index + 1, index - 1].forEach(function (n) {
        var el = slideEls[(n + SLIDES.length) % SLIDES.length];
        var img = el && el.querySelector("img");
        if (img) img.setAttribute("loading", "eager");
      });

      numEl.textContent = slide.num;
      titleEl.textContent = slide.title;
      subEl.textContent = slide.sub;

      if (!reduced) {
        [[numEl, 0], [titleEl, 130], [subEl, 260]].forEach(function (pair) {
          pair[0].style.animation = "none";
          void pair[0].offsetWidth;
          pair[0].style.animation = "mlUp .9s cubic-bezier(.19,1,.22,1) " + pair[1] + "ms both";
        });
      }

      tickFills.forEach(function (fill, i) {
        fill.style.animation = "none";
        void fill.offsetWidth;
        if (i < index) fill.style.transform = "scaleX(1)";
        else if (i > index) fill.style.transform = "scaleX(0)";
        else if (playing && !reduced) {
          fill.style.transform = "scaleX(0)";
          fill.style.animation = "mlTick " + SLIDE_MS + "ms linear forwards";
        } else {
          fill.style.transform = "scaleX(1)";
        }
      });
    }

    function sync() {
      clearInterval(timer);
      if (playing && !root.hidden) timer = setInterval(function () { step(1); }, SLIDE_MS);
    }

    function go(i) {
      if (i === index) return;
      previous = index;
      index = i;
      paint();
      sync();
    }

    function step(d) {
      go((index + d + SLIDES.length) % SLIDES.length);
    }

    function togglePlay() {
      playing = !playing;
      playBtn.innerHTML = playing ? "&#10073;&#10073; Pause" : "&#9654; Play";
      paint();
      sync();
    }

    function open() {
      if (!root) build();
      lastFocus = document.activeElement;
      index = 0;
      previous = -1;
      playing = !reduced;
      playBtn.innerHTML = playing ? "&#10073;&#10073; Pause" : "&#9654; Play";
      root.hidden = false;
      document.body.classList.add("is-locked");
      paint();
      sync();
      closeBtn.focus();
      document.addEventListener("keydown", onKey);
    }

    function close() {
      if (!root || root.hidden) return;
      root.hidden = true;
      playing = false;
      clearInterval(timer);
      document.body.classList.remove("is-locked");
      document.removeEventListener("keydown", onKey);
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    }

    function onKey(e) {
      if (!root || root.hidden) return;
      if (e.key === "Escape") { e.preventDefault(); close(); }
      else if (e.key === "ArrowRight") { e.preventDefault(); step(1); }
      else if (e.key === "ArrowLeft") { e.preventDefault(); step(-1); }
      else if (e.key === " " || e.key === "Spacebar") { e.preventDefault(); togglePlay(); }
    }

    triggers.forEach(function (btn) {
      btn.hidden = false;
      btn.addEventListener("click", function (e) {
        e.preventDefault();
        open();
      });
    });
  }

  /* ── Contact form ──────────────────────────────────────────────────── */

  function initForm() {
    var form = $("[data-contact-form]");
    if (!form) return;

    var status = $("[data-form-status]", form);
    var mailto = form.getAttribute("data-mailto") || "";

    function setError(field, message) {
      var input = field.querySelector("input, textarea");
      var slot = field.querySelector(".field__error");
      if (!input || !slot) return;
      input.setAttribute("aria-invalid", message ? "true" : "false");
      slot.textContent = message || "";
    }

    function validate() {
      var ok = true;
      var firstBad = null;

      $$(".field", form).forEach(function (field) {
        var input = field.querySelector("input, textarea");
        if (!input) return;
        var value = input.value.trim();
        var message = "";

        if (input.required && !value) {
          message = "Required.";
        } else if (input.type === "email" && value && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(value)) {
          message = "Enter a valid email address.";
        }

        setError(field, message);
        if (message) {
          ok = false;
          if (!firstBad) firstBad = input;
        }
      });

      if (firstBad) firstBad.focus();
      return ok;
    }

    // Clear an error as soon as the visitor starts fixing it.
    $$(".field input, .field textarea", form).forEach(function (input) {
      input.addEventListener("input", function () {
        if (input.getAttribute("aria-invalid") === "true") setError(input.closest(".field"), "");
      });
    });

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      status.textContent = "";
      status.removeAttribute("data-state");

      if (!validate()) {
        status.setAttribute("data-state", "error");
        status.textContent = "Please correct the highlighted fields.";
        return;
      }

      var data = new FormData(form);
      var button = form.querySelector("button[type=submit]");
      // Read at submit time so the endpoint can be set after load.
      var endpoint = (form.getAttribute("data-endpoint") || "").trim();

      if (endpoint) {
        button.disabled = true;
        status.textContent = "Sending…";
        fetch(endpoint, { method: "POST", body: data, headers: { Accept: "application/json" } })
          .then(function (res) {
            if (!res.ok) throw new Error("Request failed: " + res.status);
            form.reset();
            status.setAttribute("data-state", "ok");
            status.textContent = "Thank you — your brief is with us. We reply within one working day.";
          })
          .catch(function () {
            status.setAttribute("data-state", "error");
            status.textContent = "That did not send. Please email " + mailto + " directly.";
          })
          .finally(function () { button.disabled = false; });
        return;
      }

      // No endpoint configured yet: hand the brief to the visitor's mail client
      // rather than silently dropping it.
      var lines = [];
      data.forEach(function (value, key) {
        if (String(value).trim()) lines.push(key + ": " + value);
      });
      var href = "mailto:" + mailto +
        "?subject=" + encodeURIComponent("New brief from the website") +
        "&body=" + encodeURIComponent(lines.join("\n\n"));

      window.location.href = href;
      status.setAttribute("data-state", "ok");
      status.textContent = "Opening your email client with the brief. If nothing happens, write to " + mailto + ".";
    });
  }

  /* ── Boot ──────────────────────────────────────────────────────────── */

  function boot() {
    initNav();
    initReveal();
    initCards();
    initPanels();
    initPresentation();
    initForm();

    var year = $("[data-year]");
    if (year) year.textContent = new Date().getFullYear();

    var handlers = [initProgress(), initStage()].filter(Boolean);
    if (!handlers.length) return;

    var ticking = false;
    function onScroll() {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(function () {
        handlers.forEach(function (fn) { fn(); });
        ticking = false;
      });
    }

    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll, { passive: true });
    handlers.forEach(function (fn) { fn(); });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
