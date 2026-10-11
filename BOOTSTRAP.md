# AI Agent Self-Setup Protocol (`BOOTSTRAP.md`)

> **Instructions for AI Agents (Google Antigravity / Gemini, Claude Code, OpenAI Codex, Cursor, Windsurf, Copilot, etc.)**:
> If a user asked you to read this file or repository to configure their environment for scientific papers and research, execute the following deterministic steps.

---

## Step 1: Determine the Target Scope

1. Check if you are currently operating inside an active project workspace directory:
   - **Workspace Setup (Default)**: Configure the current working directory (`.`).
   - **New Workspace**: If the user has no active workspace open, create a dedicated research workspace directory (e.g., `research-workspace/`) and run the setup inside it.
   - **Global Setup**: If the user explicitly asked for global/machine-wide configuration, install into your platform's global config directory (e.g., `~/.gemini/config/`, `~/.claude/`, or `~/.agents/`).

---

## Step 2: Run the Automated Installer (Preferred if Shell Access is Available)

If you have terminal / command execution tool access:

### Case A: The repository is already cloned locally
Run:
```bash
bash ./install.sh --target <TARGET_DIR>
```
*(Or `bash ./install.sh --global` for global installation.)*

### Case B: You are reading this file remotely from GitHub
Clone the repository into a temporary directory and run `install.sh`:
```bash
git clone --depth 1 https://github.com/dongchankim-io/scientific-agent-skills.git /tmp/scientific-agent-skills
bash /tmp/scientific-agent-skills/install.sh --target <TARGET_DIR>
rm -rf /tmp/scientific-agent-skills
```

---

## Step 3: Manual File Creation Fallback (If Git/Clone is Unavailable)

If you are in a restricted sandbox without `git` network access and only have URL-fetching and file-writing tools, fetch and write the following files from `https://raw.githubusercontent.com/dongchankim-io/scientific-agent-skills/main/` into `<TARGET_DIR>`:

1. **Always-On Rules**:
   - Fetch `AGENTS.md` and write it to `<TARGET_DIR>/AGENTS.md`.
   - Also create compatibility copies or symlinks for your specific agent runtime:
     - Google Antigravity / Gemini: `<TARGET_DIR>/GEMINI.md`
     - Claude Code: `<TARGET_DIR>/CLAUDE.md`
2. **Skills (`.agents/skills/`)**:
   - Fetch and write each skill's `SKILL.md` and helper scripts into `<TARGET_DIR>/.agents/skills/` (and `<TARGET_DIR>/.claude/skills/` if running Claude Code):
     - `.agents/skills/literature-search/SKILL.md`
     - `.agents/skills/literature-search/scripts/bib_tool.py`
     - `.agents/skills/paper-summarizer/SKILL.md`
     - `.agents/skills/paper-summarizer/references/review_rubric.md`
     - `.agents/skills/academic-writing/SKILL.md`
     - `.agents/skills/academic-writing/scripts/lint_manuscript.py`
     - `.agents/skills/scientific-figures-tables/SKILL.md`
     - `.agents/skills/scientific-figures-tables/scripts/csv_to_table.py`
     - `.agents/skills/scientific-figures-tables/scripts/pub_style.mplstyle`
3. **Research Workspace Scaffolding**:
   - Create directories: `papers/`, `papers/notes/`, `manuscripts/`, `figures/`, `tables/`.
   - Copy `templates/references.bib` to `<TARGET_DIR>/references.bib` (if it does not already exist).
   - Copy `templates/synthesis_matrix.md` to `<TARGET_DIR>/papers/synthesis_matrix.md` (if it does not already exist).
   - Copy `templates/paper_note_template.md` to `<TARGET_DIR>/templates/paper_note_template.md`.

---

## Step 4: Verify the Installation

Run the following verification commands to confirm the helper tools work in the local Python 3 environment:

```bash
python3 <TARGET_DIR>/.agents/skills/literature-search/scripts/bib_tool.py --help
python3 <TARGET_DIR>/.agents/skills/academic-writing/scripts/lint_manuscript.py --help
python3 <TARGET_DIR>/.agents/skills/scientific-figures-tables/scripts/csv_to_table.py --help
```

---

## Step 5: Report Back to the User

Once setup and verification succeed, provide a concise summary to the user showing:
1. Which rules (`AGENTS.md`, `GEMINI.md`, `CLAUDE.md`) and skills (`.agents/skills/*`) were installed.
2. The workspace folders created (`papers/`, `manuscripts/`, `references.bib`).
3. Three example prompts they can run immediately (e.g., summarizing a paper by arXiv ID/PDF, searching literature and updating `references.bib`, or checking a manuscript draft).
