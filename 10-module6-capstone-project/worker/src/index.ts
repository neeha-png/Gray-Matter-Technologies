import { Container, getRandom } from "@cloudflare/containers";

// One container class wrapping the Flask API's Docker image (../Dockerfile).
// Stateless request/response API, so we load-balance across instances with
// getRandom() rather than pinning requests to one named instance.
export class SentimentApi extends Container {
  defaultPort = 5000;
  pingEndpoint = "/health";
  sleepAfter = "10m"; // scale to zero after 10 minutes of no traffic
  enableInternet = true; // needed so the container can call the Gemini API
}

// Env is declared globally by `wrangler types` in worker-configuration.d.ts

const API_PATHS = ["/health", "/predict", "/explain"];

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    if (API_PATHS.includes(url.pathname)) {
      const container = await getRandom(env.SENTIMENT_CONTAINER, 3);
      await container.startAndWaitForPorts();
      return container.fetch(request);
    }

    // Everything else (index.html, etc.) is served as a static asset.
    return env.ASSETS.fetch(request);
  },
};
