---
id: 1
title: Create Textbook Constitution
stage: constitution
date: 2025-01-01
surface: agent
model: Qwen
feature: none
branch: main
user: Sohail
command: /sp.constitution
labels: ["constitution", "physical-ai", "humanoid-robotics"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
 - history/prompts/constitution/1-create-textbook-constitution.constitution.prompt.md
tests:
 - none
---

## Prompt

```
/sp.constitution Project Name: Physical AI & Humanoid Robotics — Essentials

Purpose:
Create a short, clean, professional AI-Native textbook based on the Physical AI & Humanoid Robotics course. 
The book must serve as a fast, simple, high-quality learning resource built with a modern Docusaurus UI 
and a fully integrated free-tier RAG chatbot.

Scope:
- 6 short chapters:
  1. Introduction to Physical AI  
  2. Basics of Humanoid Robotics  
  3. ROS 2 Fundamentals  
  4. Digital Twin Simulation (Gazebo + Isaac)  
  5. Vision-Language-Action Systems  
  6. Capstone: Simple AI-Robot Pipeline  
- Clean UI
- Free-tier friendly
- Lightweight embeddings

Core Principles:
- Simplicity  
- Accuracy  
- Minimalism  
- Fast builds  
- Free-tier architecture
- RAG answers ONLY from book text

Key Features:
- Docusaurus textbook  
- RAG chatbot (Qdrant + Neon + FastAPI)  
- Select-text → Ask AI  
- Optional Urdu / Personalize features

Constraints:
- No heavy GPU usage  
- Minimal embeddings  

Success Criteria:
- Build success  
- Accurate chatbot  
- Clean UI  
- Smooth GitHub Pages deployment  

Generate full constitution.
```

## Response snapshot

The updated constitution for the "Physical AI & Humanoid Robotics — Essentials" textbook project has been successfully created and saved to `.specify/memory/constitution.md`. 

The new constitution includes:
- Core Principles: Simplicity, Accuracy, Minimalism, Fast builds, Free-tier architecture, and RAG answers ONLY from book text
- Technology Constraints: No heavy GPU usage; Minimal embeddings; Docusaurus for UI; Qdrant + Neon + FastAPI for RAG
- Development Workflow: Select-text → Ask AI feature implementation; Smooth GitHub Pages deployment
- Governance: All PRs must verify build success and accurate chatbot functionality

All dependent templates were checked for consistency and no updates were required. The constitution document contains a Sync Impact Report at the top showing the changes made.

## Outcome

- ✅ Impact: Created initial project constitution with 6 core principles and governance structure
- 🧪 Tests: none required
- 📁 Files: Updated .specify/memory/constitution.md with new constitution content
- 🔁 Next prompts: /sp.specify to create feature specifications based on this constitution
- 🧠 Reflection: Successfully transformed user requirements into structured constitution document with proper governance

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS - All tasks completed successfully 
- Prompt variant (if applicable): Standard constitution generation prompt
- Next experiment (smallest change to try): Begin creating feature specifications based on this constitution