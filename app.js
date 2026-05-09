const DATA_URL = "data/showcase-cases.csv";

const state = {
  cases: [],
  visibleLimit: 24,
  filters: {
    industry: "All",
    model: "All",
    subject: "All",
    tag: "All",
    search: "",
  },
};

const els = {
  grid: document.querySelector("#galleryGrid"),
  collectionStrip: document.querySelector("#collectionStrip"),
  industryFilter: document.querySelector("#industryFilter"),
  modelFilter: document.querySelector("#modelFilter"),
  subjectFilter: document.querySelector("#subjectFilter"),
  tagFilter: document.querySelector("#tagFilter"),
  searchInput: document.querySelector("#searchInput"),
  resultCount: document.querySelector("#resultCount"),
  emptyState: document.querySelector("#emptyState"),
  resetFilters: document.querySelector("#resetFilters"),
  loadMore: document.querySelector("#loadMore"),
  totalCases: document.querySelector("#totalCases"),
  totalModels: document.querySelector("#totalModels"),
  totalIndustries: document.querySelector("#totalIndustries"),
  dialog: document.querySelector("#caseDialog"),
  dialogContent: document.querySelector("#dialogContent"),
};

function parseCsv(text) {
  const rows = [];
  let row = [];
  let cell = "";
  let inQuotes = false;

  for (let i = 0; i < text.length; i += 1) {
    const char = text[i];
    const next = text[i + 1];

    if (char === '"' && inQuotes && next === '"') {
      cell += '"';
      i += 1;
      continue;
    }

    if (char === '"') {
      inQuotes = !inQuotes;
      continue;
    }

    if (char === "," && !inQuotes) {
      row.push(cell);
      cell = "";
      continue;
    }

    if ((char === "\n" || char === "\r") && !inQuotes) {
      if (char === "\r" && next === "\n") i += 1;
      row.push(cell);
      if (row.some(Boolean)) rows.push(row);
      row = [];
      cell = "";
      continue;
    }

    cell += char;
  }

  if (cell || row.length) {
    row.push(cell);
    rows.push(row);
  }

  const headers = rows.shift();
  return rows.map((values) => Object.fromEntries(headers.map((key, index) => [key, values[index] || ""])));
}

function unique(items, key) {
  return [...new Set(items.map((item) => item[key]).filter(Boolean))].sort();
}

function getTags(item) {
  return String(item.tags || "")
    .split(";")
    .map((tag) => tag.trim())
    .filter(Boolean);
}

function uniqueTags(items) {
  return [...new Set(items.flatMap(getTags))].sort();
}

function setOptions(select, values) {
  select.innerHTML = ["All", ...values]
    .map((value) => `<option value="${escapeHtml(value)}">${escapeHtml(value)}</option>`)
    .join("");
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function thumbnailPath(imagePath) {
  if (!imagePath) return "";
  const lastSlash = imagePath.lastIndexOf("/");
  const directory = lastSlash >= 0 ? imagePath.slice(0, lastSlash + 1) : "";
  const filename = lastSlash >= 0 ? imagePath.slice(lastSlash + 1) : imagePath;
  const basename = filename.replace(/\.[^.]+$/, "");
  return `${directory}thumbs/${basename}.webp`;
}

function renderStats() {
  els.totalCases.textContent = state.cases.length;
  els.totalModels.textContent = unique(state.cases, "model").length;
  els.totalIndustries.textContent = unique(state.cases, "industry").length;
}

function renderCollections() {
  const industries = unique(state.cases, "industry");
  els.collectionStrip.innerHTML = industries
    .map((industry) => {
      const cases = state.cases.filter((item) => item.industry === industry);
      const subjects = unique(cases, "subject");
      return `
        <article class="collection-card">
          <h3>${escapeHtml(industry)}</h3>
          <p>${escapeHtml(subjects.slice(0, 4).join(" · "))}</p>
          <strong>${cases.length}</strong>
        </article>
      `;
    })
    .join("");
}

function applyFilters() {
  const query = state.filters.search.trim().toLowerCase();
  return state.cases.filter((item) => {
    const matchesIndustry = state.filters.industry === "All" || item.industry === state.filters.industry;
    const matchesModel = state.filters.model === "All" || item.model === state.filters.model;
    const matchesSubject = state.filters.subject === "All" || item.subject === state.filters.subject;
    const tags = getTags(item);
    const matchesTag = state.filters.tag === "All" || tags.includes(state.filters.tag);
    const haystack = `${item.case_id} ${item.industry} ${item.subject} ${item.scene} ${item.model} ${tags.join(" ")} ${item.prompt}`.toLowerCase();
    const matchesSearch = !query || haystack.includes(query);
    return matchesIndustry && matchesModel && matchesSubject && matchesTag && matchesSearch;
  });
}

function renderTagList(item, limit = 4) {
  const tags = getTags(item).slice(0, limit);
  if (!tags.length) return "";
  return `
    <div class="case-tags">
      ${tags.map((tag) => `<span class="tag tag-secondary">${escapeHtml(tag)}</span>`).join("")}
    </div>
  `;
}

function renderGallery() {
  const visibleCases = applyFilters();
  const renderedCases = visibleCases.slice(0, state.visibleLimit);
  els.resultCount.textContent = `${visibleCases.length} case${visibleCases.length === 1 ? "" : "s"}`;
  els.emptyState.hidden = visibleCases.length > 0;
  els.loadMore.hidden = visibleCases.length <= state.visibleLimit;
  els.loadMore.textContent = `Load more cases (${Math.max(visibleCases.length - state.visibleLimit, 0)} remaining)`;
  els.grid.innerHTML = renderedCases
    .map((item, index) => `
      <article class="case-card">
        <img src="${escapeHtml(thumbnailPath(item.image))}" data-full-src="${escapeHtml(item.image)}" alt="${escapeHtml(`${item.scene} generated by ${item.model}`)}" loading="${index < 6 ? "eager" : "lazy"}" decoding="async" width="640" height="480">
        <div class="case-body">
          <div class="case-meta">
            <span class="tag">${escapeHtml(item.case_id)}</span>
            <span class="tag">${escapeHtml(item.subject)}</span>
            <span class="tag model">${escapeHtml(item.model)}</span>
          </div>
          <h3>${escapeHtml(item.scene)}</h3>
          ${renderTagList(item)}
          <p>${escapeHtml(item.prompt.slice(0, 150))}${item.prompt.length > 150 ? "..." : ""}</p>
          <button type="button" data-index="${index}">View prompt</button>
        </div>
      </article>
    `)
    .join("");

  els.grid.querySelectorAll("button").forEach((button) => {
    button.addEventListener("click", () => openDialog(renderedCases[Number(button.dataset.index)]));
  });

  els.grid.querySelectorAll("img[data-full-src]").forEach((image) => {
    image.addEventListener(
      "error",
      () => {
        image.src = image.dataset.fullSrc;
      },
      { once: true },
    );
  });
}

function openDialog(item) {
  const hasReference = Boolean(item.reference_image);
  const tagMarkup = renderTagList(item, 18);
  const mediaMarkup = hasReference
    ? `
      <div class="compare-media">
        <figure>
          <figcaption>参考图 · Reference image</figcaption>
          <img src="${escapeHtml(item.reference_image)}" alt="${escapeHtml(`Reference image for ${item.scene}`)}">
        </figure>
        <figure>
          <figcaption>生成结果 · Generated result</figcaption>
          <img src="${escapeHtml(item.image)}" alt="${escapeHtml(`${item.scene} generated by ${item.model}`)}">
        </figure>
      </div>
    `
    : `<img class="single-dialog-image" src="${escapeHtml(item.image)}" alt="${escapeHtml(`${item.scene} generated by ${item.model}`)}">`;
  const referenceLink = hasReference && item.reference_url
    ? `<a class="reference-link" href="${escapeHtml(item.reference_url)}" target="_blank" rel="noreferrer">查看参考图来源</a>`
    : "";
  els.dialogContent.innerHTML = `
    <div class="dialog-layout">
      ${mediaMarkup}
      <div class="dialog-info">
        <div class="case-meta">
          <span class="tag">${escapeHtml(item.industry)}</span>
          <span class="tag">${escapeHtml(item.subject)}</span>
          <span class="tag model">${escapeHtml(item.model)}</span>
        </div>
        <h2>${escapeHtml(item.scene)}</h2>
        ${tagMarkup}
        ${referenceLink}
        <div class="prompt-box">${escapeHtml(item.prompt)}</div>
      </div>
    </div>
  `;
  els.dialog.showModal();
}

function wireFilters() {
  els.industryFilter.addEventListener("change", () => {
    state.filters.industry = els.industryFilter.value;
    state.visibleLimit = 24;
    renderGallery();
  });
  els.modelFilter.addEventListener("change", () => {
    state.filters.model = els.modelFilter.value;
    state.visibleLimit = 24;
    renderGallery();
  });
  els.subjectFilter.addEventListener("change", () => {
    state.filters.subject = els.subjectFilter.value;
    state.visibleLimit = 24;
    renderGallery();
  });
  els.tagFilter.addEventListener("change", () => {
    state.filters.tag = els.tagFilter.value;
    state.visibleLimit = 24;
    renderGallery();
  });
  els.searchInput.addEventListener("input", () => {
    state.filters.search = els.searchInput.value;
    state.visibleLimit = 24;
    renderGallery();
  });
  els.resetFilters.addEventListener("click", () => {
    state.filters = { industry: "All", model: "All", subject: "All", tag: "All", search: "" };
    state.visibleLimit = 24;
    els.industryFilter.value = "All";
    els.modelFilter.value = "All";
    els.subjectFilter.value = "All";
    els.tagFilter.value = "All";
    els.searchInput.value = "";
    renderGallery();
  });
  els.loadMore.addEventListener("click", () => {
    state.visibleLimit += 24;
    renderGallery();
  });
  document.querySelector(".dialog-close").addEventListener("click", () => els.dialog.close());
}

async function init() {
  if (Array.isArray(window.SHOWCASE_CASES)) {
    state.cases = window.SHOWCASE_CASES.filter((item) => item.status === "ok");
  } else {
    const response = await fetch(DATA_URL);
    const csv = await response.text();
    state.cases = parseCsv(csv).filter((item) => item.status === "ok");
  }

  setOptions(els.industryFilter, unique(state.cases, "industry"));
  setOptions(els.modelFilter, unique(state.cases, "model"));
  setOptions(els.subjectFilter, unique(state.cases, "subject"));
  setOptions(els.tagFilter, uniqueTags(state.cases));
  renderStats();
  renderCollections();
  renderGallery();
  wireFilters();
}

init().catch((error) => {
  els.grid.innerHTML = `<p class="empty-state">Unable to load showcase data: ${escapeHtml(error.message)}</p>`;
});
