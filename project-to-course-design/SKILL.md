---
name: project-to-course-design
description: Use when turning an open-source project, codebase, tutorial, or technical system into a staged learning course for beginners, resume projects, interview preparation, or becoming able to build the system independently.
---

# Project To Course Design

## Core Principle

Design the course as an ability-transfer system, not as a source-code walkthrough.

Start from the final capability the learner must demonstrate, then work backward into staged milestones. Each milestone should combine concept learning, code verification, abstraction, and a concrete deliverable.

## First Step: Confirm The End Goal

Do not design the course until the final purpose is clear.

Confirm:
- Final deliverable: resume project, interview readiness, source-code mastery, extension work, open-source contribution, or internal training.
- Learner baseline: language, framework, domain, and engineering experience.
- Time budget: days, weeks, or months.
- Depth target: can use, can modify, can rebuild, can explain, or can defend in interviews.

If the answer is discoverable from the project or conversation, inspect that first instead of asking.

## Fact Boundary

Read the project before designing the path:
- README and docs define positioning and intended users.
- Directory structure reveals module boundaries.
- Type definitions, interfaces, core classes, and tests define real abstractions.
- Examples and scripts reveal the intended learning or usage path.

Do not infer protocol fields, struct fields, JSON keys, or architecture layers from natural-language nouns alone. Verify them in code or type definitions.

## Course Design Workflow

### 1. Define The Final Capability

Use this format:

```markdown
Final goal:
After the course, the learner can ...

Final artifacts:
- Runnable demo:
- Explainable architecture:
- Personal extension:
- Resume bullet:
- Interview Q&A:
```

For resume-oriented learning, require a runnable project, a personal modification, architecture explanation, technical tradeoffs, and interview defense points.

### 2. Decompose Into Milestones

Prefer ability order over repository order.

Default milestone ladder:

```markdown
Stage 0: Project positioning
Understand what problem the project solves and why it matters.

Stage 1: Minimal working loop
Run the smallest input-to-output path.

Stage 2: Core concepts
Learn only the concepts required to explain the working loop.

Stage 3: Code verification
Trace, debug, or modify the code that implements those concepts.

Stage 4: Framework understanding
Identify modules, interfaces, extension points, lifecycle, and data flow.

Stage 5: Rebuild the core
Hand-write a minimal version of the key mechanism.

Stage 6: Real project
Build or extend a complete, demonstrable application.

Stage 7: Expression and interview defense
Produce resume wording, architecture narrative, tradeoffs, and likely follow-up answers.
```

### 3. Use The Same Loop For Every Milestone

Each milestone must include:

```markdown
Milestone:

Learning objective:
What the learner can do after this node.

First-principles question:
Why does this mechanism exist? What breaks without it?

Core concepts:
Only the concepts needed for this node.

Project evidence:
Docs, files, types, functions, tests, or examples that prove the facts.

Code task:
Run, trace, modify, or rebuild a minimal example.

Advanced task:
Abstract the mechanism or apply it to a more realistic scenario.

Acceptance criteria:
How the learner proves mastery.

Common traps:
Surface-level API use, wrong abstraction boundaries, missing failure cases, or weak interview explanation.
```

### 4. Use The Wheel Pattern

Do not start with a full rewrite. Do not stop at framework calls.

Follow this sequence:

```markdown
Use the wheel:
Run the existing project or framework to build intuition.

Open the wheel:
Read the key path and understand why the modules exist.

Build a small wheel:
Reimplement the minimal mechanism by hand.

Modify the wheel:
Add a personal extension that can become a project highlight.
```

Mastery means the learner can compare the existing implementation with their simplified rebuild and explain the tradeoffs.

## Output Structure

When asked to design a course, output:

```markdown
# Project Learning Course

## 1. Final Goal
## 2. Learner Baseline And Prerequisites
## 3. Project Value
## 4. Ability Map
## 5. Stage Plan
## 6. Acceptance Criteria
## 7. Final Project Requirements
## 8. Resume And Interview Assets
## 9. Parts To Skip Or Defer
## 10. Next Action
```

## Common Mistakes

- Explaining files in repository order instead of ability order.
- Starting with too many concepts before the learner has a working loop.
- Teaching framework APIs without explaining the mechanism they hide.
- Building toy demos without moving into a real project.
- Skipping the personal extension, which makes the resume project generic.
- Ending without interview questions, tradeoffs, and failure cases.
