const CONCEPTS_URL = "data/concepts.json";
const CACHE_KEY = "common-projects-concepts-v1";
const CACHE_TIME_KEY = "common-projects-concepts-time-v1";
const CACHE_TTL_MS = 24 * 60 * 60 * 1000;

const container = document.getElementById("concept-container");

document.addEventListener("DOMContentLoaded", () => {
  loadConcepts()
    .then((concepts) => renderToday(concepts))
    .catch(() => {
      container.innerHTML = '<p class="loading">Unable to load today\'s concept. Please try again later.</p>';
    });
});

function loadConcepts() {
  const cached = readCache();
  if (cached) {
    return Promise.resolve(cached);
  }

  return fetch(CONCEPTS_URL, { cache: "no-cache" })
    .then((response) => {
      if (!response.ok) throw new Error("Failed to load concepts");
      return response.json();
    })
    .then((concepts) => {
      writeCache(concepts);
      return concepts;
    })
    .catch((error) => {
      const stale = readCache(true);
      if (stale) return stale;
      throw error;
    });
}

function readCache(allowStale = false) {
  try {
    const raw = localStorage.getItem(CACHE_KEY);
    const time = localStorage.getItem(CACHE_TIME_KEY);
    if (!raw || !time) return null;
    const age = Date.now() - Number(time);
    if (!allowStale && age > CACHE_TTL_MS) return null;
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

function writeCache(concepts) {
  try {
    localStorage.setItem(CACHE_KEY, JSON.stringify(concepts));
    localStorage.setItem(CACHE_TIME_KEY, String(Date.now()));
  } catch {
    // Ignore cache errors
  }
}

function renderToday(concepts) {
  if (!Array.isArray(concepts) || concepts.length === 0) {
    container.innerHTML = '<p class="loading">No concepts available.</p>';
    return;
  }

  const today = new Date();
  const startOfYear = new Date(today.getFullYear(), 0, 0);
  const dayOfYear = Math.floor((today - startOfYear) / 86400000);
  const index = (dayOfYear - 1) % concepts.length;
  const concept = concepts[(index + concepts.length) % concepts.length];

  const connections = Array.isArray(concept.connections_unlocked)
    ? concept.connections_unlocked.join(" ")
    : concept.connections_unlocked;

  container.innerHTML = `
    <article class="concept">
      <h1 class="concept-title">${escapeHtml(concept.concept_title)}</h1>

      <section class="section">
        <p class="section-content">${escapeHtml(concept.kindergarten_explanation)}</p>
      </section>

      <section class="section">
        <p class="section-title">Why it matters</p>
        <p class="section-content">${escapeHtml(concept.why_it_matters)}</p>
      </section>

      <section class="section">
        <p class="section-title">Connections unlocked</p>
        <p class="section-content">${escapeHtml(connections)}</p>
      </section>

      <section class="section">
        <p class="section-title">Quick exercise</p>
        <p class="section-content">${escapeHtml(concept.quick_exercise)}</p>
      </section>

      <p class="day-indicator">Day ${escapeHtml(String(concept.day))} of ${escapeHtml(String(concepts.length))}</p>
    </article>
  `;
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text ?? "";
  return div.innerHTML;
}
