import { useEffect, useState } from 'react'

// Import icons for dark and light theme toggle
import { SunIcon, MoonIcon } from '../../assets/icons/themes'

export function ThemeToggle() {
  const [isMounted, setMounted] = useState(false)
  const [theme, setTheme] = useState(typeof localStorage !== 'undefined' ? localStorage.getItem('theme') ?? 'light' : 'light')

  const handleClick = () => {
    setTheme(theme === 'dark' ? 'light' : 'dark')
  }

  useEffect(() => {
    if (theme === 'dark') document.documentElement.classList.add('dark')
    else document.documentElement.classList.remove('dark')

    typeof localStorage !== 'undefined' ? localStorage.setItem('theme', theme) : null
  }, [theme])

  useEffect(() => {
    setMounted(true)
  }, [])

  return isMounted ? (
    <button
      onClick={handleClick}
      className="bg-light hover:bg-sh-light dark:bg-dark dark:hover:bg-sh-dark text-white font-bold py-1 px-2 rounded"
    >
      {theme === 'dark' ? (
        <SunIcon className="w-10 h-10 text-tx-light dark:text-tx-dark" />
      ) : (
        <MoonIcon className="w-10 h-10 text-tx-light dark:text-tx-dark" />
      )}
    </button>
  ) : (
    <div style={{ height: '3rem' }} />
  )
}
