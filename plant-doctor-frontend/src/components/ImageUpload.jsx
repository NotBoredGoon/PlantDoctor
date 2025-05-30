import React from 'react';

const ImageUpload = ({ onImageUpload }) => {
  const handleImageChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      onImageUpload(e.target.files[0]);
    }
  };

  return (
    <div className="image-upload-container">
      <label htmlFor="image-upload" className="image-upload-label">
        Click to upload an image
      </label>
      <input
        id="image-upload"
        type="file"
        accept="image/*"
        onChange={handleImageChange}
        style={{ display: 'none' }}
      />
    </div>
  );
};

export default ImageUpload;