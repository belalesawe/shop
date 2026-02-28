FROM node:20-slim AS base

WORKDIR /app

# Install dependencies first for better caching
COPY package.json package-lock.json ./
RUN npm ci

# Copy application source
COPY . .

# Build the Next.js application
RUN npm run build

# Expose the default port
EXPOSE 3000

# Start the production server
CMD ["npm", "start"]
