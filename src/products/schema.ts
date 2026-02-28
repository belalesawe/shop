import { z } from "zod";

// Category schemas
export const createCategorySchema = z.object({
  name: z.string().min(1),
  description: z.string().nullable().optional(),
});

export type CreateCategoryInput = z.infer<typeof createCategorySchema>;

export const categoryResponseSchema = z.object({
  id: z.number(),
  name: z.string(),
  description: z.string().nullable(),
});

export type CategoryResponse = z.infer<typeof categoryResponseSchema>;

// Product schemas
export const createProductSchema = z.object({
  name: z.string().min(1),
  description: z.string().nullable().optional(),
  price: z.union([z.string(), z.number()]).transform((val) => String(val)),
  category_id: z.number().int().positive().nullable().optional(),
});

export type CreateProductInput = z.infer<typeof createProductSchema>;

export const productResponseSchema = z.object({
  id: z.number(),
  name: z.string(),
  description: z.string().nullable(),
  price: z.string(),
  category_id: z.number().nullable(),
  created_at: z.string(),
});

export type ProductResponse = z.infer<typeof productResponseSchema>;
