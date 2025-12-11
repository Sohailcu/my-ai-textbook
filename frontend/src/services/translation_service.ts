// Translation service for the textbook application
// This is a simplified implementation - in a real app, you'd use a proper i18n library

interface Translations {
  [key: string]: {
    en: string;
    ur: string;
  };
}

// Mock translations - in a real application, these would come from a proper i18n system
const TRANSLATIONS: Translations = {
  'Introduction to Physical AI': {
    en: 'Introduction to Physical AI',
    ur: 'فزکل AI کا تعارف'
  },
  'Basics of Humanoid Robotics': {
    en: 'Basics of Humanoid Robotics',
    ur: 'ہیومنوائڈ روبوٹکس کی بنیادیں'
  },
  'ROS 2 Fundamentals': {
    en: 'ROS 2 Fundamentals',
    ur: 'ROS 2 کی بنیادیں'
  },
  'Digital Twin Simulation': {
    en: 'Digital Twin Simulation',
    ur: 'ڈیجیٹل ٹوئن محاکات'
  },
  'Vision-Language-Action Systems': {
    en: 'Vision-Language-Action Systems',
    ur: 'وژن-زبان-کارروائی کے نظام'
  },
  'Capstone': {
    en: 'Capstone',
    ur: 'کیپ اسٹون'
  },
  'What is Physical AI?': {
    en: 'What is Physical AI?',
    ur: 'فزکل AI کیا ہے؟'
  },
  'What are Humanoid Robots?': {
    en: 'What are Humanoid Robots?',
    ur: 'ہیومنوائڈ روبوٹس کیا ہیں؟'
  },
  'Introduction to ROS 2': {
    en: 'Introduction to ROS 2',
    ur: 'ROS 2 کا تعارف'
  },
  'Ask a question about this chapter...': {
    en: 'Ask a question about this chapter...',
    ur: 'اس باب کے بارے میں سوال کریں...'
  },
  'Loading chapter...': {
    en: 'Loading chapter...',
    ur: 'باب لوڈ ہو رہا ہے...'
  },
  'Textbook Contents': {
    en: 'Textbook Contents',
    ur: 'ٹیکسٹ بک کا مواد'
  }
};

class TranslationService {
  private currentLanguage: string = 'en';

  setLanguage(language: string): void {
    if (language === 'en' || language === 'ur') {
      this.currentLanguage = language;
    } else {
      console.warn(`Language ${language} not supported, defaulting to English`);
      this.currentLanguage = 'en';
    }
  }

  getLanguage(): string {
    return this.currentLanguage;
  }

  translate(text: string): string {
    const translation = TRANSLATIONS[text];
    if (translation && translation[this.currentLanguage]) {
      return translation[this.currentLanguage];
    }
    // If no translation is available, return the original text
    return text;
  }

  // Translate an entire text that might contain multiple translatable phrases
  translateText(text: string): string {
    // This is a simple implementation - in a real app, you might use more sophisticated parsing
    let result = text;
    
    for (const [original, translations] of Object.entries(TRANSLATIONS)) {
      if (translations[this.currentLanguage]) {
        result = result.replace(new RegExp(original, 'g'), translations[this.currentLanguage]);
      }
    }
    
    return result;
  }
}

export const translationService = new TranslationService();

// Export a hook for React components to use
export const useTranslation = () => {
  return {
    t: (text: string) => translationService.translate(text),
    currentLanguage: translationService.getLanguage(),
    setLanguage: translationService.setLanguage.bind(translationService),
    translateText: translationService.translateText.bind(translationService)
  };
};