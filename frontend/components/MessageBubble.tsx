import React from "react"
import SchemeCard from "./SchemeCard"

// Parse a single line into React elements with bold and links
function parseLine(line: string): React.ReactNode[] {
  // First, split by bold markers **...**
  const boldParts = line.split(/(\*\*.*?\*\*)/g)
  const elements: React.ReactNode[] = []

  boldParts.forEach((part, i) => {
    if (part.startsWith("**") && part.endsWith("**")) {
      elements.push(
        <strong key={`b${i}`} className="font-semibold text-gray-900">
          {part.slice(2, -2)}
        </strong>
      )
    } else {
      // In non-bold text, find URLs and markdown links
      // Match: [text](url) OR bare https://... URLs
      const linkRegex = /(\[([^\]]+)\]\((https?:\/\/[^\s)]+)\))|(https?:\/\/[^\s,)]+)/g
      let lastIndex = 0
      let match: RegExpExecArray | null

      while ((match = linkRegex.exec(part)) !== null) {
        // Add text before the match
        if (match.index > lastIndex) {
          elements.push(part.slice(lastIndex, match.index))
        }

        if (match[1]) {
          // Markdown link [text](url)
          const linkText = match[2]
          const url = match[3]
          elements.push(
            <a
              key={`l${i}-${match.index}`}
              href={url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-indigo-600 hover:text-indigo-800 underline underline-offset-2 font-medium transition-colors"
            >
              {linkText}
            </a>
          )
        } else if (match[4]) {
          // Bare URL
          const url = match[4]
          // Clean trailing punctuation
          const cleanUrl = url.replace(/[.,;:!?]+$/, "")
          elements.push(
            <a
              key={`u${i}-${match.index}`}
              href={cleanUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="text-indigo-600 hover:text-indigo-800 underline underline-offset-2 font-medium transition-colors break-all"
            >
              {cleanUrl}
            </a>
          )
          // Add back trailing punctuation that was stripped
          if (cleanUrl.length < url.length) {
            elements.push(url.slice(cleanUrl.length))
          }
        }

        lastIndex = match.index + match[0].length
      }

      // Add remaining text after last match
      if (lastIndex < part.length) {
        elements.push(part.slice(lastIndex))
      }
    }
  })

  return elements
}

export default function MessageBubble({
  role,
  text,
  sources = [],
  sourceUrls = {}
}: {
  role: "user" | "bot"
  text: string
  sources?: string[]
  sourceUrls?: Record<string, string>
}) {
  if (role === "user") {
    return (
      <div className="flex justify-end mb-6 w-full px-4 animate-in fade-in slide-in-from-bottom-2 duration-300">
        <div className="bg-gradient-to-r from-indigo-500 to-purple-600 text-white rounded-2xl rounded-tr-sm px-5 py-3 max-w-[85%] sm:max-w-[75%] shadow-md">
          <p className="whitespace-pre-wrap text-[15px] font-medium">{text}</p>
        </div>
      </div>
    )
  }

  const formatText = (content: string) => {
    return content.split("\n").map((line, i, arr) => (
      <React.Fragment key={i}>
        {parseLine(line)}
        {i !== arr.length - 1 && <br />}
      </React.Fragment>
    ))
  }

  return (
    <div className="flex mb-6 w-full px-4 animate-in fade-in slide-in-from-bottom-2 duration-300">
      <div className="flex gap-3 max-w-[95%] sm:max-w-[85%]">
        <div className="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-100 to-purple-100 flex items-center justify-center flex-shrink-0 mt-1 border border-indigo-200 shadow-sm">
          <span className="text-indigo-600 text-xs font-bold">AI</span>
        </div>
        <div className="bg-white/80 backdrop-blur-md text-[#111827] rounded-2xl rounded-tl-sm px-5 py-4 shadow-sm border border-white/50">
          <div className="whitespace-pre-wrap text-[15px] leading-relaxed text-gray-800">
            {formatText(text)}
          </div>
          
          {sources.length > 0 && (
            <div className="mt-4 pt-3 border-t border-gray-200/60">
              <p className="text-[11px] text-indigo-600/80 mb-2 uppercase tracking-wider font-bold">Sources verified from:</p>
              <div className="flex flex-wrap gap-2">
                {sources.map(s => (
                  <SchemeCard key={s} name={s} url={sourceUrls[s]} />
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
