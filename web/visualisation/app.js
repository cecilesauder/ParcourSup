const DEFAULT_WEIGHTS = [0, 20, 40];
const PRESET_WEIGHTS = [0, 10, 20, 30, 40];
const MAX_WEIGHT = 40;
const MAX_MEAN_SCALE = 160;

const state = {
  candidates: [],
  selectedWeights: new Set(DEFAULT_WEIGHTS),
  activeWeight: 20,
  capacity: 6,
};

const byId = (id) => document.getElementById(id);
const formatNumber = (value, digits = 2) => new Intl.NumberFormat("fr-FR", {
  minimumFractionDigits: digits,
  maximumFractionDigits: digits,
}).format(value);
const formatWeight = (value) => `${value} %`;
const escapeHtml = (value) => String(value).replace(/[&<>"']/g, (character) => ({
  "&": "&amp;",
  "<": "&lt;",
  ">": "&gt;",
  '"': "&quot;",
  "'": "&#39;",
})[character]);

function percentilePriorities(values, higherIsBetter) {
  const count = values.length;
  const order = values.map((_, index) => index).sort((left, right) => {
    const difference = values[left] - values[right];
    return higherIsBetter ? -difference : difference;
  });
  const priorities = Array(count).fill(0);
  let start = 0;

  while (start < count) {
    let end = start + 1;
    while (end < count && values[order[end]] === values[order[start]]) end += 1;
    const averageRank = ((start + 1) + end) / 2;
    const percentile = count === 1 ? 0.5 : (count - averageRank) / (count - 1);
    for (let position = start; position < end; position += 1) {
      priorities[order[position]] = percentile;
    }
    start = end;
  }
  return priorities;
}

function computeScenario(weight, capacity = state.capacity) {
  const merit = percentilePriorities(state.candidates.map((candidate) => candidate.meritScore), true);
  const social = percentilePriorities(state.candidates.map((candidate) => candidate.schoolIps), false);
  const rows = state.candidates.map((candidate, index) => ({
    ...candidate,
    meritPriority: merit[index],
    socialPriority: social[index],
    compositeScore: (1 - weight / 100) * merit[index] + (weight / 100) * social[index],
  }));
  rows.sort((left, right) => {
    const compositeDifference = right.compositeScore - left.compositeScore;
    if (compositeDifference !== 0) return compositeDifference;
    const meritDifference = right.meritPriority - left.meritPriority;
    if (meritDifference !== 0) return meritDifference;
    return left.id.localeCompare(right.id, "fr");
  });
  return rows.map((candidate, index) => ({ ...candidate, rank: index + 1, inTopK: index < capacity }));
}

function median(values) {
  const ordered = [...values].sort((left, right) => left - right);
  const middle = Math.floor(ordered.length / 2);
  return ordered.length % 2 === 0
    ? (ordered[middle - 1] + ordered[middle]) / 2
    : ordered[middle];
}

function summarizeScenario(weight) {
  const rows = computeScenario(weight);
  const baselineRows = computeScenario(0);
  const baselineRanks = new Map(baselineRows.map((candidate) => [candidate.id, candidate.rank]));
  const baselineSelected = new Set(baselineRows.filter((candidate) => candidate.inTopK).map((candidate) => candidate.id));
  const selected = rows.filter((candidate) => candidate.inTopK);
  const selectedIds = new Set(selected.map((candidate) => candidate.id));
  const rankChanges = rows.map((candidate) => Math.abs(candidate.rank - baselineRanks.get(candidate.id)));
  const changedPlaces = [...baselineSelected].filter((id) => !selectedIds.has(id)).length;

  return {
    weight,
    rows,
    baselineRanks,
    selected,
    meanIps: selected.reduce((sum, candidate) => sum + candidate.schoolIps, 0) / selected.length,
    medianIps: median(selected.map((candidate) => candidate.schoolIps)),
    changedPlaces,
    movedCandidates: rankChanges.filter((change) => change > 0).length,
    meanAbsoluteRankChange: rankChanges.reduce((sum, change) => sum + change, 0) / rankChanges.length,
  };
}

function sortedSelectedWeights() {
  return [...state.selectedWeights].sort((left, right) => left - right);
}

function announce(message) {
  byId("interaction-status").textContent = message;
}

function syncCustomControls() {
  const weight = Number(byId("custom-weight").value);
  const included = state.selectedWeights.has(weight);
  byId("custom-weight-output").textContent = formatWeight(weight);
  const addButton = byId("add-custom-weight");
  addButton.disabled = included;
  addButton.innerHTML = included
    ? `Scénario ${weight} % déjà affiché <span aria-hidden="true">✓</span>`
    : `Ajouter le scénario à ${weight} % <span aria-hidden="true">＋</span>`;
}

function renderPresets() {
  const host = byId("preset-controls");
  const visibleWeights = [...new Set([...PRESET_WEIGHTS, ...sortedSelectedWeights()])]
    .sort((left, right) => left - right);
  host.innerHTML = visibleWeights.map((weight) => {
    const active = state.selectedWeights.has(weight);
    const baseline = weight === 0;
    const custom = !PRESET_WEIGHTS.includes(weight);
    const label = baseline ? `${formatWeight(weight)} · repère` : custom ? `${formatWeight(weight)} · perso ×` : formatWeight(weight);
    const action = active ? "Retirer" : "Ajouter";
    const accessibleLabel = baseline
      ? ' aria-label="Scénario de référence à 0 %, toujours visible"'
      : ` aria-label="${action} le scénario ${formatWeight(weight)}${custom ? " personnalisé" : ""}"`;
    return `<button type="button" class="weight-pill${baseline ? " baseline" : ""}" data-toggle-weight="${weight}" aria-pressed="${active}"${accessibleLabel}>${label}</button>`;
  }).join("");
  syncCustomControls();
}

function renderScenarioCards() {
  const host = byId("scenario-cards");
  const summaries = sortedSelectedWeights().map((weight) => summarizeScenario(weight));
  host.innerHTML = summaries.map((summary) => {
    const active = summary.weight === state.activeWeight;
    const label = summary.weight === 0 ? "Référence · mérite seul" : "Poids IPS illustratif";
    const changedLabel = summary.changedPlaces === 1 ? "place du top-k modifiée" : "places du top-k modifiées";
    const movedLabel = summary.movedCandidates === 1 ? "rang déplacé" : "rangs déplacés";
    return `<button type="button" class="scenario-card" data-activate-weight="${summary.weight}" aria-pressed="${active}" aria-label="Examiner le scénario ${formatWeight(summary.weight)}">
      <span class="scenario-card-header"><span><span class="scenario-title">${formatWeight(summary.weight)}</span><span class="scenario-label">${label}</span></span><span class="scenario-focus">${active ? "Examiné" : "Examiner"}</span></span>
      <span class="card-metrics">
        <span class="card-metric"><strong>${formatNumber(summary.meanIps)}</strong><span>IPS moyen du top-${state.capacity}</span></span>
        <span class="card-metric"><strong>${summary.changedPlaces}</strong><span>${changedLabel} vs 0 %</span></span>
        <span class="card-metric"><strong>${summary.movedCandidates} / ${state.candidates.length}</strong><span>${movedLabel}</span></span>
        <span class="card-metric"><strong>${formatNumber(summary.meanAbsoluteRankChange)}</strong><span>déplacement moyen en rangs</span></span>
      </span>
      <span class="card-foot">Voir le détail du classement <span aria-hidden="true">↗</span></span>
    </button>`;
  }).join("");
}

function renderAverageChart() {
  const host = byId("average-chart");
  const summaries = sortedSelectedWeights().map((weight) => summarizeScenario(weight));
  host.innerHTML = summaries.map((summary) => {
    const width = Math.min(100, Math.max(0, (summary.meanIps / MAX_MEAN_SCALE) * 100));
    const active = summary.weight === state.activeWeight;
    return `<div class="bar-row" role="listitem" aria-current="${active}">
      <button class="bar-weight" type="button" data-activate-weight="${summary.weight}" aria-label="Examiner le scénario ${formatWeight(summary.weight)}">${formatWeight(summary.weight)}</button>
      <span class="bar-track" aria-hidden="true"><span class="bar-fill" style="width:${width.toFixed(2)}%"></span></span>
      <span class="bar-value">${formatNumber(summary.meanIps)}</span>
    </div>`;
  }).join("") + '<p class="chart-foot">Échelle fixe de 0 à 160. Cliquer sur une ligne ouvre ce scénario dans le tableau.</p>';
}

function renderActiveScenarioSelect() {
  const select = byId("active-scenario");
  const weights = sortedSelectedWeights();
  if (!state.selectedWeights.has(state.activeWeight)) state.activeWeight = weights[0] ?? 0;
  select.innerHTML = weights.map((weight) => `<option value="${weight}"${weight === state.activeWeight ? " selected" : ""}>${formatWeight(weight)}${weight === 0 ? " — référence" : ""}</option>`).join("");
}

function rankMovement(candidate, baselineRank) {
  return baselineRank - candidate.rank;
}

function movementText(delta) {
  if (delta > 0) return `remonte de ${delta} ${delta === 1 ? "rang" : "rangs"}`;
  if (delta < 0) {
    const amount = Math.abs(delta);
    return `descend de ${amount} ${amount === 1 ? "rang" : "rangs"}`;
  }
  return "rang inchangé";
}

function renderMovementChart() {
  const host = byId("movement-chart");
  const scenario = summarizeScenario(state.activeWeight);
  const maxDelta = Math.max(1, state.candidates.length - 1);
  const maxHalfWidth = 44;
  host.innerHTML = scenario.rows.map((candidate) => {
    const delta = rankMovement(candidate, scenario.baselineRanks.get(candidate.id));
    const width = Math.abs(delta) / maxDelta * maxHalfWidth;
    const directionClass = delta > 0 ? "up" : delta < 0 ? "down" : "same";
    const accessible = `${candidate.id}, rang initial ${scenario.baselineRanks.get(candidate.id)}, rang simulé ${candidate.rank}, ${movementText(delta)}.`;
    const bar = delta === 0 ? "" : `<span class="move-bar ${directionClass}" style="--move-width:${width.toFixed(2)}%"></span>`;
    return `<div class="move-row" role="listitem" aria-label="${escapeHtml(accessible)}">
      <span class="move-id">${escapeHtml(candidate.id)}</span>
      <span class="move-ranks">${scenario.baselineRanks.get(candidate.id)} → ${candidate.rank}</span>
      <span class="move-track" aria-hidden="true">${bar}</span>
      <span class="move-description">${movementText(delta)}</span>
    </div>`;
  }).join("");
}

function renderCandidateTable() {
  const scenario = summarizeScenario(state.activeWeight);
  const rows = [...scenario.rows].sort((left, right) => scenario.baselineRanks.get(left.id) - scenario.baselineRanks.get(right.id));
  byId("candidate-rows").innerHTML = rows.map((candidate) => {
    const initialRank = scenario.baselineRanks.get(candidate.id);
    const delta = rankMovement(candidate, initialRank);
    const deltaClass = delta > 0 ? "delta-up" : delta < 0 ? "delta-down" : "delta-same";
    const deltaValue = delta > 0 ? `+${delta}` : String(delta);
    const status = candidate.inTopK
      ? `<span class="selection-badge in">Dans le top-${state.capacity}</span>`
      : `<span class="selection-badge out">Hors du top-${state.capacity}</span>`;
    return `<tr>
      <th scope="row"><span class="candidate-id">${escapeHtml(candidate.id)}</span></th>
      <td><span class="school-cell">${escapeHtml(candidate.school)}</span><span class="ips-cell">${formatNumber(candidate.schoolIps, 0)}</span></td>
      <td class="rank-cell">${initialRank}</td>
      <td class="rank-cell">${candidate.rank}</td>
      <td class="${deltaClass}" aria-label="${movementText(delta)}">${deltaValue}</td>
      <td>${status}</td>
    </tr>`;
  }).join("");
  byId("table-caption").textContent = `Scénario ${formatWeight(state.activeWeight)} · rang initial au mérite seul · rang simulé avec le poids sélectionné.`;
}

function renderAll() {
  byId("capacity-output").textContent = `Top ${state.capacity}`;
  byId("table-title").textContent = `Le détail, candidat·e par candidat·e · scénario ${formatWeight(state.activeWeight)}`;
  renderPresets();
  renderScenarioCards();
  renderAverageChart();
  renderActiveScenarioSelect();
  renderMovementChart();
  renderCandidateTable();
}

function toggleWeight(weight) {
  if (weight === 0) return;
  if (state.selectedWeights.has(weight)) {
    state.selectedWeights.delete(weight);
    if (state.activeWeight === weight) state.activeWeight = 0;
    announce(`Scénario ${formatWeight(weight)} retiré de la comparaison.`);
  } else {
    state.selectedWeights.add(weight);
    state.activeWeight = weight;
    announce(`Scénario ${formatWeight(weight)} ajouté à la comparaison.`);
  }
  renderAll();
}

function bindControls() {
  byId("preset-controls").addEventListener("click", (event) => {
    const button = event.target.closest("[data-toggle-weight]");
    if (button) toggleWeight(Number(button.dataset.toggleWeight));
  });

  byId("scenario-cards").addEventListener("click", (event) => {
    const button = event.target.closest("[data-activate-weight]");
    if (!button) return;
    state.activeWeight = Number(button.dataset.activateWeight);
    announce(`Scénario ${formatWeight(state.activeWeight)} affiché dans le classement détaillé.`);
    renderAll();
  });

  byId("average-chart").addEventListener("click", (event) => {
    const button = event.target.closest("[data-activate-weight]");
    if (!button) return;
    state.activeWeight = Number(button.dataset.activateWeight);
    announce(`Scénario ${formatWeight(state.activeWeight)} affiché dans le classement détaillé.`);
    renderAll();
  });

  const customSlider = byId("custom-weight");
  const addButton = byId("add-custom-weight");
  customSlider.addEventListener("input", syncCustomControls);
  addButton.addEventListener("click", () => {
    const weight = Number(customSlider.value);
    state.selectedWeights.add(weight);
    state.activeWeight = weight;
    announce(`Scénario personnalisé à ${formatWeight(weight)} ajouté à la comparaison.`);
    renderAll();
  });

  byId("capacity").addEventListener("input", (event) => {
    state.capacity = Number(event.target.value);
    renderAll();
    announce(`Taille du top-k réglée à ${state.capacity} profils fictifs.`);
  });

  byId("active-scenario").addEventListener("change", (event) => {
    state.activeWeight = Number(event.target.value);
    renderAll();
    announce(`Scénario ${formatWeight(state.activeWeight)} affiché dans le classement détaillé.`);
  });
}

async function start() {
  try {
    const response = await fetch("/data/candidates.json", { cache: "no-store" });
    if (!response.ok) throw new Error(`Chargement impossible (${response.status}).`);
    const candidates = await response.json();
    if (!Array.isArray(candidates) || candidates.length === 0) throw new Error("Échantillon fictif vide ou invalide.");
    state.candidates = candidates;
    bindControls();
    renderAll();
  } catch (error) {
    document.body.innerHTML = `<main class="load-error"><p class="eyebrow">VISUALISATION INDISPONIBLE</p><h1>Impossible de charger l’exemple fictif.</h1><p>${escapeHtml(error.message)}</p><p>Rechargez la page; aucun dossier réel n’est utilisé.</p></main>`;
  }
}

start();
