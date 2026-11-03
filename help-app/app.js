"use strict";

const state = { records: [], filtered: [], filter: "all", selected: null, query: "" };
const $ = (selector) => document.querySelector(selector);
const escapeHtml = (value) => String(value ?? "").replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[char]);
const normalize = (value) => String(value ?? "").toLowerCase().normalize("NFKC").replace(/[^0-9a-z가-힣]+/g, " ").trim();
const tokens = (value) => normalize(value).split(/\s+/).filter(Boolean);
const caseLabels = { faq: "질문과 답변", procedure: "사용 절차", troubleshooting: "오류 해결", caution: "주의사항", tip: "활용 팁" };
const observationLabels = { baseline_observed: "실화면 기본 관찰", deep_observed: "실화면 심층 관찰", completed: "실화면 기본 관찰" };

function recordKind(record) {
  if (record.type === "support_case") return `case-${record.case_type || "faq"}`;
  if (record.mapping_status === "unmapped") return "unmapped";
  if (record.type === "support_case_index" || String(record.id).startsWith("check:enrichment:")) return "inquiry";
  if (record.screen_code) return "screen";
  if (record.review_status === "candidate") return "candidate";
  if (record.type === "excel" || normalize(record.category).includes("엑셀")) return "excel";
  return "manual";
}

function scoreRecord(record, query) {
  if (!query) return record.screen_code ? 3 : record.review_status === "candidate" ? 1 : 2;
  const queryTokens = tokens(query);
  const exact = normalize(query).replace(/ /g, "");
  const screen = normalize(record.screen_code);
  const title = normalize(record.title);
  const aliases = normalize((record.aliases || []).join(" "));
  const category = normalize(record.category);
  const text = normalize(record.text);
  const caseContext = normalize(`${record.case_topic || ""} ${(record.case_topics || []).join(" ")} ${(record.case_facets || []).join(" ")} ${caseLabels[record.case_type] || ""}`);
  let score = 0;
  if (screen && exact === screen) score += 120;
  if (exact && title.replace(/ /g, "").includes(exact)) score += 45;
  if (exact && aliases.replace(/ /g, "").includes(exact)) score += 32;
  for (const token of queryTokens) {
    if (screen === token) score += 70;
    if (title.includes(token)) score += 18;
    if (aliases.includes(token)) score += 12;
    if (category.includes(token)) score += 7;
    if (caseContext.includes(token)) score += 14;
    if (text.includes(token)) score += 2;
  }
  if (queryTokens.length && queryTokens.every((token) => `${title} ${aliases} ${category} ${text}`.includes(token))) score += 12;
  if (record.review_status !== "candidate") score += 1;
  return score;
}

function matchesFilter(record) {
  if (state.filter === "all") return true;
  if (state.filter === "inquiry") return record.type === "support_case" || record.type === "support_case_index" || String(record.id).startsWith("check:enrichment:");
  if (state.filter === "unmapped") return record.mapping_status === "unmapped";
  return recordKind(record) === state.filter || (state.filter === "excel" && normalize(record.text).includes("excel premium"));
}

function updateUrl() {
  const url = new URL(location.href);
  state.query ? url.searchParams.set("q", state.query) : url.searchParams.delete("q");
  state.selected ? url.searchParams.set("id", state.selected) : url.searchParams.delete("id");
  state.filter !== "all" ? url.searchParams.set("filter", state.filter) : url.searchParams.delete("filter");
  history.replaceState(null, "", url);
}

function runSearch() {
  state.query = $("#search").value.trim();
  const ranked = state.records
    .filter(matchesFilter)
    .map((record) => ({ record, score: scoreRecord(record, state.query) }))
    .filter((item) => !state.query || item.score > 0);
  const sort = $("#sort").value;
  ranked.sort((a, b) => {
    if (sort === "screen") return String(a.record.screen_code || "9999").localeCompare(String(b.record.screen_code || "9999"));
    if (sort === "signals") return (b.record.signal_count || 0) - (a.record.signal_count || 0) || b.score - a.score;
    return b.score - a.score || String(a.record.title).localeCompare(String(b.record.title), "ko");
  });
  state.filtered = ranked.slice(0, 200).map((item) => item.record);
  renderResults();
  updateUrl();
}

function excerpt(record) {
  return String(record.text || "").replace(/[#>*|`\[\]]/g, " ").replace(/\s+/g, " ").slice(0, 150);
}

function renderResults() {
  const list = $("#results");
  $("#result-count").textContent = state.filtered.length === 200 ? "200+" : state.filtered.length;
  if (!state.filtered.length) {
    list.innerHTML = '<li class="state">일치하는 도움말이 없습니다. 다른 업무 표현이나 화면번호로 검색해 보세요.</li>';
    return;
  }
  list.innerHTML = state.filtered.map((record) => {
    const kind = recordKind(record);
    const badge = record.screen_code ? `TR ${escapeHtml(record.screen_code)}` : record.type === "support_case" ? escapeHtml(caseLabels[record.case_type] || "문의 사례") : kind === "inquiry" ? "문의 대응" : kind === "candidate" ? "검수 후보" : kind === "unmapped" ? "분류 대기" : record.type === "excel" ? "Excel" : "매뉴얼";
    return `<li class="result ${state.selected === record.id ? "active" : ""}"><button type="button" data-id="${escapeHtml(record.id)}"><div class="result-top"><span class="badge ${record.review_status === "candidate" ? "candidate" : ""}">${badge}</span>${record.signal_count ? `<span class="badge candidate">문의 ${record.signal_count}건</span>` : ""}</div><h3>${escapeHtml(record.title)}</h3><p>${escapeHtml(excerpt(record))}</p></button></li>`;
  }).join("");
}

function inlineMarkup(value) {
  return escapeHtml(value)
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/\bTR\s+(\d{4})\b/g, '<button type="button" class="inline-related" data-screen-code="$1">TR $1</button>');
}

function documentBody(markdown, title) {
  const lines = String(markdown || "").split(/\r?\n/);
  let index = 0;
  while (index < lines.length && !lines[index].trim()) index += 1;
  if (lines[index]?.replace(/^#\s+/, "").trim() === String(title || "").trim()) {
    lines.splice(index, 1);
  }
  while (index < lines.length && !lines[index].trim()) index += 1;
  if (/^>\s*출처\s*:/.test(lines[index] || "")) {
    lines.splice(index, 1);
  }
  return lines.join("\n").trim();
}

function renderMarkdown(markdown) {
  const lines = String(markdown || "").split(/\r?\n/);
  const html = [];
  let listOpen = false;
  let tableLines = [];
  const flushList = () => { if (listOpen) { html.push("</ul>"); listOpen = false; } };
  const flushTable = () => {
    if (!tableLines.length) return;
    const rows = tableLines.map((line) => line.slice(1, -1).split(/(?<!\\)\|/).map((cell) => cell.trim().replace(/\\\|/g, "|")));
    const hasDivider = rows.length > 1 && rows[1].every((cell) => /^:?-{3,}:?$/.test(cell));
    if (!hasDivider) html.push(`<pre class="raw-table">${escapeHtml(tableLines.join("\n"))}</pre>`);
    else {
      const header = `<thead><tr>${rows[0].map((cell) => `<th>${inlineMarkup(cell)}</th>`).join("")}</tr></thead>`;
      const body = rows.slice(2).map((row) => `<tr>${row.map((cell) => `<td>${inlineMarkup(cell)}</td>`).join("")}</tr>`).join("");
      html.push(`<div class="table-wrap"><table>${header}<tbody>${body}</tbody></table></div>`);
    }
    tableLines = [];
  };
  for (const line of lines) {
    if (/^\|.*\|$/.test(line)) { flushList(); tableLines.push(line); continue; }
    flushTable();
    const link = line.match(/^\[([^\]]+)\]\(([^)]+)\)$/);
    if (link) { flushList(); html.push(`<p><a class="source-link" href="${escapeHtml(link[2])}" target="_blank" rel="noopener">${inlineMarkup(link[1])}</a></p>`); continue; }
    const image = line.match(/^!\[([^\]]*)\]\(([^)]+)\)$/);
    if (image) { flushList(); html.push(`<img class="source-image" src="${escapeHtml(image[2])}" alt="${escapeHtml(image[1])}" loading="lazy">`); continue; }
    if (/^<details class="source-page">$/.test(line)) { flushList(); html.push('<details class="source-page">'); continue; }
    if (line === "</details>") { flushList(); html.push("</details>"); continue; }
    const summary = line.match(/^<summary>(.+)<\/summary>$/);
    if (summary) { flushList(); html.push(`<summary>${inlineMarkup(summary[1])}</summary>`); continue; }
    const heading = line.match(/^(#{1,3})\s+(.+)/);
    if (heading) { flushList(); html.push(`<h${heading[1].length}>${inlineMarkup(heading[2])}</h${heading[1].length}>`); continue; }
    if (line.startsWith("> ")) { flushList(); html.push(`<blockquote>${inlineMarkup(line.slice(2))}</blockquote>`); continue; }
    if (/^[-*]\s+/.test(line)) {
      if (!listOpen) { html.push("<ul>"); listOpen = true; }
      html.push(`<li>${inlineMarkup(line.replace(/^[-*]\s+/, ""))}</li>`); continue;
    }
    flushList();
    if (line.trim()) html.push(`<p>${inlineMarkup(line)}</p>`);
  }
  flushTable(); flushList();
  return html.join("");
}

function openRecord(id, push = true) {
  const record = state.records.find((item) => item.id === id);
  if (!record) return;
  state.selected = id;
  const candidate = record.review_status === "candidate";
  const caseLabel = record.type === "support_case" ? caseLabels[record.case_type] || "문의 사례" : null;
  $("#viewer").innerHTML = `<header class="doc-head"><div class="result-top"><span class="badge ${candidate ? "candidate" : ""}">${record.screen_code ? `TR ${escapeHtml(record.screen_code)}` : caseLabel ? escapeHtml(caseLabel) : candidate ? "검수 전 후보" : escapeHtml(record.type)}</span>${record.observation_status ? `<span class="badge observed">${escapeHtml(observationLabels[record.observation_status] || record.observation_status)}</span>` : ""}${record.signal_count ? `<span class="badge candidate">관련 신호 ${record.signal_count}건</span>` : ""}</div><h1>${escapeHtml(record.title)}</h1><div class="doc-meta"><span>출처: ${escapeHtml(record.source || "미기재")}</span><span>위치: ${escapeHtml(record.source_locator || "미기재")}</span>${record.case_topic ? `<span>업무·주제: ${escapeHtml(record.case_topic)}</span>` : ""}<span>ID: ${escapeHtml(record.id)}</span></div></header>${candidate ? '<div class="notice">비식별 문의 기록에서 만든 검수 전 지식입니다. 당시 대응을 공식 해결책으로 단정하지 말고, 공식 매뉴얼과 현재 제품 동작을 확인하세요.</div>' : ""}<article class="doc-body">${renderMarkdown(documentBody(record.text, record.title))}</article>${record.related?.length ? `<nav class="related"><h2>의미상 연결된 문서</h2>${record.related.map((item) => `<button type="button" data-related="${escapeHtml(item.id)}"><small>${escapeHtml(item.relation_label || "관련 문서")}</small>${item.screen_code ? `TR ${escapeHtml(item.screen_code)} · ` : ""}${escapeHtml(item.title)}</button>`).join("")}</nav>` : ""}`;
  renderResults();
  if (push) updateUrl();
  $("#viewer").scrollTo?.(0, 0);
}

function updateCounts() {
  const count = (kind) => state.records.filter((record) => kind === "all" || (kind === "inquiry" ? record.type === "support_case" || record.type === "support_case_index" || String(record.id).startsWith("check:enrichment:") : kind === "unmapped" ? record.mapping_status === "unmapped" : recordKind(record) === kind)).length;
  for (const kind of ["all", "screen", "excel", "inquiry", "case-faq", "case-procedure", "case-troubleshooting", "case-caution", "case-tip", "unmapped"]) $(`#count-${kind}`).textContent = count(kind).toLocaleString("ko-KR");
}

async function start() {
  const response = await fetch("data/knowledge.json");
  if (!response.ok) throw new Error(`도움말 데이터 응답 오류: ${response.status}`);
  state.records = await response.json();
  $("#loading").hidden = true;
  $("#results").hidden = false;
  updateCounts();
  const params = new URL(location.href).searchParams;
  $("#search").value = params.get("q") || "";
  state.filter = params.get("filter") || "all";
  document.querySelectorAll(".quick").forEach((button) => button.classList.toggle("active", button.dataset.filter === state.filter));
  runSearch();
  if (params.get("id")) openRecord(params.get("id"), false);
}

$("#search").addEventListener("input", runSearch);
$("#sort").addEventListener("change", runSearch);
$("#results").addEventListener("click", (event) => { const button = event.target.closest("[data-id]"); if (button) openRecord(button.dataset.id); });
$("#viewer").addEventListener("click", (event) => {
  const related = event.target.closest("[data-related]");
  if (related) { openRecord(related.dataset.related); return; }
  const screen = event.target.closest("[data-screen-code]");
  if (screen) {
    const record = state.records.find((item) => String(item.screen_code) === screen.dataset.screenCode);
    if (record) openRecord(record.id);
  }
});
document.querySelectorAll(".quick").forEach((button) => button.addEventListener("click", () => { state.filter = button.dataset.filter; document.querySelectorAll(".quick").forEach((item) => item.classList.toggle("active", item === button)); runSearch(); }));
document.querySelectorAll(".example").forEach((button) => button.addEventListener("click", () => { $("#search").value = button.dataset.query; runSearch(); $("#search").focus(); }));
document.addEventListener("keydown", (event) => { if (event.key === "/" && document.activeElement !== $("#search")) { event.preventDefault(); $("#search").focus(); } });
$("#theme").addEventListener("click", () => { const dark = document.documentElement.dataset.theme === "dark"; document.documentElement.dataset.theme = dark ? "light" : "dark"; localStorage.setItem("check-help-theme", dark ? "light" : "dark"); });
document.documentElement.dataset.theme = localStorage.getItem("check-help-theme") || (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
start().catch((error) => { $("#loading").textContent = `도움말을 불러오지 못했습니다: ${error.message}`; });
