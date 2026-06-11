export default function SchemeCard({
  name,
  url
}: {
  name: string
  url?: string
}) {
  const content = (
    <span className="inline-flex items-center gap-1 bg-[#e0f2fe] text-[#0369a1] text-xs font-medium px-2.5 py-1 rounded-full max-w-xs truncate border border-blue-200 shadow-sm">
      <span className="truncate">{name}</span>
      {url && <span className="text-[10px] ml-1">↗</span>}
    </span>
  )

  if (url && url !== "") {
    return (
      <a href={url} target="_blank" rel="noopener noreferrer" className="hover:opacity-80 transition-opacity">
        {content}
      </a>
    )
  }
  return content
}
