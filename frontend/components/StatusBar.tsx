export default function StatusBar({
  lastUpdated,
  schemeCount
}: {
  lastUpdated?: string
  schemeCount?: number
}) {
  return (
    <div className="bg-white/40 backdrop-blur-md border-b border-white/40 px-4 py-1.5 text-center text-gray-600 text-xs font-medium z-10 relative">
      {!lastUpdated ? (
        <span className="animate-pulse">Checking data status...</span>
      ) : (
        <span>
          Last updated: {lastUpdated} · {schemeCount} schemes indexed · Powered by RAG + Llama 3
        </span>
      )}
    </div>
  )
}
