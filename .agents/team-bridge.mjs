#!/usr/bin/env node
// Team bridge: a dependency-free MCP (stdio) server that lets one AI agent
// hand work to another. Exposes tools:
//   ask_codex  -> runs `codex exec` (ChatGPT / OpenAI Codex CLI)
//   ask_gemini -> runs `gemini -p`  (Google Gemini CLI)
// Register it in Claude Code (.mcp.json), Codex and Gemini CLI so every agent
// can delegate to the others. TEAM_DEPTH stops endless delegation loops.
import { spawn } from "node:child_process";
import { appendFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const MAX_DEPTH = Number(process.env.TEAM_MAX_DEPTH || 2);
const depth = Number(process.env.TEAM_DEPTH || 0);
const TIMEOUT_MS = Number(process.env.TEAM_TIMEOUT_MS || 10 * 60 * 1000);
const LOG = join(dirname(fileURLToPath(import.meta.url)), "logs", "team.log");

const workers = {
  ask_codex: {
    label: "Codex (ChatGPT)",
    cmd: (prompt) => ["codex", ["exec", "--skip-git-repo-check", "-s", "workspace-write", prompt]],
  },
  ask_gemini: {
    label: "Gemini",
    cmd: (prompt) => ["gemini", ["-p", prompt, "--approval-mode", "auto_edit"]],
  },
};

const SELF = process.env.TEAM_SELF; // hide the caller's own tool
const tools = Object.entries(workers).filter(([n]) => n !== SELF).map(([name, w]) => ({
  name,
  description: `Delegate a task to ${w.label}. It works in the given directory and returns its final answer.`,
  inputSchema: {
    type: "object",
    properties: {
      prompt: { type: "string", description: "The full task, with all context the worker needs." },
      cwd: { type: "string", description: "Working directory (default: current)." },
    },
    required: ["prompt"],
  },
}));

function log(line) {
  try {
    mkdirSync(dirname(LOG), { recursive: true });
    appendFileSync(LOG, `[${new Date().toISOString()}] depth=${depth} ${line}\n`);
  } catch {}
}

function run(name, { prompt, cwd }) {
  if (depth >= MAX_DEPTH) {
    return Promise.resolve({ text: `Refused: delegation depth ${depth} reached the limit (${MAX_DEPTH}). Do the task yourself.`, isError: true });
  }
  const [bin, args] = workers[name].cmd(prompt);
  log(`${name} START ${prompt.slice(0, 200).replace(/\n/g, " ")}`);
  return new Promise((resolve) => {
    const child = spawn(bin, args, {
      cwd: cwd || process.cwd(),
      env: {
        // Placeholders: the cloud network proxy swaps in the real saved keys.
        OPENAI_API_KEY: "sk-proxy-placeholder",
        CODEX_API_KEY: "sk-proxy-placeholder",
        GEMINI_API_KEY: "proxy-placeholder",
        GEMINI_CLI_TRUST_WORKSPACE: "true",
        ...process.env,
        TEAM_DEPTH: String(depth + 1),
      },
      stdio: ["ignore", "pipe", "pipe"],
    });
    let out = "", err = "";
    child.stdout.on("data", (d) => (out += d));
    child.stderr.on("data", (d) => (err += d));
    const timer = setTimeout(() => child.kill("SIGTERM"), TIMEOUT_MS);
    child.on("error", (e) => { clearTimeout(timer); resolve({ text: `Failed to start ${bin}: ${e.message}`, isError: true }); });
    child.on("close", (code) => {
      clearTimeout(timer);
      log(`${name} END code=${code}`);
      const text = code === 0 ? out.trim() : `exit ${code}\n${out}\n${err}`.trim();
      resolve({ text: text || "(no output)", isError: code !== 0 });
    });
  });
}

const send = (msg) => process.stdout.write(JSON.stringify(msg) + "\n");

let buf = "";
process.stdin.on("data", async (chunk) => {
  buf += chunk;
  let i;
  while ((i = buf.indexOf("\n")) >= 0) {
    const line = buf.slice(0, i).trim();
    buf = buf.slice(i + 1);
    if (!line) continue;
    let req;
    try { req = JSON.parse(line); } catch { continue; }
    const { id, method, params } = req;
    if (id === undefined) continue; // notification
    if (method === "initialize") {
      send({ jsonrpc: "2.0", id, result: {
        protocolVersion: params?.protocolVersion || "2025-06-18",
        capabilities: { tools: {} },
        serverInfo: { name: "team-bridge", version: "1.0.0" },
      } });
    } else if (method === "tools/list") {
      send({ jsonrpc: "2.0", id, result: { tools } });
    } else if (method === "tools/call") {
      const name = params?.name;
      if (!workers[name]) {
        send({ jsonrpc: "2.0", id, error: { code: -32602, message: `Unknown tool ${name}` } });
        continue;
      }
      const r = await run(name, params.arguments || {});
      send({ jsonrpc: "2.0", id, result: { content: [{ type: "text", text: r.text }], isError: r.isError } });
    } else if (method === "ping") {
      send({ jsonrpc: "2.0", id, result: {} });
    } else {
      send({ jsonrpc: "2.0", id, error: { code: -32601, message: `Method not found: ${method}` } });
    }
  }
});
