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

describe("Users API", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe("POST /users", () => {
    it("should create a user successfully", async () => {
      const userData = { email: "test@example.com", name: "Test User" };
      const createdUser = {
        id: 1,
        ...userData,
        createdAt: new Date("2024-01-01T00:00:00Z"),
      };

      mockPrisma.user.findUnique.mockResolvedValue(null);
      mockPrisma.user.create.mockResolvedValue(createdUser);

      const res = await request(app)
        .post("/users")
        .send(userData)
        .expect(201);

      expect(res.body).toHaveProperty("id", 1);
      expect(res.body).toHaveProperty("email", "test@example.com");
      expect(res.body).toHaveProperty("name", "Test User");
      expect(mockPrisma.user.findUnique).toHaveBeenCalledWith({
        where: { email: "test@example.com" },
      });
      expect(mockPrisma.user.create).toHaveBeenCalledWith({
        data: { email: "test@example.com", name: "Test User" },
      });
    });

    it("should return 400 when email already registered", async () => {
      const userData = { email: "existing@example.com", name: "Test User" };
      const existingUser = {
        id: 1,
        email: "existing@example.com",
        name: "Existing User",
        createdAt: new Date(),
      };

      mockPrisma.user.findUnique.mockResolvedValue(existingUser);

      const res = await request(app)
        .post("/users")
        .send(userData)
        .expect(400);

      expect(res.body).toHaveProperty("detail", "Email already registered");
      expect(mockPrisma.user.create).not.toHaveBeenCalled();
    });

    it("should return 400 for invalid email", async () => {
      const res = await request(app)
        .post("/users")
        .send({ email: "not-an-email", name: "Test" })
        .expect(400);

      expect(res.body).toHaveProperty("detail");
    });

    it("should return 400 for missing name", async () => {
      const res = await request(app)
        .post("/users")
        .send({ email: "test@example.com" })
        .expect(400);

      expect(res.body).toHaveProperty("detail");
    });
  });

  describe("GET /users/:userId", () => {
    it("should return a user by ID", async () => {
      const user = {
        id: 1,
        email: "test@example.com",
        name: "Test User",
        createdAt: new Date("2024-01-01T00:00:00Z"),
      };

      mockPrisma.user.findUnique.mockResolvedValue(user);

      const res = await request(app).get("/users/1").expect(200);

      expect(res.body).toHaveProperty("id", 1);
      expect(res.body).toHaveProperty("email", "test@example.com");
      expect(mockPrisma.user.findUnique).toHaveBeenCalledWith({
        where: { id: 1 },
      });
    });

    it("should return 404 when user not found", async () => {
      mockPrisma.user.findUnique.mockResolvedValue(null);

      const res = await request(app).get("/users/999").expect(404);

      expect(res.body).toHaveProperty("detail", "User not found");
    });
  });

  describe("GET /users", () => {
    it("should return a list of users", async () => {
      const users = [
        {
          id: 1,
          email: "user1@example.com",
          name: "User 1",
          createdAt: new Date(),
        },
        {
          id: 2,
          email: "user2@example.com",
          name: "User 2",
          createdAt: new Date(),
        },
      ];

      mockPrisma.user.findMany.mockResolvedValue(users);

      const res = await request(app).get("/users").expect(200);

      expect(res.body).toHaveLength(2);
      expect(res.body[0]).toHaveProperty("email", "user1@example.com");
      expect(res.body[1]).toHaveProperty("email", "user2@example.com");
    });

    it("should return empty array when no users exist", async () => {
      mockPrisma.user.findMany.mockResolvedValue([]);

      const res = await request(app).get("/users").expect(200);

      expect(res.body).toEqual([]);
    });
  });
});
