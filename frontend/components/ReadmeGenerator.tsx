"use client"

import { useState } from "react"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Form, FormControl, FormField, FormItem, FormMessage } from "@/components/ui/form"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { AlertCircle } from "lucide-react"
import ReadmeSkeleton from "@/components/ReadmeSkeleton"
import ReadmeDisplay from "@/components/ReadmeDisplay"

const formSchema = z.object({
  repoUrl: z
    .string()
    .url("Please enter a valid URL")
    .regex(/^https:\/\/github\.com\/[\w-]+\/[\w-]+$/, "Please enter a valid GitHub repository URL"),
})

export default function ReadmeGenerator() {
  const [isLoading, setIsLoading] = useState(false)
  const [readmeContent, setReadmeContent] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      repoUrl: "",
    },
  })

  async function onSubmit(values: z.infer<typeof formSchema>) {
    setIsLoading(true)
    setError(null)
    setReadmeContent(null)

    try {
      const response = await fetch("https://api.readmegen.example/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ repoUrl: values.repoUrl }),
      })

      if (!response.ok) {
        throw new Error("Failed to generate README")
      }

      const data = await response.json()
      setReadmeContent(data.readme)
    } catch (err) {
      setError("An error occurred while generating the README. Please try again.")
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="w-full max-w-3xl">
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
          <FormField
            control={form.control}
            name="repoUrl"
            render={({ field }) => (
              <FormItem>
                <FormControl>
                  <Input placeholder="https://github.com/username/repository" {...field} className="text-lg py-6" />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <Button type="submit" className="w-full py-6 text-lg" disabled={isLoading}>
            {isLoading ? "Generating..." : "Generate README"}
          </Button>
        </form>
      </Form>

      {error && (
        <Alert variant="destructive" className="mt-6">
          <AlertCircle className="h-4 w-4" />
          <AlertTitle>Error</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {isLoading && <ReadmeSkeleton />}

      {readmeContent && <ReadmeDisplay content={readmeContent} />}
    </div>
  )
}

