import { useState } from 'react'
import Login from './components/Login'
import Register from './components/Register'
import TypingTest from './components/TypingTest'
import Result from './components/Result'

export default function App() {
  const [screen, setScreen] = useState('login')
  const [username, setUsername] = useState('')
  const [resultData, setResultData] = useState(null)

  function handleLogin(user) {
    setUsername(user)
    setScreen('test')
  }

  function handleTestComplete(data) {
    setResultData(data)
    setScreen('result')
  }

  function handleTryAgain() {
    setScreen('test')
  }

  function handleLogout() {
    localStorage.removeItem('lypa_keep_user')
    setUsername('')
    setResultData(null)
    setScreen('login')
  }

  return (
    <div className="app">
      {screen === 'login' && (
        <Login
          onLogin={handleLogin}
          onGoToRegister={() => setScreen('register')}
        />
      )}
      {screen === 'register' && (
        <Register
          onRegistered={() => setScreen('login')}
          onGoToLogin={() => setScreen('login')}
        />
      )}
      {screen === 'test' && (
        <TypingTest
          username={username}
          onComplete={handleTestComplete}
          onLogout={handleLogout}
        />
      )}
      {screen === 'result' && (
        <Result
          username={username}
          data={resultData}
          onTryAgain={handleTryAgain}
          onLogout={handleLogout}
        />
      )}
    </div>
  )
}
