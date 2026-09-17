import en from "../messages/en.json";
import hi from "../messages/hi.json";
import ta from "../messages/ta.json";

export const translations = {
  en,
  hi,
  ta
};

export type Locale = keyof typeof translations;
export type TranslationKey = keyof typeof translations.en;

export function getTranslation(locale: string, key: TranslationKey): string {
  const loc = (locale in translations ? locale : "en") as Locale;
  return (translations[loc] as any)[key] || translations.en[key] || key;
}
