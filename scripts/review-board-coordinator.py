#!/usr/bin/env python3
"""
Review Board Coordinator
Orchestrates the execution review process with 5 specialist agents
"""

import sqlite3
import json
import sys
from pathlib import Path
from datetime import datetime
import uuid
import time
import subprocess
import re

class ReviewBoardCoordinator:
    def __init__(self):
        self.claude_home = Path.home() / '.claude'
        self.db_path = self.claude_home / 'data/workflow.db'
        self.templates_dir = self.claude_home / 'templates/review-board'

        # Review board composition - C-Suite Executives
        self.specialists = [
            {
                'role': 'cio',
                'agent': 'CIO',
                'name': 'Chief Information Officer',
                'checklist': 'checklists/cio-checklist.md'
            },
            {
                'role': 'cto',
                'agent': 'CTO',
                'name': 'Chief Technology Officer',
                'checklist': 'checklists/cto-checklist.md'
            },
            {
                'role': 'coo',
                'agent': 'COO',
                'name': 'Chief Operations Officer',
                'checklist': 'checklists/coo-checklist.md'
            }
        ]

    def get_workflow(self, project_name):
        """Get workflow by project name"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM workflows
            WHERE project_name = ?
        """, (project_name,))

        row = cursor.fetchone()
        conn.close()

        if row:
            return dict(row)
        return None

    def get_phase_documents(self, project_name):
        """Get paths to all phase documents"""
        projects_dir = self.claude_home / 'projects' / project_name.lower().replace(' ', '-')

        docs = {
            'vision': projects_dir / '01-vision.md',
            'mission': projects_dir / '02-mission.md',
            'execution': projects_dir / '03-execution.md'
        }

        # Validate all docs exist
        missing = [name for name, path in docs.items() if not path.exists()]
        if missing:
            raise FileNotFoundError(f"Missing phase documents: {', '.join(missing)}")

        return docs

    def create_review_session(self, workflow_id, project_name):
        """Create a new review board session"""
        session_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')

        # Create output directory
        project_dir = self.claude_home / 'projects' / project_name.lower().replace(' ', '-')
        review_dir = project_dir / 'review-board' / f'session-{timestamp}'
        review_dir.mkdir(parents=True, exist_ok=True)

        # Insert into database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        report_path = str(review_dir / 'consolidated-report.md')

        cursor.execute("""
            INSERT INTO review_board_sessions
            (id, workflow_id, session_timestamp, status, report_path)
            VALUES (?, ?, ?, 'in_progress', ?)
        """, (session_id, workflow_id, timestamp, report_path))

        conn.commit()
        conn.close()

        return session_id, review_dir

    def generate_specialist_prompt(self, specialist, docs, output_path, project_name):
        """Generate detailed prompt for a specialist"""
        checklist_path = self.templates_dir / specialist['checklist']

        if not checklist_path.exists():
            checklist_content = f"# {specialist['name']} Checklist\n\n- [ ] Review system design\n- [ ] Validate best practices"
        else:
            checklist_content = checklist_path.read_text()

        template_path = self.templates_dir / 'individual-review-template.md'
        if template_path.exists():
            template_content = template_path.read_text()
        else:
            template_content = "# Review Report\n\n## Executive Summary\n\n## Findings\n\n## Verdict"

        prompt = f"""# Review Board Assignment: {specialist['name']}

You are serving on the Review Board for project: **{project_name}**

## Your Role
{specialist['name']} - You are responsible for validating the {specialist['role']} aspects of this project.

## Documents to Review
1. Vision (Phase 1): {docs['vision']}
2. Mission (Phase 2): {docs['mission']}
3. Execution Plan (Phase 3): {docs['execution']}

## Your Checklist
{checklist_content}

## Research Requirements
You MUST research and cite official documentation:
- Anthropic documentation (docs.anthropic.com, docs.claude.com)
- GitHub repositories (1.5k+ stars for alternatives)
- Official service provider documentation
- Package registries for version validation

## Output Format
Produce a markdown report at: {output_path}

Use this structure:
{template_content}

## Quality Standards
- Every concern must have supporting research link
- Every recommendation must include example or documentation
- Blockers must cite official documentation showing why it's a blocker
- Include specific version numbers, not "latest"
- Be specific and actionable

## Time Budget
You have 15 minutes to complete this review.

Begin your review now. Read all three phase documents thoroughly, conduct your research, and produce your findings report.
"""
        return prompt

    def launch_specialist(self, specialist, docs, output_path, project_name):
        """Launch a single specialist agent"""
        prompt = self.generate_specialist_prompt(specialist, docs, output_path, project_name)

        # Save prompt to file for agent execution
        prompt_file = output_path.parent / f'{specialist["role"]}-prompt.txt'
        prompt_file.write_text(prompt)

        print(f"  ├─ 🔍 {specialist['name']} analyzing...")

        # Return launch configuration for Claude Code to execute
        return {
            'agent': specialist['agent'],
            'name': specialist['name'],
            'role': specialist['role'],
            'prompt_file': str(prompt_file),
            'output_path': str(output_path),
            'prompt': prompt
        }

    def _create_template_report(self, specialist, output_path):
        """Create a template report for testing"""
        report = f"""# {specialist['name']} Review Report

## Executive Summary
Analysis pending - specialist review in progress.

## Approvals ✅
- To be determined during review

## Concerns ⚠️
- To be determined during review

## Blockers ❌
- None identified yet

## Recommendations 💡
- To be determined during review

## Research Conducted
- Research in progress

## Final Verdict
- Status: PENDING
- Confidence: N/A
- Notes: Review template generated, awaiting specialist analysis
"""
        output_path.write_text(report)

    def aggregate_findings(self, session_dir):
        """Read all specialist reports and aggregate findings"""
        findings = []

        for specialist in self.specialists:
            report_path = session_dir / f"{specialist['role']}-review.md"

            if not report_path.exists():
                findings.append({
                    'specialist': specialist,
                    'verdict': 'INCOMPLETE',
                    'blockers': 0,
                    'concerns': 0,
                    'recommendations': 0
                })
                continue

            content = report_path.read_text()

            # Parse report to extract verdict and counts
            verdict = self._extract_verdict(content)
            blockers = len(re.findall(r'^- .*', content.split('## Blockers ❌')[1].split('##')[0], re.MULTILINE)) if '## Blockers ❌' in content else 0
            concerns = len(re.findall(r'^- .*', content.split('## Concerns ⚠️')[1].split('##')[0], re.MULTILINE)) if '## Concerns ⚠️' in content else 0
            recommendations = len(re.findall(r'^- .*', content.split('## Recommendations 💡')[1].split('##')[0], re.MULTILINE)) if '## Recommendations 💡' in content else 0

            findings.append({
                'specialist': specialist,
                'verdict': verdict,
                'blockers': blockers,
                'concerns': concerns,
                'recommendations': recommendations,
                'report_path': str(report_path)
            })

        return findings

    def _extract_verdict(self, content):
        """Extract verdict from report content"""
        if 'Status: APPROVED' in content or 'APPROVED' in content:
            if 'CONCERNS' in content or 'WITH CONCERNS' in content:
                return 'APPROVED_WITH_CONCERNS'
            return 'APPROVED'
        elif 'Status: BLOCKED' in content or 'BLOCKED' in content:
            return 'BLOCKED'
        elif 'Status: PENDING' in content:
            return 'PENDING'
        return 'APPROVED'  # Default

    def make_decision(self, findings):
        """Apply voting rules to determine final decision"""
        verdicts = [f['verdict'] for f in findings]

        # Count votes
        approved = verdicts.count('APPROVED')
        approved_with_concerns = verdicts.count('APPROVED_WITH_CONCERNS')
        blocked = verdicts.count('BLOCKED')
        incomplete = verdicts.count('INCOMPLETE') + verdicts.count('PENDING')

        # Decision rules (C-Suite: 3 executives)
        if blocked > 0:
            return 'REJECTED', 'One or more C-suite executives identified blocking issues'
        elif incomplete > 0:
            return 'INCOMPLETE', f'{incomplete} executives did not complete their review'
        elif approved == 3:
            return 'APPROVED', 'All 3 C-suite executives approved unanimously'
        elif (approved + approved_with_concerns) == 3:
            return 'APPROVED', 'C-suite approved with minor concerns to address'
        elif approved_with_concerns >= 2:
            return 'CONDITIONAL', 'Multiple concerns raised - address before proceeding'
        else:
            return 'APPROVED', 'Review passed with concerns noted'

    def generate_consolidated_report(self, findings, decision, reason, project_name, session_dir):
        """Generate final consolidated report"""
        status, _ = decision

        report = f"""# Review Board Decision - {project_name}

**Session Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**Final Decision:** {'✅ ' if status == 'APPROVED' else '⚠️ ' if status == 'CONDITIONAL' else '❌ '}{status}

**Reasoning:** {reason}

---

## Board Members

"""

        for finding in findings:
            icon = '✅' if finding['verdict'] == 'APPROVED' else '⚠️' if finding['verdict'] == 'APPROVED_WITH_CONCERNS' else '❌'
            report += f"- {icon} **{finding['specialist']['name']}** ({finding['specialist']['agent']}) - {finding['verdict']}\n"

        report += "\n---\n\n## Voting Results\n\n"

        verdicts = [f['verdict'] for f in findings]
        report += f"- APPROVED: {verdicts.count('APPROVED')}\n"
        report += f"- APPROVED WITH CONCERNS: {verdicts.count('APPROVED_WITH_CONCERNS')}\n"
        report += f"- BLOCKED: {verdicts.count('BLOCKED')}\n"
        report += f"- INCOMPLETE: {verdicts.count('INCOMPLETE') + verdicts.count('PENDING')}\n"

        report += "\n---\n\n## Summary of Findings\n\n"

        # Aggregate all blockers
        all_blockers = []
        all_concerns = []
        all_recommendations = []

        for finding in findings:
            if finding['blockers'] > 0:
                report_content = Path(finding['report_path']).read_text()
                blockers_section = report_content.split('## Blockers ❌')[1].split('##')[0] if '## Blockers ❌' in report_content else ''
                if blockers_section.strip():
                    all_blockers.append(f"### {finding['specialist']['name']}\n{blockers_section}")

            if finding['concerns'] > 0:
                report_content = Path(finding['report_path']).read_text()
                concerns_section = report_content.split('## Concerns ⚠️')[1].split('##')[0] if '## Concerns ⚠️' in report_content else ''
                if concerns_section.strip():
                    all_concerns.append(f"### {finding['specialist']['name']}\n{concerns_section}")

            if finding['recommendations'] > 0:
                report_content = Path(finding['report_path']).read_text()
                rec_section = report_content.split('## Recommendations 💡')[1].split('##')[0] if '## Recommendations 💡' in report_content else ''
                if rec_section.strip():
                    all_recommendations.append(f"### {finding['specialist']['name']}\n{rec_section}")

        if all_blockers:
            report += "### Critical Issues (Must Fix) ❌\n\n"
            report += "\n".join(all_blockers)
            report += "\n\n"

        if all_concerns:
            report += "### Concerns (Should Address) ⚠️\n\n"
            report += "\n".join(all_concerns)
            report += "\n\n"

        if all_recommendations:
            report += "### Recommendations 💡\n\n"
            report += "\n".join(all_recommendations)
            report += "\n\n"

        report += "---\n\n## Individual Reports\n\n"

        for finding in findings:
            report += f"- [{finding['specialist']['name']} Review]({Path(finding['report_path']).name})\n"

        report += f"\n---\n\n## Next Steps\n\n"

        if status == 'APPROVED':
            report += "✅ **You may proceed to Phase 4**\n\n"
            report += f"Run: `/next-phase \"{project_name}\"`\n"
        elif status == 'CONDITIONAL':
            report += "⚠️ **Address concerns before proceeding**\n\n"
            report += "After addressing concerns:\n"
            report += f"1. Run: `/review-board \"{project_name}\" --quick-check`\n"
            report += f"2. Then: `/next-phase \"{project_name}\"`\n"
        elif status == 'REJECTED':
            report += "❌ **Cannot proceed - critical issues found**\n\n"
            report += "Fix all blockers listed above, then:\n"
            report += f"1. Update the relevant phase documents\n"
            report += f"2. Run: `/review-board \"{project_name}\" --resubmit`\n"
        else:
            report += "⚠️ **Review incomplete**\n\n"
            report += "Some specialists did not complete their review. Consider re-running.\n"

        # Write consolidated report
        report_path = session_dir / 'consolidated-report.md'
        report_path.write_text(report)

        # Create symlink to latest
        latest_link = session_dir.parent / 'latest'
        if latest_link.exists():
            latest_link.unlink()
        latest_link.symlink_to(session_dir.name)

        return report_path

    def update_session_status(self, session_id, findings, decision):
        """Update database with final status"""
        status_map = {
            'APPROVED': 'approved',
            'CONDITIONAL': 'conditional',
            'REJECTED': 'rejected',
            'INCOMPLETE': 'incomplete'
        }

        final_status = status_map.get(decision[0], 'incomplete')

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Update session
        cursor.execute("""
            UPDATE review_board_sessions
            SET status = ?, final_decision = ?, completed_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (final_status, decision[0], session_id))

        # Insert findings
        for finding in findings:
            finding_id = str(uuid.uuid4())
            cursor.execute("""
                INSERT INTO review_board_findings
                (id, session_id, specialist_role, agent_name, verdict, report_path,
                 blockers_count, concerns_count, recommendations_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                finding_id,
                session_id,
                finding['specialist']['role'],
                finding['specialist']['agent'],
                finding['verdict'],
                finding.get('report_path', ''),
                finding['blockers'],
                finding['concerns'],
                finding['recommendations']
            ))

        conn.commit()
        conn.close()

    def prepare_review(self, project_name):
        """Prepare review session and return agent launch configs"""
        # Get workflow
        workflow = self.get_workflow(project_name)
        if not workflow:
            raise ValueError(f"Workflow not found for project '{project_name}'")

        # Get phase documents
        docs = self.get_phase_documents(project_name)

        # Create session
        session_id, session_dir = self.create_review_session(workflow['id'], project_name)

        # Generate launch configs for all specialists
        launch_configs = []
        for specialist in self.specialists:
            output_path = session_dir / f"{specialist['role']}-review.md"
            config = self.launch_specialist(specialist, docs, output_path, project_name)
            launch_configs.append(config)

        return {
            'session_id': session_id,
            'session_dir': str(session_dir),
            'project_name': project_name,
            'workflow_id': workflow['id'],
            'launch_configs': launch_configs
        }

    def finalize_review(self, session_id, session_dir, project_name):
        """Aggregate findings and generate final report"""
        session_dir = Path(session_dir)

        # Aggregate findings
        findings = self.aggregate_findings(session_dir)

        # Make decision
        decision, reason = self.make_decision(findings)

        # Generate consolidated report
        report_path = self.generate_consolidated_report(
            findings, (decision, reason), reason, project_name, session_dir
        )

        # Update database
        self.update_session_status(session_id, findings, (decision, reason))

        return {
            'decision': decision,
            'reason': reason,
            'findings': findings,
            'report_path': str(report_path)
        }

    def start_review(self, project_name):
        """Main entry point - start a full review board session (standalone mode)"""
        print(f"\n{'='*60}")
        print(f"  REVIEW BOARD SESSION")
        print(f"  Project: {project_name}")
        print(f"{'='*60}\n")

        try:
            # Prepare session
            setup = self.prepare_review(project_name)

            print("🔍 Starting Review Board session...")
            print(f"   Session ID: {setup['session_id']}")
            print(f"   Output: {setup['session_dir']}\n")

            # Deploy specialists (standalone - creates template reports)
            print("Deploying specialist review team:\n")
            for config in setup['launch_configs']:
                print(f"  ├─ 🔍 {config['name']} analyzing...")
                # In standalone mode, create template reports
                output_path = Path(config['output_path'])
                specialist = next(s for s in self.specialists if s['agent'] == config['agent'])
                self._create_template_report(specialist, output_path)

            print("\n✓ All specialists deployed\n")

            # Finalize review
            print("📊 Aggregating findings...\n")
            print("📝 Generating consolidated report...\n")

            result = self.finalize_review(
                setup['session_id'],
                setup['session_dir'],
                setup['project_name']
            )

            # Display results
            print(f"{'='*60}")
            print(f"  REVIEW BOARD DECISION: {result['decision']}")
            print(f"{'='*60}\n")

            print(f"Reasoning: {result['reason']}\n")

            print("Board Members:")
            for finding in result['findings']:
                icon = '✅' if finding['verdict'] == 'APPROVED' else '⚠️' if finding['verdict'] == 'APPROVED_WITH_CONCERNS' else '❌'
                print(f"  {icon} {finding['specialist']['name']} - {finding['verdict']}")

            print(f"\n📄 Full report: {result['report_path']}")

            if result['decision'] == 'APPROVED':
                print(f"\n✅ You may proceed to Phase 4")
                print(f"   Run: /next-phase \"{project_name}\"")
            elif result['decision'] == 'CONDITIONAL':
                print(f"\n⚠️  Address concerns before proceeding")
                print(f"   See report for details")
            elif result['decision'] == 'REJECTED':
                print(f"\n❌ Cannot proceed - fix blockers first")
                print(f"   See report for required changes")

            print()
            return True

        except Exception as e:
            print(f"❌ Error: {e}")
            return False

    @staticmethod
    def get_latest_review_status(workflow_id):
        """Get status of most recent review for a workflow"""
        db_path = Path.home() / '.claude/data/workflow.db'

        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT status, final_decision, report_path, completed_at
            FROM review_board_sessions
            WHERE workflow_id = ?
            ORDER BY created_at DESC
            LIMIT 1
        """, (workflow_id,))

        row = cursor.fetchone()
        conn.close()

        if row:
            return dict(row)
        return None


def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        print("Usage: review-board-coordinator.py <project-name>")
        sys.exit(1)

    project_name = sys.argv[1]

    coordinator = ReviewBoardCoordinator()
    success = coordinator.start_review(project_name)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
