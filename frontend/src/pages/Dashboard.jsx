import { useState, useEffect, useCallback } from 'react'

const API = '/api'

function Dashboard({ token, username, onLogout }) {
  const [url, setUrl] = useState('')
  const [customCode, setCustomCode] = useState('')
  const [result, setResult] = useState(null)
  const [urls, setUrls] = useState([])
  const [error, setError] = useState('')

  const headers = {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${token}`,
  }

  const fetchUrls = useCallback(async () => {
    try {
      const res = await fetch(`${API}/urls`, {
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
      })
      if (res.ok) {
        const data = await res.json()
        setUrls(data)
      }
    } catch {
      // ignore
    }
  }, [token])

  useEffect(() => {
    fetchUrls()
  }, [fetchUrls])

  const handleShorten = async (e) => {
    e.preventDefault()
    setError('')
    setResult(null)
    if (!url.trim()) return

    try {
      const body = { url: url.trim() }
      if (customCode.trim()) body.custom_code = customCode.trim()

      const res = await fetch(`${API}/shorten`, {
        method: 'POST',
        headers,
        body: JSON.stringify(body),
      })
      const data = await res.json()
      if (!res.ok) {
        setError(data.error || 'Failed to shorten')
        return
      }
      setResult(data)
      setUrl('')
      setCustomCode('')
      fetchUrls()
    } catch {
      setError('Could not connect to server')
    }
  }

  const handleDelete = async (id) => {
    try {
      await fetch(`${API}/urls/${id}`, { method: 'DELETE', headers })
      fetchUrls()
      if (result && result.short_code) {
        const deleted = urls.find((u) => u.id === id)
        if (deleted && deleted.short_code === result.short_code) {
          setResult(null)
        }
      }
    } catch {
      // ignore
    }
  }

  return (
    <>
      <nav className="navbar">
        <h2>ShrinkEase</h2>
        <div>
          <span style={{ fontSize: 13, marginRight: 10, color: '#666' }}>{username}</span>
          <button onClick={onLogout}>Logout</button>
        </div>
      </nav>

      <div className="shorten-form">
        <form onSubmit={handleShorten}>
          <input
            type="text"
            placeholder="Paste your long URL here"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            required
          />
          <input
            type="text"
            placeholder="Custom code (optional)"
            value={customCode}
            onChange={(e) => setCustomCode(e.target.value)}
          />
          {error && <p style={{ color: '#dc2626', fontSize: 13, marginBottom: 8 }}>{error}</p>}
          <button type="submit">Shorten</button>
        </form>
      </div>

      {result && (
        <div className="result-box">
          <p className="short-url">
            <a href={result.short_url} target="_blank" rel="noreferrer">
              {result.short_url}
            </a>
          </p>
          {result.qr_code && (
            <img src={`data:image/png;base64,${result.qr_code}`} alt="QR Code" />
          )}
        </div>
      )}

      <div className="url-list">
        <h3>Your URLs</h3>
        {urls.length === 0 && <p style={{ fontSize: 13, color: '#999' }}>No URLs yet</p>}
        {urls.map((u) => (
          <div className="url-item" key={u.id}>
            <div className="info">
              <a href={u.short_url} target="_blank" rel="noreferrer">{u.short_url}</a>
              <div className="original">{u.original_url}</div>
              <div className="meta">{u.clicks} click{u.clicks !== 1 ? 's' : ''}</div>
            </div>
            <div className="actions">
              <button className="del" onClick={() => handleDelete(u.id)}>Delete</button>
            </div>
          </div>
        ))}
      </div>
    </>
  )
}

export default Dashboard
