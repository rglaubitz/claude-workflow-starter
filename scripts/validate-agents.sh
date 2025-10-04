#!/bin/bash
# Agent Validation Script
# Validates all agent files for correct YAML frontmatter and structure

set -e

CLAUDE_AGENTS="/Users/richardglaubitz/Projects/claude-agents"
ERRORS=0
WARNINGS=0
TOTAL=0

echo "🔍 Validating Claude Code Agents..."
echo ""

# Function to validate agent file
validate_agent() {
    local file="$1"
    local filename=$(basename "$file")
    TOTAL=$((TOTAL + 1))

    echo "Checking: $filename"

    # Check YAML frontmatter exists
    if ! grep -q "^---$" "$file"; then
        echo "  ❌ ERROR: Missing YAML frontmatter"
        ERRORS=$((ERRORS + 1))
        return
    fi

    # Extract frontmatter (skip first and last --- lines)
    frontmatter=$(awk '/^---$/{flag=!flag;next}flag' "$file" | head -n 100)

    # Check required field: name
    if ! echo "$frontmatter" | grep -q "^name:"; then
        echo "  ❌ ERROR: Missing required field: name"
        ERRORS=$((ERRORS + 1))
    fi

    # Check required field: description
    if ! echo "$frontmatter" | grep -q "^description:"; then
        echo "  ❌ ERROR: Missing required field: description"
        ERRORS=$((ERRORS + 1))
    fi

    # Check required field: tools
    if ! echo "$frontmatter" | grep -q "^tools:"; then
        echo "  ⚠️  WARNING: Missing optional field: tools (will inherit all)"
        WARNINGS=$((WARNINGS + 1))
    fi

    # Validate tool names if present
    if echo "$frontmatter" | grep -q "^tools:"; then
        tools=$(echo "$frontmatter" | grep "^tools:" | cut -d: -f2 | tr ',' '\n')

        valid_tools="Task TodoWrite Bash Read Write Edit MultiEdit Grep Glob WebSearch WebFetch NotebookEdit"

        for tool in $tools; do
            tool=$(echo "$tool" | xargs)  # Trim whitespace
            if [[ ! " $valid_tools " =~ " $tool " ]]; then
                echo "  ⚠️  WARNING: Unknown tool: $tool"
                WARNINGS=$((WARNINGS + 1))
            fi
        done
    fi

    echo "  ✅ Valid"
}

# Validate all agent files
for agent_file in "$CLAUDE_AGENTS"/**/*.md; do
    if [[ -f "$agent_file" && "$agent_file" != *"README.md" ]]; then
        validate_agent "$agent_file"
    fi
done

echo ""
echo "📊 Validation Summary"
echo "  Total agents: $TOTAL"
echo "  ✅ Passed: $((TOTAL - ERRORS))"
echo "  ❌ Errors: $ERRORS"
echo "  ⚠️  Warnings: $WARNINGS"

if [ $ERRORS -gt 0 ]; then
    echo ""
    echo "❌ VALIDATION FAILED - Fix errors before deployment"
    exit 1
else
    echo ""
    echo "✅ ALL AGENTS VALID"
    exit 0
fi
