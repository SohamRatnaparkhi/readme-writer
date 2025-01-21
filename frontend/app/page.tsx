import ReadmeGenerator from "@/components/ReadmeGenerator"

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-gray-100 to-gray-200 flex flex-col items-center justify-center p-4 sm:p-8">
      <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold text-gray-800 mb-6 text-center">
        GitHub README Generator
      </h1>
      <p className="text-lg sm:text-xl text-gray-600 mb-8 text-center max-w-2xl">
        Automatically generate beautiful README files for your GitHub repositories
      </p>
      <ReadmeGenerator />
    </main>
  )
}

