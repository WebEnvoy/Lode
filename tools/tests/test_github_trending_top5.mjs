import assert from "node:assert/strict";
import test from "node:test";
import { run } from "../../sites/github/trending/scripts/read-daily-trending-top5.mjs";

function snapshotText(options = {}) {
  const rows = options.rows ?? Array.from({ length: 5 }, (_, index) => {
    const owner = `owner${index + 1}`;
    const repo = `repo${index + 1}`;
    const metadata = options.unlabeledLanguage && index === 0 ? "Rust 37,184 5,407" : "TypeScript 1,234 456";
    const rowMetadata = options.unlabeledLanguage && index === 0 ? metadata : `${metadata} Built by`;
    const stars = options.abbreviatedStars && index === 0 ? "1.2k stars today" : `${index + 1},234 stars today`;
    return `${owner} / ${repo}\nExample description ${index + 1}\n${rowMetadata}\n${stars}`;
  });
  return `GitHub Trending\n\n${rows.join("\n\n")}`;
}

function harness(options = {}) {
  const events = [];
  const pageRef = "page:github:current";
  const observationRef = "observation:github:snapshot:1";
  const snapshotResult = {
    status: "completed",
    page: { current_url: options.url ?? "https://github.com/trending", title: "Trending", page_ref: pageRef },
    snapshot: {
      text: options.text ?? snapshotText(options),
      truncated: options.truncated ?? false,
      coverage: { text: { state: options.coverage ?? "complete" } },
      observation_ref: observationRef,
      page_ref: pageRef
    }
  };
  const broker = {
    runtime: {
      async invoke(request) {
        events.push({ method: "runtime.invoke", request });
        return snapshotResult;
      }
    },
    output: {
      async write(output) {
        events.push({ method: "output.write", output });
        return { accepted: true };
      }
    }
  };
  return { broker, events, pageRef, observationRef };
}

test("maps a complete labeled daily snapshot through the two declared broker calls", async () => {
  const { broker, events, pageRef, observationRef } = harness();
  const result = await run({}, broker, {});
  assert.deepEqual(result, { accepted: true });
  assert.deepEqual(events.map(({ method }) => method), ["runtime.invoke", "output.write"]);
  assert.deepEqual(events[0].request, { operation_id: "instance.snapshot", action: "read" });

  const output = events[1].output;
  assert.equal(output.status, "available");
  assert.equal(output.normalized.rows.length, 5);
  assert.deepEqual(output.normalized.rows[0], {
    name: "owner1/repo1",
    url: "https://github.com/owner1/repo1",
    language: "TypeScript",
    language_state: "observed",
    today_stars: 1234,
    today_stars_state: "observed"
  });
  assert.deepEqual(output.source_refs, [{ ref_id: pageRef, source_kind: "harbor_page" }]);
  assert.deepEqual(output.evidence_refs, [{
    ref_id: observationRef,
    evidence_kind: "snapshot_ref",
    producer: "harbor",
    redaction: "summary_only"
  }]);
});

test("uses GitHub's bounded language-and-count row metadata with multiword languages", async () => {
  const text = snapshotText().replace("TypeScript 1,234 456 Built by", "Jupyter Notebook 1,234 456 Built by");
  const { broker, events } = harness({ text });
  await run({}, broker, {});
  assert.equal(events[1].output.normalized.rows[0].language, "Jupyter Notebook");
  assert.equal(events[1].output.status, "available");
});

test("unlabeled language is unknown and prevents a complete result", async () => {
  const { broker, events } = harness({ unlabeledLanguage: true });
  await run({}, broker, {});
  const first = events[1].output.normalized.rows[0];
  assert.equal(first.language, null);
  assert.equal(first.language_state, "unknown");
  assert.equal(events[1].output.status, "partial");
});

test("abbreviated daily stars remain unknown", async () => {
  const { broker, events } = harness({ abbreviatedStars: true });
  await run({}, broker, {});
  const first = events[1].output.normalized.rows[0];
  assert.equal(first.today_stars, null);
  assert.equal(first.today_stars_state, "unknown");
  assert.equal(events[1].output.status, "partial");
});

test("malformed comma grouping is not normalized into a guessed count", async () => {
  const text = snapshotText().replace("1,234 stars today", "1,,234 stars today");
  const { broker, events } = harness({ text });
  await run({}, broker, {});
  assert.equal(events[1].output.normalized.rows[0].today_stars, null);
  assert.equal(events[1].output.normalized.rows[0].today_stars_state, "unknown");
  assert.equal(events[1].output.status, "partial");
});

test("truncated or incomplete snapshots cannot become available", async () => {
  for (const options of [{ truncated: true }, { coverage: "omitted_on_continuation" }]) {
    const { broker, events } = harness(options);
    await run({}, broker, {});
    assert.equal(events[1].output.status, "partial");
    assert.notEqual(events[1].output.normalized.completeness, "complete");
  }
});

test("language-filtered and weekly targets are rejected instead of silently narrowed", async () => {
  for (const url of ["https://github.com/trending/javascript", "https://github.com/trending?since=weekly"]) {
    const { broker, events } = harness({ url });
    await assert.rejects(() => run({}, broker, {}), /site_changed:expected_daily_unfiltered_trending/);
    assert.deepEqual(events.map(({ method }) => method), ["runtime.invoke"]);
  }
});

test("caller input and unbounded or mismatched snapshots are rejected", async () => {
  {
    const { broker, events } = harness();
    await assert.rejects(() => run({ url: "https://github.com/trending" }, broker, {}), /invalid_contract:empty_input_required/);
    assert.deepEqual(events, []);
  }
  {
    const { broker, events } = harness({ text: "x".repeat(65_537) });
    await assert.rejects(() => run({}, broker, {}), /invalid_contract:snapshot_text_over_limit/);
    assert.deepEqual(events.map(({ method }) => method), ["runtime.invoke"]);
  }
  {
    const { broker, events } = harness();
    events.length = 0;
    const originalInvoke = broker.runtime.invoke;
    broker.runtime.invoke = async (request) => {
      const result = await originalInvoke(request);
      result.snapshot.page_ref = "page:stale";
      return result;
    };
    await assert.rejects(() => run({}, broker, {}), /site_changed:snapshot_page_mismatch/);
    assert.deepEqual(events.map(({ method }) => method), ["runtime.invoke"]);
  }
});
