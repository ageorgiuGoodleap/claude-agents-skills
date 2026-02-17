# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This repository contains **agents** and **skills** for use with Claude Code. Agents are role-based AI specialists with specific expertise (Product Architect, System Architect, QA Engineer, etc.). Skills are modular, self-contained capabilities that extend Claude's functionality with specialized knowledge, workflows, and tools.

## Repository Structure

```
claude-agents-skills/
├── agents/                    # Agent definition files
│   ├── code-reviewer.md
│   ├── devops-engineer.md
│   ├── product-architect.md
│   ├── qa-engineer.md
│   ├── security-engineer.md
│   └── system-architect.md
│
├── skills/                    # Organized by role or category
│   ├── code-reviewer/        # Code review skills
│   ├── devops-engineer/      # DevOps skills
│   ├── product-architect/    # Product management skills
│   ├── qa-engineer/          # Testing and QA skills
│   ├── security-engineer/    # Security skills
│   ├── system-architect/     # Architecture skills
│   ├── useful_skills/        # General-purpose skills
│   ├── skill-creator/        # Meta-skill for creating new skills
│   └── scrips/               # Utility scripts (note: typo in directory name)
│
└── README.md
```

## Key Concepts

### Agents
Agent definition files (`.md` in `agents/`) specify role-based AI specialists with:
- Role description and trigger keywords
- Tool access permissions
- Memory configuration
- Skills they can invoke
- Output data locations
- Quality standards and workflows

Example: `agents/product-architect.md` defines a Product Architect with skills for requirements gathering, user story creation, technical specification writing, API contract design, and product roadmap planning.

### Skills
Skills are modular packages that extend Claude's capabilities. Each skill follows a standard structure:

```
skill-name/
├── SKILL.md              # Required: YAML frontmatter + markdown instructions
├── scripts/              # Optional: Executable code (Python, Bash, etc.)
├── references/           # Optional: Documentation loaded as needed
└── assets/               # Optional: Templates, images, etc. used in output
```

**SKILL.md Structure:**
- **Frontmatter (YAML)**: Contains `name` and `description` fields that determine when the skill triggers
- **Body (Markdown)**: Instructions loaded after skill triggers

**Progressive Disclosure:** Skills use a three-level loading system to manage context efficiently:
1. Metadata (name + description) - always in context
2. SKILL.md body - loaded when skill triggers
3. Bundled resources - loaded as needed by Claude

## Working with Skills

### Creating a New Skill

1. **Initialize the skill** (from `skills/skill-creator/scripts/`):
   ```bash
   python3 init_skill.py <skill-name> --path <output-directory>
   ```
   Example:
   ```bash
   python3 init_skill.py my-new-skill --path skills/useful_skills
   ```

2. **Edit the skill:**
   - Update SKILL.md with proper name and description in YAML frontmatter
   - Add instructions in markdown body
   - Add any scripts, references, or assets as needed
   - Test scripts by running them to ensure they work

3. **Package the skill** (from `skills/skill-creator/scripts/`):
   ```bash
   python3 package_skill.py <path/to/skill-folder> [output-directory]
   ```
   Example:
   ```bash
   python3 package_skill.py skills/useful_skills/my-new-skill
   ```

   This validates and packages the skill into a `.skill` file (zip format).

### Skill Design Principles

**Keep SKILL.md Concise:**
- Default assumption: Claude is already smart
- Only add context Claude doesn't have
- Target < 500 lines for SKILL.md body
- Use references/ for detailed documentation
- Challenge each piece of information: "Does Claude really need this?"

**Set Appropriate Degrees of Freedom:**
- **High freedom** (text instructions): Multiple approaches valid, context-dependent decisions
- **Medium freedom** (pseudocode/scripts with parameters): Preferred pattern exists, some variation acceptable
- **Low freedom** (specific scripts): Operations fragile/error-prone, consistency critical

**Progressive Disclosure:**
- Keep core workflow in SKILL.md
- Split variant-specific details into references/
- Use domain-specific organization for multi-domain skills
- Include clear references to when to load additional files

**Default Output Location:**
Skills that generate output should save to:
```
~/Documents/claude-code-skills-data/<skill-name>/
```

## Skill Validation

The `quick_validate.py` script (in `skills/skill-creator/scripts/`) checks:
- YAML frontmatter format and required fields
- Skill naming conventions and directory structure
- Description completeness and quality
- File organization and resource references

Validation runs automatically during packaging.

## Python Environment

All Python scripts in this repository use Python 3 and should be run with `python3`. Scripts are typically located in:
- `skills/skill-creator/scripts/` (main utilities)
- `skills/scrips/` (duplicate location - note typo)
- Individual skill `scripts/` directories

## Agent Memory

Agents use persistent memory at `~/.claude/agent-memory/<agent-name>/`:
- `MEMORY.md` is always loaded (keep < 200 lines)
- Create topic files for detailed notes
- Record patterns, learnings, and insights
- Update or remove outdated memories

## Common Tasks

**Test a skill script:**
```bash
cd skills/<category>/<skill-name>/scripts
python3 <script-name>.py [args]
```

**Validate a skill before packaging:**
```bash
cd skills/skill-creator/scripts
python3 quick_validate.py <path/to/skill>
```

**Create and package a complete skill:**
```bash
cd skills/skill-creator/scripts
python3 init_skill.py my-skill --path skills/useful_skills
# Edit the skill...
python3 package_skill.py skills/useful_skills/my-skill
```

## Architecture Notes

**Agent-Skill Relationship:**
- Agents invoke skills using slash commands (e.g., `/requirements-gathering`)
- Skills provide procedural workflows and domain expertise
- Agents have authority over their domain (e.g., Product Architect has final say on prioritization)
- Agents collaborate by delegating to other agents when needed

**Skill Categories:**
- **Role-specific skills**: Organized under role directories (code-reviewer/, qa-engineer/, etc.)
- **General-purpose skills**: Located in useful_skills/ (web-research, prompt-upgrade, feature-spec, etc.)
- **Meta-skills**: skill-creator for building new skills

**Quality Standards:**
- Agents enforce quality standards (testable requirements, story completeness, API clarity)
- Skills should be token-efficient and well-structured
- All scripts must be tested before packaging
- Documentation should be clear and unambiguous
