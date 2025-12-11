# Production Deployment: Textbook Generation

## Overview
This document describes how to deploy the AI-native textbook with RAG chatbot to production environments.

## Architecture
- **Frontend**: Docusaurus-based static site deployed to GitHub Pages
- **Backend**: FastAPI application deployed to Railway/Render
- **Database**: PostgreSQL (Neon or self-hosted)
- **Vector Store**: Qdrant for embeddings
- **CDN**: GitHub Pages CDN for frontend assets

## Deployment Steps

### 1. Backend Deployment (Railway/Render)

#### Option A: Using Railway

1. **Install Railway CLI (optional)**
   ```bash
   npm install -g @railway/cli
   ```

2. **Deploy to Railway**
   ```bash
   # Navigate to backend directory
   cd backend
   
   # Login to Railway (if using CLI)
   railway login
   
   # Link to Railway project
   railway init  # Create new project
   # OR
   railway link  # Link to existing project
   
   # Set environment variables
   railway var set DATABASE_URL "postgresql://username:password@host:port/dbname"
   railway var set QDRANT_HOST "your-qdrant-host"
   railway var set QDRANT_PORT "6333"
   railway var set SECRET_KEY "your-super-secret-key"
   railway var set OPENAI_API_KEY "your-openai-key"  # If using OpenAI
   
   # Deploy
   railway up
   ```

#### Option B: Using Render

1. **Create a Render account** at https://render.com

2. **Create a new Web Service**
   - Connect to your GitHub repository
   - Set the root directory to `/backend`
   - Use the Dockerfile for building
   - Set environment variables in Render dashboard

3. **Configure Environment Variables** in Render dashboard:
   - `DATABASE_URL`
   - `QDRANT_HOST`
   - `QDRANT_PORT` 
   - `SECRET_KEY`
   - `OPENAI_API_KEY` (if applicable)

### 2. Frontend Deployment (GitHub Pages)

The frontend is automatically deployed via GitHub Actions when code is pushed to the main branch.

1. **Enable GitHub Pages in your repository**
   - Go to Settings > Pages
   - Select source as "GitHub Actions"

2. **Set environment variables for the frontend**:
   - `REACT_APP_API_BASE_URL`: Your backend API URL (e.g., https://your-backend.onrender.com/api)

### 3. Database Setup

#### Option A: Using Neon (Free Tier Friendly)
1. Create a Neon account at https://neon.tech
2. Create a new project
3. Get connection string and set as `DATABASE_URL` environment variable

#### Option B: Using PostgreSQL
1. Set up PostgreSQL instance
2. Create database and user for the application
3. Set connection string as `DATABASE_URL` environment variable

### 4. Vector Store Setup (Qdrant)

#### Option A: Using Qdrant Cloud (Free Tier)
1. Sign up at https://cloud.qdrant.io
2. Get your cluster URL and API key
3. Set `QDRANT_HOST` and `QDRANT_API_KEY` environment variables

#### Option B: Self-hosted Qdrant
1. Deploy Qdrant instance
2. Configure network access
3. Set `QDRANT_HOST` environment variable

## Environment Variables

### Backend
```bash
# Database
DATABASE_URL=postgresql+asyncpg://username:password@host:port/dbname

# Qdrant Vector Store
QDRANT_HOST=your-qdrant-host
QDRANT_PORT=6333
QDRANT_API_KEY=your-api-key-if-required

# Security
SECRET_KEY=your-super-secret-key # Generate with: openssl rand -hex 32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# External Services
OPENAI_API_KEY=your-openai-api-key # If using OpenAI

# Application
ENVIRONMENT=production
```

### Frontend
```bash
# In GitHub repository settings or workflow
REACT_APP_API_BASE_URL=https://your-backend-url/api
```

## Health Checks

The backend exposes a health check endpoint at:
- `GET /health`

Expected response:
```json
{
  "status": "healthy",
  "service": "textbook-generation-api"
}
```

## Scaling Recommendations

1. **Backend**: 
   - Start with 1-2 instances
   - Monitor response times and scale based on traffic
   - Consider using a load balancer for high traffic

2. **Database**:
   - Monitor query performance
   - Add read replicas if needed
   - Implement caching for frequent queries

3. **Vector Store**:
   - Monitor search performance
   - Scale based on embedding dimensionality and query volume

## Monitoring

1. **Backend**:
   - Response times
   - Error rates
   - API usage metrics
   - Database connection pool

2. **Frontend**:
   - Page load times
   - User engagement
   - Error tracking

## Rollback Plan

1. **Backend Rollback**:
   - Keep previous deployment versions accessible
   - Use Railway/Render's version history to rollback
   - Database migrations should be reversible

2. **Frontend Rollback**:
   - GitHub Pages deployments are git-based
   - Rollback by reverting commits in main branch

## Security

1. **API Security**:
   - JWT authentication for protected endpoints
   - Rate limiting to prevent abuse
   - Input validation and sanitization

2. **Data Security**:
   - Encrypt sensitive data at rest
   - Use HTTPS for all communications
   - Regular security audits

## Troubleshooting

### Common Issues

1. **Backend not starting**:
   - Check environment variables are properly set
   - Verify database connectivity
   - Check logs for specific error messages

2. **Frontend not loading**:
   - Verify `REACT_APP_API_BASE_URL` is correct
   - Check browser console for errors
   - Verify GitHub Pages is properly configured

3. **RAG not working**:
   - Verify Qdrant connection
   - Check embedding generation
   - Verify content indexing