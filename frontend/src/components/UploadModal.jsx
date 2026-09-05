import React, { useState, useRef } from 'react';
import { Flame, Upload, X } from 'lucide-react';
import { analyzeMealImage } from '../services/api';

export default function UploadModal({ onClose, onImageAnalyzed }) {
  const [isDragging, setIsDragging] = useState(false);
  const [isScanning, setIsScanning] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileSelect = async (file) => {
    if (!file) return;
    setIsScanning(true);

    try {
      // Simulate/Trigger AI image analysis
      const analysisResult = await analyzeMealImage(file);
      setTimeout(() => {
        setIsScanning(false);
        onImageAnalyzed(analysisResult);
      }, 1500); // 1.5s scanning animation for realistic feedback
    } catch (err) {
      console.error(err);
      setIsScanning(false);
    }
  };

  const onDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const onDragLeave = () => {
    setIsDragging(false);
  };

  const onDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  };

  const onFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFileSelect(e.target.files[0]);
    }
  };

  return (
    <div className="upload-modal-container animate-fadeIn">
      <div className="upload-modal-header">
        <div className="brand-logo" style={{ color: '#FFFFFF' }}>
          <Flame className="brand-icon" style={{ color: '#00B2FE' }} />
        </div>
        <button className="upload-close-btn" onClick={onClose} title="Close upload modal">
          <X size={20} />
        </button>
      </div>

      <div 
        className={`upload-area-box ${isDragging ? 'drag-over' : ''}`}
        onDragOver={onDragOver}
        onDragLeave={onDragLeave}
        onDrop={onDrop}
        onClick={() => fileInputRef.current?.click()}
      >
        {/* Camera Viewfinder Bracket Corners */}
        <div className="viewfinder-corner vf-top-left" />
        <div className="viewfinder-corner vf-top-right" />
        <div className="viewfinder-corner vf-bottom-left" />
        <div className="viewfinder-corner vf-bottom-right" />

        {isScanning && (
          <div className="scanner-overlay">
            <div className="scanner-laser-line" />
            <div className="brand-logo" style={{ color: '#FFFFFF', marginBottom: 12 }}>
              <Flame className="brand-icon" style={{ color: '#00B2FE' }} />
            </div>
            <div style={{ fontSize: '15px', fontWeight: 600, color: '#FFFFFF' }}>
              Analyzing meal photo...
            </div>
            <div style={{ fontSize: '12px', color: '#94A3B8', marginTop: 4 }}>
              Detecting foods, portions & calories
            </div>
          </div>
        )}

        <div className="upload-icon-wrapper">
          <Upload size={36} strokeWidth={1.5} />
        </div>

        <div className="upload-prompt-title">Drag a photo here</div>
        <div className="upload-prompt-sub">or browse files from your computer</div>

        <input 
          type="file" 
          ref={fileInputRef} 
          style={{ display: 'none' }} 
          accept="image/*" 
          onChange={onFileChange}
        />
      </div>

      <button className="browse-files-btn" onClick={() => fileInputRef.current?.click()}>
        Browse files
      </button>

      <div className="upload-hint-text">PNG or JPG, up to 10MB</div>
    </div>
  );
}
