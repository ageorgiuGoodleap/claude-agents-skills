# Claude Agents & Skills

A comprehensive collection of specialized agents and skills for Claude Code, designed to extend Claude's capabilities across software engineering, product management, DevOps, security, QA, and system architecture.

## 📚 Table of Contents

- [Overview](#overview)
- [What's Included](#whats-included)
- [Quick Start](#quick-start)
- [Installation](#installation)
  - [Installing Skills](#installing-skills)
  - [Installing Agents](#installing-agents)
- [Using Skills](#using-skills)
- [Creating New Skills](#creating-new-skills)
- [Documentation](#documentation)
- [Repository Structure](#repository-structure)

---

## Overview

This repository contains **50 production-ready skills** and **6 specialized agents** that extend Claude Code's capabilities. Skills are modular packages that provide specialized knowledge, workflows, and tools. Agents are role-based AI specialists that leverage these skills to accomplish complex tasks.

### What's Included

- **6 Specialized Agents**:
  - Code Reviewer
  - DevOps Engineer
  - Product Architect
  - QA Engineer
  - Security Engineer
  - System Architect

- **50 Skills** across multiple categories:
  - Code Review & Quality (8 skills)
  - DevOps & Infrastructure (6 skills)
  - Product Management (5 skills)
  - Testing & QA (6 skills)
  - Security (6 skills)
  - Architecture (6 skills)
  - General Purpose (12 skills)
  - Meta Skills (1 skill)

---

## Quick Start

### 1. Browse Available Skills

Check the [SKILLS_CATALOG.md](./SKILLS_CATALOG.md) to see all 50 available skills with descriptions, trigger keywords, and usage instructions.

### 2. Install Skills You Need

All skills are pre-packaged in the `skills/zips/` directory as `.skill` files (which are zip archives). Choose the skills you want and follow the [installation instructions](#installing-skills) below.

### 3. Start Using Skills

Once installed, invoke skills using slash commands like `/code-review`, `/unit-test-implementation`, or `/api-contract-design`.

---

## Installation

### Installing Skills

Skills are distributed as `.skill` files (zip archives) located in the `skills/zips/` directory.

#### What is a .skill file?

A `.skill` file is a packaged skill in zip format that contains:
- `SKILL.md` - Skill definition with YAML frontmatter and instructions
- `scripts/` - Optional executable code (Python, Bash, etc.)
- `references/` - Optional documentation loaded as needed
- `assets/` - Optional templates, images, or boilerplate files

#### How to Install Skills in Claude Code (CLI)

**Method 1: Copy to Claude Skills Directory**

1. Create the skills directory if it doesn't exist:
   ```bash
   mkdir -p ~/.claude/skills
   ```

2. Copy the `.skill` files you want to use:
   ```bash
   cp skills/zips/code-review.skill ~/.claude/skills/
   cp skills/zips/unit-test-implementation.skill ~/.claude/skills/
   # ... copy any other skills you need
   ```

3. Restart Claude Code or reload skills:
   ```bash
   claude code
   ```

**Method 2: Install All Skills at Once**

To install all 50 skills:
```bash
cp skills/zips/*.skill ~/.claude/skills/
```

#### How to Install Skills in Claude.ai Web UI

1. Open Claude.ai in your browser
2. Navigate to **Settings** → **Skills**
3. Click **"Upload Skill"** or **"Add Skill"**
4. Select the `.skill` file(s) from the `skills/zips/` directory
5. The skill will be validated and added to your available skills
6. Invoke the skill using its slash command (e.g., `/code-review`)

**Note**: Each `.skill` file is a self-contained package that can be shared and distributed independently.

---

### Installing Agents

Agents are role-based AI specialists defined in `.md` files. They orchestrate multiple skills to accomplish complex workflows.

#### How to Install Agents

**For Claude Code (CLI):**

1. Create the agents directory:
   ```bash
   mkdir -p ~/.claude/agents
   ```

2. Copy the agent definition files you want:
   ```bash
   cp agents/code-reviewer.md ~/.claude/agents/
   cp agents/qa-engineer.md ~/.claude/agents/
   # ... copy any other agents you need
   ```

3. Agents will be available in your next Claude Code session

**For Claude.ai Web UI:**

1. Copy the content of the agent `.md` file
2. Create a new **Project** in Claude.ai
3. Paste the agent definition into the **Project Instructions**
4. Name the project after the agent (e.g., "Code Reviewer Agent")
5. The agent will now have access to its specialized skills and workflows

**Install All Agents:**
```bash
cp agents/*.md ~/.claude/agents/
```

---

## Using Skills

### Invoking Skills

Skills are invoked using slash commands:

```
/code-review              # Comprehensive code review
/unit-test-implementation # Create unit tests with high coverage
/api-contract-design      # Design OpenAPI/GraphQL specs
/security-review          # Security vulnerability analysis
/feature-spec             # Generate implementation specs
```

### Automatic Skill Triggering

Claude automatically suggests relevant skills based on context and keywords. For example:

- Mention "code review" or "PR review" → suggests `/code-review`
- Mention "unit test" or "pytest" → suggests `/unit-test-implementation`
- Mention "API contract" or "OpenAPI" → suggests `/api-contract-design`

See [SKILLS_CATALOG.md](./SKILLS_CATALOG.md) for complete list of trigger keywords for each skill.

### Using Agents

Agents provide high-level orchestration and can be invoked by:

1. **Starting a conversation in an agent project** (Claude.ai)
2. **Mentioning the agent role** in your request: "As a QA Engineer, help me design a test strategy"
3. **Referencing agent expertise**: "Review this code for security vulnerabilities" (triggers Security Engineer agent)

---

## Creating New Skills

### Step-by-Step Process

This repository includes a `skill-creator` meta-skill that guides you through creating effective skills.

#### 1. Initialize a New Skill

From the `skills/skill-creator/scripts/` directory:

```bash
cd skills/skill-creator/scripts
python3 init_skill.py <skill-name> --path <output-directory>
```

**Example:**
```bash
python3 init_skill.py my-awesome-skill --path ../../useful_skills
```

This creates:
```
my-awesome-skill/
├── SKILL.md              # Main skill definition
├── scripts/              # Optional: executable code
├── references/           # Optional: reference documentation
└── assets/               # Optional: templates, images, etc.
```

#### 2. Edit the Skill

Open `SKILL.md` and customize:

**Frontmatter (YAML)**:
```yaml
---
name: my-awesome-skill
description: |
  Clear description of what the skill does and when to use it.
  Include trigger keywords like "my feature", "awesome task", "special workflow".
---
```

**Body (Markdown)**:
- Write clear instructions for Claude
- Add workflow steps
- Include examples and patterns
- Reference any bundled resources (scripts, references, assets)

**Key Principles**:
- Keep SKILL.md concise (< 500 lines)
- Only include information Claude doesn't already know
- Use progressive disclosure (split large content into references/)
- Test any scripts you add

#### 3. Add Bundled Resources (Optional)

**Scripts** (`scripts/`):
- Add Python, Bash, or other executable code
- Use for repetitive tasks or deterministic operations
- Example: PDF manipulation, data parsing, API calls

**References** (`references/`):
- Add detailed documentation, schemas, or patterns
- Loaded only when Claude needs them
- Example: API documentation, database schemas, company policies

**Assets** (`assets/`):
- Add templates, boilerplate, images, or fonts
- Used in output, not loaded into context
- Example: HTML templates, brand logos, config files

#### 4. Package the Skill

From the `skills/skill-creator/scripts/` directory:

```bash
python3 package_skill.py <path/to/skill-folder> [output-directory]
```

**Example:**
```bash
python3 package_skill.py ../../useful_skills/my-awesome-skill ../../zips
```

This:
1. **Validates** the skill (checks YAML, structure, naming)
2. **Packages** into a `.skill` file (zip format)
3. **Saves** to the output directory (default: current directory)

The resulting `.skill` file can be:
- Shared with others
- Uploaded to Claude.ai
- Installed in `~/.claude/skills/`

#### 5. Test and Iterate

1. Install the skill: `cp my-awesome-skill.skill ~/.claude/skills/`
2. Test it in Claude Code: `/my-awesome-skill`
3. Gather feedback and iterate
4. Re-package after changes

### Skill Design Best Practices

✅ **DO:**
- Keep SKILL.md under 500 lines
- Include comprehensive trigger keywords in the description
- Test all scripts before packaging
- Use clear, imperative language
- Organize large content into references/

❌ **DON'T:**
- Repeat information Claude already knows
- Create README.md or auxiliary documentation
- Include TODO placeholders in final version
- Overuse nested references (keep one level deep)

### Validation

The packaging script automatically validates:
- ✓ YAML frontmatter format
- ✓ Required fields (name, description)
- ✓ Skill naming conventions
- ✓ Directory structure
- ✓ File organization

Manual validation:
```bash
python3 scripts/quick_validate.py <path/to/skill>
```

---

## Documentation

### Complete Guides

- **[SKILLS_CATALOG.md](./SKILLS_CATALOG.md)** - Complete catalog of all 50 skills with descriptions, trigger keywords, and usage
- **[CLAUDE.md](./CLAUDE.md)** - Repository architecture, development workflow, and technical details
- **[agents/](./agents/)** - Individual agent definitions with capabilities and workflows

### Agent Definitions

Each agent has a detailed definition file:
- `agents/code-reviewer.md` - Code quality enforcement specialist
- `agents/devops-engineer.md` - CI/CD, containers, infrastructure automation
- `agents/product-architect.md` - Requirements, specs, roadmaps
- `agents/qa-engineer.md` - Test strategy and automation
- `agents/security-engineer.md` - Security architecture and vulnerability assessment
- `agents/system-architect.md` - System design and scalability

### Skill Documentation

Each skill directory contains:
- `SKILL.md` - Main skill definition and instructions
- `README.md` - Usage examples and overview (for some skills)
- `references/` - Detailed reference documentation
- `scripts/` - Executable code with inline comments

---

## Repository Structure

```
claude-agents-skills/
├── README.md                    # This file - setup and usage guide
├── CLAUDE.md                    # Repository technical documentation
├── SKILLS_CATALOG.md            # Complete catalog of all skills
│
├── agents/                      # Agent definitions (6 agents)
│   ├── code-reviewer.md
│   ├── devops-engineer.md
│   ├── product-architect.md
│   ├── qa-engineer.md
│   ├── security-engineer.md
│   └── system-architect.md
│
├── skills/                      # Skill source directories
│   ├── code-reviewer/          # Code review skills (8 skills)
│   ├── devops-engineer/        # DevOps skills (6 skills)
│   ├── product-architect/      # Product management skills (5 skills)
│   ├── qa-engineer/            # Testing skills (6 skills)
│   ├── security-engineer/      # Security skills (6 skills)
│   ├── system-architect/       # Architecture skills (6 skills)
│   ├── useful_skills/          # General purpose skills (12 skills)
│   ├── skill-creator/          # Meta-skill for creating skills (1 skill)
│   │   └── scripts/
│   │       ├── init_skill.py       # Initialize new skill
│   │       ├── package_skill.py    # Package skill into .skill file
│   │       └── quick_validate.py   # Validate skill structure
│   │
│   └── zips/                   # Pre-packaged .skill files (50 skills)
│       ├── code-review.skill
│       ├── unit-test-implementation.skill
│       ├── api-contract-design.skill
│       └── ... (47 more)
│
└── scripts/                     # Repository utility scripts
```

---

## Examples

### Example 1: Installing Core Development Skills

```bash
# Create skills directory
mkdir -p ~/.claude/skills

# Install essential development skills
cp skills/zips/code-review.skill ~/.claude/skills/
cp skills/zips/unit-test-implementation.skill ~/.claude/skills/
cp skills/zips/feature-spec.skill ~/.claude/skills/
cp skills/zips/pr-description.skill ~/.claude/skills/

# Restart Claude Code
claude code
```

### Example 2: Setting Up QA Engineer Agent

```bash
# Install QA Engineer agent
cp agents/qa-engineer.md ~/.claude/agents/

# Install all QA skills
cp skills/zips/unit-test-implementation.skill ~/.claude/skills/
cp skills/zips/integration-test-implementation.skill ~/.claude/skills/
cp skills/zips/e2e-test-implementation.skill ~/.claude/skills/
cp skills/zips/api-test-automation.skill ~/.claude/skills/
cp skills/zips/test-strategy-design.skill ~/.claude/skills/
cp skills/zips/test-data-management.skill ~/.claude/skills/
```

### Example 3: Creating a Custom Skill

```bash
# Navigate to skill-creator
cd skills/skill-creator/scripts

# Initialize new skill
python3 init_skill.py database-migration --path ../../useful_skills

# Edit the skill
# vim ../../useful_skills/database-migration/SKILL.md

# Package the skill
python3 package_skill.py ../../useful_skills/database-migration ../../zips

# Install the skill
cp ../../zips/database-migration.skill ~/.claude/skills/
```

---

## Troubleshooting

### Skill Not Loading

1. Check skill is in `~/.claude/skills/`
2. Verify `.skill` file is not corrupted: `unzip -t skill-name.skill`
3. Check YAML frontmatter is valid
4. Restart Claude Code

### Skill Not Triggering

1. Use explicit slash command: `/skill-name`
2. Check trigger keywords in [SKILLS_CATALOG.md](./SKILLS_CATALOG.md)
3. Ensure skill description includes relevant keywords

### Packaging Fails

1. Check YAML frontmatter syntax
2. Ensure `name` and `description` fields are present
3. Run validation: `python3 quick_validate.py path/to/skill`
4. Check for special characters in file names

---

## Contributing

To contribute new skills or improvements:

1. Fork this repository
2. Create a new skill using `init_skill.py`
3. Follow skill design best practices
4. Package and test the skill
5. Submit a pull request with:
   - The skill source directory
   - The packaged `.skill` file
   - Updated SKILLS_CATALOG.md entry

---

## Support

- **Issues**: Report bugs or request features via GitHub Issues
- **Documentation**: See [CLAUDE.md](./CLAUDE.md) for technical details
- **Skill Catalog**: Browse [SKILLS_CATALOG.md](./SKILLS_CATALOG.md) for all available skills
- **Skill Creation**: Use the `/skill-creator` skill for guided skill development

---

## License

See individual skill and agent files for license information.

---

## Quick Reference

### Common Commands

```bash
# Install a skill
cp skills/zips/skill-name.skill ~/.claude/skills/

# Install an agent
cp agents/agent-name.md ~/.claude/agents/

# Create a new skill
cd skills/skill-creator/scripts
python3 init_skill.py my-skill --path ../../useful_skills

# Package a skill
python3 package_skill.py ../../useful_skills/my-skill ../../zips

# Validate a skill
python3 quick_validate.py ../../useful_skills/my-skill
```

### Key Locations

- **Skills Install**: `~/.claude/skills/`
- **Agents Install**: `~/.claude/agents/`
- **Pre-packaged Skills**: `skills/zips/`
- **Skill Creator Scripts**: `skills/skill-creator/scripts/`
- **Agent Definitions**: `agents/`

---

## What's Next?

1. **Browse** the [SKILLS_CATALOG.md](./SKILLS_CATALOG.md) to discover available skills
2. **Install** skills relevant to your workflow
3. **Try** invoking skills with slash commands like `/code-review`
4. **Create** your own custom skills using `/skill-creator`
5. **Share** your skills with the community

Happy coding with Claude! 🚀
