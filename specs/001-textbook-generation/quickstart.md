# Quickstart Guide: textbook-generation

## Prerequisites
- Node.js 18+ for frontend development
- Python 3.11+ for backend services
- Git for version control
- Access to OpenAI API key or open-source LLM alternative

## Setting up the Frontend (Docusaurus)

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

4. The textbook application will be available at http://localhost:3000

## Setting up the Backend (FastAPI)

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

5. Start the backend server:
```bash
uvicorn src.main:app --reload
```

6. The backend API will be available at http://localhost:8000

## Adding Textbook Content

1. Textbook chapters are stored as Markdown files in `frontend/docs/`
2. Each chapter follows the naming pattern `XX-chapter-title.md`
3. Use the Docusaurus frontmatter syntax to add metadata:
```markdown
---
title: Chapter Title
sidebar_position: 1
---
```

4. Update `frontend/sidebars.js` to include new chapters in the navigation

## Configuring the RAG Service

1. The RAG service connects to:
   - Qdrant for vector storage (set QDRANT_HOST and QDRANT_API_KEY)
   - An LLM service like OpenAI (set OPENAI_API_KEY) or open-source alternative

2. To initialize embeddings for textbook content:
```bash
cd backend
python -m src.scripts.initialize_embeddings
```

## Running Tests

### Frontend Tests
```bash
cd frontend
npm test
```

### Backend Tests
```bash
cd backend
pytest
```

## Quick Validation Steps

1. Verify backend dependencies are installed:
```bash
cd backend
pip install -r requirements.txt
```

2. Verify frontend dependencies are installed:
```bash
cd frontend
npm install
```

3. Test that the backend can start:
```bash
cd backend
uvicorn src.main:app --reload
```

## Building for Production

### Frontend Build
```bash
cd frontend
npm run build
```

### Backend Deployment
```bash
cd backend
# Use your preferred Python deployment method (Docker, server, etc.)
```

## Environment Variables

### Frontend (.env)
- `REACT_APP_API_BASE_URL`: Backend API URL

### Backend (.env)
- `OPENAI_API_KEY`: OpenAI API key (or alternative LLM service key)
- `QDRANT_HOST`: Qdrant service host
- `QDRANT_API_KEY`: Qdrant API key
- `NEON_DATABASE_URL`: Neon Postgres connection string
- `JWT_SECRET_KEY`: Secret key for JWT token generation
- `ENCRYPTION_KEY`: Key for encrypting sensitive data
- `RATE_LIMIT_REQUESTS`: Number of requests allowed per window
- `RATE_LIMIT_WINDOW`: Time window in seconds