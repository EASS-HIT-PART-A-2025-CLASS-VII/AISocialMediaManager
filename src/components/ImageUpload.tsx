import React, { useCallback, useState } from 'react';
import { Upload, X, Image as ImageIcon } from 'lucide-react';

interface ImageUploadProps {
  onImageSelect: (file: File) => void;
  selectedImage: File | null;
  onRemoveImage: () => void;
}

export function ImageUpload({ onImageSelect, selectedImage, onRemoveImage }: ImageUploadProps) {
  const [isDragOver, setIsDragOver] = useState(false);
  const [imagePreview, setImagePreview] = useState<string | null>(null);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    
    const files = Array.from(e.dataTransfer.files);
    const imageFile = files.find(file => file.type.startsWith('image/'));
    
    if (imageFile) {
      onImageSelect(imageFile);
      const reader = new FileReader();
      reader.onload = (e) => {
        setImagePreview(e.target?.result as string);
      };
      reader.readAsDataURL(imageFile);
    }
  }, [onImageSelect]);

  const handleFileSelect = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file && file.type.startsWith('image/')) {
      onImageSelect(file);
      const reader = new FileReader();
      reader.onload = (e) => {
        setImagePreview(e.target?.result as string);
      };
      reader.readAsDataURL(file);
    }
  }, [onImageSelect]);

  const handleRemove = useCallback(() => {
    onRemoveImage();
    setImagePreview(null);
  }, [onRemoveImage]);

  if (selectedImage && imagePreview) {
    return (
      <div className="relative group">
        <div className="relative rounded-xl overflow-hidden bg-gray-100">
          <img
            src={imagePreview}
            alt="Selected"
            className="w-full h-64 object-cover"
          />
          <div className="absolute inset-0 bg-black bg-opacity-40 opacity-0 group-hover:opacity-100 transition-opacity duration-200 flex items-center justify-center">
            <button
              onClick={handleRemove}
              className="bg-red-500 hover:bg-red-600 text-white p-2 rounded-full transition-colors duration-200"
            >
              <X size={20} />
            </button>
          </div>
        </div>
        <div className="mt-3 text-sm text-gray-600 text-center">
          {selectedImage.name} ({(selectedImage.size / 1024 / 1024).toFixed(1)} MB)
        </div>
      </div>
    );
  }

  return (
    <div
      className={`border-2 border-dashed rounded-xl p-8 text-center transition-all duration-200 cursor-pointer
        ${isDragOver 
          ? 'border-blue-400 bg-blue-50' 
          : 'border-gray-300 hover:border-gray-400 hover:bg-gray-50'
        }`}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      onClick={() => document.getElementById('file-input')?.click()}
    >
      <input
        id="file-input"
        type="file"
        accept="image/*"
        onChange={handleFileSelect}
        className="hidden"
      />
      
      <div className="flex flex-col items-center space-y-4">
        <div className={`p-4 rounded-full transition-colors duration-200
          ${isDragOver ? 'bg-blue-100' : 'bg-gray-100'}`}>
          {isDragOver ? (
            <Upload className="w-8 h-8 text-blue-500" />
          ) : (
            <ImageIcon className="w-8 h-8 text-gray-400" />
          )}
        </div>
        
        <div>
          <p className="text-lg font-medium text-gray-700 mb-1">
            {isDragOver ? 'Drop your image here' : 'Upload an image'}
          </p>
          <p className="text-sm text-gray-500">
            Drag and drop or click to browse
          </p>
          <p className="text-xs text-gray-400 mt-2">
            Supports JPG, PNG, GIF up to 10MB
          </p>
        </div>
      </div>
    </div>
  );
}