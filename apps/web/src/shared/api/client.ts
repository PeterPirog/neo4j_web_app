import { createApiClient } from "@neo4j-web-app/api-client";

import { API_BASE_URL } from "@/shared/config/env";


export const apiClient = createApiClient(API_BASE_URL);
