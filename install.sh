#!/usr/bin/env bash
# ==============================================================================
# Scientific Agent Skills Installer (install.sh)
# Configures a project workspace or global machine environment for:
# - Universal AGENTS.md + .agents/skills/ + skills/
# - Google Antigravity / Gemini (GEMINI.md + ~/.gemini/config/plugins/scientific-agent-skills)
# - Claude Code (CLAUDE.md + .claude/skills/)
# - Cursor (.cursor/rules/scientific-agent-skills.mdc) & GitHub Copilot (.github/copilot-instructions.md)
# ==============================================================================

set -euo pipefail

MODE="workspace"
TARGET_DIR="."
REPO_URL="${SCIENTIFIC_AGENT_SKILLS_REPO:-https://github.com/dongchankim-io/scientific-agent-skills.git}"

usage() {
  cat <<EOF
Usage: $(basename "$0") [OPTIONS]

Options:
  --target <dir>     Install into a specific workspace directory (default: .)
  --global           Install globally into ~/.agents, ~/.gemini/config, and ~/.claude
  --help             Show this help message
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target)
      MODE="workspace"
      TARGET_DIR="$2"
      shift 2
      ;;
    --global)
      MODE="global"
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage
      exit 1
      ;;
  esac
done

SCRIPT_SOURCE="${BASH_SOURCE[0]:-}"
CLEANUP_TMP=""

if [[ -n "$SCRIPT_SOURCE" && -f "$(dirname "$SCRIPT_SOURCE")/AGENTS.md" ]]; then
  SRC_DIR="$(cd "$(dirname "$SCRIPT_SOURCE")" && pwd)"
else
  echo "[scientific-agent-skills] Cloning skills from $REPO_URL..."
  CLEANUP_TMP="$(mktemp -d)"
  git clone --depth 1 "$REPO_URL" "$CLEANUP_TMP"
  SRC_DIR="$CLEANUP_TMP"
fi

cleanup() {
  if [[ -n "$CLEANUP_TMP" && -d "$CLEANUP_TMP" ]]; then
    rm -rf "$CLEANUP_TMP"
  fi
}
trap cleanup EXIT

install_into_workspace() {
  local dest="$1"
  mkdir -p "$dest"
  dest="$(cd "$dest" && pwd)"

  echo "[scientific-agent-skills] Configuring workspace at: $dest"

  # 1. Install universal AGENTS.md and agent-specific compatibility links
  cp "$SRC_DIR/AGENTS.md" "$dest/AGENTS.md"

  for compat_file in "GEMINI.md" "CLAUDE.md"; do
    if [[ ! -e "$dest/$compat_file" ]]; then
      ln -s "AGENTS.md" "$dest/$compat_file" 2>/dev/null || cp "$SRC_DIR/AGENTS.md" "$dest/$compat_file"
    fi
  done

  # 2. Install skills into .agents/skills/
  mkdir -p "$dest/.agents/skills"
  cp -RL "$SRC_DIR/skills/"* "$dest/.agents/skills/"
  chmod +x "$dest/.agents/skills/"*/scripts/*.py 2>/dev/null || true

  # 3. Create .claude/skills symlink for Claude Code compatibility
  mkdir -p "$dest/.claude"
  if [[ ! -e "$dest/.claude/skills" ]]; then
    ln -s "../.agents/skills" "$dest/.claude/skills" 2>/dev/null || cp -RL "$SRC_DIR/skills" "$dest/.claude/skills"
  fi

  # 4. Install Cursor & GitHub Copilot discovery files
  mkdir -p "$dest/.cursor/rules" "$dest/.github"
  cp "$SRC_DIR/.cursor/rules/scientific-agent-skills.mdc" "$dest/.cursor/rules/scientific-agent-skills.mdc"
  if [[ ! -f "$dest/.github/copilot-instructions.md" ]]; then
    cp "$SRC_DIR/.github/copilot-instructions.md" "$dest/.github/copilot-instructions.md"
  fi

  # 5. Create research directories and starter templates (non-destructive)
  mkdir -p "$dest/papers/notes" "$dest/manuscripts" "$dest/figures" "$dest/tables" "$dest/templates"
  cp "$SRC_DIR/templates/paper_note_template.md" "$dest/templates/paper_note_template.md"
  cp "$SRC_DIR/templates/synthesis_matrix.md" "$dest/templates/synthesis_matrix.md"

  if [[ ! -f "$dest/references.bib" ]]; then
    cp "$SRC_DIR/templates/references.bib" "$dest/references.bib"
  fi
  if [[ ! -f "$dest/papers/synthesis_matrix.md" ]]; then
    cp "$SRC_DIR/templates/synthesis_matrix.md" "$dest/papers/synthesis_matrix.md"
  fi

  echo "[scientific-agent-skills] Workspace configuration complete!"
  echo "  - Rules:      $dest/AGENTS.md (linked to GEMINI.md, CLAUDE.md, .cursor/rules, .github/copilot-instructions.md)"
  echo "  - Skills:     $dest/.agents/skills/ (linked to .claude/skills/)"
  echo "  - Templates:  $dest/templates/ & $dest/references.bib"
}

install_global() {
  echo "[scientific-agent-skills] Installing global scientific agent configuration..."

  # 1. Universal ~/.agents/skills
  mkdir -p "$HOME/.agents/skills"
  cp -RL "$SRC_DIR/skills/"* "$HOME/.agents/skills/"
  chmod +x "$HOME/.agents/skills/"*/scripts/*.py 2>/dev/null || true

  # 2. Google Antigravity / Gemini Plugin (~/.gemini/config/plugins/scientific-agent-skills) & Skills
  mkdir -p "$HOME/.gemini/config/skills"
  cp -RL "$SRC_DIR/skills/"* "$HOME/.gemini/config/skills/"
  chmod +x "$HOME/.gemini/config/skills/"*/scripts/*.py 2>/dev/null || true

  local agy_plugin="$HOME/.gemini/config/plugins/scientific-agent-skills"
  mkdir -p "$agy_plugin/skills" "$agy_plugin/rules" "$agy_plugin/assets"
  cp "$SRC_DIR/plugin.json" "$agy_plugin/plugin.json"
  cp "$SRC_DIR/assets/logo.svg" "$agy_plugin/assets/logo.svg"
  cp "$SRC_DIR/AGENTS.md" "$agy_plugin/rules/AGENTS.md"
  cp -RL "$SRC_DIR/skills/"* "$agy_plugin/skills/"
  chmod +x "$agy_plugin/skills/"*/scripts/*.py 2>/dev/null || true

  # 3. Claude Code (~/.claude/skills)
  mkdir -p "$HOME/.claude/skills"
  cp -RL "$SRC_DIR/skills/"* "$HOME/.claude/skills/"
  chmod +x "$HOME/.claude/skills/"*/scripts/*.py 2>/dev/null || true
  if [[ ! -f "$HOME/.claude/CLAUDE.md" ]]; then
    cp "$SRC_DIR/AGENTS.md" "$HOME/.claude/CLAUDE.md"
  fi

  echo "[scientific-agent-skills] Global installation complete!"
  echo "  - Universal skills:    ~/.agents/skills/"
  echo "  - Antigravity Plugin:  ~/.gemini/config/plugins/scientific-agent-skills/"
  echo "  - Claude Code:         ~/.claude/skills/ & ~/.claude/CLAUDE.md"
}

if [[ "$MODE" == "global" ]]; then
  install_global
else
  install_into_workspace "$TARGET_DIR"
fi
