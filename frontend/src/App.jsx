import { useState, useEffect } from 'react'

export default function App() {
  const [view, setView] = useState('landing') // 'landing' | 'login' | 'signup' | 'dashboard'
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [user, setUser] = useState(null)
  const [movies, setMovies] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  // Restore session if token exists and fetch public movie preview
  useEffect(() => {
    const savedToken = localStorage.getItem('token')
    const savedEmail = localStorage.getItem('user_email')
    if (savedToken && savedEmail) {
      setUser({ email: savedEmail })
      setView('dashboard')
    }

    fetch('/api/movies?limit=6')
      .then((res) => (res.ok ? res.json() : []))
      .then((data) => setMovies(Array.isArray(data) ? data : data.movies || []))
      .catch(() => {})
  }, [])

  const handleAuthSubmit = async (e) => {
    e.preventDefault()
    setError('')

    if (view === 'signup' && password !== confirmPassword) {
      setError('Passwords do not match.')
      return
    }

    setLoading(true)
    const endpoint = view === 'signup' ? '/api/auth/signup' : '/api/auth/login'

    try {
      const res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      })
      const data = await res.json()

      if (!res.ok) {
        throw new Error(data.detail || 'Authentication failed.')
      }

      if (data.access_token) {
        localStorage.setItem('token', data.access_token)
        localStorage.setItem('user_email', email)
        setUser({ email })
        setView('dashboard')
      } else {
        // If signup returns user info without a token, switch to login
        setView('login')
        setError('Account created! Please log in.')
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user_email')
    setUser(null)
    setEmail('')
    setPassword('')
    setConfirmPassword('')
    setView('landing')
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
      {/* Responsive Navigation Bar */}
      <header className="border-b border-slate-800 bg-slate-950/90 backdrop-blur sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
          <button
            onClick={() => setView(user ? 'dashboard' : 'landing')}
            className="text-xl font-bold tracking-tight text-amber-400"
          >
            StarkCinema
          </button>

          <nav className="flex items-center gap-3 sm:gap-4">
            {user ? (
              <>
                <span className="hidden sm:inline text-sm text-slate-400">{user.email}</span>
                <button
                  onClick={handleLogout}
                  className="px-3.5 py-1.5 rounded-lg text-sm font-medium bg-slate-800 hover:bg-slate-700 transition"
                >
                  Log Out
                </button>
              </>
            ) : (
              <>
                <button
                  onClick={() => { setError(''); setView('login') }}
                  className="px-3.5 py-1.5 rounded-lg text-sm font-medium text-slate-300 hover:text-white transition"
                >
                  Log In
                </button>
                <button
                  onClick={() => { setError(''); setView('signup') }}
                  className="px-4 py-1.5 rounded-lg text-sm font-semibold bg-amber-400 text-slate-950 hover:bg-amber-300 transition"
                >
                  Sign Up
                </button>
              </>
            )}
          </nav>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-1">
        {view === 'landing' && (
          <div className="max-w-6xl mx-auto px-4 sm:px-6 py-12 sm:py-20">
            {/* Hero Section */}
            <div className="text-center max-w-2xl mx-auto space-y-6">
              <span className="inline-block px-3 py-1 text-xs font-semibold uppercase tracking-wider rounded-full bg-amber-400/10 text-amber-400 border border-amber-400/20">
                Curated Decade Collection
              </span>
              <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight leading-tight">
                Discover &amp; Rate the Best Films of the Last 10 Years
              </h1>
              <p className="text-base sm:text-lg text-slate-400">
                Explore 200 hand-picked releases, build your personal watchlist, and get tailored movie recommendations across all your devices.
              </p>
              <div className="flex flex-col sm:flex-row gap-3 justify-center pt-2">
                <button
                  onClick={() => { setError(''); setView('signup') }}
                  className="w-full sm:w-auto px-6 py-3 rounded-xl font-semibold bg-amber-400 text-slate-950 hover:bg-amber-300 transition"
                >
                  Create Free Account
                </button>
                <button
                  onClick={() => { setError(''); setView('login') }}
                  className="w-full sm:w-auto px-6 py-3 rounded-xl font-semibold bg-slate-800 text-white hover:bg-slate-700 transition"
                >
                  Sign In
                </button>
              </div>
            </div>

            {/* Catalog Preview Grid */}
            <section className="mt-16">
              <h2 className="text-lg font-semibold text-slate-300 mb-6">
                Featured in the Catalog
              </h2>
              {movies.length > 0 ? (
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                  {movies.map((movie, idx) => (
                    <div
                      key={movie.id || idx}
                      className="rounded-xl bg-slate-900 border border-slate-800 p-5 flex flex-col justify-between"
                    >
                      <div>
                        <h3 className="font-bold text-lg text-white">
                          {movie.title || 'Untitled Film'}
                        </h3>
                        <p className="text-xs text-amber-400 mt-1">
                          {movie.release_year || movie.year || 'Recent Release'}
                        </p>
                        <p className="text-sm text-slate-400 mt-3 line-clamp-3">
                          {movie.overview || movie.description || 'Available in your Neon catalog.'}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
                  {['Sci-Fi & Thrillers', 'Critically Acclaimed Dramas', 'Modern Action & Adventure'].map((category) => (
                    <div key={category} className="rounded-xl bg-slate-900 border border-slate-800 p-6">
                      <h3 className="font-semibold text-white">{category}</h3>
                      <p className="text-sm text-slate-400 mt-2">
                        Sign up to browse full ratings, genres, and personalized picks from our 200-movie archive.
                      </p>
                    </div>
                  ))}
                </div>
              )}
            </section>
          </div>
        )}

        {(view === 'login' || view === 'signup') && (
          <div className="max-w-md mx-auto px-4 py-12 sm:py-20">
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 sm:p-8 shadow-xl">
              <h2 className="text-2xl font-bold text-center">
                {view === 'signup' ? 'Create Your Account' : 'Welcome Back'}
              </h2>
              <p className="text-sm text-slate-400 text-center mt-1">
                {view === 'signup'
                  ? 'Sign up with your email and password to start rating movies.'
                  : 'Log in to access your movie catalog and recommendations.'}
              </p>

              {error && (
                <div className="mt-4 p-3 rounded-lg bg-red-500/10 border border-red-500/30 text-red-300 text-sm">
                  {error}
                </div>
              )}

              <form onSubmit={handleAuthSubmit} className="mt-6 space-y-4">
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-1">
                    Email Address
                  </label>
                  <input
                    type="email"
                    required
                    autoComplete="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="you@example.com"
                    className="w-full px-3.5 py-2.5 rounded-lg bg-slate-950 border border-slate-700 text-white focus:outline-none focus:border-amber-400"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-1">
                    Password
                  </label>
                  <input
                    type="password"
                    required
                    minLength={8}
                    autoComplete={view === 'signup' ? 'new-password' : 'current-password'}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="At least 8 characters"
                    className="w-full px-3.5 py-2.5 rounded-lg bg-slate-950 border border-slate-700 text-white focus:outline-none focus:border-amber-400"
                  />
                </div>

                {view === 'signup' && (
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-1">
                      Confirm Password
                    </label>
                    <input
                      type="password"
                      required
                      minLength={8}
                      autoComplete="new-password"
                      value={confirmPassword}
                      onChange={(e) => setConfirmPassword(e.target.value)}
                      placeholder="Re-enter your password"
                      className="w-full px-3.5 py-2.5 rounded-lg bg-slate-950 border border-slate-700 text-white focus:outline-none focus:border-amber-400"
                    />
                  </div>
                )}

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full py-2.5 rounded-lg font-semibold bg-amber-400 text-slate-950 hover:bg-amber-300 disabled:opacity-50 transition"
                >
                  {loading
                    ? 'Please wait...'
                    : view === 'signup'
                    ? 'Sign Up'
                    : 'Log In'}
                </button>
              </form>

              <p className="mt-6 text-center text-sm text-slate-400">
                {view === 'signup' ? 'Already have an account? ' : "Don't have an account? "}
                <button
                  type="button"
                  onClick={() => {
                    setError('')
                    setView(view === 'signup' ? 'login' : 'signup')
                  }}
                  className="text-amber-400 hover:underline font-medium"
                >
                  {view === 'signup' ? 'Log In' : 'Sign Up'}
                </button>
              </p>
            </div>
          </div>
        )}

        {view === 'dashboard' && user && (
          <div className="max-w-6xl mx-auto px-4 sm:px-6 py-10">
            <h2 className="text-2xl font-bold">Welcome, {user.email}</h2>
            <p className="text-slate-400 mt-1">
              You are signed in. Your movie catalog and rating features will appear here.
            </p>
          </div>
        )}
      </main>
    </div>
  )
}