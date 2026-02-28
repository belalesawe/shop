import { vi } from "vitest";

// Mock the environment module before anything else
vi.mock("../src/lib/env.js", () => ({
  env: {
    DATABASE_URL: "postgresql://test:test@localhost:5432/test",
    PORT: 3001,
    CORS_ORIGIN: "http://localhost:3000",
  },
}));
