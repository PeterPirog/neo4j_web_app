export function apiError(error: unknown): Error {
  if (error && typeof error === "object" && "detail" in error) {
    return new Error(String((error as { detail: unknown }).detail));
  }
  return new Error("API request failed");
}
