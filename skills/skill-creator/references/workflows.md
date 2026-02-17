# Workflow Patterns

This reference provides proven patterns for designing multi-step workflows in skills.

## Sequential Workflows

For complex tasks, break operations into clear, sequential steps. It is often helpful to give Claude an overview of the process towards the beginning of SKILL.md:

```markdown
Filling a PDF form involves these steps:

1. Analyze the form (run analyze_form.py)
2. Create field mapping (edit fields.json)
3. Validate mapping (run validate_fields.py)
4. Fill the form (run fill_form.py)
5. Verify output (run verify_output.py)
```

**Real-world example from pdf skill:**
The PDF form-filling workflow uses numbered steps with specific scripts at each stage, making it crystal clear what to do and in what order.

## Conditional Workflows

For tasks with branching logic, guide Claude through decision points:

```markdown
1. Determine the modification type:
   **Creating new content?** → Follow "Creation workflow" below
   **Editing existing content?** → Follow "Editing workflow" below

2. Creation workflow: [steps]
3. Editing workflow: [steps]
```

**Real-world example from doc-coauthoring skill:**
The skill presents three stages (Context Gathering, Refinement, Reader Testing) with conditional paths based on whether the user has integrations available, wants to skip stages, or needs different artifact handling.

## Feedback Loop Pattern

For workflows requiring validation or iteration, build in explicit feedback loops:

```markdown
## Document editing process

1. Make your edits to `word/document.xml`
2. **Validate immediately**: `python scripts/validate.py unpacked_dir/`
3. If validation fails:
   - Review the error message carefully
   - Fix the issues in the XML
   - Run validation again
4. **Only proceed when validation passes**
5. Rebuild the document
```

This pattern prevents Claude from moving forward with invalid work and creates clear checkpoints.

**Real-world example from pdf skill (forms.md):**
The non-fillable form workflow has explicit validation steps with image generation and bounding box checking before proceeding to fill the form.

## Iterative Refinement Pattern

For creative or quality-critical tasks, guide Claude through multiple passes:

```markdown
## Design Process

### First Pass - Core Design
1. Create initial design based on user requirements
2. Apply design philosophy and aesthetic direction

### Second Pass - Refinement
**IMPORTANT**: The user ALREADY said "It isn't perfect enough."

CRITICAL: To refine the work, avoid adding more graphics; instead refine what has been created. Rather than adding new elements, ask: "How can I make what's already here more of a piece of art?"

Take a second pass and refine/polish to make this a masterpiece.
```

**Real-world example from canvas-design skill:**
The skill explicitly includes a "FINAL STEP" that forces a refinement pass, preventing Claude from settling for the first draft.

## Multi-Stage Workflow with User Confirmation

For complex workflows involving user input at multiple points:

```markdown
## Stage 1: Context Gathering

**Goal:** Close the gap between what you know and what Claude knows.

[Detailed stage 1 instructions]

**Exit condition:** Sufficient context gathered
**Transition:** Ask if ready to move to drafting or if more context is needed

## Stage 2: Refinement & Structure

**Goal:** Build the document section by section.

[Detailed stage 2 instructions]

**Exit condition:** All sections drafted and refined
**Transition:** Ask if ready for reader testing

## Stage 3: Reader Testing

**Goal:** Verify the output works for readers.

[Detailed stage 3 instructions]

**Exit condition:** Reader Claude answers questions correctly
```

This pattern makes long workflows manageable by creating clear stages with goals and transitions.

**Real-world example from doc-coauthoring skill:**
The three-stage workflow provides clear goals, instructions, exit conditions, and transition points between stages.

## Decision Tree Pattern

For skills with multiple paths based on initial conditions:

```markdown
## Workflow Decision Tree

**First, determine the task type:**

1. **Working with fillable PDF forms?**
   → Run `python scripts/check_fillable_fields.py <file.pdf>`
   → Follow "Fillable fields" section below

2. **Working with non-fillable PDF forms?**
   → Follow "Non-fillable fields" section below

3. **Need to create a new PDF?**
   → Follow "PDF Creation" section below

## Fillable fields
[Specific workflow for fillable forms]

## Non-fillable fields
[Specific workflow for non-fillable forms]

## PDF Creation
[Specific workflow for PDF creation]
```

**Real-world example from pdf skill (forms.md):**
The skill immediately branches based on whether the PDF has fillable fields, directing Claude to completely different workflows.

## Progressive Complexity Pattern

Start simple, add complexity only when needed:

```markdown
## Quick Start (Simple Cases)

For basic usage:
```python
[simple example]
```

## Advanced Usage (Complex Cases)

For complex scenarios requiring more control, see:
- **Complex layouts**: See [ADVANCED.md](references/ADVANCED.md)
- **Custom styling**: See [STYLING.md](references/STYLING.md)
- **Error handling**: See [ERRORS.md](references/ERRORS.md)
```

This keeps the main path simple while making advanced options discoverable.

## Best Practices for Workflows

1. **Number steps explicitly** - Makes it easy to reference specific steps
2. **Use bold for critical actions** - Draws attention to important decisions
3. **Include exit conditions** - Makes it clear when a stage is complete
4. **Add checkpoints** - Validation steps prevent cascading errors
5. **Be explicit about order** - Use words like "first", "then", "only after"
6. **Indicate optional steps** - Mark steps that can be skipped
7. **Provide escape hatches** - Let users deviate when appropriate