#!/bin/bash
set -euo pipefail

# Amazing PsyCoder — validated, staged cross-platform installer

MODE="install"
SCOPE="user"
PROJECT_DIR="$(pwd)"
REQUESTED=""

usage() {
    cat <<'EOF'
Usage:
  ./install.sh [--check] claude|codex|hermes|openclaw
  ./install.sh [--check] [--scope project] [--project-dir PATH] claude|codex|openclaw
  ./install.sh [--check] /absolute/path/to/skills

Examples:
  ./install.sh claude
  ./install.sh codex
  ./install.sh hermes
  ./install.sh openclaw
  ./install.sh --scope project --project-dir /path/to/repo claude
  ./install.sh --check codex

Project scope is defined for Claude Code, Codex, and an OpenClaw agent
workspace. For a custom Hermes directory, pass its absolute skills path.
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --check)
            MODE="check"
            shift
            ;;
        --scope)
            [[ $# -ge 2 ]] || { echo "--scope 需要 user 或 project"; exit 1; }
            SCOPE="$2"
            shift 2
            ;;
        --project-dir)
            [[ $# -ge 2 ]] || { echo "--project-dir 需要路径"; exit 1; }
            PROJECT_DIR="$2"
            shift 2
            ;;
        --help|-h)
            usage
            exit 0
            ;;
        --*)
            echo "未知参数: $1"
            usage
            exit 1
            ;;
        *)
            [[ -z "$REQUESTED" ]] || { echo "只能指定一个平台或安装路径"; exit 1; }
            REQUESTED="$1"
            shift
            ;;
    esac
done

[[ "$SCOPE" == "user" || "$SCOPE" == "project" ]] || {
    echo "未知 scope: $SCOPE（仅支持 user 或 project）"
    exit 1
}

detect_platform() {
    local requested="${1:-}"
    local candidates=()

    # Explicit platform/path always wins over auto-detection.
    if [[ -n "$requested" ]]; then
        echo "$requested"
        return
    fi

    [[ -n "${CLAUDE_CODE:-}" ]] && candidates+=("claude")
    command -v codex &>/dev/null && candidates+=("codex")
    command -v hermes &>/dev/null && candidates+=("hermes")
    [[ -n "${HOME:-}" && -d "${HOME}/.openclaw" ]] && candidates+=("openclaw")

    if [[ ${#candidates[@]} -eq 1 ]]; then
        echo "${candidates[0]}"
    elif [[ ${#candidates[@]} -gt 1 ]]; then
        echo "ambiguous:${candidates[*]}"
    fi
}

PLATFORM=$(detect_platform "$REQUESTED")

if [[ "$PLATFORM" == ambiguous:* ]]; then
    echo "检测到多个宿主：${PLATFORM#ambiguous:}"
    echo "请显式指定 claude、codex、hermes 或 openclaw。"
    exit 1
fi

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
    if [[ -z "${HOME:-}" ]]; then
        echo "无法确定安装目录：HOME 环境变量未设置。请传入绝对路径。"
        exit 1
    fi
    if [[ "$SCOPE" == "project" ]]; then
        PROJECT_DIR="$(cd "$PROJECT_DIR" && pwd)"
        case "$PLATFORM" in
            claude) SKILLS_DIR="$PROJECT_DIR/.claude/skills" ;;
            codex|openclaw) SKILLS_DIR="$PROJECT_DIR/.agents/skills" ;;
            *) echo "$PLATFORM 暂不支持 --scope project；请传入绝对安装路径"; exit 1 ;;
        esac
    else
        case "$PLATFORM" in
            claude)   SKILLS_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills" ;;
            codex)    SKILLS_DIR="$HOME/.agents/skills" ;;
            hermes)   SKILLS_DIR="$HOME/.hermes/skills" ;;
            openclaw) SKILLS_DIR="$HOME/.openclaw/skills" ;;
            *)        echo "未知平台: $PLATFORM"; exit 1 ;;
        esac
    fi
fi

if [[ "$MODE" == "install" ]]; then
    mkdir -p "$SKILLS_DIR"
elif [[ ! -d "$SKILLS_DIR" ]]; then
    echo "未安装：目录不存在 $SKILLS_DIR"
    exit 1
fi

echo "平台: $PLATFORM"
echo "范围: $SCOPE"
echo "目录: $SKILLS_DIR"
echo ""

SKILL_ROOT="$(cd "$(dirname "$0")" && pwd)"
VALIDATOR_PYTHON="${PYTHON_BIN:-python3}"

if [[ "$MODE" == "install" ]]; then
    echo "验证源 skill..."
    "$VALIDATOR_PYTHON" "$SKILL_ROOT/scripts/validate_skills.py" --portable
    echo ""
fi

TX_DIR=""
TX_COMMITTED=()

rollback_transaction() {
    local index name dest backup
    set +e
    for ((index=${#TX_COMMITTED[@]}-1; index>=0; index--)); do
        name="${TX_COMMITTED[$index]}"
        dest="$SKILLS_DIR/$name"
        backup="$TX_DIR/backup/$name"
        rm -rf "$dest"
        if [[ -e "$backup" || -L "$backup" ]]; then
            mv "$backup" "$dest"
        fi
    done
    [[ -n "$TX_DIR" ]] && rm -rf "$TX_DIR"
    TX_DIR=""
    TX_COMMITTED=()
    set -e
}

trap 'status=$?; if [[ -n "$TX_DIR" ]]; then echo "安装中断；回滚整批 skill。"; rollback_transaction; fi; exit "$status"' ERR
trap 'if [[ -n "$TX_DIR" ]]; then echo "安装中断；回滚整批 skill。"; rollback_transaction; fi; exit 130' INT TERM HUP

install_all() {
    local pairs=(
        "$SKILL_ROOT|amazing-psycoder"
        "$SKILL_ROOT/psy-exp-designer|psy-exp-designer"
        "$SKILL_ROOT/psy-exp-coder|psy-exp-coder"
        "$SKILL_ROOT/psy-exp-reviewer|psy-exp-reviewer"
        "$SKILL_ROOT/psy-ana-designer|psy-ana-designer"
        "$SKILL_ROOT/psy-ana-coder|psy-ana-coder"
        "$SKILL_ROOT/psy-ana-reviewer|psy-ana-reviewer"
    )
    local pair src name dest backup

    TX_DIR=$(mktemp -d "$SKILLS_DIR/.amazing-psycoder.transaction.XXXXXX")
    mkdir -p "$TX_DIR/stage" "$TX_DIR/backup"

    # Copy every source before changing any installed skill.
    for pair in "${pairs[@]}"; do
        src="${pair%%|*}"
        name="${pair#*|}"
        mkdir "$TX_DIR/stage/$name"
        cp -R "$src"/. "$TX_DIR/stage/$name"/
    done

    # Same-filesystem moves make each replacement atomic; backups remain until all seven commit.
    for pair in "${pairs[@]}"; do
        name="${pair#*|}"
        dest="$SKILLS_DIR/$name"
        backup="$TX_DIR/backup/$name"
        if [[ -e "$dest" || -L "$dest" ]]; then
            mv "$dest" "$backup"
        fi
        if ! mv "$TX_DIR/stage/$name" "$dest"; then
            if [[ -e "$backup" || -L "$backup" ]]; then
                mv "$backup" "$dest"
            fi
            echo "  ✗ 安装失败: ${name}；回滚整批 skill"
            rollback_transaction
            return 1
        fi
        TX_COMMITTED+=("$name")
        echo "  ✓ $name"
    done

    rm -rf "$TX_DIR"
    TX_DIR=""
    TX_COMMITTED=()
}

check_dir() {
    local src="$1"
    local name="$2"
    local dest="$SKILLS_DIR/$name"
    if [[ ! -d "$dest" ]]; then
        echo "  ✗ 未安装 $name"
        return 1
    fi
    if diff -qr "$src" "$dest" >/dev/null; then
        echo "  ✓ $name 与工作区一致"
    else
        echo "  ✗ $name 已漂移或版本落后"
        return 1
    fi
}

run_for_all() {
    local action="$1"
    local status=0
    local pairs=(
        "$SKILL_ROOT|amazing-psycoder"
        "$SKILL_ROOT/psy-exp-designer|psy-exp-designer"
        "$SKILL_ROOT/psy-exp-coder|psy-exp-coder"
        "$SKILL_ROOT/psy-exp-reviewer|psy-exp-reviewer"
        "$SKILL_ROOT/psy-ana-designer|psy-ana-designer"
        "$SKILL_ROOT/psy-ana-coder|psy-ana-coder"
        "$SKILL_ROOT/psy-ana-reviewer|psy-ana-reviewer"
    )
    local pair src name
    for pair in "${pairs[@]}"; do
        src="${pair%%|*}"
        name="${pair#*|}"
        if ! "$action" "$src" "$name"; then
            status=1
            [[ "$action" == "check_dir" ]] || return 1
        fi
    done
    return "$status"
}

if [[ "$MODE" == "check" ]]; then
    echo "检查已安装 skill 与当前工作区..."
    if run_for_all check_dir; then
        echo "全部已安装 skill 与工作区一致。"
        exit 0
    fi
    echo "检测到安装漂移；确认后重新运行安装命令以同步。"
    exit 1
fi

echo "安装 Amazing PsyCoder..."

install_all

echo ""
echo "完成。启动方式（因平台而异）："
echo "  Claude Code: /amazing-psycoder"
echo "  Codex:       \$amazing-psycoder"
echo "  Hermes:      /amazing-psycoder (或自动匹配)"
echo "  OpenClaw:    /amazing-psycoder (或自动匹配)"
echo ""
echo "实验流水线: psy-exp-designer → psy-exp-coder → psy-exp-reviewer"
echo "分析流水线: psy-ana-designer → psy-ana-coder → psy-ana-reviewer"
