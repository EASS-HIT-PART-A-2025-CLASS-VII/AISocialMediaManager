import React from 'react';
import { Heart, Github, Twitter } from 'lucide-react';

export function Footer() {
  return (
    <footer className="bg-gray-50 border-t border-gray-200 mt-12">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center space-y-4">
          <div className="flex items-center justify-center space-x-2 text-gray-600">
            <span>Made with</span>
            <Heart className="w-4 h-4 text-red-500" />
            <span>for content creators</span>
          </div>
          
          <div className="flex items-center justify-center space-x-6">
            <a href="#" className="text-gray-400 hover:text-gray-600 transition-colors duration-200">
              <Github className="w-5 h-5" />
            </a>
            <a href="#" className="text-gray-400 hover:text-gray-600 transition-colors duration-200">
              <Twitter className="w-5 h-5" />
            </a>
          </div>
          
          <div className="text-sm text-gray-500">
            <p>Transform your images into engaging social media content</p>
            <p className="mt-1">© 2024 AI Caption Generator. All rights reserved.</p>
          </div>
        </div>
      </div>
    </footer>
  );
}