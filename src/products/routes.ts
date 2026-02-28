import { Router, Request, Response } from "express";
import { CreateCategorySchema, CreateProductSchema } from "./schema.js";
import * as service from "./service.js";
import { AppError } from "../lib/middleware.js";

const products = Router();
const categories = Router();

// --- Categories ---

categories.post("/", async (req: Request, res: Response) => {
  const parsed = CreateCategorySchema.safeParse(req.body);
  if (!parsed.success) {
    throw new AppError(400, parsed.error.errors[0]?.message ?? "Invalid input");
  }
  const category = await service.createCategory(parsed.data);
  res.status(201).json(category);
});

categories.get("/", async (_req: Request, res: Response) => {
  const result = await service.listCategories();
  res.json(result);
});

// --- Products ---

products.post("/", async (req: Request, res: Response) => {
  const parsed = CreateProductSchema.safeParse(req.body);
  if (!parsed.success) {
    throw new AppError(400, parsed.error.errors[0]?.message ?? "Invalid input");
  }
  const product = await service.createProduct(parsed.data);
  res.status(201).json(product);
});

products.get("/:productId", async (req: Request, res: Response) => {
  const id = Number(req.params.productId);
  if (isNaN(id)) {
    throw new AppError(400, "Invalid product ID");
  }
  const product = await service.getProduct(id);
  res.json(product);
});

products.get("/", async (_req: Request, res: Response) => {
  const result = await service.listProducts();
  res.json(result);
});

export default { products, categories };
