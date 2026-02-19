import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';

export default function FileUpload({ onFileSelect }) {
  const onDrop = useCallback(acceptedFiles => {
    if (acceptedFiles.length > 0) {
      onFileSelect(acceptedFiles[0]);
    }
  }, [onFileSelect]);

  const { getRootProps, getInputProps, isDragActive, fileRejections } = useDropzone({
    onDrop,
    accept: {
      'text/plain': ['.vcf']
    },
    maxSize: 5 * 1024 * 1024, // 5MB
    multiple: false
  });

  return (
    <div>
      <label className="block mb-2 font-semibold text-gray-700">
        VCF File Upload
      </label>
      <div 
        {...getRootProps()} 
        className={`border-2 border-dashed p-8 text-center cursor-pointer rounded-lg transition ${
          isDragActive 
            ? 'border-blue-500 bg-blue-50' 
            : 'border-gray-300 hover:border-blue-400 hover:bg-gray-50'
        }`}
      >
        <input {...getInputProps()} />
        <div className="text-gray-600">
          {isDragActive ? (
            <p className="text-blue-600 font-semibold">📁 Drop the VCF file here...</p>
          ) : (
            <>
              <p className="font-semibold mb-1">📤 Drag & drop a VCF file here</p>
              <p className="text-sm">or click to select</p>
              <p className="text-xs text-gray-500 mt-2">VCF v4.2 format, max 5MB</p>
            </>
          )}
        </div>
      </div>
      {fileRejections.length > 0 && (
        <p className="text-red-600 text-sm mt-2">
          ⚠ File rejected: {fileRejections[0].errors[0].message}
        </p>
      )}
    </div>
  );
}