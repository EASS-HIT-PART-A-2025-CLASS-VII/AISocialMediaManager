import React, { useState } from 'react';
import { Wand2, Copy, Check, RefreshCw, Save, Download } from 'lucide-react';
import { SavedPost, CaptionFormat, FormatOption } from '../types';

interface CaptionGeneratorProps {
  image: File | null;
  onSavePost: (post: SavedPost) => void;
}

const formatOptions: FormatOption[] = [
  { id: 'casual', label: 'Casual', description: 'Friendly and relaxed', color: 'bg-blue-500' },
  { id: 'formal', label: 'Formal', description: 'Professional and polished', color: 'bg-gray-700' },
  { id: 'funny', label: 'Funny', description: 'Humorous and entertaining', color: 'bg-yellow-500' },
  { id: 'trendy', label: 'Trendy', description: 'Hip and contemporary', color: 'bg-pink-500' },
  { id: 'professional', label: 'Professional', description: 'Business-focused', color: 'bg-indigo-600' },
  { id: 'inspirational', label: 'Inspirational', description: 'Motivating and uplifting', color: 'bg-green-500' }
];

const sampleCaptions: Record<CaptionFormat, string[]> = {
  casual: [
    "Just captured this amazing moment! 📸 What do you think? #life #moments #vibes",
    "Living my best life, one photo at a time ✨ #blessed #goodvibes #memories",
    "Sometimes you just have to stop and appreciate the little things 💙 #mindfulness #gratitude"
  ],
  formal: [
    "Pleased to share this moment from today's experience. Grateful for these opportunities to grow and learn. #professional #growth",
    "Reflecting on the beauty found in everyday moments and the importance of mindful observation. #reflection #mindfulness",
    "Today served as a reminder of the profound impact that simple moments can have on our perspective. #wisdom #insight"
  ],
  funny: [
    "Me pretending I know what I'm doing 😅 #FakeItTillYouMakeIt #relatable #comedy",
    "Plot twist: I have no idea what's happening here but it looks cool! 🤷‍♀️ #confused #butmakeitfashion",
    "Warning: May contain traces of awkwardness and overconfidence 😂 #authentic #reallife #funny"
  ],
  trendy: [
    "Main character energy only ✨ #ThatGirl #Aesthetic #Vibes #MainCharacter",
    "Serving looks and living dreams 💅 #BossBabe #Slay #Unbothered #Blessed",
    "POV: You're living your best life and it shows 🔥 #POV #Aesthetic #Vibes #Energy"
  ],
  professional: [
    "Celebrating another milestone in our journey toward excellence. Grateful for the opportunity to grow and learn. #business #success #growth #leadership",
    "Success is built on moments like these – dedication, focus, and unwavering commitment to our goals. #success #dedication #goals #achievement",
    "Behind every achievement lies countless hours of preparation and an unwavering belief in the vision. #hardwork #vision #success #business"
  ],
  inspirational: [
    "Every great journey begins with a single step. What step will you take today? 🌟 #inspiration #motivation #journey #dreams",
    "Dreams don't work unless you do. Keep pushing forward, beautiful souls! 💪 #motivation #dreams #hustle #believe",
    "The only impossible journey is the one you never begin. Start where you are, use what you have. ✨ #inspiration #start #believe #possible"
  ]
};

export function CaptionGenerator({ image, onSavePost }: CaptionGeneratorProps) {
  const [selectedFormat, setSelectedFormat] = useState<CaptionFormat>('casual');
  const [generatedCaption, setGeneratedCaption] = useState<string>('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [isCopied, setIsCopied] = useState(false);
  const [isSaved, setIsSaved] = useState(false);
  const [autoCopy, setAutoCopy] = useState(false);

  const generateCaption = async () => {
    if (!image) return;
    
    setIsGenerating(true);
    
    // Simulate AI processing time
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    const captions = sampleCaptions[selectedFormat];
    const randomCaption = captions[Math.floor(Math.random() * captions.length)];
    setGeneratedCaption(randomCaption);
    setIsGenerating(false);
    
    // Auto-copy if enabled
    if (autoCopy) {
      await copyToClipboard(randomCaption);
    }
  };

  const copyToClipboard = async (text?: string) => {
    const textToCopy = text || generatedCaption;
    if (textToCopy) {
      await navigator.clipboard.writeText(textToCopy);
      setIsCopied(true);
      setTimeout(() => setIsCopied(false), 2000);
    }
  };

  const regenerateCaption = () => {
    if (generatedCaption) {
      generateCaption();
    }
  };

  const savePost = async () => {
    if (!image || !generatedCaption) return;

    // Convert image to base64
    const reader = new FileReader();
    reader.onload = (e) => {
      const imageData = e.target?.result as string;
      
      const post: SavedPost = {
        id: '', // Will be set in parent component
        image: imageData,
        caption: generatedCaption,
        format: selectedFormat,
        timestamp: Date.now(),
        imageFile: image
      };
      
      onSavePost(post);
      setIsSaved(true);
      setTimeout(() => setIsSaved(false), 2000);
    };
    
    reader.readAsDataURL(image);
  };

  const downloadImage = () => {
    if (!image) return;
    
    const url = URL.createObjectURL(image);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${image.name.split('.')[0]}_with_caption.${image.name.split('.').pop()}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  if (!image) {
    return (
      <div className="text-center text-gray-500 py-12">
        <Wand2 className="w-12 h-12 mx-auto mb-4 text-gray-300" />
        <p className="text-lg">Upload an image to generate captions</p>
        <p className="text-sm mt-2">AI will analyze your image and create engaging social media captions</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Auto-copy toggle */}
      <div className="flex items-center justify-between p-4 bg-blue-50 rounded-lg">
        <div>
          <h4 className="font-medium text-gray-800">Auto-copy captions</h4>
          <p className="text-sm text-gray-600">Automatically copy generated captions to clipboard</p>
        </div>
        <label className="relative inline-flex items-center cursor-pointer">
          <input
            type="checkbox"
            checked={autoCopy}
            onChange={(e) => setAutoCopy(e.target.checked)}
            className="sr-only peer"
          />
          <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
        </label>
      </div>

      {/* Format Selection */}
      <div>
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Choose Caption Style</h3>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
          {formatOptions.map((option) => (
            <button
              key={option.id}
              onClick={() => setSelectedFormat(option.id)}
              className={`p-3 rounded-lg border-2 transition-all duration-200 text-left
                ${selectedFormat === option.id
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
                }`}
            >
              <div className="flex items-center space-x-3">
                <div className={`w-3 h-3 rounded-full ${option.color}`}></div>
                <div>
                  <div className="font-medium text-gray-800">{option.label}</div>
                  <div className="text-xs text-gray-500">{option.description}</div>
                </div>
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Generate Button */}
      <div className="text-center">
        <button
          onClick={generateCaption}
          disabled={isGenerating}
          className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 
                   disabled:from-gray-400 disabled:to-gray-500 text-white px-8 py-3 rounded-xl font-medium 
                   transition-all duration-200 transform hover:scale-105 disabled:scale-100 disabled:cursor-not-allowed
                   shadow-lg hover:shadow-xl"
        >
          {isGenerating ? (
            <div className="flex items-center space-x-2">
              <RefreshCw className="w-5 h-5 animate-spin" />
              <span>Generating Caption...</span>
            </div>
          ) : (
            <div className="flex items-center space-x-2">
              <Wand2 className="w-5 h-5" />
              <span>Generate Caption</span>
            </div>
          )}
        </button>
      </div>

      {/* Generated Caption */}
      {generatedCaption && (
        <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
          <div className="flex items-start justify-between mb-4">
            <h4 className="text-lg font-semibold text-gray-800">Generated Caption</h4>
            <div className="flex space-x-2">
              <button
                onClick={regenerateCaption}
                className="p-2 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors duration-200"
                title="Regenerate caption"
              >
                <RefreshCw className="w-4 h-4" />
              </button>
              <button
                onClick={() => copyToClipboard()}
                className="p-2 text-gray-500 hover:text-green-600 hover:bg-green-50 rounded-lg transition-colors duration-200"
                title="Copy to clipboard"
              >
                {isCopied ? <Check className="w-4 h-4 text-green-600" /> : <Copy className="w-4 h-4" />}
              </button>
              <button
                onClick={savePost}
                className="p-2 text-gray-500 hover:text-purple-600 hover:bg-purple-50 rounded-lg transition-colors duration-200"
                title="Save to preview"
              >
                {isSaved ? <Check className="w-4 h-4 text-purple-600" /> : <Save className="w-4 h-4" />}
              </button>
              <button
                onClick={downloadImage}
                className="p-2 text-gray-500 hover:text-orange-600 hover:bg-orange-50 rounded-lg transition-colors duration-200"
                title="Download image"
              >
                <Download className="w-4 h-4" />
              </button>
            </div>
          </div>
          
          <div className="bg-gray-50 rounded-lg p-4 mb-4">
            <p className="text-gray-800 leading-relaxed">{generatedCaption}</p>
          </div>
          
          <div className="flex items-center justify-between text-sm text-gray-500">
            <span>Style: <span className="font-medium capitalize">{selectedFormat}</span></span>
            <span>{generatedCaption.length} characters • {generatedCaption.split(' ').length} words</span>
          </div>

          {/* Action Buttons */}
          <div className="flex space-x-3 mt-4">
            <button
              onClick={() => copyToClipboard()}
              className={`flex-1 flex items-center justify-center space-x-2 py-2 px-4 rounded-lg font-medium transition-all duration-200 ${
                isCopied 
                  ? 'bg-green-100 text-green-700 border border-green-200' 
                  : 'bg-blue-100 text-blue-700 border border-blue-200 hover:bg-blue-200'
              }`}
            >
              {isCopied ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
              <span>{isCopied ? 'Copied!' : 'Copy Caption'}</span>
            </button>
            
            <button
              onClick={savePost}
              className={`flex-1 flex items-center justify-center space-x-2 py-2 px-4 rounded-lg font-medium transition-all duration-200 ${
                isSaved 
                  ? 'bg-purple-100 text-purple-700 border border-purple-200' 
                  : 'bg-purple-100 text-purple-700 border border-purple-200 hover:bg-purple-200'
              }`}
            >
              {isSaved ? <Check className="w-4 h-4" /> : <Save className="w-4 h-4" />}
              <span>{isSaved ? 'Saved!' : 'Save to Preview'}</span>
            </button>
          </div>
        </div>
      )}
    </div>
  );
}