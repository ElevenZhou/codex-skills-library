#!/usr/bin/env node
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname, extname, isAbsolute, resolve } from "node:path";
import { execFile } from "node:child_process";
import { promisify } from "node:util";

const DEFAULT_MODEL = "grok-imagine-video";
const DEFAULT_BASE_URL = "https://sg01-cli.api.flaios.com/";
// Shared key registry; K_NODE is the sg01/n04 node key.
const DEFAULT_PROVIDERS_JSON = "E:/Dev-2/本地大模型调用/config/providers.json";
const ALLOWED_SECONDS = new Set(["6", "10"]);
const ALLOWED_SIZES = new Set(["720x1280", "1280x720", "1024x1792", "1792x1024"]);

function printHelp() {
  console.log(`
Usage:
  node generate-grok-video.mjs [options] "prompt"

Options:
  --base-url <url>      Defaults to GROK_VIDEO_BASE_URL or ${DEFAULT_BASE_URL}
  --api-key <key>       Defaults to GROK_VIDEO_API_KEY, then K_NODE in providers.json
  --model <model>       Defaults to GROK_VIDEO_MODEL or ${DEFAULT_MODEL} (also: grok-imagine-video-1.5)
  --output <path>       Output mp4 path. Defaults to output/grok-video-<timestamp>.mp4
  --seconds <6|10>      Defaults to 6
  --size <size>         One of 720x1280, 1280x720, 1024x1792, 1792x1024
  --task <id>           Resume an already-submitted task instead of creating a new one
  --poll <seconds>      Poll timeout in seconds. Defaults to 600
  --interval <seconds>  Poll interval in seconds. Defaults to 10
  --help                Show this help

Examples:
  node generate-grok-video.mjs --seconds 6 --size 1280x720 --output output/demo.mp4 "A cinematic product shot..."
  node generate-grok-video.mjs --seconds 10 --size 720x1280 "A vertical social video..."
`);
}

function parseArgs(argv) {
  const options = {};
  const promptParts = [];

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--help" || arg === "-h") {
      options.help = true;
      continue;
    }
    if (arg.startsWith("--")) {
      const key = arg.slice(2);
      const value = argv[i + 1];
      if (!value || value.startsWith("--")) {
        throw new Error(`Missing value for --${key}`);
      }
      options[key] = value;
      i += 1;
      continue;
    }
    promptParts.push(arg);
  }

  options.prompt = promptParts.join(" ").trim();
  return options;
}

function timestamp() {
  return new Date().toISOString().replace(/[:.]/g, "-");
}

function replaceExtension(path, extension) {
  const current = extname(path);
  return current ? path.slice(0, -current.length) + extension : path + extension;
}

function outputPathFrom(options) {
  const output = options.output || `output/grok-video-${timestamp()}.mp4`;
  const withExt = extname(output) ? output : `${output}.mp4`;
  return isAbsolute(withExt) ? withExt : resolve(process.cwd(), withExt);
}

function baseUrlFrom(value) {
  return (value || DEFAULT_BASE_URL).replace(/\/+$/, "").replace(/\/v1$/, "");
}

async function apiRequest({ baseUrl, apiKey, method, path, body }) {
  const response = await fetch(`${baseUrl}/v1${path}`, {
    method,
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  const contentType = response.headers.get("content-type") || "";
  const parsed = contentType.includes("application/json")
    ? await response.json().catch(() => null)
    : await response.text();

  if (!response.ok) {
    const message =
      parsed?.error?.message ||
      (typeof parsed?.error === "string" ? parsed.error : undefined) ||
      parsed?.message ||
      (typeof parsed === "string" ? parsed.slice(0, 500) : undefined) ||
      response.statusText;
    throw new Error(`${method} ${path} failed: ${response.status} ${message}`);
  }
  return parsed;
}

async function keyFromProviders() {
  const path = process.env.GROK_VIDEO_PROVIDERS_JSON || DEFAULT_PROVIDERS_JSON;
  try {
    const data = JSON.parse(await readFile(path, "utf8"));
    return data.providers?.find((provider) => provider.key_alias === "K_NODE")?.key;
  } catch {
    return undefined;
  }
}

async function download(url) {
  let response;
  try {
    response = await fetch(url);
  } catch (error) {
    // Node fetch ignores HTTPS_PROXY; vidgen.x.ai is usually unreachable without it, curl honors it.
    console.warn(`fetch failed (${error.cause?.code || error.message}); retrying download with curl...`);
    const { stdout } = await promisify(execFile)("curl", ["-sSfL", "--max-time", "300", url], {
      encoding: "buffer",
      maxBuffer: 1024 * 1024 * 1024,
    });
    return stdout;
  }
  if (!response.ok) {
    throw new Error(`Video download failed: ${response.status} ${await response.text()}`);
  }
  return Buffer.from(await response.arrayBuffer());
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  if (options.help) {
    printHelp();
    return;
  }

  if (!options.prompt) {
    printHelp();
    throw new Error("Prompt is required.");
  }

  const apiKey = options["api-key"] || process.env.GROK_VIDEO_API_KEY || (await keyFromProviders());
  if (!apiKey) {
    throw new Error("No API key: set GROK_VIDEO_API_KEY, pass --api-key, or check K_NODE in providers.json.");
  }

  const baseUrl = baseUrlFrom(options["base-url"] || process.env.GROK_VIDEO_BASE_URL);
  const model = options.model || process.env.GROK_VIDEO_MODEL || DEFAULT_MODEL;
  const seconds = String(options.seconds || "6");
  const size = options.size || "1280x720";
  const pollSeconds = Number(options.poll || 600);
  const intervalSeconds = Number(options.interval || 10);

  if (!ALLOWED_SECONDS.has(seconds)) {
    throw new Error(`Invalid --seconds ${seconds}. Use 6 or 10.`);
  }
  if (!ALLOWED_SIZES.has(size)) {
    throw new Error(`Invalid --size ${size}. Use one of ${Array.from(ALLOWED_SIZES).join(", ")}.`);
  }
  if (!Number.isFinite(pollSeconds) || pollSeconds <= 0) {
    throw new Error("--poll must be a positive number.");
  }
  if (!Number.isFinite(intervalSeconds) || intervalSeconds <= 0) {
    throw new Error("--interval must be a positive number.");
  }

  const outputPath = outputPathFrom(options);
  const promptPath = replaceExtension(outputPath, ".txt");
  const metadataPath = replaceExtension(outputPath, ".json");

  let created;
  if (options.task) {
    console.log(`Resuming Grok video task ${options.task}...`);
    created = { id: options.task, resumed: true };
  } else {
    console.log(`Creating Grok video with ${model}, ${seconds}s, ${size}...`);
    created = await apiRequest({
      baseUrl,
      apiKey,
      method: "POST",
      path: "/videos",
      body: {
        model,
        prompt: options.prompt,
        seconds,
        size,
      },
    });
  }

  // sg01 now answers in xAI-native shape: { request_id } only.
  const taskId = created.id || created.task_id || created.request_id;
  if (!taskId) {
    throw new Error(`Video API returned no task id: ${JSON.stringify(created)}`);
  }

  console.log(`Task: ${taskId}`);
  const deadline = Date.now() + pollSeconds * 1000;
  let latest = created;
  let first = true;
  while (Date.now() <= deadline) {
    if (!first || !options.task) {
      await new Promise((resolve) => setTimeout(resolve, intervalSeconds * 1000));
    }
    first = false;
    latest = await apiRequest({
      baseUrl,
      apiKey,
      method: "GET",
      path: `/videos/${taskId}`,
    });

    const status = String(latest.status || "").toLowerCase();
    const progress = latest.progress ?? "";
    console.log(`Status: ${latest.status || "unknown"} ${progress}%`);

    if (status === "done" || status === "completed" || status === "succeeded") {
      break;
    }
    if (status === "failed" || status === "failure" || status === "error") {
      throw new Error(`Video task failed: ${JSON.stringify(latest)}`);
    }
  }

  const videoUrl = latest?.video?.url || latest?.url || latest?.data?.[0]?.url;
  if (!videoUrl) {
    throw new Error(`Video task did not return a downloadable video URL: ${JSON.stringify(latest)}`);
  }

  const bytes = await download(videoUrl);
  await mkdir(dirname(outputPath), { recursive: true });
  await writeFile(outputPath, bytes);
  await writeFile(promptPath, `${options.prompt}\n`, "utf8");
  await writeFile(
    metadataPath,
    JSON.stringify(
      {
        id: taskId,
        model,
        base_url: baseUrl,
        seconds,
        size,
        output: outputPath,
        prompt: promptPath,
        source_url: videoUrl,
        created,
        result: latest,
        saved_at: new Date().toISOString(),
      },
      null,
      2,
    ),
    "utf8",
  );

  console.log(`Saved: ${outputPath}`);
  console.log(`Prompt: ${promptPath}`);
  console.log(`Metadata: ${metadataPath}`);
}

main().catch((error) => {
  console.error(error.message);
  process.exitCode = 1;
});
