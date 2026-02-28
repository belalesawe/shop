import { describe, it, expect, vi, beforeEach } from "vitest";
import request from "supertest";
import { createMockPrisma, type MockPrisma } from "./helpers.js";

let mockPrisma: MockPrisma;

vi.mock("../src/lib/db.js", () => {
  const mock = createMockPrisma();
  mockPrisma = mock;
  return { default: mock };
});

// Import app after mocking
const { default: app } = await import("../src/app.js");

describe("Inventory API", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe("GET /inventory/:productId", () => {
    it("should return inventory for a product", async () => {
      const inventory = {
        productId: 1,
        quantity: 100,
        reserved: 10,
        lastUpdated: new Date("2024-01-01T00:00:00Z"),
      };

      mockPrisma.inventory.findUnique.mockResolvedValue(inventory);

      const res = await request(app).get("/inventory/1").expect(200);

      expect(res.body).toHaveProperty("productId", 1);
      expect(res.body).toHaveProperty("quantity", 100);
      expect(res.body).toHaveProperty("reserved", 10);
      expect(mockPrisma.inventory.findUnique).toHaveBeenCalledWith({
        where: { productId: 1 },
      });
    });

    it("should return 404 when inventory not found", async () => {
      mockPrisma.inventory.findUnique.mockResolvedValue(null);

      const res = await request(app).get("/inventory/999").expect(404);

      expect(res.body).toHaveProperty("detail", "Inventory not found");
    });
  });

  describe("PUT /inventory/:productId", () => {
    it("should update inventory quantity", async () => {
      const existingInventory = {
        productId: 1,
        quantity: 50,
        reserved: 5,
        lastUpdated: new Date("2024-01-01T00:00:00Z"),
      };
      const updatedInventory = {
        ...existingInventory,
        quantity: 200,
        lastUpdated: new Date("2024-06-01T00:00:00Z"),
      };

      mockPrisma.inventory.findUnique.mockResolvedValue(existingInventory);
      mockPrisma.inventory.update.mockResolvedValue(updatedInventory);

      const res = await request(app)
        .put("/inventory/1")
        .send({ quantity: 200 })
        .expect(200);

      expect(res.body).toHaveProperty("quantity", 200);
      expect(mockPrisma.inventory.update).toHaveBeenCalledWith({
        where: { productId: 1 },
        data: {
          quantity: 200,
          lastUpdated: expect.any(Date),
        },
      });
    });

    it("should return 404 when product inventory not found", async () => {
      mockPrisma.inventory.findUnique.mockResolvedValue(null);

      const res = await request(app)
        .put("/inventory/999")
        .send({ quantity: 100 })
        .expect(404);

      expect(res.body).toHaveProperty("detail", "Inventory not found");
    });

    it("should return 400 for invalid quantity", async () => {
      const res = await request(app)
        .put("/inventory/1")
        .send({ quantity: -5 })
        .expect(400);

      expect(res.body).toHaveProperty("detail");
    });
  });

  describe("POST /inventory/:productId/reserve", () => {
    it("should reserve stock successfully", async () => {
      const existingInventory = {
        productId: 1,
        quantity: 100,
        reserved: 10,
        lastUpdated: new Date("2024-01-01T00:00:00Z"),
      };
      const updatedInventory = {
        ...existingInventory,
        reserved: 15,
        lastUpdated: new Date("2024-06-01T00:00:00Z"),
      };

      mockPrisma.inventory.findUnique.mockResolvedValue(existingInventory);
      mockPrisma.inventory.update.mockResolvedValue(updatedInventory);

      const res = await request(app)
        .post("/inventory/1/reserve")
        .send({ quantity: 5 })
        .expect(200);

      expect(res.body).toHaveProperty("reserved", 15);
      expect(mockPrisma.inventory.update).toHaveBeenCalledWith({
        where: { productId: 1 },
        data: {
          reserved: { increment: 5 },
          lastUpdated: expect.any(Date),
        },
      });
    });

    it("should return 400 with insufficient inventory message", async () => {
      const existingInventory = {
        productId: 1,
        quantity: 10,
        reserved: 8,
        lastUpdated: new Date("2024-01-01T00:00:00Z"),
      };

      mockPrisma.inventory.findUnique.mockResolvedValue(existingInventory);

      const res = await request(app)
        .post("/inventory/1/reserve")
        .send({ quantity: 5 })
        .expect(400);

      expect(res.body.detail).toContain("Insufficient inventory");
      expect(res.body.detail).toContain("Available: 2");
      expect(res.body.detail).toContain("Requested: 5");
    });

    it("should return 404 when product inventory not found", async () => {
      mockPrisma.inventory.findUnique.mockResolvedValue(null);

      const res = await request(app)
        .post("/inventory/999/reserve")
        .send({ quantity: 5 })
        .expect(404);

      expect(res.body).toHaveProperty("detail", "Inventory not found");
    });

    it("should return 400 for zero reserve quantity", async () => {
      const res = await request(app)
        .post("/inventory/1/reserve")
        .send({ quantity: 0 })
        .expect(400);

      expect(res.body).toHaveProperty("detail");
    });
  });
});
