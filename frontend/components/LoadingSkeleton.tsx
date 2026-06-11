export default function LoadingSkeleton() {
  return (
    <div className="flex mb-6 w-full px-4 animate-pulse">
      <div className="flex gap-3 w-full max-w-[85%]">
        <div className="w-8 h-8 rounded-full bg-gray-200 flex-shrink-0 mt-1"></div>
        <div className="bg-[#f3f4f6] rounded-2xl rounded-tl-sm p-5 w-full">
          <div className="h-4 bg-gray-200 rounded w-[80%] mb-3"></div>
          <div className="h-4 bg-gray-200 rounded w-[60%] mb-3"></div>
          <div className="h-4 bg-gray-200 rounded w-[40%]"></div>
        </div>
      </div>
    </div>
  )
}
