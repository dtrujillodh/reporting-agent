import { useState, useRef, useEffect } from 'react'
import ReactMarkdown from 'react-markdown'
import { 
  FileText, 
  Upload, 
  Send, 
  Copy, 
  Settings, 
  CheckCircle2, 
  Loader2,
  Trash2,
  PieChart,
  Eye
} from 'lucide-react'
import './App.css'

function App() {
  const [message, setMessage] = useState('')
  const [files, setFiles] = useState<File[]>([])
  const [response, setResponse] = useState('')
  const [rawContext, setRawContext] = useState('')
  const [pdfUrl, setPdfUrl] = useState('')
  const [showPdf, setShowPdf] = useState(true)
  const [loading, setLoading] = useState(false)
  const [apiUrl, setApiUrl] = useState('')
  const [showSettings, setShowSettings] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    const savedUrl = localStorage.getItem('reporting-api-url')
    if (savedUrl && savedUrl.startsWith('http')) {
      setApiUrl(savedUrl)
    } else {
      setApiUrl('')
    }
  }, [])

  const handleUrlChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value
    setApiUrl(value)
    if (value) {
      localStorage.setItem('reporting-api-url', value)
    } else {
      localStorage.removeItem('reporting-api-url')
    }
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFiles(Array.from(e.target.files))
    }
  }

  const removeFile = (index: number) => {
    setFiles(prev => prev.filter((_, i) => i !== index))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!message && files.length === 0) return
    
    setLoading(true)
    setResponse('')
    setRawContext('')
    if (pdfUrl) URL.revokeObjectURL(pdfUrl)
    setPdfUrl('')

    const formData = new FormData()
    formData.append('message', message || "Generate report based on the uploaded files.")
    files.forEach(file => {
      formData.append('files', file)
    })

    try {
      const fetchUrl = apiUrl ? `${apiUrl.replace(/\/$/, '')}/report` : '/report'
      
      const res = await fetch(fetchUrl, {
        method: 'POST',
        body: formData,
      })
      
      if (!res.ok) throw new Error(`Server error: ${res.status}`)
      
      const data = await res.json()
      setResponse(data.response)
      setRawContext(data.raw_context || '')
      
      if (data.pdf_data) {
        const byteCharacters = atob(data.pdf_data)
        const byteNumbers = new Array(byteCharacters.length)
        for (let i = 0; i < byteCharacters.length; i++) {
          byteNumbers[i] = byteCharacters.charCodeAt(i)
        }
        const byteArray = new Uint8Array(byteNumbers)
        const blob = new Blob([byteArray], { type: 'application/pdf' })
        const url = URL.createObjectURL(blob)
        setPdfUrl(url)
        setShowPdf(true)
      }
    } catch (error) {
      console.error(error)
      setResponse(`### ⚠️ Connection Error
Could not reach the backend. Please check your API URL in settings.`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-layout">
      {/* Sidebar */}
      <aside className={`sidebar ${showSettings ? 'open' : ''}`}>
        <div className="sidebar-header">
          <PieChart size={24} color="#6366f1" />
          <span>Analytics Admin</span>
        </div>
        
        <nav className="sidebar-nav">
          <div className="nav-item active">
            <FileText size={18} />
            <span>New Report</span>
          </div>
          <div className="nav-group-label">Configuration</div>
          <div className="settings-panel">
            <div className="settings-item">
              <label><Settings size={14} /> Backend URL</label>
              <input
                type="text"
                value={apiUrl}
                onChange={handleUrlChange}
                placeholder="Relative (/report)"
              />
            </div>
          </div>
        </nav>
        
        <div className="sidebar-footer">
          <div className="status-badge">
            <div className="status-dot"></div>
            System Online
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        <header className="top-bar">
          <div className="breadcrumb">Dashboard / <strong>Report Generator</strong></div>
          <button 
            className="mobile-toggle" 
            onClick={() => setShowSettings(!showSettings)}
          >
            <Settings size={20} />
          </button>
        </header>

        <div className="content-grid">
          {/* Input Section */}
          <section className="input-card">
            <div className="card-header">
              <h2>Build Report</h2>
            </div>

            <form onSubmit={handleSubmit} className="report-form">
              <div className="form-group">
                <textarea
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  placeholder="Instructions..."
                  rows={3}
                />
              </div>

              <div className="upload-zone" onClick={() => fileInputRef.current?.click()}>
                <Upload size={24} className="upload-icon" />
                <p><strong>Upload files</strong></p>
                <input
                  type="file"
                  ref={fileInputRef}
                  onChange={handleFileChange}
                  multiple
                  hidden
                />
              </div>

              {files.length > 0 && (
                <div className="file-list">
                  {files.map((file, i) => (
                    <div key={i} className="file-item">
                      <FileText size={14} />
                      <span className="file-name">{file.name}</span>
                      <button type="button" onClick={() => removeFile(i)}><Trash2 size={14} /></button>
                    </div>
                  ))}
                </div>
              )}

              <button type="submit" disabled={loading || (!message && files.length === 0)} className="generate-btn">
                {loading ? (
                  <>
                    <Loader2 size={18} className="spin" />
                    <span>Processing...</span>
                  </>
                ) : (
                  <>
                    <Send size={18} />
                    <span>Generate</span>
                  </>
                )}
              </button>
            </form>
          </section>

          {/* Source Data Section */}
          <section className="output-card source-card">
            <div className="card-header">
              <div className="header-left">
                <h2>Source Data</h2>
                <span className="badge">{pdfUrl ? 'PDF Original' : 'Extracted Context'}</span>
              </div>
              {pdfUrl && (
                <button 
                  className={`icon-btn ${!showPdf ? 'active' : ''}`} 
                  onClick={() => setShowPdf(!showPdf)}
                  title="Toggle View Mode"
                >
                  <Eye size={18} />
                </button>
              )}
            </div>
            <div className="document-viewer raw-viewer">
               {showPdf && pdfUrl ? (
                 <iframe 
                   src={pdfUrl} 
                   className="pdf-preview" 
                   title="Source PDF"
                 />
               ) : (
                 <div className="raw-content">
                   <pre>{rawContext}</pre>
                 </div>
               )}
            </div>
          </section>

          {/* Output Section */}
          <section className="output-card report-card">
            <div className="card-header">
              <div className="header-left">
                <h2>Generated Report</h2>
                {response && <span className="badge success"><CheckCircle2 size={12} /> Ready</span>}
              </div>
              {response && (
                <button 
                  className="icon-btn" 
                  onClick={() => navigator.clipboard.writeText(response)}
                  title="Copy to Clipboard"
                >
                  <Copy size={18} />
                </button>
              )}
            </div>

            <div className="document-viewer">
              {response ? (
                <div className="prose">
                  <ReactMarkdown>{response}</ReactMarkdown>
                </div>
              ) : (
                <div className="empty-state">
                  <div className="empty-icon">
                    <FileText size={48} strokeWidth={1} />
                  </div>
                  <h3>No report yet</h3>
                </div>
              )}
            </div>
          </section>
        </div>
      </main>
    </div>
  )
}

export default App
