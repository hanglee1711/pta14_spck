import { useState, useEffect, useRef, useCallback } from 'react'
import { words } from '../words'
import './TypingTest.css'

const CHARS_PER_LINE = 80
const TIME_OPTIONS = [15, 30, 60, 120]

function generateLines() {
  const lines = []
  let currentLine = ''
  for (let i = 0; i < 1000; i++) {
    const word = words[Math.floor(Math.random() * words.length)]
    if ((currentLine.length + word.length + 1) > CHARS_PER_LINE) {
      lines.push(currentLine)
      currentLine = ''
    }
    currentLine += word + ' '
  }
  if (currentLine.length > 0) {
    lines.push(currentLine)
  }
  return lines
}

export default function TypingTest({ username, onComplete, onLogout }) {
  const [lines, setLines] = useState(() => generateLines())
  const [currentLineIndex, setCurrentLineIndex] = useState(0)
  const [typed, setTyped] = useState('')
  const [totalTyped, setTotalTyped] = useState([])
  const [selectedTime, setSelectedTime] = useState(30)
  const [timeLeft, setTimeLeft] = useState(30)
  const [started, setStarted] = useState(false)
  const [cursorVisible, setCursorVisible] = useState(true)
  const inputRef = useRef(null)
  const timerRef = useRef(null)
  const blinkRef = useRef(null)
  const charRefs = useRef([])

  const displayLines = lines.slice(currentLineIndex, currentLineIndex + 3)

  useEffect(() => {
    charRefs.current = []
  }, [currentLineIndex])

  const stop = useCallback(() => {
    if (timerRef.current) clearInterval(timerRef.current)
    if (blinkRef.current) clearInterval(blinkRef.current)

    const allTyped = [...totalTyped]
    if (typed.length > 0) {
      allTyped.push({ lineIndex: currentLineIndex, text: typed })
    }

    let totalWords = 0
    let totalLetters = 0
    let totalIncorrects = 0

    for (const entry of allTyped) {
      const line = lines[entry.lineIndex]
      const text = entry.text
      let wordCorrect = true

      for (let i = 0; i < text.length; i++) {
        const expected = line[i]
        const actual = text[i]

        if (expected === ' ') {
          if (wordCorrect) {
            totalWords++
          }
          wordCorrect = true
        } else {
          if (actual !== expected) {
            totalIncorrects++
            wordCorrect = false
          }
          totalLetters++
        }
      }
    }

    const elapsed = selectedTime
    const wpm = totalWords > 0 ? Math.round((totalWords / elapsed) * 60 * 100) / 100 : 0
    const accuracy = totalLetters > 0
      ? Math.round(((totalLetters - totalIncorrects) / totalLetters) * 100 * 100) / 100
      : 0

    onComplete({ wpm, accuracy, words: totalWords, seconds: elapsed })
  }, [totalTyped, typed, currentLineIndex, lines, selectedTime, onComplete])

  useEffect(() => {
    if (started && timeLeft <= 0) {
      stop()
    }
  }, [timeLeft, started, stop])

  useEffect(() => {
    blinkRef.current = setInterval(() => {
      setCursorVisible(v => !v)
    }, 500)
    return () => {
      if (blinkRef.current) clearInterval(blinkRef.current)
    }
  }, [])

  useEffect(() => {
    focusInput()
  }, [])

  function focusInput() {
    if (inputRef.current) {
      inputRef.current.focus()
    }
  }

  function handleTimeSelect(time) {
    if (started) return
    setSelectedTime(time)
    setTimeLeft(time)
  }

  function handleInput(e) {
    const value = e.target.value

    if (!started) {
      setStarted(true)
      timerRef.current = setInterval(() => {
        setTimeLeft(prev => {
          const next = prev - 0.2
          return next <= 0 ? 0 : Math.round(next * 10) / 10
        })
      }, 200)
    }

    setCursorVisible(true)
    setTyped(value)

    const currentLine = lines[currentLineIndex]
    if (value.length >= currentLine.length) {
      setTotalTyped(prev => [...prev, { lineIndex: currentLineIndex, text: value }])
      setCurrentLineIndex(prev => prev + 1)
      setTyped('')
      if (inputRef.current) inputRef.current.value = ''
    }
  }

  function getCharClass(lineOffset, charIndex) {
    if (lineOffset > 0) return 'char-inactive'
    if (charIndex >= typed.length) return 'char-inactive'

    const expected = displayLines[lineOffset][charIndex]
    const actual = typed[charIndex]
    return actual === expected ? 'char-correct' : 'char-incorrect'
  }

  function getCursorPosition() {
    if (!charRefs.current[0]) return null
    const idx = typed.length
    const lineChars = displayLines[0] || ''

    if (idx >= lineChars.length) return null

    const el = charRefs.current[0]?.[idx]
    if (!el) return null

    const container = el.closest('.typing-lines')
    if (!container) return null

    const containerRect = container.getBoundingClientRect()
    const charRect = el.getBoundingClientRect()

    return {
      left: charRect.left - containerRect.left,
      top: charRect.top - containerRect.top,
    }
  }

  const cursorPos = getCursorPosition()

  return (
    <div className="typing-container" onClick={focusInput}>
      <div className="typing-topbar">
        <div className="typing-topbar-left">
          <img src="/lypa.png" alt="Lypa" className="typing-logo" />
          <span className="typing-brand">Lypa</span>
        </div>
        <div className="typing-topbar-center">
          <div className="typing-welcome">Welcome back,</div>
          <div className="typing-username">{username}</div>
        </div>
        <div className="typing-topbar-right">
          <span className="typing-logout" onClick={onLogout}>Logout</span>
        </div>
      </div>

      <div className="typing-bottom">
        <div className="typing-panel">
          <span className="typing-time-label">Time left: {Math.ceil(timeLeft)}s</span>
          {TIME_OPTIONS.map(t => (
            <span
              key={t}
              className={`time-btn ${selectedTime === t ? 'time-btn-active' : ''}`}
              onClick={() => handleTimeSelect(t)}
            >
              {t}s
            </span>
          ))}
        </div>

        <div className="typing-area">
          <div className="typing-lines">
            {displayLines.map((line, lineOffset) => (
              <div key={currentLineIndex + lineOffset} className="typing-line">
                {line.split('').map((char, charIndex) => {
                  return (
                    <span
                      key={charIndex}
                      ref={el => {
                        if (!charRefs.current[lineOffset]) charRefs.current[lineOffset] = []
                        charRefs.current[lineOffset][charIndex] = el
                      }}
                      className={`typing-char ${getCharClass(lineOffset, charIndex)}`}
                    >
                      {char}
                    </span>
                  )
                })}
              </div>
            ))}
            {cursorPos && (
              <div
                className={`typing-cursor ${cursorVisible ? '' : 'cursor-hidden'}`}
                style={{
                  left: cursorPos.left + 'px',
                  top: cursorPos.top + 'px',
                }}
              />
            )}
          </div>
        </div>
      </div>

      <input
        ref={inputRef}
        className="typing-hidden-input"
        onInput={handleInput}
        autoFocus
        autoCapitalize="off"
        autoCorrect="off"
        autoComplete="off"
        spellCheck="false"
      />
    </div>
  )
}
