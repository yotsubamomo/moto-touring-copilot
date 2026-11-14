// G3 audit regression check for prototype/index.html (mock data only). Serve the folder, open the page, then in the console:
//   (0, eval)(await (await fetch("/g3-audit-check.js")).text()); await __all()
// Returns the failed checks (empty when all pass) and panel heights. Keep the browser tab visible while it runs.
window.__g3 = async function () {
  const wait = (ms) => new Promise((r) => setTimeout(r, ms));
  const g = (id) => document.getElementById(id);
  const R = () => g("panel-result"), V = () => g("panel-valid");
  const txt = (el) => el.innerText.replace(/\s+/g, " ");
  const fails = [], notes = {};
  const ok = (name, cond, info) => { if (!cond) fails.push(name + (info !== undefined ? " :: " + JSON.stringify(info) : "")); };
  const layout = (label) => {
    const de = document.documentElement;
    ok(label + " page overflow", de.scrollWidth <= de.clientWidth, [de.scrollWidth, de.clientWidth]);
    const p = document.querySelector("[role=tabpanel]:not([hidden])");
    ok(label + " exactly one panel visible", document.querySelectorAll("[role=tabpanel]:not([hidden])").length === 1);
    const wrapped = [...p.querySelectorAll(".badge")].filter((b) => b.getClientRects().length && b.getBoundingClientRect().height > (b.classList.contains("big") ? 46 : 32)).map((b) => b.innerText.trim());
    ok(label + " wrapped badges", wrapped.length === 0, wrapped.slice(0, 3));
    const big = [...document.querySelectorAll("svg")].filter((e) => { const r = e.getBoundingClientRect(); return r.width > 24 || r.height > 24; }).length;
    ok(label + " oversize icon", big === 0, big);
    const small = [...p.querySelectorAll("a, button, input, select, summary")].filter((e) => e.getClientRects().length).filter((e) => { const r = e.getBoundingClientRect(); return (r.width < 24 || r.height < 24) && e.tagName !== "A"; }).length;
    ok(label + " target under 24px", small === 0, small);
  };
  const run = async (id, tweak) => {
    applyScenario(id); if (tweak) tweak();
    g("plan-btn").click();
    await wait(60);
    const during = { disabled: g("plan-btn").disabled, steps: txt(g("steps")) };
    await wait(1900);
    let asked = false;
    if (!g("ask-card").hidden) {
      asked = true; const before = txt(R());
      notes.askNoPlanningBeforeReply = !during.disabled && !state.planning;
      g("ask-submit").click(); await wait(60);
      during.disabled = g("plan-btn").disabled; during.steps = txt(g("steps"));
      await wait(1900); notes.askResultChanged = before !== txt(R());
    }
    return { during, asked };
  };

  // idle
  ok("idle result", /尚未規劃/.test(txt(R())));
  ok("no snapshot label when idle and unchecked", !/Snapshot Mode/.test(txt(g("topbar"))));

  const expect = {
    feasible: ["FEASIBLE 可行", "搜尋完成 COMPLETE"], conditional: ["CONDITIONAL 有條件可行", "搜尋完成 COMPLETE"],
    beyond: ["CONDITIONAL 有條件可行", "搜尋完成 COMPLETE"], dusk: ["FEASIBLE 可行", "搜尋完成 COMPLETE"],
    rain: ["FEASIBLE 可行", "搜尋完成 COMPLETE"], "rain-early": ["FEASIBLE 可行", "搜尋完成 COMPLETE"],
    "replan-ok": ["CONDITIONAL 有條件可行", "搜尋完成 COMPLETE"], infeasible: ["INFEASIBLE 不可行", "搜尋完成 COMPLETE"],
    "infeasible-time": ["INFEASIBLE 不可行", "搜尋完成 COMPLETE"], incomplete: ["CONDITIONAL 有條件可行", "搜尋未完成 INCOMPLETE"],
    template: ["CONDITIONAL 有條件可行", "搜尋完成 COMPLETE"], "output-error": null,
    ask: ["CONDITIONAL 有條件可行", "搜尋完成 COMPLETE"], conflict: ["CONDITIONAL 有條件可行", "搜尋完成 COMPLETE"],
  };
  ok("14 scenarios", SCENARIOS.length === 14, SCENARIOS.length);

  for (const s of SCENARIOS) {
    const id = s.id, r = await run(id);
    selectTab("tab-result");
    const rt = txt(R()), head = [...R().querySelectorAll(".badge")].slice(0, 2).map((b) => b.innerText.trim());
    ok(id + " button disabled while planning", r.during.disabled);
    ok(id + " steps without percent", !/%/.test(r.during.steps) && /進行中/.test(r.during.steps), r.during.steps.slice(0, 30));
    ok(id + " status card collapsed after planning", g("status-card").classList.contains("compact") && g("status-card").getBoundingClientRect().height < 70, Math.round(g("status-card").getBoundingClientRect().height));
    if (expect[id]) ok(id + " status badges", head[0] === expect[id][0] && head[1] === expect[id][1], head);
    else { ok(id + " no plan status badge", !/FEASIBLE|CONDITIONAL|INFEASIBLE/.test(rt)); ok(id + " error message", /輸出驗證錯誤/.test(rt)); }
    ok(id + " tab-result selected after planning", g("tab-result").getAttribute("aria-selected") === "true" && !R().hidden);
    ok(id + " no 真實 API badge on mock rows", [...R().querySelectorAll(".badge")].every((x) => !/真實 API/.test(x.textContent)));
    ok(id + " every source row badge says 模擬", (() => { const t = [...R().querySelectorAll("table")].find((x) => /來源證據/.test(x.caption ? x.caption.innerText : "")); return t && [...t.tBodies[0].rows].every((row) => row.cells[2].querySelector(".badge").innerText.trim() === "模擬" && /正式產品：/.test(row.cells[2].innerText)); })());
    ok(id + " no P90 on page", !/P90/i.test(document.body.innerText));
    ok(id + " no free chat input in results", !R().querySelector("input, textarea") && V().querySelectorAll("textarea, input:not([type=radio])").length === 0);
    ok(id + " badges all have text", [...document.querySelectorAll(".badge")].every((b) => b.textContent.trim().length > 0));
    layout(id + " result");
    selectTab("tab-valid"); layout(id + " valid");
    const vt = txt(V());
    if (state.result.best && !state.result.outputError) {
      ok(id + " rule cards 1-4", V().querySelectorAll(".rule").length >= 5);
      ok(id + " heading names recommended", /逐條規則結果：推薦的候選/.test(vt));
      ok(id + " details collapsed by default", !g("cand-details").open);
      ok(id + " summary says all candidates", /全部候選（共 \d+ 個/.test(txt(g("cand-details").querySelector("summary"))));
    }
    ok(id + " replan log present", /重新規劃紀錄/.test(vt));
    ok(id + " no raw planner text", !/原始/.test(vt));
    selectTab("tab-result");

    // scenario-specific
    if (id === "conditional") {
      const kids = [...R().children];
      ok("todo box right after status row", kids[1].classList.contains("warn") && /出發前要確認的事項（1 項）/.test(txt(kids[1])) && /仍然是「有條件可行」/.test(txt(kids[1])));
      ok("four metrics", R().querySelectorAll(".metric").length === 4);
      ok("label latest feasible", /最晚的可行出發時間/.test(rt));
      selectTab("tab-valid");
      const unk = [...V().querySelectorAll(".rule")].find((x) => /UNKNOWN 無法判定/.test(x.innerText));
      ok("unknown four items", unk && ["缺失的項目", "原因", "來源與時間", "人工確認指引"].every((k) => unk.innerText.includes(k)) && /不會把這條規則改為 PASS/.test(unk.innerText));
      // candidate selection: main block stays, picked shows below, focus kept
      const mainBefore = txt(V().querySelector("h3:nth-of-type(2)") || V());
      g("cand-details").open = true; state.candOpen = true;
      const radios = [...V().querySelectorAll('input[name="cand"]')];
      radios[0].focus(); radios[0].click(); await wait(50);
      const act = document.activeElement;
      ok("focus stays on chosen radio", act && act.name === "cand" && act.checked, act && act.tagName);
      ok("details stay open after selection", g("cand-details").open);
      ok("main block still recommended", /逐條規則結果：推薦的候選/.test(txt(V())));
      ok("picked block below table", /選取的候選：13:00 出發/.test(txt(g("picked"))) && g("picked").querySelectorAll(".rule").length === 4);
      ok("picked block is after the table", !!(g("cand-details").querySelector("table").compareDocumentPosition(g("picked")) & Node.DOCUMENT_POSITION_FOLLOWING));
      ok("recommended row marked", /推薦/.test(txt(g("cand-details").querySelector("table"))));
      const recRadio = radios.length && [...V().querySelectorAll('input[name="cand"]')].find((x) => x.value === state.result.best.planId);
      recRadio.click(); await wait(50);
      ok("picking the recommended row points upward", /它的逐條規則結果在上方/.test(txt(g("picked"))));
      selectTab("tab-result");
    }
    if (id === "beyond") ok("beyond: two todo items and no weather data", /出發前要確認的事項（2 項）/.test(rt) && /沒有天氣資料/.test(rt));
    if (id === "incomplete") ok("incomplete label and notice", /建議的出發時間（搜尋未完成）/.test(rt) && !/最晚的可行出發時間<\/div>/.test(R().innerHTML) && /只評估了 8 \/ \d+ 個候選/.test(rt));
    if (id === "template") ok("template notice", /說明文字已改用固定模板/.test(rt) && /來源：固定模板/.test(rt));
    if (id === "output-error") { ok("output error keeps conditions and sources", /採用的條件/.test(rt) && /來源證據/.test(rt)); selectTab("tab-valid"); ok("rule 5 FAIL shown", /規則 5 可追溯 FAIL 未通過/.test(txt(V()))); selectTab("tab-result"); }
    if (id === "replan-ok") { selectTab("tab-valid"); ok("replan log two rounds with refuel", /重新規劃 1/.test(txt(V())) && /新增加油/.test(txt(V()))); selectTab("tab-result"); ok("refuel in conditions", /由重新規劃加入/.test(rt)); }
    if (id === "rain") { ok("rain caption", /不是氣象署的警特報/.test(rt)); ok("rain: later candidate fails rule 3", state.result.candidates.some((c) => c.rules[3].r === "FAIL") && state.result.best.rules[3].r === "PASS"); }
    if (id === "rain-early") ok("rain-early: alert label shown while rule 3 passes", /高降雨機率提醒/.test(rt) && state.result.best.rules[3].r === "PASS");
    if (id === "dusk") ok("dusk: later candidates fail rule 1 on civil dusk", state.result.candidates.some((c) => c.rules[1].r === "FAIL" && /民用暮光終/.test(c.rules[1].detail)));
    if (id === "infeasible") {
      ok("infeasible result tab wording", /原因、代表候選與替代方案在/.test(rt) && !R().querySelector(".metric"));
      selectTab("tab-valid"); const t = txt(V());
      ok("infeasible: representative label", /代表性失敗候選：15:45 出發/.test(t) && /這不是有效的建議/.test(t));
      ok("infeasible: basis matches rule", /取 FAIL 規則數最少的候選；無法再比較時取出發時間最晚的一個/.test(t));
      ok("infeasible: alternatives unverified", /替代方案（未經驗證，不會自動執行）/.test(t));
      ok("infeasible: early stop", /提前停止/.test(t));
      ok("infeasible: rule 5 not applicable", /規則 5 不適用/.test(t));
      ok("infeasible: fail statistics", /各規則的 FAIL 統計/.test(t));
      const rows = [...g("cand-details").querySelectorAll("tbody tr")];
      const marked = rows.filter((x) => /代表候選/.test(x.textContent));
      const nf = (c) => Object.values(c.rules).filter((x) => x.r === "FAIL").length;
      const minF = Math.min(...state.result.candidates.map(nf));
      const want = state.result.candidates.filter((c) => nf(c) === minF).reduce((x, y) => (y.d > x.d ? y : x));
      ok("infeasible: one row marked, the latest departure among fewest-FAIL candidates", marked.length === 1 && marked[0].textContent.includes(fmt(want.d)) && state.result.representative.c === want, [marked.length, fmt(want.d)]);
      selectTab("tab-result");
    }
    if (id === "infeasible-time") { selectTab("tab-valid"); const t = txt(V()); ok("time-only: closest label and basis", /最接近時間限制的候選：16:05 出發/.test(t) && /全部候選都只違反規則 1/.test(t) && /這不是有效的建議/.test(t)); selectTab("tab-result"); }
    if (id === "ask") ok("ask then break", r.asked && notes.askResultChanged && /休息 20 分鐘/.test(rt));
    if (id === "conflict") ok("conflict notice", /自然語言與表單不一致/.test(rt) && /以表單的「最早可出發時間」為準/.test(rt));
  }

  // representative naming, mixed failures (not one of the 14 scenarios)
  applyScenario("feasible"); env = { road: "simulated_clear", highPop: ["17:50", "18:30"] };
  g("earliest").value = "16:40"; g("deadline").value = "18:00"; g("plan-btn").click(); await wait(1900);
  let rep = state.result.representative;
  ok("mixed A: not called closest when others break other rules", rep.label === "代表性失敗候選" && fmt(rep.c.d) === "16:40" && /其他候選還違反別的規則/.test(rep.basis), [rep.label, fmt(rep.c.d)]);
  // earlier candidate has the smaller overrun but also breaks rule 3
  applyScenario("feasible"); env = { road: "simulated_clear", highPop: ["17:15", "17:36"] };
  g("earliest").value = "16:40"; g("deadline").value = "18:00"; g("plan-btn").click(); await wait(1900);
  rep = state.result.representative;
  notes.mixedB = state.result.candidates.map((c) => fmt(c.d) + ":" + Object.entries(c.rules).filter(([, x]) => x.r === "FAIL").map(([n]) => n).join("+")).join(" ") + " -> " + rep.label + " " + fmt(rep.c.d);
  ok("mixed B: fewest-FAIL candidate is not named closest", rep.label === "代表性失敗候選", notes.mixedB);

  // snapshot label follows the result on screen
  const top = () => txt(g("topbar"));
  const mode = () => (R().innerText.match(/資料模式\s*([^\n]+)/) || [])[1];
  const prod = () => [...R().querySelectorAll("table")].pop().innerText.match(/正式產品：[^\n\t]+/g).join("|");
  g("snapshot").checked = false; applyScenario("conditional"); g("plan-btn").click(); await wait(1900);
  ok("snap A normal plan", !/Snapshot Mode/.test(top()) && mode() === "一般模式" && /正式產品：真實 API/.test(prod()) && g("stale").hidden);
  g("snapshot").click(); await wait(30);
  ok("snap B toggle on keeps label with old result", !/Snapshot Mode/.test(top()) && mode() === "一般模式" && !g("stale").hidden && /Snapshot Mode/.test(txt(g("stale"))), [top(), txt(g("stale")).slice(0, 40)]);
  g("plan-btn").click(); await wait(1900);
  ok("snap C snapshot plan", /Snapshot Mode：目前顯示的結果/.test(top()) && /Snapshot Mode/.test(mode()) && /正式產品：資料快照/.test(prod()) && !/正式產品：真實 API/.test(prod()) && g("stale").hidden);
  g("snapshot").click(); await wait(30);
  ok("snap D toggle off keeps label with old result", /Snapshot Mode：目前顯示的結果/.test(top()) && /Snapshot Mode/.test(mode()) && !g("stale").hidden, top());
  g("plan-btn").click(); await wait(1900);

  // stale names the changed fields and keeps the old result
  const beforeStale = txt(R());
  g("fuel").value = "60"; g("fuel").dispatchEvent(new Event("input", { bubbles: true }));
  g("deadline").value = "16:30"; g("deadline").dispatchEvent(new Event("input", { bubbles: true }));
  ok("stale lists changed fields", !g("stale").hidden && /最晚抵達終點時間、出發油量/.test(txt(g("stale"))), txt(g("stale")).slice(0, 60));
  ok("stale keeps old result", txt(R()) === beforeStale);
  g("fuel").value = "80"; g("fuel").dispatchEvent(new Event("input", { bubbles: true }));
  g("deadline").value = "17:00"; g("deadline").dispatchEvent(new Event("input", { bubbles: true }));
  ok("stale clears when inputs match again", g("stale").hidden);

  // field errors
  const err = async (label, fn, re) => {
    applyScenario("feasible"); fn(); g("plan-btn").click(); await wait(80);
    const es = g("error-summary");
    ok("err " + label, !es.hidden && re.test(txt(es)) && document.activeElement === es && !state.planning, txt(es).slice(0, 40));
    const bad = document.querySelectorAll('[aria-invalid="true"]');
    ok("err " + label + " aria-invalid + inline error", bad.length === 1 && !g(bad[0].getAttribute("aria-describedby")).hidden);
    const a = es.querySelector("a"); a.click(); await wait(50);
    ok("err " + label + " link focuses field", document.activeElement === bad[0]);
  };
  await err("fuel empty", () => { g("fuel").value = ""; }, /請填出發油量/);
  await err("fuel over", () => { g("fuel").value = "140"; }, /0 到 100/);
  await err("deadline before earliest", () => { g("earliest").value = "15:00"; g("deadline").value = "14:00"; }, /必須晚於/);
  applyScenario("feasible"); g("plan-btn").click(); await wait(1900);
  ok("errors cleared after a valid plan", g("error-summary").hidden && !document.querySelector('[aria-invalid="true"]'));
  ok("required legend", /必填欄位/.test(txt(document.querySelector("#planner-title").parentElement)));

  // tabs by keyboard
  g("tab-result").focus(); g("tab-result").dispatchEvent(new KeyboardEvent("keydown", { key: "ArrowRight", bubbles: true }));
  ok("arrow right selects validation tab", g("tab-valid").getAttribute("aria-selected") === "true" && document.activeElement === g("tab-valid") && !V().hidden && R().hidden);
  g("tab-valid").dispatchEvent(new KeyboardEvent("keydown", { key: "ArrowLeft", bubbles: true }));
  ok("arrow left returns", g("tab-result").getAttribute("aria-selected") === "true" && !R().hidden);

  const src = await fetch("/index.html").then((x) => x.text());
  ok("no external urls", (src.match(/https?:\/\/[^\s"'<>)]+/g) || []).every((u) => u.startsWith("http://www.w3.org/")));
  ok("no emoji", !/[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}]/u.test(src));
  return { vw: document.documentElement.clientWidth, vh: innerHeight, failCount: fails.length, fails, notes };
};
"loaded";

window.__m = async () => { const wait = (ms) => new Promise((r) => setTimeout(r, ms)); const g = (id) => document.getElementById(id); const o = { vw: document.documentElement.clientWidth };
  for (const id of ["feasible", "conditional", "incomplete", "infeasible"]) { applyScenario(id); g("plan-btn").click(); await wait(1900); selectTab("tab-result");
    const a = Math.round(g("panel-result").getBoundingClientRect().height); const sc = [...g("panel-result").querySelectorAll(".table-wrap")].filter((w) => w.scrollWidth > w.clientWidth + 1).length;
    selectTab("tab-valid"); const b = Math.round(g("panel-valid").getBoundingClientRect().height); selectTab("tab-result");
    o[id] = { R: a, V: b, status: Math.round(g("status-card").getBoundingClientRect().height), tabTop: Math.round(document.querySelector("[role=tablist]").getBoundingClientRect().top + scrollY), scrollTablesR: sc }; }
  return o; };
window.__all = async () => { const r = await window.__g3(); const m = await window.__m(); return { vw: r.vw, failCount: r.failCount, fails: r.fails, m }; };
