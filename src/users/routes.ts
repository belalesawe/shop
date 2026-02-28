import { Router, Request, Response } from "express";
import { CreateUserSchema } from "./schema.js";
import * as service from "./service.js";
import { AppError } from "../lib/middleware.js";

const router = Router();

router.post("/", async (req: Request, res: Response) => {
  const parsed = CreateUserSchema.safeParse(req.body);
  if (!parsed.success) {
    throw new AppError(400, parsed.error.errors[0]?.message ?? "Invalid input");
  }
  const user = await service.create(parsed.data);
  res.status(201).json(user);
});

router.get("/:userId", async (req: Request, res: Response) => {
  const id = Number(req.params.userId);
  if (isNaN(id)) {
    throw new AppError(400, "Invalid user ID");
  }
  const user = await service.getById(id);
  res.json(user);
});

router.get("/", async (_req: Request, res: Response) => {
  const users = await service.list();
  res.json(users);
});

export default router;
