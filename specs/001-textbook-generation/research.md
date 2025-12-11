# Research Summary: textbook-generation

## Technology Choices & Rationale

### Frontend Framework: Docusaurus
- **Decision**: Use Docusaurus as the static site generator for the textbook
- **Rationale**: Docusaurus is purpose-built for documentation sites, offers excellent markdown support, automatic sidebar generation, and is extensible with custom components for the RAG chatbot
- **Alternatives considered**: 
  - Next.js with custom markdown handling
  - Gatsby
  - Hugo (less ideal for interactive features)

### Backend Framework: FastAPI
- **Decision**: Use FastAPI for the backend services
- **Rationale**: FastAPI provides automatic API documentation, strong performance, easy integration with Pydantic for data validation, and excellent support for async operations needed for RAG
- **Alternatives considered**: 
  - Flask (slower, less modern)
  - Django (overkill for this use case)
  - Node.js/Express (would introduce more language complexity)

### Vector Database: Qdrant
- **Decision**: Use Qdrant for vector storage and similarity search
- **Rationale**: Qdrant offers a free tier, excellent performance, Python SDK, and supports complex filtering needed for RAG implementation
- **Alternatives considered**: 
  - Pinecone (no free tier)
  - Weaviate (more complex setup)
  - Chroma (self-hosted option but less mature)

### Database: Neon
- **Decision**: Use Neon Postgres for storing user preferences and session data
- **Rationale**: Neon provides a generous free tier, Postgres compatibility, and serverless scaling which fits our requirements
- **Alternatives considered**: 
  - Supabase (also good but Neon specifically mentioned in requirements)
  - AWS RDS (not free tier friendly)
  - SQLite (not suitable for concurrent users)

### Textbook Content Structure
- **Decision**: Store textbook content as Markdown files in the Docusaurus docs directory
- **Rationale**: Docusaurus is designed for this approach, making content management straightforward and enabling automatic sidebar generation
- **Organization**: Each chapter will be a separate Markdown file with appropriate metadata

### RAG Implementation Approach
- **Decision**: Use LangChain framework with OpenAI API or open-source alternative for RAG functionality
- **Rationale**: LangChain provides mature tools for RAG, including document loaders, text splitters, embedding models, and LLM integration
- **Alternative models**: 
  - Open-source models (like Llama) to avoid API costs (but may impact performance)
  - Hugging Face transformers directly (more manual work)

### Authentication System
- **Decision**: Implement JWT-based authentication for personalization features only
- **Rationale**: JWT is stateless and suitable for microservice architecture, sufficient for the optional personalization features
- **Scope**: Core textbook and RAG features remain publicly accessible

## Performance & Scalability Research

### Embedding Strategy
- **Approach**: Pre-compute embeddings for textbook content during build/deployment
- **Rationale**: Reduces query time and API calls during runtime, suitable for static textbook content
- **Model**: OpenAI ada-002 or similar efficient embedding model (or open-source alternative to stay within free tier)

### Caching Considerations
- **Strategy**: Implement response caching for common RAG queries
- **Rationale**: Will reduce compute costs and improve response times for repeated questions
- **Implementation**: Could use Redis (if available in free tier) or simple in-memory caching

## Security & Privacy Notes

### Content Isolation
- **Requirement**: Ensure RAG responses only use textbook content
- **Implementation**: Use strict content filtering and retrieval mechanisms
- **Testing**: Include tests to verify responses don't contain external hallucinated content

### Embedding Security
- **Consideration**: Protect embedding endpoints from misuse
- **Approach**: Rate limiting and authentication for embedding-related endpoints

## Deployment Strategy

### Frontend Deployment
- **Platform**: GitHub Pages (free, reliable)
- **Process**: CI/CD pipeline to build and deploy Docusaurus site

### Backend Deployment
- **Platform**: Consider Railway, Render, or similar free-tier hosting
- **Alternative**: AWS Lambda/Cloudflare Workers for cost-effective scaling

## Free Tier Considerations

### API Limits
- **Monitoring**: Track API usage for embeddings and LLM calls
- **Optimization**: Batch operations where possible to reduce API calls
- **Fallback**: Have open-source alternatives ready if hitting limits