import { Container, getRandom } from "@cloudflare/containers";
import { DurableObject } from "cloudflare:workers";

// One container class wrapping the Flask API's Docker image (../Dockerfile).
// Stateless request/response API, so we load-balance across instances with
// getRandom() rather than pinning requests to one named instance.
export class SentimentApi extends Container<Env> {
  defaultPort = 5000;
  pingEndpoint = "/health";
  sleepAfter = "10m"; // scale to zero after 10 minutes of no traffic
  enableInternet = true; // needed so the container can call the Groq API

  constructor(ctx: DurableObject["ctx"], env: Env) {
    super(ctx, env);
    // Forward the Worker secret into the container's process environment,
    // where src/api.py reads it via os.environ.get("GROQ_API_KEY").
    this.envVars = { GROQ_API_KEY: env.GROQ_API_KEY };
  }
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
