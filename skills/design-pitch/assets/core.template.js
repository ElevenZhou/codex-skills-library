/* 比稿共享行为模板（所有方向一致）。复制到 <lab>/shared/core.js 后按项目改。
 * 完整的真实例子见同目录 core.reference.js（言出必办派发看板，含演示回放）。
 *
 * 约定（各方向只依赖这些）：
 *   APP.on(fn)             fn(state, reason)；reason: init|tick|clock|select|filter|conn|finish|toast
 *   APP.state()            { items, liveIds, selectedId, filter, conn, loading, toast, reduced }
 *   APP.filtered()         列表（筛选后）
 *   APP.select(id|null)    打开 / 关闭详情
 *   APP.setFilter(patch)
 *   APP.metrics()          页头指标
 *   APP.action(kind, id)   示意操作 → toast（比稿阶段不连后端）
 *   APP.fmt.*              格式化
 * 查询参数：?state=loading|empty|offline|error   ?motion=reduced
 */
(function () {
  const snap = window.APP_SNAPSHOT || { items: [] };          // ← 由导出脚本生成的真实数据
  const params = new URLSearchParams(location.search);
  const forced = params.get("state");
  const reduced = params.get("motion") === "reduced" ||
    (window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches);

  const listeners = [];
  let S = {
    items: forced === "empty" ? [] : snap.items.slice(),
    liveIds: [], selectedId: null,
    filter: { kind: "all", state: "all", q: "" },               // ← 按项目改
    conn: forced === "offline" ? "reconnecting" : forced === "error" ? "error" : "live",
    loading: true, toast: null, reduced,
  };
  const emit = (reason) => listeners.forEach((fn) => { try { fn(S, reason); } catch (e) { console.error(e); } });

  /* 演示回放：挑真实记录，按真实时间间隔加速重放，标记 demo:true（界面必须标注「演示回放」）。
     实现参考 core.reference.js 的 startReplay / tickReplay。 */
  function tick() { /* 推进回放；有变化 emit("tick")，否则 emit("clock") */ emit("clock"); }

  function filtered() {
    const f = S.filter, q = f.q.trim().toLowerCase();
    return S.items.filter((x) => !x.demo)
      .filter((x) => f.kind === "all" || x.kind === f.kind)
      .filter((x) => f.state === "all" || x.state === f.state)
      .filter((x) => !q || JSON.stringify(x).toLowerCase().includes(q));
  }
  function metrics() { return { total: S.items.filter((x) => !x.demo).length }; }   // ← 按项目改

  function action(kind, id) {
    S.toast = { text: "比稿演示：" + kind + "（未连接后端，正式版会真的执行）", at: Date.now() };
    emit("toast");
    setTimeout(() => { if (S.toast && Date.now() - S.toast.at > 3500) { S.toast = null; emit("toast"); } }, 3800);
  }
  function move(dir) {
    const list = filtered(); if (!list.length) return;
    let i = list.findIndex((x) => x.id === S.selectedId);
    i = i < 0 ? 0 : Math.max(0, Math.min(list.length - 1, i + dir));
    S.selectedId = list[i].id; emit("select");
  }
  document.addEventListener("keydown", (e) => {
    const typing = /INPUT|TEXTAREA|SELECT/.test((e.target || {}).tagName || "");
    if (e.key === "/" && !typing) { e.preventDefault(); document.dispatchEvent(new CustomEvent("app:focus-search")); }
    else if (e.key === "Escape") { if (typing) e.target.blur(); else if (S.selectedId) { S.selectedId = null; emit("select"); } }
    else if (!typing && (e.key === "j" || e.key === "ArrowDown")) { e.preventDefault(); move(1); }
    else if (!typing && (e.key === "k" || e.key === "ArrowUp")) { e.preventDefault(); move(-1); }
  });

  let timer = null;
  const start = () => { if (!timer) timer = setInterval(tick, 1000); };
  const stop = () => { clearInterval(timer); timer = null; };
  document.addEventListener("visibilitychange", () => (document.hidden ? stop() : start()));
  setTimeout(() => {
    if (forced === "loading") return;                            // 停在骨架屏，供状态检查
    S.loading = false; emit("init"); start();
  }, forced ? 50 : 700);

  const fmt = {
    ago(t) { const d = Math.floor(Date.now() / 1000) - t; return d < 60 ? "刚刚" : d < 3600 ? Math.floor(d / 60) + " 分钟前" : d < 86400 ? Math.floor(d / 3600) + " 小时前" : Math.floor(d / 86400) + " 天前"; },
    dur(s) { return s == null ? "—" : s < 60 ? s + " 秒" : Math.floor(s / 60) + " 分 " + (s % 60) + " 秒"; },
  };

  window.APP = {
    on(fn) { listeners.push(fn); fn(S, "init"); },
    state: () => S, filtered, metrics, action, fmt,
    select(id) { S.selectedId = id; emit("select"); },
    setFilter(p) { S.filter = Object.assign({}, S.filter, p); emit("filter"); },
    reconnect() { S.conn = "live"; emit("conn"); },
  };
})();
