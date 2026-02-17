# Feature Spec Skill

## Purpose

The `feature-spec` skill transforms feature requests into comprehensive, actionable technical specifications by analyzing your codebase and understanding existing patterns.

## What It Does

This skill acts as a senior technical architect to:

1. **Analyze your codebase** - Understands architectural patterns, tech stack, and conventions
2. **Ask clarifying questions** - Gathers requirements through targeted questions (5-7 max)
3. **Generate detailed specs** - Creates a `FEATURE_SPEC.md` with implementation roadmap
4. **Ground in reality** - Ensures specs follow existing patterns and are immediately actionable

## When to Use

Trigger this skill when you need to:

- Plan a new feature implementation
- Create technical specifications before coding
- Analyze requirements and scope
- Document implementation approach
- Bridge the gap between "what" (requirements) and "how" (implementation)

## How It Works

### Phase 1: Intake
The skill captures your feature request and extracts:
- Core functionality
- Constraints and preferences
- Success criteria

### Phase 2: Codebase Analysis
Explores your repository using a structured 3-step strategy:
- **Initial reconnaissance** (5 files): Tech stack, project purpose, entry points
- **Pattern discovery** (20 files): Files matching feature keywords
- **Deep dive** (up to 50 files): Integration points, test patterns, configuration
- Includes concrete search examples for consistent analysis

### Phase 3: Clarification
Asks 5-7 prioritized questions:
1. Scope boundaries (always)
2. Integration points (if multi-system)
3. Technical approach (if multiple patterns exist)
4. Edge cases (if critical)
5. Success criteria (if not implicit)
- Handles conflicts between user preferences and codebase patterns

### Phase 4: Spec Generation
Creates `FEATURE_SPEC.md` with structured metadata:
- **YAML frontmatter**: Complexity, file counts, dependencies, breaking changes
- **Feature overview**: Name, purpose, scope
- **Current state analysis**: Existing patterns, dependencies
- **Requirements**: Functional, non-functional, acceptance criteria
- **Implementation plan**: Files, sequence, testing, rollout
- **Technical decisions**: Choices, tradeoffs, alternatives
- **Verification checklist**: Implementation verification

### Phase 5: Quality Verification
Self-checks before presenting:
- Completeness (all phases executed, metadata populated)
- Specificity (concrete paths, testable requirements)
- Grounding (actual file paths, real patterns)
- Quality (verifiable criteria, explicit tradeoffs)

### Phase 6: Completion
Presents comprehensive summary with:
- Purpose and scope
- Impact metrics (files modified/created)
- Key technical decisions
- Open questions
- Next steps

### Phase 7: Iteration
Supports spec evolution:
- Surgical updates for changes (not full regeneration)
- Conflict resolution workflows
- Revision tracking
- Implementation feedback integration

## Output

The skill generates a `FEATURE_SPEC.md` file in your project root with:

- **Feature Overview**: Name, purpose, and scope
- **Current State Analysis**: Relevant code, patterns, dependencies
- **Requirements**: What must be built
- **Implementation Plan**: Files to modify/create, sequence, testing strategy
- **Technical Decisions**: Design choices and tradeoffs
- **Verification Checklist**: How to verify completion

## Example Usage

```
User: "I need to add user authentication to the app"
Claude: [Activates feature-spec skill]
        [Analyzes codebase for existing auth patterns]
        [Asks clarifying questions about auth method, scope, etc.]
        [Generates comprehensive FEATURE_SPEC.md]
```

## Constraints

- Does NOT implement code during spec creation
- Reads maximum 50 files during analysis
- Asks focused questions only
- Follows existing codebase patterns
- Avoids unrelated refactors

## Enhanced Capabilities (v2.0)

This skill now includes cutting-edge features aligned with CLAUDE.md best practices:

### Quality Assurance
- **Concrete examples**: Shows 3 example specs (simple, complex, greenfield) for consistency
- **Pre-flight checklist**: 16-point verification before presenting specs
- **Structured metadata**: Machine-readable YAML frontmatter for tooling integration

### Robust Workflows
- **Systematic search strategy**: 3-step codebase analysis with concrete examples
- **Prioritized questions**: Ordered by impact (scope → integration → approach)
- **Conflict resolution**: Handles disagreements between user preferences and codebase patterns

### Edge Case Handling
Gracefully handles 6 common edge cases:
- Empty/new codebases (greenfield projects)
- No similar patterns found
- Vague or minimal requirements
- Large scope (>50 files)
- Unanswered clarification questions
- Technical blockers

### Iterative Support
- **Surgical updates**: Modify only affected sections, not full regeneration
- **Revision tracking**: Timestamps and changelog for spec evolution
- **Implementation feedback**: Update specs based on development findings

## What Makes This Different

Unlike generic planning, this skill:
- **Grounds in your codebase**: Uses actual patterns from your code with systematic search
- **Quality-verified**: Self-checks 16 quality criteria before presenting
- **Actionable immediately**: Concrete examples show expected output quality
- **Handles edge cases**: Works in greenfield, legacy, and complex codebases
- **Supports iteration**: Specs evolve with your project, not static documents
- **Minimal questions**: 5-7 prioritized questions, not open-ended discussions

## Next Steps After Spec Creation

Once `FEATURE_SPEC.md` is created:
1. Review the specification
2. Verify the approach matches your expectations
3. Use the spec to guide implementation
4. Reference it during code review

## Structure

```
feature-spec/
└── SKILL.md              # Main skill instructions
```

This is a pure instruction-based skill with no bundled scripts, references, or assets.

## Technical Details

- **Name**: `feature-spec`
- **Version**: 2.0 (Enhanced with 100% CLAUDE.md compliance)
- **Type**: Workflow-based skill
- **Complexity**: Medium
- **Size**: 336 lines (67% of 500-line limit)
- **Output**: `FEATURE_SPEC.md` with YAML frontmatter in project root
- **Dependencies**: None (uses built-in tools: Grep, Glob, Read, AskUserQuestion)
- **Best Practices**: 10/10 CLAUDE.md patterns implemented

## License

See LICENSE.txt for complete terms.
