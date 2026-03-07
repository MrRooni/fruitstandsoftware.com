const site = window.siteData;

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

renderSite();
initReveal();
