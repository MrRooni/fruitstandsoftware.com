const site = window.siteData;
const NOON_HOUR = 12;
const SWIPE_THRESHOLD = 48;
const galleryImages = [
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
];

function setText(key, value) {
  document.querySelectorAll(`[data-site="${key}"]`).forEach((node) => {
    node.textContent = value;
  });
}

function setMeta(selector, content) {
  const node = document.querySelector(selector);
  if (node) {
    node.setAttribute("content", content);
  }
}

function renderParagraphs(key, paragraphs) {
  document.querySelectorAll(`[data-site="${key}"]`).forEach((node) => {
    node.replaceChildren();
    paragraphs.forEach((paragraph) => {
      const item = document.createElement("p");
      item.textContent = paragraph;
      node.append(item);
    });
  });
}

function renderList(key, items) {
  document.querySelectorAll(`[data-site="${key}"]`).forEach((node) => {
    node.replaceChildren();
    items.forEach((item) => {
      const listItem = document.createElement("li");
      listItem.textContent = item;
      node.append(listItem);
    });
  });
}

function renderReleaseNotes() {
  const intro =
    "Welcome to the first version of 40 Below! I hope you enjoy it as much as I enjoyed making it. 40 Below will never prompt you for a review, but if you're feeling kind, ";
  const linkedSentence = "a nice 5-star review would sure be great.";

  document.querySelectorAll('[data-site="release-notes-rich"]').forEach((node) => {
    node.replaceChildren();

    node.append(document.createTextNode(intro));

    const link = document.createElement("a");
    link.className = "release-action";
    link.href = "https://apps.apple.com/app/id6759849820?action=write-review";
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    link.textContent = linkedSentence;

    node.append(link);
  });
}

function updateScreenshotForThemeAndTime() {
  const darkSource = document.getElementById("hero-screenshot-dark-source");
  if (!darkSource) {
    return;
  }

  const currentHour = new Date().getHours();
  const darkScreenshot =
    currentHour < NOON_HOUR ? "Cold_Morning_Dark.png" : "Warm_Night_Dark.png";

  darkSource.setAttribute("srcset", darkScreenshot);
}

function initGalleryLightbox() {
  const lightbox = document.querySelector("[data-lightbox]");
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
  const thumbs = document.querySelectorAll("[data-gallery-index]");

  if (
    !lightbox ||
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

  let activeIndex = 0;
  let lastFocused = null;
  let touchStartX = 0;
  let touchDeltaX = 0;
  let isDragging = false;
  let isAnimating = false;
  let pendingStep = 0;

  function getWrappedIndex(index) {
    return (index + galleryImages.length) % galleryImages.length;
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
    const previous = galleryImages[getWrappedIndex(activeIndex - 1)];
    const image = galleryImages[activeIndex];
    const next = galleryImages[getWrappedIndex(activeIndex + 1)];

    previousImage.setAttribute("src", previous.src);
    previousImage.setAttribute("alt", previous.alt);
    lightboxImage.setAttribute("src", image.src);
    lightboxImage.setAttribute("alt", image.alt);
    nextImage.setAttribute("src", next.src);
    nextImage.setAttribute("alt", next.alt);
    lightboxStatus.textContent = `${image.label} (${activeIndex + 1}/${galleryImages.length})`;
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

  function openLightbox(index) {
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

  thumbs.forEach((thumb) => {
    thumb.addEventListener("click", () => {
      const index = Number.parseInt(thumb.getAttribute("data-gallery-index") || "0", 10);
      openLightbox(index);
    });
  });

  previousButton.addEventListener("click", showPreviousImage);
  nextButton.addEventListener("click", showNextImage);

  closeButtons.forEach((button) => {
    button.addEventListener("click", closeLightbox);
  });

  stage.addEventListener(
    "touchstart",
    (event) => {
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

function renderSite() {
  if (!site) {
    return;
  }

  document.documentElement.lang = site.locale;
  document.title = site.seo.title;
  setMeta('meta[name="description"]', site.seo.description);
  setMeta('meta[property="og:title"]', site.seo.ogTitle);
  setMeta('meta[property="og:description"]', site.seo.ogDescription);
  setMeta('meta[name="keywords"]', site.seo.keywords);

  setText("product-name", site.product.name);
  setText("product-subtitle", site.product.subtitle);
  setText("product-promo", site.product.promotionalText);
  setText("feature-heading", site.product.featureHeading);
  setText("location-text", site.product.locationText);
  setText("footer-copyright", site.footer.copyright);

  renderParagraphs("description-paragraphs", site.product.descriptionParagraphs);
  renderList("feature-list", site.product.features);
  renderReleaseNotes();

  document.querySelectorAll('[data-site="screenshot"]').forEach((node) => {
    node.setAttribute("alt", site.product.screenshot.alt);
  });

  updateScreenshotForThemeAndTime();
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

renderSite();
initReveal();
observeColorSchemeChanges();
initGalleryLightbox();
