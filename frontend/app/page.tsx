"use client"

import { useState, useEffect, useRef } from "react"
import { useAuth } from "@/lib/auth"
import LoginPage from "@/components/LoginPage"
import Header from "@/components/Header"
import StatusBar from "@/components/StatusBar"
import FilterBar from "@/components/FilterBar"
import ChatBox from "@/components/ChatBox"
import MessageBubble from "@/components/MessageBubble"
import SuggestedQueries from "@/components/SuggestedQueries"
import LoadingSkeleton from "@/components/LoadingSkeleton"
import { querySchemes, getSchemes, getLastUpdated } from "@/lib/api"

type Message = {
  id: string
  role: "user" | "bot"
  text: string
  sources: string[]
  sourceUrls: Record<string, string>
}

export default function Home() {
  const { user, loading: authLoading } = useAuth()
  const [messages, setMessages] = useState<Message[]>([])
  const [loading, setLoading] = useState(false)
  const [filters, setFilters] = useState({ category: "All Categories", state: "All States" })
  const [schemeUrls, setSchemeUrls] = useState<Record<string, string>>({})
  const [lastUpdated, setLastUpdated] = useState<{ last_updated: string; scheme_count: number } | null>(null)
  
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!user) return
    // Fetch initial data only when logged in
    const init = async () => {
      const data = await getLastUpdated()
      setLastUpdated(data)

      const schemesList = await getSchemes()
      const urls: Record<string, string> = {}
      schemesList.forEach(s => {
        urls[s.name] = s.url
      })
      setSchemeUrls(urls)
    }
    init()
  }, [user])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages, loading])

  const handleSend = async (queryText: string) => {
    const userMsg: Message = {
      id: Date.now().toString(),
      role: "user",
      text: queryText,
      sources: [],
      sourceUrls: {}
    }
    setMessages(prev => [...prev, userMsg])
    setLoading(true)

    try {
      const result = await querySchemes(queryText, filters)
      const botMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: "bot",
        text: result.answer,
        sources: result.sources,
        sourceUrls: { ...schemeUrls, ...result.source_urls }
      }
      setMessages(prev => [...prev, botMsg])
    } catch (err) {
      const errorMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: "bot",
        text: "Sorry, there was an error processing your request. Please try again.",
        sources: [],
        sourceUrls: {}
      }
      setMessages(prev => [...prev, errorMsg])
    } finally {
      setLoading(false)
    }
  }

  // Show loading spinner while checking auth
  if (authLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <div className="google-spinner" style={{ width: 32, height: 32 }} />
      </div>
    )
  }

  // Show login page if not authenticated
  if (!user) {
    return <LoginPage />
  }

  return (
    <>
      <div className="app-bg" />
      <main className="flex flex-col h-screen max-h-screen overflow-hidden relative z-10">
        <Header />
        <StatusBar 
          lastUpdated={lastUpdated?.last_updated} 
          schemeCount={lastUpdated?.scheme_count} 
        />
        <FilterBar filters={filters} onChange={setFilters} />
        
        <div className="flex-1 overflow-y-auto w-full px-2 sm:px-4 lg:px-8 pb-4">
          <div className="max-w-4xl mx-auto py-6 flex flex-col min-h-full relative">
            <div className="glass-panel flex-1 rounded-2xl overflow-hidden flex flex-col relative shadow-xl">
              {messages.length === 0 && !loading ? (
                <div className="flex-1 flex items-center justify-center bg-white/20 overflow-y-auto">
                  <SuggestedQueries onSelect={handleSend} />
                </div>
              ) : (
                <div className="flex-1 overflow-y-auto p-4 sm:p-6 flex flex-col justify-end">
                  {messages.map(msg => (
                    <MessageBubble
                      key={msg.id}
                      role={msg.role}
                      text={msg.text}
                      sources={msg.sources}
                      sourceUrls={msg.sourceUrls}
                    />
                  ))}
                  {loading && <LoadingSkeleton />}
                  <div ref={messagesEndRef} />
                </div>
              )}

              <ChatBox onSend={handleSend} loading={loading} />
            </div>
          </div>
        </div>
      </main>
    </>
  )
}
