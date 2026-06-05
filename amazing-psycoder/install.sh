#!/bin/bash
set -e

# Amazing PsyCoder — 单脚本全平台安装器
# 自动检测当前平台，或通过参数指定

detect_platform() {
    if [[ -n "$CLAUDE_CODE" ]] || [[ "$1" == "claude" ]]; then
        echo "claude"
    elif command -v codex &>/dev/null || [[ "$1" == "codex" ]]; then
        echo "codex"
    elif command -v hermes &>/dev/null || [[ "$1" == "hermes" ]]; then
        echo "hermes"
    elif [[ -d "$HOME/.openclaw" ]] || [[ "$1" == "openclaw" ]]; then
        echo "openclaw"
    elif [[ -n "$1" ]]; then
        echo "$1"
    else
        echo ""
    fi
}

PLATFORM=$(detect_platform "${1:-}")

if [[ -z "$PLATFORM" ]]; then
    echo "无法自动检测平台，请手动指定："
    echo "  ./install.sh claude"
    echo "  ./install.sh codex"
    echo "  ./install.sh hermes"
    echo "  ./install.sh openclaw"
    echo "  或直接指定路径： ./install.sh /path/to/skills"
    exit 1
fi

# 如果参数是路径，直接使用
if [[ "$PLATFORM" == /* ]]; then
    SKILLS_DIR="$PLATFORM"
else
    declare -A DIRS
    DIRS[claude]="$HOME/.claude/skills"
    DIRS[codex]="$HOME/.agents/skills"
    DIRS[hermes]="$HOME/.hermes/skills"
    DIRS[openclaw]="$HOME/.openclaw/workspace/skills"
    SKILLS_DIR="${DIRS[$PLATFORM]}"
fi

echo "平台: $PLATFORM"
echo "目录: $SKILLS_DIR"
echo ""

SKILL_ROOT="$(cd "$(dirname "$0")" && pwd)"

install_dir() {
    local src="$1"
    local name="$2"
    local dest="$SKILLS_DIR/$name"

    if [[ -d "$dest" ]]; then
        echo "  ⚠ 已存在 $name，覆盖..."
        rm -rf "$dest"
    fi

    cp -r "$src" "$dest"
    echo "  ✓ $name"
}

echo "安装 Amazing PsyCoder..."

install_dir "$SKILL_ROOT"                                      "amazing-psycoder"
install_dir "$SKILL_ROOT/psych-experiment-programming"         "psych-experiment-programming"
install_dir "$SKILL_ROOT/psych-experiment-coder"               "psych-experiment-coder"
install_dir "$SKILL_ROOT/psych-experiment-code-reviewer"       "psych-experiment-code-reviewer"

echo ""
echo "完成。输入 /amazing-psycoder 启动。"
