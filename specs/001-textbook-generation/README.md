# Textbook Generation Feature

This feature implements an AI-native textbook with RAG chatbot functionality focused on Physical AI and Humanoid Robotics.

## Features

- Six comprehensive chapters covering Physical AI and Humanoid Robotics topics
- RAG chatbot that responds based only on textbook content
- Automatic sidebar navigation
- Personalization options including language selection
- Optional Urdu translation support

## Architecture

The application follows a microservices architecture with:
- Frontend: Docusaurus-based static site for textbook content and UI
- Backend: FastAPI services for RAG processing, authentication, and personalization
- Database: Neon Postgres for user data
- Vector Store: Qdrant for embeddings

## Setup

See `quickstart.md` for detailed setup instructions.

## API Endpoints

- `/api/textbook/chapters` - Retrieve all textbook chapters
- `/api/rag/query` - Submit questions to the RAG system
- `/api/auth/login` - User authentication
- `/api/user/preferences` - User preferences management

## Technologies Used

- Docusaurus for frontend
- FastAPI for backend API
- Qdrant for vector storage
- Neon for database
- React for UI components