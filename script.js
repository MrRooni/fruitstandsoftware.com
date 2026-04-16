const DEFAULT_LOCALE = "en-US";
const LOCALE_STORAGE_KEY = "fruitstandsoftware.locale";
const NOON_HOUR = 12;
const SWIPE_THRESHOLD = 48;
const defaultGalleryGroups = {
  default: [
    {
      src: "Cold_Morning_Dark.png",
      alt: "40 Below screen in a cold morning dark theme",
      label: "Cold Morning Dark",
    },
    {
      src: "Cold_Morning_Dark_Forecast.png",
      alt: "40 Below forecast screen in a cold morning dark theme",
      label: "Cold Morning Dark Forecast",
    },
    {
      src: "Warm_Midday_Light.png",
      alt: "40 Below screen in a warm midday light theme",
      label: "Warm Midday Light",
    },
    {
      src: "Hot_Afternoon_Light.png",
      alt: "40 Below screen in a hot afternoon light theme",
      label: "Hot Afternoon Light",
    },
    {
      src: "Cold_Night_Dark.png",
      alt: "40 Below screen in a cold night dark theme",
      label: "Cold Night Dark",
    },
    {
      src: "Warm_Night_Dark.png",
      alt: "40 Below screen in a warm night dark theme",
      label: "Warm Night Dark",
    },
  ],
};

function getGalleryGroups() {
  if (window.galleryGroups && typeof window.galleryGroups === "object") {
    return window.galleryGroups;
  }

  return defaultGalleryGroups;
}

function resolveGalleryAssetPath(src) {
  if (!src) {
    return "";
  }

  if (
    src.startsWith("../") ||
    src.startsWith("./") ||
    src.startsWith("/") ||
    src.startsWith("http://") ||
    src.startsWith("https://")
  ) {
    return src;
  }

  return `../${src}`;
}

function getAvailableLocales() {
  return Array.from(document.querySelectorAll(".locale-switcher option"))
    .map((option) => option.value)
    .filter(Boolean);
}

function normalizeLocale(locale) {
  return (locale || "").trim();
}

function sameLanguageLocale(requestedLocale, availableLocales) {
  const requestedBase = normalizeLocale(requestedLocale).split("-")[0].toLowerCase();
  if (!requestedBase) {
    return "";
  }

  return (
    availableLocales.find((candidate) => candidate.split("-")[0].toLowerCase() === requestedBase) || ""
  );
}

function resolveLocale(requestedLocales, availableLocales = getAvailableLocales()) {
  for (const requestedLocale of requestedLocales) {
    const normalized = normalizeLocale(requestedLocale);
    if (!normalized) {
      continue;
    }

    const exactLocale = availableLocales.find(
      (candidate) => candidate.toLowerCase() === normalized.toLowerCase()
    );
    if (exactLocale) {
      return exactLocale;
    }

    const languageMatch = sameLanguageLocale(normalized, availableLocales);
    if (languageMatch) {
      return languageMatch;
    }
  }

  return DEFAULT_LOCALE;
}

function buildLocalePath(locale, currentPath = window.location.pathname) {
  if (currentPath.endsWith("/support.html")) {
    return `/${locale}/support.html`;
  }

  if (currentPath.endsWith("/privacy-policy.html")) {
    return `/${locale}/privacy-policy.html`;
  }

  if (currentPath.endsWith("/press.html")) {
    return locale === DEFAULT_LOCALE ? `/${DEFAULT_LOCALE}/press.html` : `/${locale}/`;
  }

  return `/${locale}/`;
}

function initPromoRedeemPage() {
  const config = window.promoPageConfig;
  const button = document.querySelector("[data-promo-button]");
  const status = document.querySelector("[data-promo-status]");
  const intro = document.querySelector("[data-promo-intro]");
  const title = document.querySelector("[data-promo-title]");

  if (!config || !button || !status || !intro || !title) {
    return;
  }

  const params = new URLSearchParams(window.location.search);
  const promo = (params.get("promo") || "").trim();
  const name = (params.get("name") || "").trim();
  const promoPattern = new RegExp(config.validPattern);
  const introLead = name || "Congratulations";
  const introText = config.introTemplate.replace("Congratulations", introLead);

  intro.textContent = introText;

  if (!promo) {
    intro.hidden = true;
    title.hidden = true;
    status.textContent = config.missingMessage;
    button.textContent = config.fallbackCta;
    button.setAttribute("href", config.appStoreUrl);
    return;
  }

  if (!promoPattern.test(promo)) {
    intro.hidden = true;
    title.hidden = true;
    status.textContent = config.malformedMessage;
    button.textContent = config.fallbackCta;
    button.setAttribute("href", config.appStoreUrl);
    return;
  }

  intro.hidden = false;
  title.hidden = false;
  status.textContent = "";
  button.textContent = config.successCta;
  button.setAttribute("href", `${config.redeemBaseUrl}${encodeURIComponent(promo)}`);
}

function updateScreenshotForThemeAndTime() {
  const darkSource = document.getElementById("hero-screenshot-dark-source");
  if (!darkSource) {
    return;
  }

  const currentHour = new Date().getHours();
  const darkScreenshot =
    currentHour < NOON_HOUR ? "Cold_Morning_Dark.png" : "Warm_Night_Dark.png";

  darkSource.setAttribute("srcset", `../${darkScreenshot}`);
}

function initGalleryLightbox() {
  const galleryGroups = getGalleryGroups();
  const lightbox = document.querySelector("[data-lightbox]");
  const lightboxShell = document.querySelector(".lightbox-shell");
  const lightboxImage = document.querySelector("[data-lightbox-image]");
  const previousImage = document.querySelector("[data-lightbox-prev-image]");
  const nextImage = document.querySelector("[data-lightbox-next-image]");
  const lightboxStatus = document.getElementById("lightbox-title");
  const stage = document.querySelector("[data-lightbox-stage]");
  const viewport = document.querySelector("[data-lightbox-viewport]");
  const track = document.querySelector("[data-lightbox-track]");
  const previousButton = document.querySelector("[data-gallery-prev]");
  const nextButton = document.querySelector("[data-gallery-next]");
  const closeButtons = document.querySelectorAll("[data-lightbox-close]");
  const thumbs = Array.from(document.querySelectorAll("[data-gallery-index]")).filter((thumb) => {
    const groupName = thumb.getAttribute("data-gallery-group") || "default";
    return Array.isArray(galleryGroups[groupName]) && galleryGroups[groupName].length > 0;
  });

  if (
    !lightbox ||
    !lightboxShell ||
    !lightboxImage ||
    !previousImage ||
    !nextImage ||
    !lightboxStatus ||
    !stage ||
    !viewport ||
    !track ||
    thumbs.length === 0
  ) {
    return;
  }

  let activeGroup = thumbs[0].getAttribute("data-gallery-group") || "default";
  let activeIndex = 0;
  let lastFocused = null;
  let touchStartX = 0;
  let touchDeltaX = 0;
  let isDragging = false;
  let isAnimating = false;
  let pendingStep = 0;

  function getActiveImages() {
    return galleryGroups[activeGroup] || [];
  }

  function getWrappedIndex(index) {
    const activeImages = getActiveImages();
    return (index + activeImages.length) % activeImages.length;
  }

  function isTouchOnControl(target) {
    return target instanceof Element && Boolean(target.closest(".lightbox-arrow, .lightbox-close"));
  }

  function updateTrackMetrics() {
    const viewportWidth = viewport.clientWidth;

    if (viewportWidth <= 0) {
      return false;
    }

    track.style.setProperty("--lightbox-track-base", `${-viewportWidth}px`);
    return true;
  }

  function setTrackOffset(offsetX) {
    track.style.setProperty("--lightbox-track-drag-x", `${offsetX}px`);
  }

  function resetDragOffset() {
    touchStartX = 0;
    touchDeltaX = 0;
    isDragging = false;
    stage.classList.remove("is-dragging");
    setTrackOffset(0);
  }

  function renderLightboxImage() {
    const activeImages = getActiveImages();
    const previous = activeImages[getWrappedIndex(activeIndex - 1)];
    const image = activeImages[activeIndex];
    const next = activeImages[getWrappedIndex(activeIndex + 1)];
    const imageMaxWidth = image.lightbox_max_width || image.lightboxMaxWidth || image.width || 520;

    lightboxShell.style.setProperty("--lightbox-image-max-width", `${imageMaxWidth}px`);

    previousImage.setAttribute("src", resolveGalleryAssetPath(previous.src));
    previousImage.setAttribute("alt", previous.alt);
    previousImage.setAttribute("width", previous.lightbox_width || previous.lightboxWidth || previous.width || 500);
    previousImage.setAttribute(
      "height",
      previous.lightbox_height || previous.lightboxHeight || previous.height || 1036
    );
    lightboxImage.setAttribute("src", resolveGalleryAssetPath(image.src));
    lightboxImage.setAttribute("alt", image.alt);
    lightboxImage.setAttribute("width", image.lightbox_width || image.lightboxWidth || image.width || 500);
    lightboxImage.setAttribute(
      "height",
      image.lightbox_height || image.lightboxHeight || image.height || 1036
    );
    nextImage.setAttribute("src", resolveGalleryAssetPath(next.src));
    nextImage.setAttribute("alt", next.alt);
    nextImage.setAttribute("width", next.lightbox_width || next.lightboxWidth || next.width || 500);
    nextImage.setAttribute("height", next.lightbox_height || next.lightboxHeight || next.height || 1036);
    lightboxStatus.textContent = `${image.label} (${activeIndex + 1}/${activeImages.length})`;
    const disableArrows = activeImages.length < 2;
    previousButton.disabled = disableArrows;
    nextButton.disabled = disableArrows;
  }

  function finishSnap(nextIndex) {
    activeIndex = getWrappedIndex(nextIndex);
    track.classList.remove("is-snapping");
    resetDragOffset();
    renderLightboxImage();
    updateTrackMetrics();
    pendingStep = 0;
    isAnimating = false;
  }

  function snapToStep(step) {
    const offset = step * viewport.clientWidth;
    isAnimating = true;
    pendingStep = step;
    isDragging = false;
    stage.classList.remove("is-dragging");
    track.classList.add("is-snapping");
    setTrackOffset(offset);
  }

  function openLightbox(groupName, index) {
    activeGroup = groupName;
    activeIndex = index;
    lastFocused = document.activeElement;
    resetDragOffset();
    renderLightboxImage();
    lightbox.hidden = false;
    document.body.classList.add("lightbox-open");
    requestAnimationFrame(() => {
      updateTrackMetrics();
    });
    previousButton.focus();
  }

  function closeLightbox() {
    pendingStep = 0;
    isAnimating = false;
    resetDragOffset();
    track.classList.remove("is-snapping");
    lightbox.hidden = true;
    document.body.classList.remove("lightbox-open");
    if (lastFocused instanceof HTMLElement) {
      lastFocused.focus();
    }
  }

  function showNextImage() {
    if (isAnimating) {
      return;
    }

    snapToStep(-1);
  }

  function showPreviousImage() {
    if (isAnimating) {
      return;
    }

    snapToStep(1);
  }

  function bindControlPress(button, action) {
    let handledTouch = false;

    button.addEventListener(
      "touchend",
      (event) => {
        handledTouch = true;
        event.preventDefault();
        event.stopPropagation();
        action();
      },
      { passive: false }
    );

    button.addEventListener("click", (event) => {
      event.preventDefault();
      event.stopPropagation();

      if (handledTouch) {
        handledTouch = false;
        return;
      }

      action();
    });
  }

  thumbs.forEach((thumb) => {
    thumb.addEventListener("click", () => {
      const index = Number.parseInt(thumb.getAttribute("data-gallery-index") || "0", 10);
      const groupName = thumb.getAttribute("data-gallery-group") || "default";
      openLightbox(groupName, index);
    });
  });

  bindControlPress(previousButton, showPreviousImage);
  bindControlPress(nextButton, showNextImage);

  closeButtons.forEach((button) => {
    bindControlPress(button, closeLightbox);
  });

  stage.addEventListener(
    "touchstart",
    (event) => {
      if (isTouchOnControl(event.target)) {
        resetDragOffset();
        return;
      }

      if (event.touches.length !== 1) {
        resetDragOffset();
        return;
      }

      if (isAnimating) {
        return;
      }

      touchStartX = event.touches[0].clientX;
      touchDeltaX = 0;
      isDragging = true;
      stage.classList.add("is-dragging");
    },
    { passive: true }
  );

  stage.addEventListener(
    "touchmove",
    (event) => {
      if (isTouchOnControl(event.target)) {
        return;
      }

      if (!isDragging || event.touches.length !== 1) {
        return;
      }

      touchDeltaX = event.touches[0].clientX - touchStartX;
      setTrackOffset(touchDeltaX);
      event.preventDefault();
    },
    { passive: false }
  );

  stage.addEventListener(
    "touchend",
    (event) => {
      if (isTouchOnControl(event.target)) {
        resetDragOffset();
        return;
      }

      if (!isDragging) {
        return;
      }

      const touchEndX = event.changedTouches[0].clientX;
      const deltaX = touchEndX - touchStartX;

      if (Math.abs(deltaX) < SWIPE_THRESHOLD) {
        snapToStep(0);
        return;
      }

      if (deltaX < 0) {
        showNextImage();
      } else {
        showPreviousImage();
      }
    },
    { passive: true }
  );

  stage.addEventListener(
    "touchcancel",
    () => {
      if (isDragging) {
        snapToStep(0);
      }
    },
    { passive: true }
  );

  track.addEventListener("transitionend", (event) => {
    if (event.propertyName !== "transform" || !track.classList.contains("is-snapping")) {
      return;
    }

    if (pendingStep === -1) {
      finishSnap(activeIndex + 1);
      return;
    }

    if (pendingStep === 1) {
      finishSnap(activeIndex - 1);
      return;
    }

    finishSnap(activeIndex);
  });

  window.addEventListener("resize", () => {
    if (!lightbox.hidden && !isAnimating) {
      requestAnimationFrame(() => {
        updateTrackMetrics();
      });
    }
  });

  document.addEventListener("keydown", (event) => {
    if (lightbox.hidden) {
      return;
    }

    if (event.key === "Escape") {
      closeLightbox();
    } else if (event.key === "ArrowRight") {
      showNextImage();
    } else if (event.key === "ArrowLeft") {
      showPreviousImage();
    }
  });
}

function initLocaleSwitcher() {
  const switchers = document.querySelectorAll(".locale-switcher");
  if (switchers.length === 0) {
    return;
  }

  const currentLocale = document.documentElement.lang || DEFAULT_LOCALE;

  switchers.forEach((switcher) => {
    switcher.value = currentLocale;
    switcher.addEventListener("change", () => {
      const nextLocale = switcher.value || resolveLocale(navigator.languages || []);

      try {
        window.localStorage.setItem(LOCALE_STORAGE_KEY, nextLocale);
      } catch (error) {
        // Ignore storage access failures and continue navigating.
      }

      window.location.assign(buildLocalePath(nextLocale));
    });
  });
}

function initYear() {
  document.querySelectorAll("#year").forEach((node) => {
    node.textContent = new Date().getFullYear();
  });
}

function initReveal() {
  const revealItems = document.querySelectorAll(".reveal");

  if (!("IntersectionObserver" in window)) {
    revealItems.forEach((item) => item.classList.add("visible"));
    return;
  }

  const observer = new IntersectionObserver(
    (entries, obs) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          obs.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: "0px 0px -5% 0px" }
  );

  revealItems.forEach((item) => observer.observe(item));
}

function observeColorSchemeChanges() {
  const darkMode = window.matchMedia("(prefers-color-scheme: dark)");

  if ("addEventListener" in darkMode) {
    darkMode.addEventListener("change", updateScreenshotForThemeAndTime);
    return;
  }

  darkMode.addListener(updateScreenshotForThemeAndTime);
}

updateScreenshotForThemeAndTime();
initLocaleSwitcher();
initYear();
initReveal();
observeColorSchemeChanges();
initGalleryLightbox();
initPromoRedeemPage();
