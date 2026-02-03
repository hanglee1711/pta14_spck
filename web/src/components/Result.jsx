import { useEffect, useMemo, useRef } from 'react'
import { Line } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'
import { addTestResult, getTestResults } from '../data'
import './Result.css'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)

export default function Result({ username, data, onTryAgain, onLogout }) {
  const savedRef = useRef(false)

  useEffect(() => {
    if (data && !savedRef.current) {
      savedRef.current = true
      addTestResult(username, data.wpm, data.accuracy)
    }
  }, [username, data])

  const history = useMemo(() => getTestResults(username), [username, data])

  const chartData = useMemo(() => {
    let wpmData = history.wpm || []
    let accData = history.accuracy || []

    if (wpmData.length === 1) {
      wpmData = [wpmData[0], wpmData[0]]
      accData = [accData[0], accData[0]]
    }

    const labels = wpmData.map((_, i) => `${i + 1}`)

    return {
      labels,
      datasets: [
        {
          label: 'WPM',
          data: wpmData,
          borderColor: 'rgb(90, 200, 255)',
          backgroundColor: 'rgba(90, 200, 255, 0.1)',
          yAxisID: 'y',
          tension: 0,
          borderWidth: 3,
          pointRadius: 0,
        },
        {
          label: 'Accuracy %',
          data: accData,
          borderColor: 'rgb(120, 255, 120)',
          backgroundColor: 'rgba(120, 255, 120, 0.1)',
          yAxisID: 'y1',
          tension: 0,
          borderWidth: 3,
          pointRadius: 0,
        },
      ],
    }
  }, [history])

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    interaction: {
      mode: 'index',
      intersect: false,
    },
    plugins: {
      legend: { display: false },
    },
    scales: {
      x: {
        display: false,
      },
      y: {
        type: 'linear',
        display: true,
        position: 'left',
        min: 0,
        max: 300,
        title: {
          display: true,
          text: 'WPM',
          color: 'rgb(90, 200, 255)',
          font: { size: 14 },
        },
        ticks: { color: 'rgb(90, 200, 255)' },
        grid: { color: 'rgba(255, 255, 255, 0.05)' },
      },
      y1: {
        type: 'linear',
        display: true,
        position: 'right',
        min: 0,
        max: 100,
        title: {
          display: true,
          text: 'Accuracy %',
          color: 'rgb(120, 255, 120)',
          font: { size: 14 },
        },
        ticks: { color: 'rgb(120, 255, 120)' },
        grid: { drawOnChartArea: false },
      },
    },
  }

  return (
    <div className="result-container">
      <div className="result-top">
        <h1 className="result-wpm">{Math.round(data.wpm)} wpm</h1>
      </div>

      <div className="result-middle">
        <div className="result-stats">
          <p>{data.words} words</p>
          <p>{data.seconds} seconds</p>
          <p>{Math.round(data.accuracy)}% accuracy</p>
        </div>
        {history.wpm.length > 0 && (
          <div className="result-chart-wrapper">
            <Line data={chartData} options={chartOptions} />
          </div>
        )}
      </div>

      <div className="result-bottom">
        <span className="result-try-again" onClick={onTryAgain}>try again</span>
      </div>
    </div>
  )
}
