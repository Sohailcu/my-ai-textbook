import React, { useState, useEffect } from 'react';
import { textbookApi } from '../../services/api_client';

interface Chapter {
  id: string;
  title: string;
  chapter_number: number;
  sections: string[];
}

const Sidebar: React.FC = () => {
  const [chapters, setChapters] = useState<Chapter[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchChapters = async () => {
      try {
        setLoading(true);
        const response = await textbookApi.getChapters();
        
        if (response.success && response.data) {
          // Sort chapters by chapter number
          const sortedChapters = response.data.sort(
            (a: Chapter, b: Chapter) => a.chapter_number - b.chapter_number
          );
          setChapters(sortedChapters);
        } else {
          setError(response.error || 'Failed to fetch chapters');
        }
      } catch (err) {
        setError('An error occurred while fetching chapters');
      } finally {
        setLoading(false);
      }
    };

    fetchChapters();
  }, []);

  if (loading) {
    return <div className="sidebar">Loading navigation...</div>;
  }

  if (error) {
    return <div className="sidebar">Error: {error}</div>;
  }

  return (
    <div className="sidebar">
      <h3>Textbook Contents</h3>
      <ul style={{ listStyleType: 'none', padding: 0 }}>
        {chapters.map((chapter) => (
          <li key={chapter.id} style={{ marginBottom: '10px' }}>
            <div>
              <strong>
                {chapter.chapter_number}. {chapter.title}
              </strong>
              {chapter.sections.length > 0 && (
                <ul style={{ listStyleType: 'none', paddingLeft: '15px', marginTop: '5px' }}>
                  {chapter.sections.map((section, idx) => (
                    <li key={idx} style={{ fontSize: '0.9em', marginTop: '3px' }}>
                      • {section}
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Sidebar;