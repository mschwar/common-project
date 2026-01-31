const CONCEPTS_URL = "data/concepts.json";
const CACHE_KEY = "common-projects-concepts-v3";
const CACHE_TIME_KEY = "common-projects-concepts-time-v3";
const CACHE_TTL_MS = 24 * 60 * 60 * 1000;

// Temporarily hardcode to Day 4 (index 3) for featured card
const FEATURED_INDEX = 3;

const container = document.getElementById("concept-container");

document.addEventListener("DOMContentLoaded", () => {
  loadConcepts()
    .then((concepts) => renderConcept(concepts))
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

function renderConcept(concepts) {
  if (!Array.isArray(concepts) || concepts.length === 0) {
    container.innerHTML = '<p class="loading">No concepts available.</p>';
    return;
  }

  const concept = concepts[FEATURED_INDEX];

  const connections = Array.isArray(concept.connections_unlocked)
    ? concept.connections_unlocked.join(" ")
    : concept.connections_unlocked;

  container.innerHTML = `
    <article class="concept">
      <h1 class="concept-title">${escapeHtml(concept.concept_title)}</h1>

      <section class="section">
        <div class="section-content">${formatText(concept.kindergarten_explanation)}</div>
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
        <p class="section-content">${formatExercise(concept.quick_exercise)}</p>
      </section>

      <footer class="site-footer">Day ${concept.day}: ${escapeHtml(concept.concept_title)} | Common Projects</footer>
    </article>
  `;
}

function formatText(text) {
  if (!text) return "";

  // Handle code blocks - convert to grid class
  let formatted = text.replace(/```\n?([\s\S]*?)```/g, (match, code) => {
    return `<pre class="grid">${escapeHtml(code.trim())}</pre>`;
  });

  // Split by pre tags to handle text vs code separately
  const parts = formatted.split(/(<pre class="grid">[\s\S]*?<\/pre>)/);
  return parts.map(part => {
    if (part.startsWith('<pre')) return part;
    // Handle bold text
    let processed = part.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    // Escape and handle line breaks
    processed = escapeHtml(processed)
      .replace(/&lt;strong&gt;/g, '<strong>')
      .replace(/&lt;\/strong&gt;/g, '</strong>')
      .replace(/\n\n/g, '</p><p>')
      .replace(/\n/g, '<br>');
    return processed;
  }).join('');
}

function formatExercise(text) {
  if (!text) return "";
  // Handle em tags for pro tip
  return text.replace(/<em>(.*?)<\/em>/g, '<em>$1</em>');
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text ?? "";
  return div.innerHTML;
}
