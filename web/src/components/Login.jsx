import { useState, useEffect } from 'react'
import { login } from '../data'
import './Login.css'

export default function Login({ onLogin, onGoToRegister }) {
  const [identifier, setIdentifier] = useState('')
  const [password, setPassword] = useState('')
  const [keepLoggedIn, setKeepLoggedIn] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    const saved = localStorage.getItem('lypa_keep_user')
    if (saved) {
      onLogin(saved)
    }
  }, [])

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    const result = await login(identifier, password)
    if (result.success) {
      if (keepLoggedIn) {
        localStorage.setItem('lypa_keep_user', result.username)
      } else {
        localStorage.removeItem('lypa_keep_user')
      }
      onLogin(result.username)
    } else {
      setError(result.error)
    }
  }

  return (
    <div className="login-container">
      <div className="login-left">
        <h1 className="login-welcome">Welcome</h1>
        <form onSubmit={handleSubmit} className="login-form">
          <div className="field-group">
            <label className="field-label">Username</label>
            <input
              type="text"
              placeholder="Fill in your username or email"
              value={identifier}
              onChange={e => setIdentifier(e.target.value)}
              autoComplete="username"
            />
          </div>
          <div className="field-group">
            <label className="field-label">Password</label>
            <input
              type="password"
              placeholder="Fill in your password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              autoComplete="current-password"
            />
          </div>
          <label className="keep-logged-in">
            <input
              type="checkbox"
              checked={keepLoggedIn}
              onChange={e => setKeepLoggedIn(e.target.checked)}
            />
            <span>Keep me logged in</span>
          </label>
          {error && <p className="error-text">{error}</p>}
          <button type="submit" className="btn-gradient">Login</button>
          <div className="login-register-row">
            <span className="login-register-text">No account?</span>
            <a className="login-register-link" onClick={onGoToRegister}>Register</a>
          </div>
        </form>
      </div>
      <div className="login-right">
        <span className="login-brand-text">Lypa</span>
        <img src="/lypa.png" alt="Lypa" className="login-logo" />
      </div>
    </div>
  )
}
