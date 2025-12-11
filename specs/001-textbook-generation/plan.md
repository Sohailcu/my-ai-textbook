# Implementation Plan: textbook-generation

**Branch**: `001-textbook-generation` | **Date**: 2025-01-01 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-textbook-generation/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

The textbook-generation feature will implement an AI-native textbook with RAG chatbot functionality, focused on Physical AI and Humanoid Robotics. The implementation follows a web application architecture with a Docusaurus frontend for textbook content and user interface, and a FastAPI backend for RAG processing, authentication, and personalization services. The system will include six chapters, a RAG chatbot that responds based only on textbook content with 80% accuracy, automatic sidebar navigation, optional Urdu translation, and personalization features requiring authentication. The architecture is designed to operate within free tier service limits while maintaining performance goals of 3-second page loads and 5-second RAG response times.

## Technical Context

**Language/Version**: JavaScript/TypeScript for frontend, Python 3.11+ for backend services
**Primary Dependencies**: Docusaurus for frontend, FastAPI for backend API, Qdrant for vector storage, Neon for database
**Storage**: Neon Postgres for user preferences and session data, file storage for textbook content and embeddings
**Testing**: pytest for backend services, Jest/React Testing Library for frontend components
**Target Platform**: Web-based application accessible via browsers, deployed on GitHub Pages with backend API
**Project Type**: Web application with frontend and backend components
**Performance Goals**: Page load under 3 seconds, RAG response time under 5 seconds for 80% of queries
**Constraints**: Must operate within free tier limits of all services (Qdrant Cloud, Neon, hosting), minimal GPU usage
**Scale/Scope**: Support for multiple concurrent users querying the RAG system, textbook content for 6 chapters

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Simplicity**: ✅ The architecture uses standard web technologies (Docusaurus, FastAPI) to keep implementation simple and accessible.

**Accuracy**: ✅ The RAG system will be designed to ensure responses are factually correct and sourced from the textbook content only.

**Minimalism**: ✅ Using Docusaurus for the UI provides a clean, lightweight interface with minimal dependencies. The architecture follows a microservice approach with distinct backend services.

**Fast builds**: ✅ Docusaurus provides fast static site generation. Backend services are designed to be lightweight and efficient.

**Free-tier architecture**: ✅ All components (Docusaurus frontend, FastAPI backend, Qdrant vector storage, Neon database) are selected to operate within free tier limits.

**RAG answers ONLY from book text**: ✅ The RAG implementation will be strictly constrained to respond only with information from the textbook content, preventing hallucinations.

## Project Structure

### Documentation (this feature)

```text
specs/001-textbook-generation/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   ├── services/
│   │   ├── rag_service.py      # RAG implementation
│   │   ├── textbook_service.py # Textbook content management
│   │   └── auth_service.py     # User authentication for personalization
│   ├── api/
│   │   ├── rag_router.py
│   │   ├── textbook_router.py
│   │   └── auth_router.py
│   └── utils/
│       ├── embedding_utils.py
│       └── text_processing.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── contract/
└── requirements.txt

frontend/
├── src/
│   ├── components/
│   │   ├── textbook/
│   │   │   ├── ChapterViewer.tsx
│   │   │   ├── TextSelection.tsx
│   │   │   └── RAGChat.tsx
│   │   ├── navigation/
│   │   │   └── Sidebar.tsx
│   │   └── personalization/
│   │       └── Settings.tsx
│   └── services/
│       ├── api_client.ts
│       └── auth_service.ts
├── docs/
│   ├── 01-intro-physical-ai.md
│   ├── 02-basics-humanoid-robotics.md
│   ├── 03-ros2-fundamentals.md
│   ├── 04-digital-twin-simulation.md
│   ├── 05-vision-language-action.md
│   └── 06-capstone.md
├── docusaurus.config.js
├── sidebars.js
└── package.json
```

**Structure Decision**: Web application with separate frontend and backend components. The frontend uses Docusaurus to manage textbook content and UI, while the backend provides APIs for RAG functionality, user authentication, and personalization features.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
