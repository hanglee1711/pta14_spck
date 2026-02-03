import { useState } from 'react'
import { register } from '../data'
import './Register.css'

export default function Register({ onRegistered, onGoToLogin }) {
  const [email, setEmail] = useState('')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setSuccess('')
    const result = await register(email, username, password, confirmPassword)
    if (result.success) {
      setSuccess('Account created!')
      setTimeout(() => onRegistered(), 1000)
    } else {
      setError(result.error)
    }
  }

  return (
    <div className="register-container">
      <div className="register-left">
        <h1 className="register-heading">Create an account</h1>
        <form onSubmit={handleSubmit} className="register-form">
          <div className="field-group">
            <label className="field-label">Email</label>
            <input
              type="email"
              placeholder="Fill in your email"
              value={email}
              onChange={e => setEmail(e.target.value)}
              autoComplete="email"
            />
          </div>
          <div className="field-group">
            <label className="field-label">Username</label>
            <input
              type="text"
              placeholder="Fill in your username"
              value={username}
              onChange={e => setUsername(e.target.value)}
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
              autoComplete="new-password"
            />
          </div>
          <div className="field-group">
            <label className="field-label">Confirm Password</label>
            <input
              type="password"
              placeholder="Confirm your password"
              value={confirmPassword}
              onChange={e => setConfirmPassword(e.target.value)}
              autoComplete="new-password"
            />
          </div>
          {error && <p className="error-text">{error}</p>}
          {success && <p className="success-text">{success}</p>}
          <button type="submit" className="btn-gradient">Register</button>
          <div className="register-login-row">
            <span className="register-login-text">Have an account?</span>
            <a className="register-login-link" onClick={onGoToLogin}>Login</a>
          </div>
        </form>
      </div>
      <div className="register-right">
        <span className="register-brand-text">Lypa</span>
        <img src="/lypa.png" alt="Lypa" className="register-logo" />
      </div>
    </div>
  )
}
