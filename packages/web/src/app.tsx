import { useEffect, useState } from 'preact/hooks'
import '@picocss/pico'
import './app.css'

export function App() {
  const [q, setQ] = useState('')
  const [a, setA] = useState('')
  const [loading, setLoading] = useState(false)
  async function onQuest(quest: string) {
    try {
      setQ(quest)
      setLoading(true)
      const p = new URLSearchParams()
      p.set('q', quest)
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
      if (
        ev.target instanceof HTMLTextAreaElement &&
        ev.key === 'Enter' &&
        ev.ctrlKey
      ) {
        ev.preventDefault()
        await onQuest(ev.target.value)
      }
    }
    window.addEventListener('keydown', onHandle)
    return () => window.removeEventListener('keydown', onHandle)
  }, [])

  return (
    <>
      <textarea
        rows={4}
        value={q}
        onChange={(e) => setQ((e.target as HTMLTextAreaElement).value)}
      ></textarea>
      <button aria-busy={loading} type={'button'} onClick={() => onQuest(q)}>
        Commit
      </button>
      <p>{a}</p>
    </>
  )
}
