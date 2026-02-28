import { z } from "zod";

export const CreateCategorySchema = z.object({
  name: z.string().min(1),
  description: z.string().nullable().optional(),
});

export const CreateProductSchema = z.object({
  name: z.string().min(1),
  description: z.string().nullable().optional(),
  price: z.union([z.string(), z.number()]).transform((val) => String(val)),
  category_id: z.number().int().positive().nullable().optional(),
});

export type CreateCategory = z.infer<typeof CreateCategorySchema>;
export type CreateProduct = z.infer<typeof CreateProductSchema>;
