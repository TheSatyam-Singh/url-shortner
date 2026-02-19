import { useState } from 'react'

const API = '/api/auth'

function Login({ onLogin }) {
  const [isRegister, setIsRegister] = useState(false)
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    const endpoint = isRegister ? `${API}/register` : `${API}/login`

    try {
      const res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      })
      const data = await res.json()
      if (!res.ok) {
        setError(data.error || 'Something went wrong')
        return
      }
      onLogin(data.token, data.username)
    } catch {
      setError('Could not connect to server')
    }
  }

  return (
    <div className="auth-page">
      <h2>{isRegister ? 'Register' : 'Login'}</h2>
      {error && <p className="error">{error}</p>}
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">{isRegister ? 'Register' : 'Login'}</button>
      </form>
      <p className="toggle">
        {isRegister ? 'Already have an account? ' : "Don't have an account? "}
        <a href="#" onClick={(e) => { e.preventDefault(); setIsRegister(!isRegister); setError('') }}>
          {isRegister ? 'Login' : 'Register'}
        </a>
      </p>
    </div>
  )
}

export default Login
