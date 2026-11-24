/* 言出必办 · 派发看板比稿 — shared behaviour (identical for every direction).
 * Data: window.SD_SNAPSHOT (real runs from ~/say-done-runs, see dashboard/server/export_runs.py).
 * Live: two real runs are replayed as "running" (demo replay, clearly labelled) so motion and
 * state changes can be compared. Variants only render; they never change data or behaviour.
 *
 *   SD.on(fn)            fn(state, reason) on every change (reason: init|tick|select|filter|conn|finish|toast)
 *   SD.state()           { runs, liveIds, selectedId, filter, conn, loading, toast }
 *   SD.filtered()        history list after agent/state/search filter (live runs excluded)
 *   SD.select(id|null)   open / close detail
 *   SD.setFilter(patch)  { agent: 'all'|agent, state: 'all'|state, q: string }
 *   SD.metrics()         header strip numbers
 *   SD.agentStats()      per-agent comparison rows
 *   SD.dayStats()        [{day, count, done, failed}] oldest → newest
 *   SD.action(kind, id)  stub actions (open|stop|send|continue) → toast
 *   SD.fmt.{dur,ago,clock,date,cost}
 *   SD.AGENTS            identity: label, hue family, tagline
 *   SD.STATES            state labels
 * Query params: ?state=loading|empty|offline|error   ?motion=reduced
 */
(function () {
  const snap = window.SD_SNAPSHOT || { runs: [] };
  const params = new URLSearchParams(location.search);
  const forced = params.get("state");
  const reduced = params.get("motion") === "reduced" ||
    (window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches);

  const AGENTS = {
    codex: { label: "Codex", family: "cyan", tagline: "OpenAI" },
    claude: { label: "Claude", family: "coral", tagline: "Anthropic" },
    opencode: { label: "OpenCode", family: "violet", tagline: "opencode" },
    grok: { label: "Grok", family: "magenta", tagline: "xAI · grok-4.7" },
  };
  const STATES = {
    running: "运行中", starting: "启动中", done: "完成", failed: "失败",
    interrupted: "已中断", cancelled: "已取消",
  };

  const now = () => Math.floor(Date.now() / 1000);
  const listeners = [];
  const base = forced === "empty" ? [] : snap.runs.map((r) => Object.assign({}, r));
  let S = {
    runs: base, liveIds: [], selectedId: null,
    filter: { agent: "all", state: "all", q: "" },
    conn: forced === "offline" ? "reconnecting" : forced === "error" ? "error" : "live",
    loading: true, toast: null, reduced,
  };

  function emit(reason) { listeners.forEach((fn) => { try { fn(S, reason); } catch (e) { console.error(e); } }); }

  /* ---------------- demo replay of two real runs ---------------- */
  function pickSources() {
    const rich = base.filter((r) => r.timeline && r.timeline.length >= 6 && r.duration);
    rich.sort((a, b) => b.timeline.length - a.timeline.length);
    const out = [];
    for (const r of rich) { if (!out.find((x) => x.agent === r.agent)) out.push(r); if (out.length === 2) break; }
    return out;
  }
  const replays = [];
  function startReplay(src, slot) {
    const id = "live-" + slot;
    const t = now();
    const run = Object.assign({}, src, {
      id, demo: true, sourceId: src.id, state: "running", phase: "exec",
      created: t, started: t, finished: null, duration: null,
      counters: { commands: 0, file_changes: 0, messages: 0 },
      timeline: [], screen: [], result: "", activity: "启动 " + AGENTS[src.agent].label + "…",
    });
    S.runs = S.runs.filter((r) => r.id !== id);
    S.runs.unshift(run);
    if (!S.liveIds.includes(id)) S.liveIds.push(id);
    const speed = Math.max(4, (src.duration || 60) / 45); // whole run ≈ 45 s on screen
    replays[slot] = { src, run, i: 0, speed, t0: Date.now(), screenStep: src.screen.length / Math.max(1, src.timeline.length) };
  }
  function tickReplay(slot) {
    const rp = replays[slot];
    if (!rp) return false;
    const { src, run } = rp;
    const elapsed = (Date.now() - rp.t0) / 1000 * rp.speed;
    let changed = false;
    while (rp.i < src.timeline.length && (src.timeline[rp.i].offset ?? rp.i * 8) <= elapsed) {
      const ev = Object.assign({}, src.timeline[rp.i], { fresh: Date.now() });
      run.timeline.push(ev);
      if (ev.kind === "command") { run.counters.commands++; run.activity = ev.text; }
      if (ev.kind === "edit") { run.counters.file_changes++; run.activity = "改文件 " + ev.text; }
      if (ev.kind === "message") { run.counters.messages++; run.activity = ev.text.split("\n")[0]; }
      const upto = Math.min(src.screen.length, Math.round((rp.i + 1) * rp.screenStep) + 6);
      run.screen = src.screen.slice(0, upto);
      rp.i++; changed = true;
    }
    if (rp.i >= src.timeline.length && run.state === "running") {
      run.state = src.state === "running" ? "done" : src.state;
      run.phase = "interactive"; run.finished = now(); run.duration = run.finished - run.started;
      run.result = src.result; run.screen = src.screen.slice(); run.cost = src.cost;
      run.justFinished = Date.now();
      emit("finish");
      setTimeout(() => { if (forced !== "empty") { startReplay(src, slot); emit("tick"); } }, 9000);
      return false;
    }
    return changed;
  }

  /* ---------------- derived data ---------------- */
  function filtered() {
    const f = S.filter, q = f.q.trim().toLowerCase();
    return S.runs.filter((r) => !r.demo)
      .filter((r) => f.agent === "all" || r.agent === f.agent)
      .filter((r) => f.state === "all" || r.state === f.state)
      .filter((r) => !q || [r.title, r.project, r.agent, r.id, r.prompt, r.result].join(" ").toLowerCase().includes(q));
  }
  function metrics() {
    const day = new Date(); day.setHours(0, 0, 0, 0);
    const today = S.runs.filter((r) => !r.demo && (r.created || 0) * 1000 >= day.getTime());
    const hist = S.runs.filter((r) => !r.demo);
    return {
      running: S.runs.filter((r) => r.state === "running").length,
      todayDone: today.filter((r) => r.state === "done").length,
      todayTotal: today.length,
      failed: hist.filter((r) => r.state === "failed" || r.state === "interrupted").length,
      total: hist.length,
      successRate: hist.length ? hist.filter((r) => r.state === "done").length / hist.length : 0,
      cost: hist.reduce((s, r) => s + (r.cost || 0), 0),
      commands: hist.reduce((s, r) => s + ((r.counters || {}).commands || 0), 0),
    };
  }
  function agentStats() {
    return Object.keys(AGENTS).map((a) => {
      const rs = S.runs.filter((r) => !r.demo && r.agent === a);
      const done = rs.filter((r) => r.state === "done");
      const durs = rs.map((r) => r.duration).filter((d) => d != null);
      return {
        agent: a, label: AGENTS[a].label, family: AGENTS[a].family, runs: rs.length,
        success: rs.length ? done.length / rs.length : 0,
        avgDuration: durs.length ? Math.round(durs.reduce((s, d) => s + d, 0) / durs.length) : null,
        cost: rs.reduce((s, r) => s + (r.cost || 0), 0),
        commands: rs.reduce((s, r) => s + ((r.counters || {}).commands || 0), 0),
        denials: rs.reduce((s, r) => s + (r.denials || 0), 0),
      };
    });
  }
  function dayStats() {
    const m = {};
    S.runs.filter((r) => !r.demo && r.created).forEach((r) => {
      const d = new Date(r.created * 1000); const k = (d.getMonth() + 1) + "/" + d.getDate();
      m[k] = m[k] || { day: k, count: 0, done: 0, failed: 0, t: r.created };
      m[k].count++; if (r.state === "done") m[k].done++; else m[k].failed++;
      m[k].t = Math.min(m[k].t, r.created);
    });
    return Object.values(m).sort((a, b) => a.t - b.t);
  }

  /* ---------------- formatting ---------------- */
  const fmt = {
    dur(s) { if (s == null) return "—"; if (s < 60) return s + " 秒"; const m = Math.floor(s / 60); return m < 60 ? m + " 分 " + (s % 60) + " 秒" : Math.floor(m / 60) + " 时 " + (m % 60) + " 分"; },
    ago(t) { if (!t) return "—"; const d = now() - t; if (d < 60) return "刚刚"; if (d < 3600) return Math.floor(d / 60) + " 分钟前"; if (d < 86400) return Math.floor(d / 3600) + " 小时前"; return Math.floor(d / 86400) + " 天前"; },
    clock(t) { if (!t) return "—"; const d = new Date(t * 1000); return String(d.getHours()).padStart(2, "0") + ":" + String(d.getMinutes()).padStart(2, "0"); },
    date(t) { if (!t) return "—"; const d = new Date(t * 1000); return (d.getMonth() + 1) + "月" + d.getDate() + "日 " + fmt.clock(t); },
    cost(c) { return c ? "$" + c.toFixed(c < 1 ? 3 : 2) : "—"; },
    elapsed(r) { return r.state === "running" ? now() - (r.started || now()) : r.duration; },
  };

  /* ---------------- actions & keyboard ---------------- */
  const ACTIONS = { open: "在电脑上打开窗口", stop: "停止任务", send: "发送一句话", continue: "复制续接话术" };
  function action(kind, id) {
    const r = S.runs.find((x) => x.id === id);
    const name = r ? "【" + r.title + "】" : "";
    S.toast = { text: "比稿演示：" + ACTIONS[kind] + " " + name + "（未连接后端，正式版会真的执行）", at: Date.now() };
    emit("toast");
    setTimeout(() => { if (S.toast && Date.now() - S.toast.at > 3500) { S.toast = null; emit("toast"); } }, 3800);
  }
  function move(dir) {
    const list = S.liveIds.map((id) => S.runs.find((r) => r.id === id)).filter(Boolean).concat(filtered());
    if (!list.length) return;
    let i = list.findIndex((r) => r.id === S.selectedId);
    i = i < 0 ? 0 : Math.max(0, Math.min(list.length - 1, i + dir));
    S.selectedId = list[i].id; emit("select");
  }
  document.addEventListener("keydown", (e) => {
    const typing = /INPUT|TEXTAREA|SELECT/.test((e.target || {}).tagName || "");
    if (e.key === "/" && !typing) { e.preventDefault(); document.dispatchEvent(new CustomEvent("sd:focus-search")); }
    else if (e.key === "Escape") { if (typing) e.target.blur(); else if (S.selectedId) { S.selectedId = null; emit("select"); } }
    else if (!typing && (e.key === "j" || e.key === "ArrowDown")) { e.preventDefault(); move(1); }
    else if (!typing && (e.key === "k" || e.key === "ArrowUp")) { e.preventDefault(); move(-1); }
  });

  /* ---------------- lifecycle ---------------- */
  let timer = null;
  function loop() {
    let changed = false;
    replays.forEach((_, i) => { if (tickReplay(i)) changed = true; });
    emit(changed ? "tick" : "clock");
  }
  function start() { if (!timer) timer = setInterval(loop, 1000); }
  function stop() { clearInterval(timer); timer = null; }
  document.addEventListener("visibilitychange", () => (document.hidden ? stop() : start()));

  setTimeout(() => {
    if (forced === "loading") return; // stays in skeleton for the state check
    S.loading = false;
    if (forced !== "empty" && forced !== "error") pickSources().forEach((src, i) => startReplay(src, i));
    emit("init"); start();
  }, forced ? 50 : 700);

  window.SD = {
    on(fn) { listeners.push(fn); fn(S, "init"); },
    state: () => S, filtered, metrics, agentStats, dayStats, fmt, action, AGENTS, STATES,
    select(id) { S.selectedId = id; emit("select"); },
    setFilter(p) { S.filter = Object.assign({}, S.filter, p); emit("filter"); },
    run: (id) => S.runs.find((r) => r.id === id),
    live: () => S.liveIds.map((id) => S.runs.find((r) => r.id === id)).filter(Boolean),
    reconnect() { S.conn = "live"; emit("conn"); },
  };
})();
