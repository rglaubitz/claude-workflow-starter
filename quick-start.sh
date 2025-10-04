#!/bin/bash

echo "============================================"
echo "Claude Workflow Starter - Quick Setup"
echo "============================================"
echo ""

PROJECT_NAME="$(basename "$PWD")"

echo "Project: $PROJECT_NAME"
echo ""

# Step 1: Copy project brief template
if [ ! -f "00-project-brief.md" ]; then
    echo "Step 1: Creating project brief..."
    cp templates/phases/00-project-brief-template.md 00-project-brief.md
    echo "  ✅ Created 00-project-brief.md"
else
    echo "Step 1: Project brief already exists"
    echo "  ℹ️  00-project-brief.md found"
fi

echo ""
echo "============================================"
echo "Next Steps:"
echo "============================================"
echo ""
echo "1. Edit the project brief:"
echo "   vim 00-project-brief.md"
echo ""
echo "2. Fill in:"
echo "   - Problem statement"
echo "   - Goals and success metrics"
echo "   - Must-have features"
echo "   - Constraints"
echo ""
echo "3. Start Claude Code:"
echo "   claude"
echo ""
echo "4. Initialize the workflow:"
echo "   /start-project $PROJECT_NAME"
echo ""
echo "5. Follow the 5-phase process:"
echo "   /start-vision → /approve-vision"
echo "   /start-mission → /approve-mission"
echo "   /start-execution-planning → /approve-execution-plan"
echo "   /start-review-board → /approve-review-board"
echo "   /start-implementation → /complete-implementation"
echo "   /start-testing → /approve-testing"
echo ""
echo "Ready to go! 🚀"
echo ""
