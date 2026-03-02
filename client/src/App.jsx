import React, { useState, useRef, useEffect } from 'react';
import {
  Upload,
  Send,
  FileText,
  Bot,
  User,
  Loader2,
  X,
  AlertCircle,
  CheckCircle2
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import axios from 'axios';

const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

function App() {
  const [file, setFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('idle'); // idle, uploading, success, error
  const [sessionId, setSessionId] = useState(null);
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([]);
  const [isThinking, setIsThinking] = useState(false);
  const [error, setError] = useState(null);
  const [backendStatus, setBackendStatus] = useState('unknown'); // unknown, online, offline

  const chatEndRef = useRef(null);
  const fileInputRef = useRef(null);

  // Health check on mount
  useEffect(() => {
    const checkHealth = async () => {
      try {
        await axios.get(`${API_BASE_URL}/health`);
        setBackendStatus('online');
      } catch {
        setBackendStatus('offline');
      }
    };
    checkHealth();
    const interval = setInterval(checkHealth, 10000); // Check every 10s
    return () => clearInterval(interval);
  }, []);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isThinking]);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    validateAndSetFile(selectedFile);
  };

  const validateAndSetFile = (selectedFile) => {
    setError(null);
    if (!selectedFile) return;

    if (selectedFile.type !== 'application/pdf') {
      setError('Only PDF files are allowed.');
      return;
    }

    if (selectedFile.size > MAX_FILE_SIZE) {
      setError('File size must be under 10MB.');
      return;
    }

    setFile(selectedFile);
    uploadFile(selectedFile);
  };

  const uploadFile = async (fileToUpload) => {
    setUploadStatus('uploading');
    setError(null);
    const formData = new FormData();
    formData.append('file', fileToUpload);

    try {
      const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      const newSessionId = response.data.session_id;
      setSessionId(newSessionId);
      setUploadStatus('success');

      setMessages([{
        id: Date.now(),
        type: 'ai',
        text: `Successfully uploaded ${fileToUpload.name}. I've indexed the content. How can I help you understand this document?`
      }]);
    } catch (err) {
      setUploadStatus('error');
      const detail = err.response?.data?.detail || 'Failed to upload document. Please ensure the backend is running.';
      setError(detail);
      setFile(null);
    }
  };

  const handleSendQuery = async (e) => {
    e.preventDefault();
    if (!query.trim() || isThinking || uploadStatus !== 'success' || !sessionId) return;

    const currentQuery = query.trim();
    const userMessage = { id: Date.now(), type: 'user', text: currentQuery };
    setMessages(prev => [...prev, userMessage]);
    setQuery('');
    setIsThinking(true);
    setError(null);

    try {
      const response = await axios.post(`${API_BASE_URL}/query`, {
        session_id: sessionId,
        query: currentQuery
      });

      const aiMessage = {
        id: Date.now() + 1,
        type: 'ai',
        text: response.data.answer || 'I couldn\'t find an answer to that.'
      };
      setMessages(prev => [...prev, aiMessage]);
    } catch (err) {
      const detail = err.response?.data?.detail || 'Failed to get a response.';
      setError(detail);
      const errorMessage = {
        id: Date.now() + 2,
        type: 'ai',
        text: `Error: ${detail}. Please try again.`
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsThinking(false);
    }
  };

  const clearFile = () => {
    setFile(null);
    setSessionId(null);
    setUploadStatus('idle');
    setMessages([]);
    setError(null);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  return (
    <div className="app-container">
      {/* Sidebar - Document Management */}
      <aside className="glass-panel sidebar">
        <div className="logo-area">
          <Bot className="logo-icon" size={32} />
          <h1 className="logo-text">RAG Insight</h1>
        </div>

        <div className="upload-section">
          {!file ? (
            <div
              className="drop-zone"
              onClick={() => fileInputRef.current?.click()}
              onDragOver={(e) => { e.preventDefault(); e.currentTarget.classList.add('dragging'); }}
              onDragLeave={(e) => { e.preventDefault(); e.currentTarget.classList.remove('dragging'); }}
              onDrop={(e) => {
                e.preventDefault();
                e.currentTarget.classList.remove('dragging');
                validateAndSetFile(e.dataTransfer.files[0]);
              }}
            >
              <Upload className="upload-icon" size={40} strokeWidth={1.5} />
              <div className="upload-text">
                <p>Click or drag PDF</p>
                <p style={{ fontSize: '0.75rem', marginTop: '4px' }}>Max size: 10MB</p>
              </div>
              <input
                type="file"
                ref={fileInputRef}
                onChange={handleFileChange}
                accept=".pdf"
                hidden
              />
            </div>
          ) : (
            <div className="file-info">
              <FileText className="logo-icon" size={20} />
              <span className="file-name">{file.name}</span>
              <button
                onClick={clearFile}
                style={{ marginLeft: 'auto', background: 'none', border: 'none', color: 'var(--text-dim)', cursor: 'pointer' }}
              >
                <X size={16} />
              </button>
            </div>
          )}

          {error && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="status-badge"
              style={{ color: 'var(--error)', marginTop: '1rem' }}
            >
              <AlertCircle size={14} />
              {error}
            </motion.div>
          )}

          {uploadStatus === 'uploading' && (
            <div className="status-badge" style={{ marginTop: '1rem' }}>
              <Loader2 className="animate-spin" size={14} />
              Processing document...
            </div>
          )}

          {uploadStatus === 'success' && (
            <div className="status-badge" style={{ marginTop: '1rem', color: 'var(--success)' }}>
              <CheckCircle2 size={14} />
              Ready for questions
            </div>
          )}
        </div>

        <div style={{ marginTop: 'auto', color: 'var(--text-dim)', fontSize: '0.75rem' }}>
          By Antigravity AI
        </div>
      </aside>

      {/* Main Chat Interface */}
      <main className="glass-panel chat-area">
        <header className="chat-header">
          <div>
            <h2 style={{ fontSize: '1.25rem', fontWeight: 600 }}>Document Q&A</h2>
            <div className="status-badge">
              <div
                className="pulse"
                style={{ background: backendStatus === 'online' ? 'var(--success)' : 'var(--error)' }}
              />
              {backendStatus === 'online' ? 'Server Online' : 'Server Offline'}
              {uploadStatus === 'success' && ' • Document Active'}
            </div>
          </div>
        </header>

        <div className="chat-messages">
          {messages.length === 0 && uploadStatus === 'idle' && (
            <div style={{ height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', opacity: 0.5 }}>
              <Bot size={64} style={{ marginBottom: '1rem' }} />
              <p>Upload a PDF to start analyzing</p>
            </div>
          )}

          <AnimatePresence initial={false}>
            {messages.map((msg) => (
              <motion.div
                key={msg.id}
                initial={{ opacity: 0, y: 12, scale: 0.95 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                className={`message ${msg.type}`}
              >
                {msg.text}
              </motion.div>
            ))}
          </AnimatePresence>

          {isThinking && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="message ai"
              style={{ display: 'flex', alignItems: 'center', gap: '8px' }}
            >
              <Loader2 className="animate-spin" size={16} />
              Thinking...
            </motion.div>
          )}
          <div ref={chatEndRef} />
        </div>

        <form className="chat-input-container" onSubmit={handleSendQuery}>
          <div className="input-wrapper">
            <input
              type="text"
              placeholder={uploadStatus === 'success' ? "Ask anything about the document..." : "Upload a document first..."}
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              disabled={uploadStatus !== 'success' || isThinking}
            />
            <button
              type="submit"
              className="send-button"
              disabled={!query.trim() || isThinking || uploadStatus !== 'success'}
            >
              <Send size={20} />
            </button>
          </div>
        </form>
      </main>

      <style>{`
        .animate-spin {
          animation: spin 1s linear infinite;
        }
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}

export default App;
