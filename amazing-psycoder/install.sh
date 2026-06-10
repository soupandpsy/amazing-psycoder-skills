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
    case "$PLATFORM" in
        claude)   SKILLS_DIR="$HOME/.claude/skills" ;;
        codex)    SKILLS_DIR="$HOME/.agents/skills" ;;
        hermes)   SKILLS_DIR="$HOME/.hermes/skills" ;;
        openclaw) SKILLS_DIR="$HOME/.openclaw/workspace/skills" ;;
        *)        echo "未知平台: $PLATFORM"; exit 1 ;;
    esac
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
install_dir "$SKILL_ROOT/psy-exp-designer"         "psy-exp-designer"
install_dir "$SKILL_ROOT/psy-exp-coder"               "psy-exp-coder"
install_dir "$SKILL_ROOT/psy-exp-reviewer"       "psy-exp-reviewer"
install_dir "$SKILL_ROOT/psy-ana-designer"         "psy-ana-designer"
install_dir "$SKILL_ROOT/psy-ana-coder"               "psy-ana-coder"
install_dir "$SKILL_ROOT/psy-ana-reviewer"       "psy-ana-reviewer"

echo ""
echo "完成。启动方式（因平台而异）："
echo "  Claude Code: /amazing-psycoder"
echo "  Codex:       \$amazing-psycoder"
echo "  Hermes:      /amazing-psycoder (或自动匹配)"
echo "  OpenClaw:    /amazing-psycoder (或自动匹配)"
echo ""
echo "实验流水线: psy-exp-designer → psy-exp-coder → psy-exp-reviewer"
echo "分析流水线: psy-ana-designer → psy-ana-coder → psy-ana-reviewer"
