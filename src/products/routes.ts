import { Router } from "express";
import type { Request, Response } from "express";
import prisma from "../lib/db.js";
import { createCategorySchema, createProductSchema } from "./schema.js";
import * as service from "./service.js";
import type { ProductResponse, CategoryResponse } from "./schema.js";

export const categoryRoutes = Router();
export const productRoutes = Router();

// --- Category Routes ---

categoryRoutes.post("/", async (req: Request, res: Response) => {
  const parsed = createCategorySchema.safeParse(req.body);
  if (!parsed.success) {
    res.status(400).json({ detail: parsed.error.issues[0].message });
    return;
  }

  const category = await service.createCategory(prisma, parsed.data);
  const response: CategoryResponse = {
    id: category.id,
    name: category.name,
    description: category.description,
  };
  res.status(201).json(response);
});

categoryRoutes.get("/", async (_req: Request, res: Response) => {
  const categories = await service.listCategories(prisma);
  const response: CategoryResponse[] = categories.map((c) => ({
    id: c.id,
    name: c.name,
    description: c.description,
  }));
  res.json(response);
});

// --- Product Routes ---

productRoutes.post("/", async (req: Request, res: Response) => {
  const parsed = createProductSchema.safeParse(req.body);
  if (!parsed.success) {
    res.status(400).json({ detail: parsed.error.issues[0].message });
    return;
  }

  const product = await service.createProduct(prisma, parsed.data);
  const response: ProductResponse = {
    id: product.id,
    name: product.name,
    description: product.description,
    price: product.price.toString(),
    category_id: product.categoryId,
    created_at: product.createdAt.toISOString(),
  };
  res.status(201).json(response);
});

productRoutes.get("/:productId", async (req: Request, res: Response) => {
  const productId = parseInt(req.params["productId"] as string, 10);
  if (isNaN(productId)) {
    res.status(400).json({ detail: "Invalid product ID" });
    return;
  }

  const product = await service.getProduct(prisma, productId);
  const response: ProductResponse = {
    id: product.id,
    name: product.name,
    description: product.description,
    price: product.price.toString(),
    category_id: product.categoryId,
    created_at: product.createdAt.toISOString(),
  };
  res.json(response);
});

productRoutes.get("/", async (_req: Request, res: Response) => {
  const products = await service.listProducts(prisma);
  const response: ProductResponse[] = products.map((p) => ({
    id: p.id,
    name: p.name,
    description: p.description,
    price: p.price.toString(),
    category_id: p.categoryId,
    created_at: p.createdAt.toISOString(),
  }));
  res.json(response);
});
