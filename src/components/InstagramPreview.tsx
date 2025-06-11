import React, { useState } from 'react';
import { DragDropContext, Droppable, Draggable, DropResult } from 'react-beautiful-dnd';
import { Grid3X3, List, Trash2, Copy, Heart, MessageCircle, Send, Bookmark, MoreHorizontal, User } from 'lucide-react';
import { SavedPost } from '../types';

interface InstagramPreviewProps {
  posts: SavedPost[];
  onDeletePost: (id: string) => void;
  onReorderPosts: (reorderedPosts: SavedPost[]) => void;
}

export function InstagramPreview({ posts, onDeletePost, onReorderPosts }: InstagramPreviewProps) {
  const [viewMode, setViewMode] = useState<'grid' | 'feed'>('grid');
  const [selectedPost, setSelectedPost] = useState<SavedPost | null>(null);

  const handleDragEnd = (result: DropResult) => {
    if (!result.destination) return;

    const items = Array.from(posts);
    const [reorderedItem] = items.splice(result.source.index, 1);
    items.splice(result.destination.index, 0, reorderedItem);

    onReorderPosts(items);
  };

  const copyCaption = async (caption: string) => {
    await navigator.clipboard.writeText(caption);
  };

  const formatDate = (timestamp: number) => {
    return new Date(timestamp).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    });
  };

  if (posts.length === 0) {
    return (
      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center py-16">
          <Grid3X3 className="w-16 h-16 mx-auto mb-4 text-gray-300" />
          <h2 className="text-2xl font-bold text-gray-900 mb-2">No Posts Yet</h2>
          <p className="text-gray-600 mb-6">Start by generating some captions and saving them to see your Instagram preview</p>
          <a
            href="/"
            className="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-6 py-3 rounded-lg font-medium hover:from-blue-600 hover:to-purple-700 transition-all duration-200"
          >
            Generate Your First Caption
          </a>
        </div>
      </main>
    );
  }

  return (
    <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Instagram Preview</h1>
          <p className="text-gray-600 mt-1">Organize and preview your posts before publishing</p>
        </div>
        
        <div className="flex items-center space-x-4">
          <div className="bg-white rounded-lg border border-gray-200 p-1 flex">
            <button
              onClick={() => setViewMode('grid')}
              className={`p-2 rounded-md transition-colors duration-200 ${
                viewMode === 'grid' ? 'bg-blue-100 text-blue-600' : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              <Grid3X3 className="w-5 h-5" />
            </button>
            <button
              onClick={() => setViewMode('feed')}
              className={`p-2 rounded-md transition-colors duration-200 ${
                viewMode === 'feed' ? 'bg-blue-100 text-blue-600' : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              <List className="w-5 h-5" />
            </button>
          </div>
          
          <div className="text-sm text-gray-500">
            {posts.length} post{posts.length !== 1 ? 's' : ''} saved
          </div>
        </div>
      </div>

      {/* Grid View */}
      {viewMode === 'grid' && (
        <DragDropContext onDragEnd={handleDragEnd}>
          <Droppable droppableId="instagram-grid" direction="horizontal">
            {(provided) => (
              <div
                {...provided.droppableProps}
                ref={provided.innerRef}
                className="grid grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-2 md:gap-4"
              >
                {posts.map((post, index) => (
                  <Draggable key={post.id} draggableId={post.id} index={index}>
                    {(provided, snapshot) => (
                      <div
                        ref={provided.innerRef}
                        {...provided.draggableProps}
                        {...provided.dragHandleProps}
                        className={`group relative aspect-square bg-gray-100 rounded-lg overflow-hidden cursor-pointer transition-all duration-200 ${
                          snapshot.isDragging ? 'shadow-2xl scale-105 rotate-2' : 'hover:shadow-lg'
                        }`}
                        onClick={() => setSelectedPost(post)}
                      >
                        <img
                          src={post.image}
                          alt="Post preview"
                          className="w-full h-full object-cover"
                        />
                        <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-40 transition-all duration-200 flex items-center justify-center">
                          <div className="opacity-0 group-hover:opacity-100 transition-opacity duration-200 flex space-x-4 text-white">
                            <div className="flex items-center space-x-1">
                              <Heart className="w-5 h-5" />
                              <span className="text-sm font-medium">0</span>
                            </div>
                            <div className="flex items-center space-x-1">
                              <MessageCircle className="w-5 h-5" />
                              <span className="text-sm font-medium">0</span>
                            </div>
                          </div>
                        </div>
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            onDeletePost(post.id);
                          }}
                          className="absolute top-2 right-2 p-1 bg-red-500 text-white rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-200 hover:bg-red-600"
                        >
                          <Trash2 className="w-3 h-3" />
                        </button>
                        <div className="absolute bottom-2 left-2 bg-black bg-opacity-70 text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                          {post.format}
                        </div>
                      </div>
                    )}
                  </Draggable>
                ))}
                {provided.placeholder}
              </div>
            )}
          </Droppable>
        </DragDropContext>
      )}

      {/* Feed View */}
      {viewMode === 'feed' && (
        <div className="max-w-md mx-auto space-y-8">
          {posts.map((post) => (
            <div key={post.id} className="bg-white border border-gray-200 rounded-2xl overflow-hidden shadow-sm">
              {/* Post Header */}
              <div className="flex items-center justify-between p-4">
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                    <User className="w-4 h-4 text-white" />
                  </div>
                  <div>
                    <p className="font-semibold text-gray-900">your_username</p>
                    <p className="text-xs text-gray-500">{formatDate(post.timestamp)}</p>
                  </div>
                </div>
                <button className="p-2 hover:bg-gray-100 rounded-full transition-colors duration-200">
                  <MoreHorizontal className="w-5 h-5 text-gray-600" />
                </button>
              </div>

              {/* Post Image */}
              <div className="aspect-square bg-gray-100">
                <img
                  src={post.image}
                  alt="Post"
                  className="w-full h-full object-cover"
                />
              </div>

              {/* Post Actions */}
              <div className="p-4">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center space-x-4">
                    <button className="hover:text-red-500 transition-colors duration-200">
                      <Heart className="w-6 h-6" />
                    </button>
                    <button className="hover:text-blue-500 transition-colors duration-200">
                      <MessageCircle className="w-6 h-6" />
                    </button>
                    <button className="hover:text-blue-500 transition-colors duration-200">
                      <Send className="w-6 h-6" />
                    </button>
                  </div>
                  <button className="hover:text-gray-700 transition-colors duration-200">
                    <Bookmark className="w-6 h-6" />
                  </button>
                </div>

                <p className="font-semibold text-sm text-gray-900 mb-2">0 likes</p>

                {/* Caption */}
                <div className="space-y-2">
                  <p className="text-sm text-gray-900">
                    <span className="font-semibold">your_username</span> {post.caption}
                  </p>
                  <div className="flex items-center justify-between">
                    <p className="text-xs text-gray-500 uppercase tracking-wide">
                      {post.format} style
                    </p>
                    <button
                      onClick={() => copyCaption(post.caption)}
                      className="flex items-center space-x-1 text-xs text-blue-600 hover:text-blue-700 transition-colors duration-200"
                    >
                      <Copy className="w-3 h-3" />
                      <span>Copy</span>
                    </button>
                  </div>
                </div>

                <button
                  onClick={() => onDeletePost(post.id)}
                  className="mt-3 flex items-center space-x-1 text-xs text-red-600 hover:text-red-700 transition-colors duration-200"
                >
                  <Trash2 className="w-3 h-3" />
                  <span>Delete Post</span>
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Post Detail Modal */}
      {selectedPost && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-xl font-bold text-gray-900">Post Details</h3>
                <button
                  onClick={() => setSelectedPost(null)}
                  className="p-2 hover:bg-gray-100 rounded-full transition-colors duration-200"
                >
                  <Trash2 className="w-5 h-5 text-gray-600" />
                </button>
              </div>
              
              <div className="space-y-4">
                <img
                  src={selectedPost.image}
                  alt="Post detail"
                  className="w-full aspect-square object-cover rounded-lg"
                />
                
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-gray-700">Caption Style:</span>
                    <span className="text-sm text-gray-600 capitalize">{selectedPost.format}</span>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-gray-700">Created:</span>
                    <span className="text-sm text-gray-600">{formatDate(selectedPost.timestamp)}</span>
                  </div>
                  
                  <div>
                    <span className="text-sm font-medium text-gray-700 block mb-2">Caption:</span>
                    <div className="bg-gray-50 rounded-lg p-3">
                      <p className="text-sm text-gray-800 leading-relaxed">{selectedPost.caption}</p>
                    </div>
                  </div>
                  
                  <div className="flex space-x-3">
                    <button
                      onClick={() => copyCaption(selectedPost.caption)}
                      className="flex-1 flex items-center justify-center space-x-2 py-2 px-4 bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200 transition-colors duration-200"
                    >
                      <Copy className="w-4 h-4" />
                      <span>Copy Caption</span>
                    </button>
                    
                    <button
                      onClick={() => {
                        onDeletePost(selectedPost.id);
                        setSelectedPost(null);
                      }}
                      className="flex-1 flex items-center justify-center space-x-2 py-2 px-4 bg-red-100 text-red-700 rounded-lg hover:bg-red-200 transition-colors duration-200"
                    >
                      <Trash2 className="w-4 h-4" />
                      <span>Delete Post</span>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </main>
  );
}