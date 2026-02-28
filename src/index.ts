import { env } from "./lib/env.js";
import app from "./app.js";

const port = env.PORT;

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
