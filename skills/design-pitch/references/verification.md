# 验收手册（真实浏览器）

## 预览服务器

优先用 Claude Browser 的 `preview_start`（`.claude/launch.json`），没有就用 `playwright` 技能。

**NAS / 网络卷上的坑（实测 2026-11-13）**：预览进程读不了 `/Volumes/...` 上的目录，`os.getcwd()` 直接 PermissionError。解决：
1. 把实验目录镜像到本机：`rsync -a --delete <项目>/design/lab/ ~/<名字>-lab/`（每次子代理改完都要重新同步）。
2. launch.json 用隔离模式并在 Python 里 chdir（避免 cwd 在 NAS 上）：

```json
{ "version": "0.0.1", "configurations": [ {
  "name": "design-lab", "runtimeExecutable": "/usr/bin/python3",
  "runtimeArgs": ["-I", "-c", "import os,sys,runpy;os.chdir('/Users/<you>/<名字>-lab');sys.argv=['http.server','8766','--bind','127.0.0.1'];runpy.run_module('http.server',run_name='__main__')"],
  "port": 8766 } ] }
```

局域网访问：把 `127.0.0.1` 换成 `0.0.0.0` 并重启；**先告诉用户页面里有什么数据**，用完改回。本机 IP：`ipconfig getifaddr en0` / `en1`。

## JS 语法与逻辑检查（无 Node 时）

```bash
J=/System/Library/Frameworks/JavaScriptCore.framework/Versions/Current/Helpers/jsc
printf 'var window={};var location={search:""};var document={addEventListener(){},dispatchEvent(){},hidden:false};var matchMedia=()=>({matches:false});var CustomEvent=function(){};var URLSearchParams=function(){return {get(){return null}}};var console={error:print,log:print};\n' > /tmp/jsc-shim.js
$J /tmp/jsc-shim.js shared/data.js shared/core.js -e 'print(JSON.stringify(window.SD.metrics()))'
```
（`setInterval` 未定义的报错可忽略。jsc 打不开含中文的路径，先把文件复制到 `/tmp` 再检查。）

## 每个方向必须做的检查

1. **截图**：桌面 1440×900、手机 390×844（`preview_resize` 后 `location.reload()`），亲眼看：首屏是否看得到关键信息、文字是否可读、标志时刻是否可见、有没有截断/重叠。
2. **状态扫描**（在对照台页面里用 iframe 批量跑，一次别超过 ~25 秒，超时就拆成两批）：

```js
(async () => {
  const out = [];
  for (const d of ['a-x','b-y','c-z']) for (const q of ['state=loading','state=empty','state=offline','state=error','motion=reduced']) {
    const f = document.createElement('iframe'); f.style.cssText='width:1440px;height:900px;position:absolute;left:-9999px';
    const errs=[]; f.src=`/${d}/index.html?${q}`; document.body.appendChild(f);
    await new Promise(r=>f.onload=r); f.contentWindow.addEventListener('error',e=>errs.push(e.message));
    await new Promise(r=>setTimeout(r,500));
    out.push(`${d} ${q}: errs=${errs.length} overflow=${f.contentDocument.documentElement.scrollWidth-1440}`); f.remove();
  }
  return out.join('\n');
})()
```

3. **交互冒烟**（同样用 iframe，调用共享 core 的 API）：筛选为空 → 页面出现"没有匹配"文案；清空 → 选中第一条 → 详情里出现它独有的字段（如会话编号）→ 派发 Escape → 选中状态清空。另外在真实页面按键（如 `j`）后检查 `document.activeElement` 是否落在详情的关闭按钮。
4. **控制台**：`preview_console_logs level=warn` 为空；`performance.getEntriesByType('resource')` 无 4xx。

## 常见问题清单（上一轮实际发现过的）

- 高饱和元素用成纯白块、压住文字 → 改身份色细条，文字独立一行或实底。
- 标志时刻被其他层挡住看不见（例如背景网格被内容盖住）。
- 加载态只有一行字，没有骨架。
- 浅色方向：标签压在彩条上难读、手机上标签被视口边缘截断。
- 首屏放了太多"氛围"，关键运行信息掉到折叠线下。
- 程序化选中（键盘）打开详情时焦点落在跳转链接上。
- 回放结束的对象看起来仍像"运行中"。

## 不能自动验证、要在交付里写明的

指针悬停/倾斜类效果、动画是否流畅、长时间 CPU 占用、真实数据量放大后的性能。

## 补充经验（看板正式版验收，2026-11-13）

- **子代理做的前端要自己用"真的在运行"的数据验一遍**：它在无头环境里常常没有运行中的任务，节拍、计时、静默提示等都没测到。派一个真实任务（例如三条各睡 12 秒的命令）再看。
- **页面设了 `X-Frame-Options` / `frame-ancestors` 就不能用 iframe 批量扫状态页**（contentDocument 为 null）。改成：逐个导航当前标签页，或另起带参数的服务实例（空数据目录 = 空状态；一个只回 500 的小服务 = 出错状态）。
- **预览进程是沙箱的**：除了读不了 NAS，它启动的子进程（如 tmux）可能无限挂起而不是报错。后端调用外部命令一律加超时，超时当作"未知"，不要推断。真实的后端要验证时，用 Bash 在沙箱外启动，再让预览标签页导航过去。
- 子代理报告"已验证"的内容不能直接采信；它说无头浏览器忽略了 390 宽度，手机排版必须自己在真实浏览器里用 `preview_resize` 验。
