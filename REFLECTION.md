# Reflection: Building EcoTrack with Vibe Coding

## 1. Configuration of AI Agent Rules (.cursorrules)

The project's `.cursorrules` file defines how the AI agent behaves. It sets a senior engineer persona, a clear project philosophy (clean architecture, modularity, readability over cleverness), and explicit tech preferences: Next.js/React or Python/FastAPI for full-stack, Streamlit for rapid prototyping, TailwindCSS for styling, and RESTful APIs. The rules also include code quality guidelines (separation of concerns, meaningful names, comments for complex logic) and a workflow that favours small, iterative changes and full working files over partial implementations. Critically, the rules state the project goal: *"Build fast prototypes using AI-assisted development (Vibe Coding)."* This frames the AI as a prototyping partner rather than a generic assistant, and the "Streamlit allowed" clause makes it clear that lightweight tools are acceptable for speed.

## 2. Challenges When Delegating Coding to AI

Several challenges emerged when delegating implementation to the AI. First, **context and environment assumptions** caused friction: the README instructed `cd ecotrack` and `streamlit run app.py`, but the user's terminal was already inside `ecotrack`, and `streamlit` was not on the Windows PATH. The AI had to infer the real error (wrong working directory, missing PATH) from user reports and adjust instructions. Second, **over-specification vs. under-specification**: a broad request like "improve code quality and UI" led to many changes at once; without clear priorities, the AI had to guess what mattered most. Third, **consistency across iterations**: early versions used raw dicts; later refactors introduced dataclasses. Keeping a coherent mental model of the codebase across sessions required explicit references to architecture and modules. Finally, **tooling differences** (e.g. PowerShell vs. bash, Replit vs. local) forced repeated adjustments to commands and configuration.

## 3. From Writing Code to Orchestrating a Vision

Building EcoTrack shifted the developer's role from writing code to **orchestrating a vision**. Instead of implementing each function, the developer described the goal ("estimate CO₂ from natural language"), constraints ("Python, Streamlit, modular"), and architecture ("separate emission factors, parser, calculator, UI"). The AI produced the initial structure and implementation. The developer then steered through feedback: "fix this error," "improve UI," "ensure Replit compatibility." The value came from **articulating intent**, **reviewing outputs**, and **guiding iterations** rather than from typing code. This mirrors product ownership: defining what to build, validating that it matches the vision, and refining until it does. The trade-off is less direct control over implementation details in exchange for faster delivery and exploration of design options.

## 4. The Role of Cursor and Replit

**Cursor** acted as the primary orchestration environment. Its integration of an AI agent with the codebase (via `.cursorrules`, file context, and chat) allowed natural-language instructions to be translated into edits across multiple files. The agent could read the project structure, apply rules, and propose coherent changes. The ability to reference specific files (`@app.py`) and to iterate in conversation reduced the need for long, detailed prompts. **Replit** served as a deployment and portability target: the `requirements.txt` was adjusted for Replit compatibility, and run commands were specified for its hosting model. Replit's cloud-based, reproducible environment complemented Cursor's local, AI-assisted workflow: develop and refine locally, then deploy in a standardised environment. Together, Cursor and Replit supported a Vibe Coding loop of describe → generate → run → refine, with minimal manual setup.

---

*Word count: ~480*
