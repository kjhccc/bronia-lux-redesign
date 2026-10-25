/* =========================================================
   Броня-Люкс — концепт редизайна
   Меню, аккордеон, валидация формы, появление блоков
   ========================================================= */

(() => {
  "use strict";

  const header = document.getElementById("header");
  const nav = document.getElementById("nav");
  const burger = document.querySelector(".burger");
  const form = document.getElementById("lead-form");
  const success = document.getElementById("lead-success");
  const resetButton = document.getElementById("lead-reset");
  const phoneInput = document.getElementById("phone");

  /* ---------- Тень шапки при прокрутке ---------- */
  const onScroll = () => {
    if (!header) return;
    header.classList.toggle("is-scrolled", window.scrollY > 8);
  };

  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- Мобильное меню ---------- */
  const closeNav = () => {
    if (!nav || !burger) return;
    nav.classList.remove("is-open");
    burger.setAttribute("aria-expanded", "false");
    burger.setAttribute("aria-label", "Открыть меню");
  };

  if (burger && nav) {
    burger.addEventListener("click", () => {
      const isOpen = nav.classList.toggle("is-open");
      burger.setAttribute("aria-expanded", String(isOpen));
      burger.setAttribute("aria-label", isOpen ? "Закрыть меню" : "Открыть меню");
    });

    nav.addEventListener("click", (event) => {
      if (event.target.closest("a")) closeNav();
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") closeNav();
    });

    document.addEventListener("click", (event) => {
      if (!nav.classList.contains("is-open")) return;
      if (nav.contains(event.target) || burger.contains(event.target)) return;
      closeNav();
    });

    window.addEventListener("resize", () => {
      if (window.innerWidth > 900) closeNav();
    });
  }

  /* ---------- Телефон: маска и проверка ---------- */
  const digitsOf = (value) => value.replace(/\D/g, "");

  const formatPhone = (raw) => {
    let digits = digitsOf(raw);
    if (!digits) return "";
    if (digits[0] === "8") digits = "7" + digits.slice(1);
    if (digits[0] !== "7") digits = "7" + digits;
    digits = digits.slice(0, 11);

    const rest = digits.slice(1);
    let out = "+7";
    if (rest.length) out += ` (${rest.slice(0, 3)}`;
    if (rest.length >= 3) out += ")";
    if (rest.length > 3) out += ` ${rest.slice(3, 6)}`;
    if (rest.length > 6) out += `-${rest.slice(6, 8)}`;
    if (rest.length > 8) out += `-${rest.slice(8, 10)}`;
    return out;
  };

  if (phoneInput) {
    phoneInput.addEventListener("input", () => {
      const formatted = formatPhone(phoneInput.value);
      phoneInput.value = formatted;
      if (phoneInput.getAttribute("aria-invalid") === "true") {
        setFieldError("phone", "");
      }
    });

    phoneInput.addEventListener("focus", () => {
      if (!phoneInput.value) phoneInput.value = "+7 (";
    });

    phoneInput.addEventListener("blur", () => {
      if (digitsOf(phoneInput.value).length <= 1) phoneInput.value = "";
    });
  }

  /* ---------- Валидация и отправка формы ---------- */
  const setFieldError = (name, message) => {
    const error = document.querySelector(`[data-error-for="${name}"]`);
    if (error) error.textContent = message;

    const field = document.getElementById(name);
    if (field) {
      if (message) field.setAttribute("aria-invalid", "true");
      else field.removeAttribute("aria-invalid");
    }
  };

  if (form && success) {
    form.addEventListener("submit", (event) => {
      event.preventDefault();

      const name = document.getElementById("name");
      const consent = form.querySelector('input[name="consent"]');
      const digits = digitsOf(phoneInput ? phoneInput.value : "");

      let valid = true;

      if (!name || name.value.trim().length < 2) {
        setFieldError("name", "Напишите, как к вам обращаться");
        valid = false;
      } else {
        setFieldError("name", "");
      }

      if (digits.length !== 11) {
        setFieldError("phone", "Введите номер полностью: 11 цифр");
        valid = false;
      } else {
        setFieldError("phone", "");
      }

      if (!consent || !consent.checked) {
        setFieldError("consent", "Нужно согласие на обработку данных");
        valid = false;
      } else {
        setFieldError("consent", "");
      }

      if (!valid) {
        const firstInvalid = form.querySelector('[aria-invalid="true"]');
        if (firstInvalid) firstInvalid.focus();
        return;
      }

      const submit = form.querySelector('button[type="submit"]');
      if (submit) {
        submit.disabled = true;
        submit.textContent = "Отправляем…";
      }

      // Демо: здесь будет запрос к вашему обработчику формы.
      window.setTimeout(() => {
        form.hidden = true;
        success.hidden = false;
        const title = success.querySelector("h3");
        if (title) {
          title.setAttribute("tabindex", "-1");
          title.focus();
        }
      }, 500);
    });

    if (resetButton) {
      resetButton.addEventListener("click", () => {
        success.hidden = true;
        form.hidden = false;
        form.reset();
        setFieldError("name", "");
        setFieldError("phone", "");
        setFieldError("consent", "");
        const submit = form.querySelector('button[type="submit"]');
        if (submit) {
          submit.disabled = false;
          submit.textContent = "Записаться на замер";
        }
        const name = document.getElementById("name");
        if (name) name.focus();
      });
    }
  }

  /* ---------- Один открытый вопрос в FAQ ---------- */
  const faqItems = [...document.querySelectorAll(".faq__item")];
  faqItems.forEach((item) => {
    item.addEventListener("toggle", () => {
      if (!item.open) return;
      faqItems.forEach((other) => {
        if (other !== item) other.open = false;
      });
    });
  });

  /* ---------- Плавное появление секций ---------- */
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (!reduceMotion && "IntersectionObserver" in window) {
    const targets = [
      ...document.querySelectorAll(
        ".section__head, .service, .step, .work, .contact-card, .form, .promo__inner, .stats",
      ),
    ];

    const belowFold = targets.filter((el) => el.getBoundingClientRect().top > window.innerHeight * 0.9);

    belowFold.forEach((el) => {
      el.classList.add("reveal");
      const siblings = [...(el.parentElement?.children || [])];
      const index = siblings.indexOf(el);
      if (index > 0) el.style.transitionDelay = `${Math.min(index, 5) * 55}ms`;
    });

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.05 },
    );

    belowFold.forEach((el) => observer.observe(el));
  }
})();
