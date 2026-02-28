import express from "express";
import cors from "cors";
import { env } from "./lib/env.js";
import { errorHandler } from "./lib/middleware.js";
import productRoutes from "./products/routes.js";
import userRoutes from "./users/routes.js";
import inventoryRoutes from "./inventory/routes.js";

const app = express();

// Middleware
app.use(cors({ origin: env.CORS_ORIGIN }));
app.use(express.json());

// Health check
app.get("/", (_req, res) => {
  res.json({ status: "healthy", service: "ecommerce-api" });
});

// Routes
app.use("/products", productRoutes.products);
app.use("/categories", productRoutes.categories);
app.use("/users", userRoutes);
app.use("/inventory", inventoryRoutes);

// Error handler (must be last)
app.use(errorHandler);

export default app;
