import express from "express";
import cors from "cors";
import { errorHandler } from "./lib/middleware.js";
import { productRoutes, categoryRoutes } from "./products/routes.js";

const app = express();

// Middleware
app.use(cors({ origin: process.env.CORS_ORIGIN || "http://localhost:3000" }));
app.use(express.json());

// Health check
app.get("/", (_req, res) => {
  res.json({ status: "healthy", service: "ecommerce-monolith" });
});

// Domain routes
app.use("/categories", categoryRoutes);
app.use("/products", productRoutes);

// Global error handler (must be registered last)
app.use(errorHandler);

export default app;
