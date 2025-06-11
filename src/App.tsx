import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Header } from './components/Header';
import { ImageUpload } from './components/ImageUpload';
import { CaptionGenerator } from './components/CaptionGenerator';
import { InstagramPreview } from './components/InstagramPreview';
import { Footer } from './components/Footer';
import { SavedPost } from './types';

function App() {
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [savedPosts, setSavedPosts] = useState<SavedPost[]>([]);

  const handleImageSelect = (file: File) => {
    setSelectedImage(file);
  };

  const handleRemoveImage = () => {
    setSelectedImage(null);
  };

  const handleSavePost = (post: SavedPost) => {
    setSavedPosts(prev => [...prev, { ...post, id: Date.now().toString() }]);
  };

  const handleDeletePost = (id: string) => {
    setSavedPosts(prev => prev.filter(post => post.id !== id));
  };

  const handleReorderPosts = (reorderedPosts: SavedPost[]) => {
    setSavedPosts(reorderedPosts);
  };

  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
        <Header />
        
        <Routes>
          <Route path="/" element={
            <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
              <div className="space-y-8">
                {/* Hero Section */}
                <div className="text-center space-y-4">
                  <h2 className="text-3xl md:text-4xl font-bold text-gray-900">
                    Turn Your Photos Into
                    <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent"> Viral Content</span>
                  </h2>
                  <p className="text-lg text-gray-600 max-w-2xl mx-auto">
                    Upload any image and let our AI create compelling social media captions 
                    tailored to your preferred style and tone.
                  </p>
                </div>

                {/* Main Content */}
                <div className="grid lg:grid-cols-2 gap-8">
                  {/* Image Upload Section */}
                  <div className="space-y-6">
                    <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6">
                      <h3 className="text-xl font-semibold text-gray-800 mb-4">Upload Your Image</h3>
                      <ImageUpload
                        onImageSelect={handleImageSelect}
                        selectedImage={selectedImage}
                        onRemoveImage={handleRemoveImage}
                      />
                    </div>

                    {/* Features */}
                    <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6">
                      <h3 className="text-lg font-semibold text-gray-800 mb-4">Why Choose Our AI?</h3>
                      <div className="space-y-3">
                        <div className="flex items-start space-x-3">
                          <div className="w-2 h-2 bg-blue-500 rounded-full mt-2"></div>
                          <div>
                            <p className="font-medium text-gray-700">Smart Image Analysis</p>
                            <p className="text-sm text-gray-500">AI understands your image content and context</p>
                          </div>
                        </div>
                        <div className="flex items-start space-x-3">
                          <div className="w-2 h-2 bg-purple-500 rounded-full mt-2"></div>
                          <div>
                            <p className="font-medium text-gray-700">Multiple Styles</p>
                            <p className="text-sm text-gray-500">From casual to professional, we've got you covered</p>
                          </div>
                        </div>
                        <div className="flex items-start space-x-3">
                          <div className="w-2 h-2 bg-green-500 rounded-full mt-2"></div>
                          <div>
                            <p className="font-medium text-gray-700">Instagram Preview</p>
                            <p className="text-sm text-gray-500">See how your posts will look before publishing</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Caption Generation Section */}
                  <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6">
                    <h3 className="text-xl font-semibold text-gray-800 mb-6">AI Caption Generator</h3>
                    <CaptionGenerator 
                      image={selectedImage} 
                      onSavePost={handleSavePost}
                    />
                  </div>
                </div>

                {/* How It Works */}
                <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-8">
                  <h3 className="text-2xl font-bold text-gray-900 text-center mb-8">How It Works</h3>
                  <div className="grid md:grid-cols-4 gap-6">
                    <div className="text-center space-y-4">
                      <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto">
                        <span className="text-2xl font-bold text-blue-600">1</span>
                      </div>
                      <h4 className="text-lg font-semibold text-gray-800">Upload Image</h4>
                      <p className="text-gray-600">Simply drag and drop or click to upload your image</p>
                    </div>
                    <div className="text-center space-y-4">
                      <div className="bg-purple-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto">
                        <span className="text-2xl font-bold text-purple-600">2</span>
                      </div>
                      <h4 className="text-lg font-semibold text-gray-800">Choose Style</h4>
                      <p className="text-gray-600">Select your preferred caption style and tone</p>
                    </div>
                    <div className="text-center space-y-4">
                      <div className="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto">
                        <span className="text-2xl font-bold text-green-600">3</span>
                      </div>
                      <h4 className="text-lg font-semibold text-gray-800">Get Caption</h4>
                      <p className="text-gray-600">AI generates the perfect caption ready to copy and share</p>
                    </div>
                    <div className="text-center space-y-4">
                      <div className="bg-orange-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto">
                        <span className="text-2xl font-bold text-orange-600">4</span>
                      </div>
                      <h4 className="text-lg font-semibold text-gray-800">Preview & Plan</h4>
                      <p className="text-gray-600">Save posts and organize your Instagram feed</p>
                    </div>
                  </div>
                </div>
              </div>
            </main>
          } />
          
          <Route path="/preview" element={
            <InstagramPreview 
              posts={savedPosts}
              onDeletePost={handleDeletePost}
              onReorderPosts={handleReorderPosts}
            />
          } />
          
          <Route path="*" element={<Navigate to="/\" replace />} />
        </Routes>

        <Footer />
      </div>
    </Router>
  );
}

export default App;