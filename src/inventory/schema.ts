import { z } from "zod";

export const InventoryUpdateSchema = z.object({
  quantity: z.number().int().min(0),
});

export const ReserveRequestSchema = z.object({
  quantity: z.number().int().positive(),
});

export type InventoryUpdate = z.infer<typeof InventoryUpdateSchema>;
export type ReserveRequest = z.infer<typeof ReserveRequestSchema>;
