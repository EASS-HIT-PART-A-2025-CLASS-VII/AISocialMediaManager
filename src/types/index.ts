export interface SavedPost {
  id: string;
  image: string; // base64 or URL
  caption: string;
  format: string;
  timestamp: number;
  imageFile?: File;
}

export type CaptionFormat = 'casual' | 'formal' | 'funny' | 'trendy' | 'professional' | 'inspirational';

export interface FormatOption {
  id: CaptionFormat;
  label: string;
  description: string;
  color: string;
}