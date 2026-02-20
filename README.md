# E-Commerce Shop

A modern full-stack e-commerce application built with .NET 8 (ASP.NET Core Web API) and Next.js (React/TypeScript).

## Project Structure

```
/
  backend/           # ASP.NET Core Web API
    src/
      Shop.Api/            # Web API host
      Shop.Application/    # Application services, DTOs
      Shop.Domain/         # Domain entities, interfaces
      Shop.Infrastructure/ # EF Core, repositories
    tests/
      Shop.UnitTests/      # xUnit unit tests
  frontend/          # Next.js web application (see shop-fe repo)
  infra/             # Infrastructure & deployment
  docs/              # Architecture documentation
```

## Prerequisites

- [.NET SDK 8.0](https://dotnet.microsoft.com/download/dotnet/8.0)
- [Node.js 20+ LTS](https://nodejs.org/)
- SQLite (included, no separate installation needed)

## Getting Started

### Backend

```bash
cd backend
dotnet restore
dotnet build
dotnet run --project src/Shop.Api
```

The API will be available at `http://localhost:5000`.

### Frontend

See the `shop-fe` repository for frontend setup instructions.

## API Endpoints

### Products
- `GET /api/v1/products` - List all products (supports search, filtering, pagination)
- `GET /api/v1/products/{id}` - Get product details

### Categories
- `GET /api/v1/categories` - List all categories

## Testing

### Backend Unit Tests

```bash
cd backend
dotnet test
```

## Architecture

The backend follows a **Clean Architecture** pattern with four layers:

1. **Domain** - Core business entities and repository interfaces
2. **Application** - Use cases, DTOs, and application services
3. **Infrastructure** - Data access (EF Core), external integrations
4. **API** - HTTP controllers, middleware, and configuration
