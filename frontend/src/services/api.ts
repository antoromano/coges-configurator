import type {
  FinestreCatalog,
  FinestreQuoteRequestCreate,
  FinestreConfiguration,
  FinestrePriceCalculationResponse,
  PergoleCatalog,
  PergoleQuoteRequestCreate,
  PergoleConfiguration,
  PergolePriceCalculationResponse,
  PortonciniCatalog,
  PortonciniQuoteRequestCreate,
  PortonciniConfiguration,
  PortonciniPriceCalculationResponse,
  ProductFamily,
  QuoteRequestCreatedResponse,
  QuoteRequestOut,
  QuoteRequestStatus,
} from "../types";

const API_BASE_URL = import.meta.env.VITE_API_URL;

export class ApiError extends Error {}

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    let detail = response.statusText;
    try {
      const body = await response.json();
      if (body?.detail) {
        detail = typeof body.detail === "string" ? body.detail : JSON.stringify(body.detail);
      }
    } catch {
      // corpo non JSON, si usa lo statusText come messaggio
    }
    throw new ApiError(detail);
  }
  return response.json() as Promise<T>;
}

function get<T>(path: string, staffToken?: string): Promise<T> {
  return fetch(`${API_BASE_URL}${path}`, {
    headers: staffToken ? { "X-Staff-Token": staffToken } : undefined,
  }).then(handleResponse<T>);
}

function post<T>(path: string, body: unknown, staffToken?: string): Promise<T> {
  return fetch(`${API_BASE_URL}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(staffToken ? { "X-Staff-Token": staffToken } : {}),
    },
    body: JSON.stringify(body),
  }).then(handleResponse<T>);
}

function patch<T>(path: string, body: unknown, staffToken: string): Promise<T> {
  return fetch(`${API_BASE_URL}${path}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json", "X-Staff-Token": staffToken },
    body: JSON.stringify(body),
  }).then(handleResponse<T>);
}

export function fetchProductFamilies(): Promise<ProductFamily[]> {
  return get<ProductFamily[]>("/api/product-families");
}

export function fetchFinestreCatalog(): Promise<FinestreCatalog> {
  return get<FinestreCatalog>("/api/catalog/finestre");
}

export function calculateFinestrePrice(
  config: FinestreConfiguration,
): Promise<FinestrePriceCalculationResponse> {
  return post<FinestrePriceCalculationResponse>("/api/calculate-price/finestre", config);
}

export function submitFinestreQuoteRequest(
  payload: FinestreQuoteRequestCreate,
): Promise<QuoteRequestCreatedResponse> {
  return post<QuoteRequestCreatedResponse>("/api/quote-requests/finestre", payload);
}

export function fetchPortonciniCatalog(): Promise<PortonciniCatalog> {
  return get<PortonciniCatalog>("/api/catalog/portoncini");
}

export function calculatePortonciniPrice(
  config: PortonciniConfiguration,
): Promise<PortonciniPriceCalculationResponse> {
  return post<PortonciniPriceCalculationResponse>("/api/calculate-price/portoncini", config);
}

export function submitPortonciniQuoteRequest(
  payload: PortonciniQuoteRequestCreate,
): Promise<QuoteRequestCreatedResponse> {
  return post<QuoteRequestCreatedResponse>("/api/quote-requests/portoncini", payload);
}

export function fetchPergoleCatalog(): Promise<PergoleCatalog> {
  return get<PergoleCatalog>("/api/catalog/pergole");
}

export function calculatePergolePrice(
  config: PergoleConfiguration,
): Promise<PergolePriceCalculationResponse> {
  return post<PergolePriceCalculationResponse>("/api/calculate-price/pergole", config);
}

export function submitPergoleQuoteRequest(
  payload: PergoleQuoteRequestCreate,
): Promise<QuoteRequestCreatedResponse> {
  return post<QuoteRequestCreatedResponse>("/api/quote-requests/pergole", payload);
}

// ---------------------------------------------------------------------------
// Area staff (protetta da password condivisa, vedi StaffQuoteRequests.tsx)
// ---------------------------------------------------------------------------

export function fetchQuoteRequests(staffToken: string): Promise<QuoteRequestOut[]> {
  return get<QuoteRequestOut[]>("/api/quote-requests", staffToken);
}

export function updateQuoteRequestStatus(
  id: number,
  status: QuoteRequestStatus,
  staffToken: string,
): Promise<QuoteRequestOut> {
  return patch<QuoteRequestOut>(`/api/quote-requests/${id}/status`, { status }, staffToken);
}
