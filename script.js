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
  const lightboxStatus = document.getElementById("lightbox-title");
  const stage = document.querySelector("[data-lightbox-stage]");
  const previousButton = document.querySelector("[data-gallery-prev]");
  const nextButton = document.querySelector("[data-gallery-next]");
  const closeButtons = document.querySelectorAll("[data-lightbox-close]");
  const thumbs = document.querySelectorAll("[data-gallery-index]");

  if (!lightbox || !lightboxImage || !lightboxStatus || !stage || thumbs.length === 0) {
    return;
  }

  let activeIndex = 0;
  let lastFocused = null;
  let touchStartX = 0;

  function renderLightboxImage() {
    const image = galleryImages[activeIndex];
    lightboxImage.setAttribute("src", image.src);
    lightboxImage.setAttribute("alt", image.alt);
    lightboxStatus.textContent = `${image.label} (${activeIndex + 1}/${galleryImages.length})`;
  }

  function openLightbox(index) {
    activeIndex = index;
    lastFocused = document.activeElement;
    renderLightboxImage();
    lightbox.hidden = false;
    document.body.classList.add("lightbox-open");
    previousButton.focus();
  }

  function closeLightbox() {
    lightbox.hidden = true;
    document.body.classList.remove("lightbox-open");
    if (lastFocused instanceof HTMLElement) {
      lastFocused.focus();
    }
  }

  function showNextImage() {
    activeIndex = (activeIndex + 1) % galleryImages.length;
    renderLightboxImage();
  }

  function showPreviousImage() {
    activeIndex = (activeIndex - 1 + galleryImages.length) % galleryImages.length;
    renderLightboxImage();
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
      touchStartX = event.changedTouches[0].clientX;
    },
    { passive: true }
  );

  stage.addEventListener(
    "touchend",
    (event) => {
      const touchEndX = event.changedTouches[0].clientX;
      const deltaX = touchEndX - touchStartX;

      if (Math.abs(deltaX) < SWIPE_THRESHOLD) {
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
