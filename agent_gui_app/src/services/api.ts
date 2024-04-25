import { ref } from 'vue'
import { baseUrl } from './appConfig.ts'
import { Message } from './database.ts'

export type GenerateCompletionRequest = {
  prompt?: string
}

export type GenerateCompletionCompletedResponse = {
  response: string
  done: boolean
}

export type GenerateCompletionPartResponse = {
  response: string
  done: boolean
}

export type GenerateCompletionResponse = GenerateCompletionCompletedResponse | GenerateCompletionPartResponse

export type Model = {
  name: string
  modified_at: string
  size: number
}

// Define a method to get the full API URL for a given path
const getApiUrl = (path: string) =>
  `${baseUrl.value || 'http://localhost:800/api'}${path}`

const abortController = ref<AbortController>(new AbortController())
const signal = ref<AbortSignal>(abortController.value.signal)

// Define the API client functions
export const useApi = () => {
  const error = ref(null)

  const generateCompletion = async (
    request: GenerateCompletionRequest,
    onDataReceived: (data: GenerateCompletionResponse) => void,
  ): Promise<GenerateCompletionResponse[]> => {
    const res = await fetch(getApiUrl('/generate'), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    })
    alert(res)
    if (!res.ok) {
      throw new Error('Network response was not ok')
    }

    const reader = res.body?.getReader()
    let results: GenerateCompletionResponse[] = []

    if (reader) {
      while (true) {
        const { done, value } = await reader.read()
        if (done) {
          break
        }

        const chunk = new TextDecoder().decode(value)
        const parsedChunk: GenerateCompletionPartResponse = JSON.parse(chunk)

        onDataReceived(parsedChunk)
        results.push(parsedChunk)
      }
    }

    return results
  }

  return {
    error,
    generateCompletion
  }
}
