const REPOSITORY = /^[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+$/;
const COUNT = /^(?:0|[1-9]\d*|[1-9]\d{0,2}(?:,\d{3})+)$/;
const TODAY_STARS = /^((?:0|[1-9]\d*|[1-9]\d{0,2}(?:,\d{3})+))\s+stars?\s+today$/i;
const LABELED_LANGUAGE = /^Language:\s*(.*?)\s*$/i;
const TRENDING_ROW_METADATA = /^(.+?)\s+((?:0|[1-9]\d*|[1-9]\d{0,2}(?:,\d{3})+))\s+((?:0|[1-9]\d*|[1-9]\d{0,2}(?:,\d{3})+))\s+Built by$/i;
const MAX_SNAPSHOT_TEXT = 65_536;

function normalizedLines(text) {
  return text.replace(/\r\n?/g, "\n").split("\n").map((line) => line.trim());
}

function repositoryAt(lines, index) {
  const line = lines[index] ?? "";
  const compact = line.match(/^([A-Za-z0-9_.-]+)\s*\/\s*([A-Za-z0-9_.-]+)$/);
  if (compact) return { name: `${compact[1]}/${compact[2]}`, nextIndex: index + 1 };

  const split = line.match(/^([A-Za-z0-9_.-]+)\s*\/\s*$/);
  const next = lines[index + 1]?.match(/^([A-Za-z0-9_.-]+)$/);
  if (split && next) return { name: `${split[1]}/${next[1]}`, nextIndex: index + 2 };
  return undefined;
}

function parseCount(value) {
  const source = String(value ?? "");
  if (!COUNT.test(source)) return undefined;
  const digits = source.replace(/,/g, "");
  const count = Number(digits);
  return Number.isSafeInteger(count) ? count : undefined;
}

function parseRows(text) {
  const lines = normalizedLines(text);
  const headings = [];
  for (let index = 0; index < lines.length;) {
    const heading = repositoryAt(lines, index);
    if (!heading) {
      index += 1;
      continue;
    }
    headings.push({ ...heading, startIndex: index });
    index = heading.nextIndex;
  }

  const selected = headings.slice(0, 5);
  const rows = selected.map((heading, rowIndex) => {
    const endIndex = headings[rowIndex + 1]?.startIndex ?? lines.length;
    const block = lines.slice(heading.nextIndex, endIndex).filter(Boolean);
    const languageCandidates = block.flatMap((line) => {
      const labeled = line.match(LABELED_LANGUAGE);
      if (labeled) return [{ value: labeled[1].trim(), explicitlyAbsent: /^none$/i.test(labeled[1].trim()) }];
      const metadata = line.match(TRENDING_ROW_METADATA);
      return metadata ? [{ value: metadata[1].trim(), explicitlyAbsent: false }] : [];
    });
    const languageText = languageCandidates.length === 1 ? languageCandidates[0].value : "";
    const languageState = languageCandidates.length !== 1 ? "unknown" : languageText.length === 0 || languageCandidates[0].explicitlyAbsent ? "observed_absent" : "observed";
    const starMatches = block.map((line) => line.match(TODAY_STARS)).filter(Boolean);
    const todayStars = starMatches.length === 1 ? parseCount(starMatches[0][1]) : undefined;
    const todayStarsState = todayStars === undefined ? "unknown" : "observed";
    const language = languageState === "observed" ? languageText : null;

    return {
      name: heading.name,
      url: `https://github.com/${heading.name}`,
      language,
      language_state: languageState,
      today_stars: todayStars ?? null,
      today_stars_state: todayStarsState
    };
  });
  return { rows, headings, lines };
}

function snapshotCoverage(snapshot) {
  const state = snapshot.coverage?.text?.state;
  if (["complete", "truncated", "omitted_on_continuation", "unavailable"].includes(state)) return state;
  return "unknown";
}

function requireDailyTrendingPage(urlValue) {
  let url;
  try {
    url = new URL(urlValue);
  } catch {
    throw new Error("site_changed:invalid_page_url");
  }
  const allowedQuery = [...url.searchParams.entries()];
  const daily = allowedQuery.length === 0 || allowedQuery.length === 1 && allowedQuery[0][0] === "since" && allowedQuery[0][1] === "daily";
  if (url.origin !== "https://github.com" || url.pathname !== "/trending" || !daily || url.hash || url.username || url.password) {
    throw new Error("site_changed:expected_daily_unfiltered_trending");
  }
}

function buildOutput(result) {
  const { snapshot, page } = result;
  if (result.status !== "completed" || typeof page?.current_url !== "string" || typeof page?.page_ref !== "string" ||
      typeof snapshot?.text !== "string" || typeof snapshot?.observation_ref !== "string" || typeof snapshot?.page_ref !== "string") {
    throw new Error("resource_unavailable:bounded_snapshot_missing");
  }
  requireDailyTrendingPage(page.current_url);
  if (snapshot.page_ref !== page.page_ref) throw new Error("site_changed:snapshot_page_mismatch");
  if (snapshot.text.length > MAX_SNAPSHOT_TEXT) throw new Error("invalid_contract:snapshot_text_over_limit");

  const parsed = parseRows(snapshot.text);
  const rows = parsed.rows;
  const namesUnique = new Set(rows.map((row) => row.name)).size === rows.length;
  const textCoverage = snapshotCoverage(snapshot);
  const completeSnapshot = snapshot.truncated === false && textCoverage === "complete";
  const completeRows = rows.length === 5 && rows.every((row) => row.language_state !== "unknown" && row.today_stars_state === "observed");
  const status = completeSnapshot && completeRows && namesUnique ? "available" : "partial";
  const completeness = status === "available" ? "complete" : textCoverage === "unavailable" ? "unknown" : "partial";

  return {
    result_kind: "github_trending_daily_top5",
    status,
    normalized: {
      period: "daily",
      requested_count: 5,
      rows,
      completeness,
      snapshot_coverage: textCoverage
    },
    source_refs: [{ ref_id: page.page_ref, source_kind: "harbor_page" }],
    evidence_refs: [{ ref_id: snapshot.observation_ref, evidence_kind: "snapshot_ref", producer: "harbor", redaction: "summary_only" }]
  };
}

export async function run(input, broker, context) {
  if (input == null || typeof input !== "object" || Array.isArray(input) || Object.keys(input).length !== 0) {
    throw new Error("invalid_contract:empty_input_required");
  }
  if (!broker?.runtime?.invoke || !broker?.output?.write) throw new Error("invalid_contract:required_broker_methods_unavailable");

  const snapshotResult = await broker.runtime.invoke({ operation_id: "instance.snapshot", action: "read" });
  const output = buildOutput(snapshotResult);
  return await broker.output.write(output);
}
