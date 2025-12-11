# Data Model: textbook-generation

## Entity: TextbookChapter
- **Fields**:
  - id: string (unique identifier)
  - title: string (chapter title)
  - content: string (markdown content of the chapter)
  - chapter_number: integer (1-6 for the required chapters)
  - section_structure: JSON object (outline of sections in the chapter)
  - created_at: datetime
  - updated_at: datetime

## Entity: RAGQuery
- **Fields**:
  - id: string (unique identifier)
  - user_id: string (optional, for authenticated users)
  - question: string (user's question text)
  - response: string (AI-generated response based on textbook content)
  - context: string (textbook content used to generate response)
  - accuracy_confidence: float (0-1, confidence level in response accuracy)
  - timestamp: datetime
  - was_answered: boolean (whether AI provided a response based on textbook content)

## Entity: UserPreference
- **Fields**:
  - user_id: string (foreign key to user session)
  - language: string (default 'en', optional 'ur' for Urdu)
  - personalization_enabled: boolean (whether personalization features are on)
  - preferred_chapters: array of integers (order of preference for chapter recommendations)
  - last_accessed_chapter: integer (last chapter user was reading)
  - created_at: datetime
  - updated_at: datetime

## Entity: UserSession
- **Fields**:
  - session_id: string (unique identifier)
  - user_id: string (unique user identifier, null for anonymous)
  - is_authenticated: boolean (whether user has logged in)
  - created_at: datetime
  - expires_at: datetime
  - ip_address: string (for rate limiting purposes)

## Relationships
- UserSession [1] -> [0..*] RAGQuery (a session can have multiple queries)
- UserSession [1] -> [0..1] UserPreference (a session can have user preferences)
- RAGQuery -> TextbookChapter (queries are contextualized to specific chapters)

## Validation Rules
- TextbookChapter: title and content are required, chapter_number must be 1-6
- RAGQuery: question is required, response should not exceed 2000 characters
- UserPreference: user_id required if authenticated, language must be in supported list
- UserSession: session_id is required and unique

## State Transitions
- UserSession: [Active] -> [Expired] when session expires
- RAGQuery: [Created] -> [Processing] -> [Completed] -> [Rated] (optional user rating)