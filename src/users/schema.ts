import { z } from "zod";

export const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1),
});

export type CreateUser = z.infer<typeof CreateUserSchema>;
