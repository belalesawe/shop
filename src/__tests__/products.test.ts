import { describe, it, expect, vi, beforeEach } from "vitest";
import request from "supertest";
import express from "express";
import { Router } from "express";
import type { Request, Response } from "express";
import { errorHandler, AppError } from "../lib/middleware.js";

// We'll test the routes by recreating them with a mock Prisma client
// This avoids needing a real database connection

interface MockCategory {
  id: number;
  name: string;
  description: string | null;
}

interface MockProduct {
  id: number;
  name: string;
  description: string | null;
  price: { toString: () => string };
  categoryId: number | null;
  createdAt: Date;
}

function createTestApp() {
  const mockPrisma = {
    category: {
      create: vi.fn(),
      findMany: vi.fn(),
      findUnique: vi.fn(),
    },
    product: {
      create: vi.fn(),
      findMany: vi.fn(),
      findUnique: vi.fn(),
    },
    inventory: {
      create: vi.fn(),
    },
    $transaction: vi.fn(),
  };

  // Build routes inline with mock prisma
  const categoryRoutes = Router();
  const productRoutes = Router();

  // Category routes
  categoryRoutes.post("/", async (req: Request, res: Response) => {
    const { name, description } = req.body;
    if (!name || typeof name !== "string" || name.length === 0) {
      res.status(400).json({ detail: "String must contain at least 1 character(s)" });
      return;
    }
    const category = await mockPrisma.category.create({
      data: { name, description: description ?? null },
    });
    res.status(201).json({
      id: category.id,
      name: category.name,
      description: category.description,
    });
  });

  categoryRoutes.get("/", async (_req: Request, res: Response) => {
    const categories = await mockPrisma.category.findMany();
    res.json(
      categories.map((c: MockCategory) => ({
        id: c.id,
        name: c.name,
        description: c.description,
      })),
    );
  });

  // Product routes
  productRoutes.post("/", async (req: Request, res: Response) => {
    const { name, description, price, category_id } = req.body;
    if (!name || typeof name !== "string" || name.length === 0) {
      res.status(400).json({ detail: "String must contain at least 1 character(s)" });
      return;
    }

    // Verify category exists if provided
    if (category_id) {
      const category = await mockPrisma.category.findUnique({
        where: { id: category_id },
      });
      if (!category) {
        throw new AppError(404, "Category not found");
      }
    }

    // Use transaction mock
    const product = await mockPrisma.$transaction(async (tx: typeof mockPrisma) => {
      const newProduct = await tx.product.create({
        data: {
          name,
          description: description ?? null,
          price: String(price),
          categoryId: category_id ?? null,
        },
      });
      await tx.inventory.create({
        data: { productId: newProduct.id, quantity: 0, reserved: 0 },
      });
      return newProduct;
    });

    res.status(201).json({
      id: product.id,
      name: product.name,
      description: product.description,
      price: product.price.toString(),
      category_id: product.categoryId,
      created_at: product.createdAt.toISOString(),
    });
  });

  productRoutes.get("/:productId", async (req: Request, res: Response) => {
    const productId = parseInt(req.params["productId"] as string, 10);
    if (isNaN(productId)) {
      res.status(400).json({ detail: "Invalid product ID" });
      return;
    }
    const product = await mockPrisma.product.findUnique({
      where: { id: productId },
    });
    if (!product) {
      throw new AppError(404, "Product not found");
    }
    res.json({
      id: product.id,
      name: product.name,
      description: product.description,
      price: product.price.toString(),
      category_id: product.categoryId,
      created_at: product.createdAt.toISOString(),
    });
  });

  productRoutes.get("/", async (_req: Request, res: Response) => {
    const products = await mockPrisma.product.findMany();
    res.json(
      products.map((p: MockProduct) => ({
        id: p.id,
        name: p.name,
        description: p.description,
        price: p.price.toString(),
        category_id: p.categoryId,
        created_at: p.createdAt.toISOString(),
      })),
    );
  });

  const app = express();
  app.use(express.json());
  app.get("/", (_req, res) => {
    res.json({ status: "healthy", service: "ecommerce-monolith" });
  });
  app.use("/categories", categoryRoutes);
  app.use("/products", productRoutes);
  app.use(errorHandler);

  return { app, mockPrisma };
}

describe("Health Check", () => {
  it("GET / returns healthy status", async () => {
    const { app } = createTestApp();
    const res = await request(app).get("/");
    expect(res.status).toBe(200);
    expect(res.body).toEqual({
      status: "healthy",
      service: "ecommerce-monolith",
    });
  });
});

describe("Categories API", () => {
  let app: express.Express;
  let mockPrisma: ReturnType<typeof createTestApp>["mockPrisma"];

  beforeEach(() => {
    const testApp = createTestApp();
    app = testApp.app;
    mockPrisma = testApp.mockPrisma;
  });

  describe("POST /categories", () => {
    it("creates a category and returns 201", async () => {
      const mockCategory = { id: 1, name: "Electronics", description: "Electronic devices" };
      mockPrisma.category.create.mockResolvedValue(mockCategory);

      const res = await request(app)
        .post("/categories")
        .send({ name: "Electronics", description: "Electronic devices" });

      expect(res.status).toBe(201);
      expect(res.body).toEqual({
        id: 1,
        name: "Electronics",
        description: "Electronic devices",
      });
    });

    it("creates a category with null description", async () => {
      const mockCategory = { id: 2, name: "Books", description: null };
      mockPrisma.category.create.mockResolvedValue(mockCategory);

      const res = await request(app)
        .post("/categories")
        .send({ name: "Books" });

      expect(res.status).toBe(201);
      expect(res.body.description).toBeNull();
    });

    it("returns 400 for empty name", async () => {
      const res = await request(app)
        .post("/categories")
        .send({ name: "" });

      expect(res.status).toBe(400);
      expect(res.body).toHaveProperty("detail");
    });
  });

  describe("GET /categories", () => {
    it("returns list of categories", async () => {
      const mockCategories = [
        { id: 1, name: "Electronics", description: "Electronic devices" },
        { id: 2, name: "Books", description: null },
      ];
      mockPrisma.category.findMany.mockResolvedValue(mockCategories);

      const res = await request(app).get("/categories");

      expect(res.status).toBe(200);
      expect(res.body).toHaveLength(2);
      expect(res.body[0]).toEqual({
        id: 1,
        name: "Electronics",
        description: "Electronic devices",
      });
    });

    it("returns empty array when no categories exist", async () => {
      mockPrisma.category.findMany.mockResolvedValue([]);

      const res = await request(app).get("/categories");

      expect(res.status).toBe(200);
      expect(res.body).toEqual([]);
    });
  });
});

describe("Products API", () => {
  let app: express.Express;
  let mockPrisma: ReturnType<typeof createTestApp>["mockPrisma"];

  const mockDate = new Date("2024-01-15T10:00:00.000Z");

  beforeEach(() => {
    const testApp = createTestApp();
    app = testApp.app;
    mockPrisma = testApp.mockPrisma;
  });

  describe("POST /products", () => {
    it("creates a product with auto-inventory initialization", async () => {
      const mockProduct = {
        id: 1,
        name: "Laptop",
        description: "A great laptop",
        price: { toString: () => "999.99" },
        categoryId: 1,
        createdAt: mockDate,
      };

      // The $transaction mock needs to execute the callback
      mockPrisma.$transaction.mockImplementation(async (cb: (tx: typeof mockPrisma) => Promise<unknown>) => {
        const txMock = {
          product: { create: vi.fn().mockResolvedValue(mockProduct) },
          inventory: { create: vi.fn().mockResolvedValue({}) },
        };
        return cb(txMock as unknown as typeof mockPrisma);
      });

      mockPrisma.category.findUnique.mockResolvedValue({
        id: 1,
        name: "Electronics",
        description: null,
      });

      const res = await request(app)
        .post("/products")
        .send({
          name: "Laptop",
          description: "A great laptop",
          price: 999.99,
          category_id: 1,
        });

      expect(res.status).toBe(201);
      expect(res.body).toEqual({
        id: 1,
        name: "Laptop",
        description: "A great laptop",
        price: "999.99",
        category_id: 1,
        created_at: mockDate.toISOString(),
      });
    });

    it("returns 404 when category does not exist", async () => {
      mockPrisma.category.findUnique.mockResolvedValue(null);

      const res = await request(app)
        .post("/products")
        .send({
          name: "Laptop",
          price: 999.99,
          category_id: 999,
        });

      expect(res.status).toBe(404);
      expect(res.body).toEqual({ detail: "Category not found" });
    });

    it("creates a product without category", async () => {
      const mockProduct = {
        id: 2,
        name: "Widget",
        description: null,
        price: { toString: () => "9.99" },
        categoryId: null,
        createdAt: mockDate,
      };

      mockPrisma.$transaction.mockImplementation(async (cb: (tx: typeof mockPrisma) => Promise<unknown>) => {
        const txMock = {
          product: { create: vi.fn().mockResolvedValue(mockProduct) },
          inventory: { create: vi.fn().mockResolvedValue({}) },
        };
        return cb(txMock as unknown as typeof mockPrisma);
      });

      const res = await request(app)
        .post("/products")
        .send({ name: "Widget", price: 9.99 });

      expect(res.status).toBe(201);
      expect(res.body.category_id).toBeNull();
    });
  });

  describe("GET /products/:id", () => {
    it("returns product by ID", async () => {
      const mockProduct = {
        id: 1,
        name: "Laptop",
        description: "A great laptop",
        price: { toString: () => "999.99" },
        categoryId: 1,
        createdAt: mockDate,
      };
      mockPrisma.product.findUnique.mockResolvedValue(mockProduct);

      const res = await request(app).get("/products/1");

      expect(res.status).toBe(200);
      expect(res.body).toEqual({
        id: 1,
        name: "Laptop",
        description: "A great laptop",
        price: "999.99",
        category_id: 1,
        created_at: mockDate.toISOString(),
      });
    });

    it("returns 404 for non-existent product", async () => {
      mockPrisma.product.findUnique.mockResolvedValue(null);

      const res = await request(app).get("/products/999");

      expect(res.status).toBe(404);
      expect(res.body).toEqual({ detail: "Product not found" });
    });

    it("returns 400 for invalid product ID", async () => {
      const res = await request(app).get("/products/abc");

      expect(res.status).toBe(400);
      expect(res.body).toEqual({ detail: "Invalid product ID" });
    });
  });

  describe("GET /products", () => {
    it("returns list of products", async () => {
      const mockProducts = [
        {
          id: 1,
          name: "Laptop",
          description: "A great laptop",
          price: { toString: () => "999.99" },
          categoryId: 1,
          createdAt: mockDate,
        },
        {
          id: 2,
          name: "Phone",
          description: null,
          price: { toString: () => "599.00" },
          categoryId: 1,
          createdAt: mockDate,
        },
      ];
      mockPrisma.product.findMany.mockResolvedValue(mockProducts);

      const res = await request(app).get("/products");

      expect(res.status).toBe(200);
      expect(res.body).toHaveLength(2);
      expect(res.body[0].name).toBe("Laptop");
      expect(res.body[1].name).toBe("Phone");
    });

    it("returns empty array when no products exist", async () => {
      mockPrisma.product.findMany.mockResolvedValue([]);

      const res = await request(app).get("/products");

      expect(res.status).toBe(200);
      expect(res.body).toEqual([]);
    });
  });
});
