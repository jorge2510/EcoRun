<p align="center">
  <img src="docs/icon-256.png" alt="EcoRun" width="120">
</p>

<h1 align="center">EcoRun</h1>

<p align="center">
  <b>Your best ally for building projects while saving tokens.</b><br>
  A Claude skill and plugin that picks the right model and effort level for each task,<br>
  so you spend fewer tokens without lowering the quality of the result.
</p>

<p align="center"><a href="README.md">Versión en español</a></p>

---

## What it does

EcoRun applies Anthropic's official model-selection guide ([Which Claude model should you build with?](https://claude.dev/blog/which-claude-model-should-you-build-with/)) to every task:

| Task type | Model |
|---|---|
| Searching, reading logs, extracting, classifying (mistakes are easy to spot) | **Haiku** |
| Well-scoped work with a clear spec, everyday documents | **Sonnet** |
| Work that needs judgment, design or hard debugging (the default starting point) | **Opus** |
| Large refactors and migrations, architecture, deep research | **Fable** (if you have access; otherwise Opus at `high`) |

It also follows a **quality ladder**: before moving up a model, it first gives Claude a way to verify its own work, then raises effort, and only then switches model.

The skill is written in Spanish, but Claude always answers in your language.

## Where it works

No skill can change the model of your main conversation; you choose that. What EcoRun does:

| Surface | Behavior |
|---|---|
| **Claude.ai and apps** | When a task starts and another model fits better, it writes one line such as `Suggested model: Sonnet · medium — scoped task` and keeps working. If you're already on the right model, it says nothing. |
| **Cowork** | Same as Claude.ai. If Cowork lets it spawn subagents with their own model, it delegates heavy reading to them. |
| **Claude Code** | Real routing: search, log reading and extraction go to Haiku subagents. For the main session it suggests `/model` and `/effort` when worthwhile. |
| **API** | Gives you the rules to choose `model` in code per step type. |

**Fable is automatic:** you don't configure anything. If Fable isn't available, EcoRun falls back to Opus at `high` without asking.

## Install

### Claude.ai and Cowork (skill)

1. Download [`dist/ecorun.zip`](dist/ecorun.zip).
2. Make sure code execution and file creation is enabled in Claude's capabilities settings.
3. Go to **Customize → Skills**, click **+**, choose **Create skill → Upload a skill**, and upload the ZIP.
4. Turn the skill on.

On Team or Enterprise plans, menu names may differ or an admin may need to enable skills. Skills enabled in your account also sync to Claude Code when you sign in with the same account.

### Claude Code (plugin, recommended)

The plugin includes the skill **and** the Haiku subagents, which is where most of the savings come from:

```
/plugin marketplace add jorge2510/EcoRun
/plugin install ecorun@ecorun
```

Optional but recommended: keep Claude Code's built-in exploration on Haiku too:

```bash
mkdir -p ~/.claude/agents
curl -o ~/.claude/agents/Explore.md https://raw.githubusercontent.com/jorge2510/EcoRun/main/templates/agents/Explore.md
```

Use a recent Claude Code (`claude update`). Don't set `CLAUDE_CODE_SUBAGENT_MODEL_FORCE`: it forces every subagent onto one model and disables the routing.

### Skill only, in Claude Code

Copy `skills/ecorun` to `~/.claude/skills/ecorun` (all projects) or `.claude/skills/ecorun` (one project). It works, without the bundled subagents.

## Usage

It triggers on its own at the start of substantial tasks, or when you talk about saving tokens, choosing a model or setting up subagents. You can also call it directly: "use EcoRun for this task" in Claude.ai, or `/ecorun:ecorun` in Claude Code.

## Docs

- [How EcoRun works](docs/como-funciona.md) (Spanish)
- [FAQ](docs/faq.md) (Spanish)
- [Claude Code and API reference](skills/ecorun/references/claude-code.md) (Spanish)

## Limitations

- No skill can switch the main conversation's model; EcoRun recommends and, where subagents exist, delegates.
- Model names and prices change. The price table shows when it was last checked; with a newer model, EcoRun applies the same rules per family and flags that the table may be outdated.
- Savings figures come from Anthropic's published tests. Your real savings depend on your tasks; measure them with `/usage` in Claude Code.

## License

[MIT](LICENSE) © 2026 Jorge Cabrera. EcoRun is an independent project and is not affiliated with Anthropic.
