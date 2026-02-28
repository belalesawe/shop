import prisma from "../lib/db.js";
import { AppError } from "../lib/middleware.js";

export async function get(productId: number) {
  const inventory = await prisma.inventory.findUnique({
    where: { productId },
  });
  if (!inventory) {
    throw new AppError(404, "Inventory not found");
  }
  return inventory;
}

export async function updateQuantity(productId: number, quantity: number) {
  const inventory = await prisma.inventory.findUnique({
    where: { productId },
  });
  if (!inventory) {
    throw new AppError(404, "Inventory not found");
  }

  return prisma.inventory.update({
    where: { productId },
    data: {
      quantity,
      lastUpdated: new Date(),
    },
  });
}

export async function reserve(productId: number, quantity: number) {
  const inventory = await prisma.inventory.findUnique({
    where: { productId },
  });
  if (!inventory) {
    throw new AppError(404, "Inventory not found");
  }

  const available = inventory.quantity - inventory.reserved;
  if (available < quantity) {
    throw new AppError(
      400,
      `Insufficient inventory. Available: ${available}, Requested: ${quantity}`,
    );
  }

  // Use atomic increment for better concurrency
  return prisma.inventory.update({
    where: { productId },
    data: {
      reserved: { increment: quantity },
      lastUpdated: new Date(),
    },
  });
}
