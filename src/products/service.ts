import type { PrismaClient } from "@prisma/client";
import { AppError } from "../lib/middleware.js";
import type { CreateCategoryInput, CreateProductInput } from "./schema.js";

export async function createCategory(
  prisma: PrismaClient,
  data: CreateCategoryInput,
) {
  const category = await prisma.category.create({
    data: {
      name: data.name,
      description: data.description ?? null,
    },
  });
  return category;
}

export async function listCategories(prisma: PrismaClient) {
  return prisma.category.findMany();
}

export async function createProduct(
  prisma: PrismaClient,
  data: CreateProductInput,
) {
  // Verify category exists if provided
  if (data.category_id) {
    const category = await prisma.category.findUnique({
      where: { id: data.category_id },
    });
    if (!category) {
      throw new AppError(404, "Category not found");
    }
  }

  // Create product and initialize inventory in a transaction
  const product = await prisma.$transaction(async (tx) => {
    const newProduct = await tx.product.create({
      data: {
        name: data.name,
        description: data.description ?? null,
        price: data.price,
        categoryId: data.category_id ?? null,
      },
    });

    // Initialize inventory for new product (matches products/api.py:49-53)
    await tx.inventory.create({
      data: {
        productId: newProduct.id,
        quantity: 0,
        reserved: 0,
      },
    });

    return newProduct;
  });

  return product;
}

export async function getProduct(prisma: PrismaClient, productId: number) {
  const product = await prisma.product.findUnique({
    where: { id: productId },
  });
  if (!product) {
    throw new AppError(404, "Product not found");
  }
  return product;
}

export async function listProducts(prisma: PrismaClient) {
  return prisma.product.findMany();
}
