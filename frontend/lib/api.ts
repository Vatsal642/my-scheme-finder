const BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

export async function querySchemes(
  query: string,
  filters: { category?: string; state?: string }
): Promise<{
  answer: string
  sources: string[]
  source_urls: Record<string, string>
}> {
  const res = await fetch(`${BASE}/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, filters })
  })
  if (!res.ok) throw new Error("Query failed")
  return res.json()
}

export async function getSchemes(): Promise<
  Array<{ name: string; url: string; category: string }>
> {
  try {
    const res = await fetch(`${BASE}/schemes`)
    if (!res.ok) return []
    return res.json()
  } catch {
    return []
  }
}

export async function getLastUpdated(): Promise<{
  last_updated: string
  scheme_count: number
  source: string
}> {
  try {
    const res = await fetch(`${BASE}/last-updated`)
    if (!res.ok) return { 
      last_updated: "Unknown", 
      scheme_count: 0, 
      source: "unknown" 
    }
    return res.json()
  } catch {
    return { 
      last_updated: "Unknown", 
      scheme_count: 0, 
      source: "unknown" 
    }
  }
}

export async function triggerRefresh(): Promise<boolean> {
  try {
    const res = await fetch(`${BASE}/refresh`, { method: "POST" })
    return res.ok
  } catch {
    return false
  }
}
