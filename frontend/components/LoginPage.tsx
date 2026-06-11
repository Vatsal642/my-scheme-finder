"use client"

import { useState } from "react"
import { useAuth } from "@/lib/auth"

export default function LoginPage() {
  const { login } = useAuth()
  const [showForm, setShowForm] = useState(false)
  const [name, setName] = useState("")
  const [email, setEmail] = useState("")
  const [animating, setAnimating] = useState(false)

  const handleGoogleClick = () => {
    setAnimating(true)
    // Simulate Google OAuth popup delay
    setTimeout(() => {
      setShowForm(true)
      setAnimating(false)
    }, 800)
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!name.trim() || !email.trim()) return

    const initials = name
      .split(" ")
      .map((n) => n[0])
      .join("")
      .toUpperCase()
      .slice(0, 2)

    login({
      name: name.trim(),
      email: email.trim(),
      avatar: initials,
    })
  }

  return (
    <div className="login-page">
      {/* Animated background */}
      <div className="login-bg">
        <div className="login-bg-gradient" />
        <div className="login-bg-circles">
          <div className="circle c1" />
          <div className="circle c2" />
          <div className="circle c3" />
        </div>
      </div>

      <div className="login-container">
        {/* Logo & Branding */}
        <div className="login-branding">
          <div className="login-logo">
            <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
              <rect width="48" height="48" rx="12" fill="url(#logo-grad)" />
              <path
                d="M14 24C14 18.477 18.477 14 24 14C29.523 14 34 18.477 34 24C34 29.523 29.523 34 24 34"
                stroke="white"
                strokeWidth="2.5"
                strokeLinecap="round"
              />
              <path
                d="M24 20V28M20 24H28"
                stroke="white"
                strokeWidth="2.5"
                strokeLinecap="round"
              />
              <defs>
                <linearGradient id="logo-grad" x1="0" y1="0" x2="48" y2="48">
                  <stop stopColor="#4F46E5" />
                  <stop offset="1" stopColor="#7C3AED" />
                </linearGradient>
              </defs>
            </svg>
          </div>
          <h1 className="login-title">Scheme Finder</h1>
          <p className="login-subtitle">
            Discover thousands of government schemes tailored specifically to your profile. We&apos;ll match you with the support you deserve.
          </p>
        </div>

        {/* Login Card */}
        <div className="login-card">
          {!showForm ? (
            <div className="login-card-inner">
              <h2 className="login-card-title">Welcome</h2>
              <p className="login-card-desc">
                Sign in to get personalized scheme recommendations
              </p>

              <button
                className={`google-btn ${animating ? "google-btn-loading" : ""}`}
                onClick={handleGoogleClick}
                disabled={animating}
              >
                {animating ? (
                  <div className="google-spinner" />
                ) : (
                  <svg className="google-icon" viewBox="0 0 24 24">
                    <path
                      d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z"
                      fill="#4285F4"
                    />
                    <path
                      d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                      fill="#34A853"
                    />
                    <path
                      d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                      fill="#FBBC05"
                    />
                    <path
                      d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                      fill="#EA4335"
                    />
                  </svg>
                )}
                <span>{animating ? "Connecting..." : "Continue with Google"}</span>
              </button>

              <div className="login-divider">
                <span>Trusted by thousands of citizens</span>
              </div>

              <div className="login-features">
                <div className="login-feature">
                  <span className="feature-icon">🏛️</span>
                  <span>700+ Government Schemes</span>
                </div>
                <div className="login-feature">
                  <span className="feature-icon">🤖</span>
                  <span>AI-Powered Matching</span>
                </div>
                <div className="login-feature">
                  <span className="feature-icon">🔄</span>
                  <span>Auto-Updated Weekly</span>
                </div>
              </div>
            </div>
          ) : (
            <div className="login-card-inner fade-in">
              <h2 className="login-card-title">Complete Sign In</h2>
              <p className="login-card-desc">
                Enter your details to continue
              </p>

              <form onSubmit={handleSubmit} className="login-form">
                <div className="form-group">
                  <label htmlFor="name">Full Name</label>
                  <input
                    id="name"
                    type="text"
                    placeholder="e.g. Rahul Kumar"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                    autoFocus
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="email">Email Address</label>
                  <input
                    id="email"
                    type="email"
                    placeholder="e.g. rahul@gmail.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                </div>
                <button type="submit" className="login-submit-btn">
                  Start Finding Schemes
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M5 12h14M12 5l7 7-7 7" />
                  </svg>
                </button>
              </form>

              <button
                className="back-btn"
                onClick={() => setShowForm(false)}
              >
                ← Back to sign in options
              </button>
            </div>
          )}
        </div>

        <p className="login-footer">
          🇮🇳 Made for every Indian citizen · Free & open
        </p>
      </div>
    </div>
  )
}
