#!/usr/bin/env bash
# ==============================================================================
# Scientific Agent Skills Installer (install.sh)
# Configures a project workspace or global machine environment for:
# - Universal AGENTS.md + .agents/skills/
# - Google Antigravity / Gemini (GEMINI.md + ~/.gemini/config/skills/)
# - Claude Code (CLAUDE.md + .claude/skills/)
# - Cursor (.cursor/rules/scientific.mdc) & GitHub Copilot
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

# Locate source directory (either local script directory or shallow git clone if piped via curl)
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

  # 1. Install universal AGENTS.md and agent-specific compatibility files
  cp "$SRC_DIR/AGENTS.md" "$dest/AGENTS.md"

  for compat_file in "GEMINI.md" "CLAUDE.md"; do
    if [[ ! -e "$dest/$compat_file" ]]; then
      ln -s "AGENTS.md" "$dest/$compat_file" 2>/dev/null || cp "$SRC_DIR/AGENTS.md" "$dest/$compat_file"
    fi
  done

  # 2. Install .agents/skills/
  mkdir -p "$dest/.agents/skills"
  cp -R "$SRC_DIR/.agents/skills/"* "$dest/.agents/skills/"
  chmod +x "$dest/.agents/skills/"*/scripts/*.py 2>/dev/null || true

  # 3. Create .claude/skills symlink for Claude Code compatibility
  mkdir -p "$dest/.claude"
  if [[ ! -e "$dest/.claude/skills" ]]; then
    ln -s "../.agents/skills" "$dest/.claude/skills" 2>/dev/null || cp -R "$SRC_DIR/.agents/skills" "$dest/.claude/skills"
  fi

  # 4. Create research directories and starter templates (non-destructive)
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
  echo "  - Rules:      $dest/AGENTS.md (linked to GEMINI.md & CLAUDE.md)"
  echo "  - Skills:     $dest/.agents/skills/ (linked to .claude/skills/)"
  echo "  - Templates:  $dest/templates/ & $dest/references.bib"
}

install_global() {
  echo "[scientific-agent-skills] Installing global scientific agent configuration..."

  # 1. Universal ~/.agents/skills
  mkdir -p "$HOME/.agents/skills"
  cp -R "$SRC_DIR/.agents/skills/"* "$HOME/.agents/skills/"
  chmod +x "$HOME/.agents/skills/"*/scripts/*.py 2>/dev/null || true

  # 2. Google Antigravity / Gemini (~/.gemini/config)
  mkdir -p "$HOME/.gemini/config/skills"
  cp -R "$SRC_DIR/.agents/skills/"* "$HOME/.gemini/config/skills/"
  if [[ ! -f "$HOME/.gemini/config/GEMINI.md" ]]; then
    cp "$SRC_DIR/AGENTS.md" "$HOME/.gemini/config/GEMINI.md"
  fi

  # 3. Claude Code (~/.claude/skills)
  mkdir -p "$HOME/.claude/skills"
  cp -R "$SRC_DIR/.agents/skills/"* "$HOME/.claude/skills/"
  if [[ ! -f "$HOME/.claude/CLAUDE.md" ]]; then
    cp "$SRC_DIR/AGENTS.md" "$HOME/.claude/CLAUDE.md"
  fi

  echo "[scientific-agent-skills] Global installation complete!"
  echo "  - Universal skills:   ~/.agents/skills/"
  echo "  - Antigravity/Gemini: ~/.gemini/config/skills/ & ~/.gemini/config/GEMINI.md"
  echo "  - Claude Code:        ~/.claude/skills/ & ~/.claude/CLAUDE.md"
}

if [[ "$MODE" == "global" ]]; then
  install_global
else
  install_into_workspace "$TARGET_DIR"
fi
