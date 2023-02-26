import { useEffect, useState } from 'preact/hooks'
import '@picocss/pico'
import './app.css'

export function App() {
  const [q, setQ] = useState('')
  const [a, setA] = useState('')
  const [loading, setLoading] = useState(false)
  async function onQuest(quest: string) {
    const q = quest.trim()
    if (q.length === 0) {
      return
    }
    try {
      setQ(q)
      setLoading(true)
      const p = new URLSearchParams()
      p.set('q', quest.trim())
      const resp = await fetch(
        import.meta.env.VITE_BASE_URL + '?' + p.toString(),
      )
      const r = await resp.text()
      // console.log('r', r)
      setA(r)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    const onHandle = async (ev: KeyboardEvent): Promise<void> => {
      if (ev.target instanceof HTMLInputElement && ev.key === 'Enter') {
        ev.preventDefault()
        await onQuest(ev.target.value)
      }
    }
    window.addEventListener('keydown', onHandle)
    return () => window.removeEventListener('keydown', onHandle)
  }, [])

  return (
    <>
      <h2>to the stars robot</h2>
      <input
        value={q}
        onChange={(e) => setQ((e.target as HTMLTextAreaElement).value)}
        onInput={(e) => setQ((e.target as HTMLTextAreaElement).value)}
      />
      <button
        aria-busy={loading}
        disabled={q.length === 0}
        type={'button'}
        onClick={() => onQuest(q)}
      >
        Quest
      </button>
      <p>{a}</p>
    </>
  )
}
