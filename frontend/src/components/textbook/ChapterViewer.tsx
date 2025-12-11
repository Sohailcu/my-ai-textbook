import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import { textbookApi } from '../../services/api_client';

interface ChapterViewerProps {
  chapterId: string;
}

interface Chapter {
  id: string;
  title: string;
  content: string;
  chapter_number: number;
  section_structure?: string;
}

const ChapterViewer: React.FC<ChapterViewerProps> = ({ chapterId }) => {
  const [chapter, setChapter] = useState<Chapter | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchChapter = async () => {
      try {
        setLoading(true);
        const response = await textbookApi.getChapter(chapterId);
        
        if (response.success && response.data) {
          setChapter(response.data);
        } else {
          setError(response.error || 'Failed to fetch chapter');
        }
      } catch (err) {
        setError('An error occurred while fetching the chapter');
      } finally {
        setLoading(false);
      }
    };

    fetchChapter();
  }, [chapterId]);

  if (loading) {
    return <div>Loading chapter...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  if (!chapter) {
    return <div>Chapter not found</div>;
  }

  return (
    <div className="chapter-viewer">
      <h1>{chapter.title}</h1>
      <div className="chapter-content">
        <ReactMarkdown>{chapter.content}</ReactMarkdown>
      </div>
    </div>
  );
};

export default ChapterViewer;