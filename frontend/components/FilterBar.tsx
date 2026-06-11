export default function FilterBar({
  filters,
  onChange
}: {
  filters: { category: string; state: string }
  onChange: (filters: { category: string; state: string }) => void
}) {
  const categories = [
    "All Categories", "Agriculture", "Education", "Health", 
    "Housing", "Women", "Employment", "Finance", "Disability", "Social Welfare"
  ]
  const states = [
    "All States", "Central Schemes", "Maharashtra", "Delhi", 
    "Karnataka", "Tamil Nadu", "Uttar Pradesh", "Bihar", "Rajasthan", 
    "West Bengal", "Gujarat", "Punjab", "Madhya Pradesh"
  ]

  return (
    <div className="glass-header px-4 py-3 flex flex-wrap sm:flex-nowrap gap-3 sm:gap-4 z-10 relative shadow-sm">
      <div className="flex flex-col flex-1 min-w-[140px] max-w-[200px] sm:max-w-none">
        <label className="text-[10px] sm:text-[11px] text-gray-600 mb-1 font-bold uppercase tracking-wider">Category</label>
        <select 
          className="bg-white/60 backdrop-blur-sm border border-white/80 rounded-lg text-sm px-2 sm:px-3 py-2 text-gray-800 font-medium focus:outline-none focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 transition-all shadow-inner w-full"
          value={filters.category}
          onChange={e => onChange({ ...filters, category: e.target.value })}
        >
          {categories.map(c => <option key={c} value={c}>{c}</option>)}
        </select>
      </div>
      <div className="flex flex-col flex-1 min-w-[140px] max-w-[200px] sm:max-w-none">
        <label className="text-[10px] sm:text-[11px] text-gray-600 mb-1 font-bold uppercase tracking-wider">State / Coverage</label>
        <select 
          className="bg-white/60 backdrop-blur-sm border border-white/80 rounded-lg text-sm px-2 sm:px-3 py-2 text-gray-800 font-medium focus:outline-none focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 transition-all shadow-inner w-full"
          value={filters.state}
          onChange={e => onChange({ ...filters, state: e.target.value })}
        >
          {states.map(s => <option key={s} value={s}>{s}</option>)}
        </select>
      </div>
    </div>
  )
}
