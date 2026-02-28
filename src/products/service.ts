import prisma from "../lib/db.js";
import { AppError } from "../lib/middleware.js";
import type { CreateCategory, CreateProduct } from "./schema.js";

export async function createCategory(data: CreateCategory) {
  return prisma.category.create({
    data: {
      name: data.name,
      description: data.description ?? null,
    },
  });
}

export async function listCategories() {
  return prisma.category.findMany();
}

export async function createProduct(data: CreateProduct) {
  // Verify category exists if provided
  if (data.category_id) {
    const category = await prisma.category.findUnique({
      where: { id: data.category_id },
    });
    if (!category) {
      throw new AppError(404, "Category not found");
    }
  }

  const product = await prisma.product.create({
    data: {
      name: data.name,
      description: data.description ?? null,
      price: data.price,
      categoryId: data.category_id ?? null,
    },
  });

  // Initialize inventory for new product
  await prisma.inventory.create({
    data: {
      productId: product.id,
      quantity: 0,
      reserved: 0,
    },
  });

  return product;
}

export async function getProduct(id: number) {
  const product = await prisma.product.findUnique({ where: { id } });
  if (!product) {
    throw new AppError(404, "Product not found");
  }
  return product;
}

export async function listProducts() {
  return prisma.product.findMany();
}
