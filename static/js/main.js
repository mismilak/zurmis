/* ============================================================
   اسکریپت اصلی سایت — انیمیشن ورود، ناوبار موبایل، فرم و ...
   ============================================================ */
(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- نمایش تدریجی المان‌ها هنگام اسکرول ---------- */
  function initReveal() {
    var items = document.querySelectorAll(".reveal");
    if (!items.length) return;
    if (!("IntersectionObserver" in window) || reduceMotion) {
      items.forEach(function (el) { el.classList.add("in"); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        // تاخیر پلکانی برای المان‌های هم‌گروه
        var siblings = Array.prototype.slice.call(el.parentNode.children).filter(function (n) {
          return n.classList && n.classList.contains("reveal");
        });
        var index = Math.min(siblings.indexOf(el), 6);
        el.style.transitionDelay = (index > 0 ? index * 90 : 0) + "ms";
        el.classList.add("in");
        io.unobserve(el);
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -60px 0px" });
    items.forEach(function (el) { io.observe(el); });
  }

  /* ---------- شمارنده آمار ---------- */
  var FA_DIGITS = ["۰", "۱", "۲", "۳", "۴", "۵", "۶", "۷", "۸", "۹"];
  function toFa(num) {
    return String(num).replace(/\d/g, function (d) { return FA_DIGITS[+d]; });
  }
  function animateCounter(el) {
    var target = parseInt(el.dataset.target, 10) || 0;
    if (reduceMotion) { el.textContent = toFa(target); return; }
    var duration = 1400, start = null;
    function step(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / duration, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = toFa(Math.round(target * eased));
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  function initCounters() {
    var counters = document.querySelectorAll(".counter");
    if (!counters.length) return;
    if (!("IntersectionObserver" in window)) {
      counters.forEach(animateCounter);
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { animateCounter(entry.target); io.unobserve(entry.target); }
      });
    }, { threshold: 0.4 });
    counters.forEach(function (el) { io.observe(el); });
  }

  /* ---------- هدر چسبان + ناوبار پایین شناور ---------- */
  function initScrollUI() {
    var header = document.getElementById("siteHeader");
    var bottomNav = document.getElementById("bottomNav");
    var toTop = document.getElementById("backToTop");
    var lastY = window.pageYOffset;
    var ticking = false;

    function update() {
      var y = window.pageYOffset;
      if (header) header.classList.toggle("scrolled", y > 12);
      if (toTop) toTop.classList.toggle("show", y > 420);
      if (bottomNav) {
        // مثل تلگرام: با اسکرول به پایین مخفی، با اسکرول به بالا ظاهر می‌شود
        var goingDown = y > lastY && y > 160;
        bottomNav.classList.toggle("hidden", goingDown);
      }
      lastY = y;
      ticking = false;
    }
    window.addEventListener("scroll", function () {
      if (!ticking) { requestAnimationFrame(update); ticking = true; }
    }, { passive: true });
    update();

    if (toTop) {
      toTop.addEventListener("click", function () {
        window.scrollTo({ top: 0, behavior: reduceMotion ? "auto" : "smooth" });
      });
    }
  }

  /* ---------- فعال‌سازی آیتم ناوبار پایین بر اساس بخش دیده‌شده ---------- */
  function initBottomNavSpy() {
    var nav = document.getElementById("bottomNav");
    if (!nav || !document.body.classList.contains("page-home")) return;
    var links = Array.prototype.slice.call(nav.querySelectorAll('a[href*="#"]'));
    var map = {};
    links.forEach(function (a) {
      var hash = a.getAttribute("href").split("#")[1];
      if (hash && document.getElementById(hash)) map[hash] = a;
    });
    var sections = Object.keys(map).map(function (id) { return document.getElementById(id); });
    if (!sections.length || !("IntersectionObserver" in window)) return;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var link = map[entry.target.id];
        if (!link || link.classList.contains("bn-cta")) return;
        nav.querySelectorAll(".bn-item").forEach(function (el) { el.classList.remove("active"); });
        link.classList.add("active");
      });
    }, { threshold: 0.35 });
    sections.forEach(function (s) { io.observe(s); });
  }

  /* ---------- جست‌وجوی هدر ---------- */
  function initSearch() {
    var toggle = document.getElementById("searchToggle");
    var panel = document.getElementById("searchPanel");
    if (!toggle || !panel) return;
    toggle.addEventListener("click", function () {
      panel.hidden = !panel.hidden;
      if (!panel.hidden) {
        var input = panel.querySelector("input");
        if (input) input.focus();
      }
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") panel.hidden = true;
    });
  }

  /* ---------- آکاردئون سوالات متداول ---------- */
  function initAccordion() {
    document.querySelectorAll("[data-accordion]").forEach(function (acc) {
      acc.querySelectorAll(".acc-head").forEach(function (head) {
        head.addEventListener("click", function () {
          var item = head.closest(".acc-item");
          var body = item.querySelector(".acc-body");
          var isOpen = item.classList.contains("open");

          acc.querySelectorAll(".acc-item.open").forEach(function (other) {
            other.classList.remove("open");
            other.querySelector(".acc-body").style.maxHeight = null;
            other.querySelector(".acc-head").setAttribute("aria-expanded", "false");
          });

          if (!isOpen) {
            item.classList.add("open");
            body.style.maxHeight = body.scrollHeight + "px";
            head.setAttribute("aria-expanded", "true");
          }
        });
      });
    });
  }

  /* ---------- تب‌های سوابق ---------- */
  function initTabs() {
    document.querySelectorAll("[data-tabs]").forEach(function (box) {
      box.querySelectorAll(".tab-btn").forEach(function (btn) {
        btn.addEventListener("click", function () {
          var key = btn.dataset.tab;
          box.querySelectorAll(".tab-btn").forEach(function (b) { b.classList.toggle("active", b === btn); });
          box.querySelectorAll(".tab-pane").forEach(function (p) {
            p.classList.toggle("active", p.dataset.pane === key);
          });
        });
      });
    });
  }

  /* ---------- اسلایدر نظرات ---------- */
  function initSlider() {
    document.querySelectorAll("[data-slider]").forEach(function (slider) {
      var track = slider.querySelector(".testimonial-track");
      if (!track) return;
      slider.querySelectorAll(".slider-btn").forEach(function (btn) {
        btn.addEventListener("click", function () {
          var card = track.querySelector(".testimonial-card");
          var step = card ? card.offsetWidth + 20 : 320;
          // در چیدمان راست‌به‌چپ، جهت اسکرول معکوس است
          track.scrollBy({ left: btn.dataset.dir === "next" ? -step : step, behavior: "smooth" });
        });
      });
    });
  }

  /* ---------- ارسال فرم مشاوره با AJAX ---------- */
  function getCookie(name) {
    var match = document.cookie.match(new RegExp("(^|; )" + name + "=([^;]*)"));
    return match ? decodeURIComponent(match[2]) : null;
  }

  function initConsultForm() {
    document.querySelectorAll('form[data-ajax="true"]').forEach(function (form) {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        var button = form.querySelector('button[type="submit"]');
        var spinner = form.querySelector(".btn-spinner");
        var result = form.querySelector(".form-result");

        form.querySelectorAll(".field-error").forEach(function (el) { el.textContent = ""; });
        if (result) { result.hidden = true; result.className = "form-result"; }
        if (button) button.disabled = true;
        if (spinner) spinner.hidden = false;

        var data = new FormData(form);
        fetch(form.action, {
          method: "POST",
          body: data,
          headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken") || (data.get("csrfmiddlewaretoken") || "")
          },
          credentials: "same-origin"
        })
          .then(function (res) { return res.json().then(function (json) { return { ok: res.ok, json: json }; }); })
          .then(function (payload) {
            var json = payload.json || {};
            if (payload.ok && json.ok) {
              form.reset();
              if (result) {
                result.textContent = json.message || "درخواست شما ثبت شد.";
                result.className = "form-result ok";
                result.hidden = false;
              }
            } else {
              if (json.errors) {
                Object.keys(json.errors).forEach(function (field) {
                  var box = form.querySelector('[data-error-for="' + field + '"]');
                  if (box) box.textContent = json.errors[field].join(" ");
                });
              }
              if (result) {
                result.textContent = json.message || "ارسال انجام نشد. دوباره تلاش کنید.";
                result.className = "form-result err";
                result.hidden = false;
              }
            }
          })
          .catch(function () {
            if (result) {
              result.textContent = "خطای ارتباط با سرور. لطفاً دوباره تلاش کنید.";
              result.className = "form-result err";
              result.hidden = false;
            }
          })
          .finally(function () {
            if (button) button.disabled = false;
            if (spinner) spinner.hidden = true;
          });
      });
    });
  }

  /* ---------- کپی لینک اشتراک‌گذاری ---------- */
  function initCopy() {
    document.querySelectorAll("[data-copy]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var text = btn.dataset.copy;
        var done = function () {
          var old = btn.textContent;
          btn.textContent = "✓";
          setTimeout(function () { btn.textContent = old; }, 1600);
        };
        if (navigator.clipboard) {
          navigator.clipboard.writeText(text).then(done).catch(done);
        } else {
          var input = document.createElement("input");
          input.value = text;
          document.body.appendChild(input);
          input.select();
          try { document.execCommand("copy"); } catch (err) { /* ignore */ }
          document.body.removeChild(input);
          done();
        }
      });
    });
  }

  /* ---------- پنهان کردن خودکار پیام‌ها ---------- */
  function initToasts() {
    document.querySelectorAll(".toast").forEach(function (toast) {
      setTimeout(function () {
        toast.style.transition = "opacity .5s, transform .5s";
        toast.style.opacity = "0";
        toast.style.transform = "translateY(-10px)";
        setTimeout(function () { toast.remove(); }, 500);
      }, 6000);
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.documentElement.classList.remove("no-js");
    initReveal();
    initCounters();
    initScrollUI();
    initBottomNavSpy();
    initSearch();
    initAccordion();
    initTabs();
    initSlider();
    initConsultForm();
    initCopy();
    initToasts();
  });
})();
