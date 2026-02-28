import prisma from "../lib/db.js";
import { AppError } from "../lib/middleware.js";
import type { CreateUser } from "./schema.js";

export async function create(data: CreateUser) {
  // Check if email already exists (pre-query pattern matching source)
  const existing = await prisma.user.findUnique({
    where: { email: data.email },
  });
  if (existing) {
    throw new AppError(400, "Email already registered");
  }

  return prisma.user.create({
    data: {
      email: data.email,
      name: data.name,
    },
  });
}

export async function getById(id: number) {
  const user = await prisma.user.findUnique({ where: { id } });
  if (!user) {
    throw new AppError(404, "User not found");
  }
  return user;
}

export async function list() {
  return prisma.user.findMany();
}
