import { create } from 'zustand';

export interface Citation {
  id?: string;
  citation_number: number;
  source_title: string;
  authority: string;
  provision_ref?: string;
  quote_text?: string;
  source_url?: string;
  version?: string;
  effective_date?: string;
  verification_status: string;
}

export interface Confidence {
  level: string; // High, Medium, Low, Abstain
  score: number;
  source_authority_score: number;
  retrieval_relevance_score: number;
  jurisdiction_match_score: number;
  source_freshness_score: number;
  citation_grounding_score: number;
  explanation: string;
}

export interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  short_answer?: string;
  jurisdiction: string;
  domain?: string;
  confidence?: Confidence;
  citations: Citation[];
  recommended_next_steps?: string[];
  followup_suggestions?: string[];
  is_abstained?: boolean;
  abstention_reason?: string;
  created_at: string;
}

interface AppState {
  jurisdiction: 'India' | 'International';
  selectedCountry: string;
  language: 'en' | 'hi' | 'ta';
  activeConversationId: string | null;
  activeSourceDrawer: Citation | null;
  isEscalationModalOpen: boolean;
  escalationContext: {
    question?: string;
    productCategory?: string;
    aiAnalysis?: string;
  } | null;

  setJurisdiction: (j: 'India' | 'International') => void;
  setSelectedCountry: (c: string) => void;
  setLanguage: (l: 'en' | 'hi' | 'ta') => void;
  setActiveConversationId: (id: string | null) => void;
  setActiveSourceDrawer: (c: Citation | null) => void;
  setEscalationModal: (open: boolean, ctx?: any) => void;
}

export const useAppStore = create<AppState>((set) => ({
  jurisdiction: 'India',
  selectedCountry: 'USA',
  language: 'en',
  activeConversationId: null,
  activeSourceDrawer: null,
  isEscalationModalOpen: false,
  escalationContext: null,

  setJurisdiction: (j) => set({ jurisdiction: j }),
  setSelectedCountry: (c) => set({ selectedCountry: c }),
  setLanguage: (l) => set({ language: l }),
  setActiveConversationId: (id) => set({ activeConversationId: id }),
  setActiveSourceDrawer: (c) => set({ activeSourceDrawer: c }),
  setEscalationModal: (open, ctx = null) => set({ isEscalationModalOpen: open, escalationContext: ctx }),
}));
