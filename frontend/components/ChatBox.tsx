import { useState, KeyboardEvent } from "react"

export default function ChatBox({
  onSend,
  loading
}: {
  onSend: (text: string) => void
  loading: boolean
}) {
  const [text, setText] = useState("")

  const handleSend = () => {
    if (text.trim() && !loading) {
      onSend(text)
      setText("")
    }
  }

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="glass-chat-box p-3 sm:p-4 rounded-b-2xl w-full">
      <div className="max-w-4xl mx-auto flex gap-2 sm:gap-3 items-end">
        <textarea
          className="flex-1 bg-white/60 backdrop-blur-sm border border-white/80 rounded-xl p-3 sm:p-3.5 resize-none focus:outline-none focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 min-h-[52px] max-h-[120px] shadow-inner text-gray-800 placeholder-gray-500 transition-all text-sm sm:text-base"
          placeholder="Describe yourself — e.g. I am a 32 year old woman farmer..."
          value={text}
          onChange={e => setText(e.target.value)}
          onKeyDown={handleKeyDown}
          rows={text.split('\n').length > 4 ? 4 : Math.max(1, text.split('\n').length)}
        />
        <button
          onClick={handleSend}
          disabled={!text.trim() || loading}
          className={`px-4 sm:px-6 py-3 sm:py-3.5 rounded-xl font-semibold whitespace-nowrap transition-all flex items-center justify-center h-[52px] shadow-sm ${
            !text.trim() || loading
              ? "bg-white/50 text-gray-400 cursor-not-allowed border border-white/50"
              : "bg-gradient-to-r from-indigo-500 to-purple-600 text-white hover:shadow-md hover:-translate-y-0.5 border border-transparent"
          }`}
          aria-label="Find Schemes"
        >
          {loading ? (
            <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          ) : (
            <>
              <span className="hidden sm:inline mr-2">Find Schemes</span>
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="w-5 h-5">
                <path d="M3.105 2.289a.75.75 0 00-.826.95l1.414 4.925A1.5 1.5 0 005.135 9.25h6.115a.75.75 0 010 1.5H5.135a1.5 1.5 0 00-1.442 1.086l-1.414 4.926a.75.75 0 00.826.95 28.896 28.896 0 0015.293-7.154.75.75 0 000-1.115A28.897 28.897 0 003.105 2.289z" />
              </svg>
            </>
          )}
        </button>
      </div>
    </div>
  )
}
