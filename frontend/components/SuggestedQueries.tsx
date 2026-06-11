export default function SuggestedQueries({
  onSelect
}: {
  onSelect: (query: string) => void
}) {
  const queries = [
    "I am a 28 year old woman farmer from UP, income below 1.5 lakh",
    "I am a student from Bihar looking for a scholarship",
    "I want to start a small business, I belong to SC category",
    "I am a 45 year old BPL family member needing health coverage",
    "I am a daily wage worker in Delhi with no savings"
  ]

  return (
    <div className="flex flex-col items-center justify-center py-10 px-4 w-full h-full text-center">
      <h2 className="text-gray-700 font-bold text-lg mb-6 drop-shadow-sm">Try asking...</h2>
      <div className="flex flex-wrap justify-center gap-3 max-w-3xl">
        {queries.map(q => (
          <button
            key={q}
            onClick={() => onSelect(q)}
            className="bg-white/70 backdrop-blur-sm border border-indigo-200/50 text-indigo-700 px-5 py-2.5 rounded-full text-sm font-medium hover:bg-white hover:text-indigo-900 hover:shadow-md hover:-translate-y-0.5 transition-all shadow-sm"
          >
            {q}
          </button>
        ))}
      </div>
    </div>
  )
}
