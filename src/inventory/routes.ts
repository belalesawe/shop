import { Router, Request, Response } from "express";
import { InventoryUpdateSchema, ReserveRequestSchema } from "./schema.js";
import * as service from "./service.js";
import { AppError } from "../lib/middleware.js";

const router = Router();

router.get("/:productId", async (req: Request, res: Response) => {
  const productId = Number(req.params.productId);
  if (isNaN(productId)) {
    throw new AppError(400, "Invalid product ID");
  }
  const inventory = await service.get(productId);
  res.json(inventory);
});

router.put("/:productId", async (req: Request, res: Response) => {
  const productId = Number(req.params.productId);
  if (isNaN(productId)) {
    throw new AppError(400, "Invalid product ID");
  }
  const parsed = InventoryUpdateSchema.safeParse(req.body);
  if (!parsed.success) {
    throw new AppError(400, parsed.error.errors[0]?.message ?? "Invalid input");
  }
  const inventory = await service.updateQuantity(productId, parsed.data.quantity);
  res.json(inventory);
});

router.post("/:productId/reserve", async (req: Request, res: Response) => {
  const productId = Number(req.params.productId);
  if (isNaN(productId)) {
    throw new AppError(400, "Invalid product ID");
  }
  const parsed = ReserveRequestSchema.safeParse(req.body);
  if (!parsed.success) {
    throw new AppError(400, parsed.error.errors[0]?.message ?? "Invalid input");
  }
  const inventory = await service.reserve(productId, parsed.data.quantity);
  res.json(inventory);
});

export default router;
