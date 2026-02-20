using Microsoft.EntityFrameworkCore;
using Shop.Domain.Entities;

namespace Shop.Infrastructure.Data;

/// <summary>
/// Seeds the database with initial product catalog data.
/// </summary>
public static class ShopDbContextSeed
{
    public static async Task SeedAsync(ShopDbContext context)
    {
        // Ensure database is created
        await context.Database.EnsureCreatedAsync();

        // Only seed if empty
        if (await context.Categories.AnyAsync())
            return;

        var categories = new List<Category>
        {
            new() { Name = "Electronics", Description = "Electronic devices and gadgets" },
            new() { Name = "Clothing", Description = "Apparel and fashion items" },
            new() { Name = "Books", Description = "Physical and digital books" },
            new() { Name = "Home & Garden", Description = "Home improvement and garden supplies" },
            new() { Name = "Sports", Description = "Sports equipment and accessories" }
        };

        context.Categories.AddRange(categories);
        await context.SaveChangesAsync();

        var products = new List<Product>
        {
            new()
            {
                Name = "Wireless Bluetooth Headphones",
                Description = "High-quality noise-canceling wireless headphones with 30-hour battery life",
                Price = 79.99m,
                CategoryId = categories[0].Id,
                CreatedAt = DateTime.UtcNow
            },
            new()
            {
                Name = "USB-C Charging Cable",
                Description = "Fast charging USB-C cable, 6ft braided nylon",
                Price = 12.99m,
                CategoryId = categories[0].Id,
                CreatedAt = DateTime.UtcNow
            },
            new()
            {
                Name = "Smart Watch",
                Description = "Fitness tracker with heart rate monitor and GPS",
                Price = 199.99m,
                CategoryId = categories[0].Id,
                CreatedAt = DateTime.UtcNow
            },
            new()
            {
                Name = "Cotton T-Shirt",
                Description = "Comfortable 100% cotton crew neck t-shirt",
                Price = 19.99m,
                CategoryId = categories[1].Id,
                CreatedAt = DateTime.UtcNow
            },
            new()
            {
                Name = "Denim Jeans",
                Description = "Classic fit stretch denim jeans",
                Price = 49.99m,
                CategoryId = categories[1].Id,
                CreatedAt = DateTime.UtcNow
            },
            new()
            {
                Name = "Running Shoes",
                Description = "Lightweight breathable running shoes with cushioned sole",
                Price = 89.99m,
                CategoryId = categories[4].Id,
                CreatedAt = DateTime.UtcNow
            },
            new()
            {
                Name = "Programming in C#",
                Description = "Comprehensive guide to C# programming and .NET development",
                Price = 39.99m,
                CategoryId = categories[2].Id,
                CreatedAt = DateTime.UtcNow
            },
            new()
            {
                Name = "Garden Tool Set",
                Description = "5-piece stainless steel garden tool set with carrying bag",
                Price = 34.99m,
                CategoryId = categories[3].Id,
                CreatedAt = DateTime.UtcNow
            },
            new()
            {
                Name = "Yoga Mat",
                Description = "Non-slip exercise yoga mat, 6mm thick",
                Price = 24.99m,
                CategoryId = categories[4].Id,
                CreatedAt = DateTime.UtcNow
            },
            new()
            {
                Name = "LED Desk Lamp",
                Description = "Adjustable LED desk lamp with USB charging port",
                Price = 29.99m,
                CategoryId = categories[3].Id,
                CreatedAt = DateTime.UtcNow
            }
        };

        context.Products.AddRange(products);
        await context.SaveChangesAsync();

        // Initialize inventory for all products
        var inventoryItems = products.Select(p => new Inventory
        {
            ProductId = p.Id,
            Quantity = Random.Shared.Next(10, 100),
            Reserved = 0,
            LastUpdated = DateTime.UtcNow
        }).ToList();

        context.Inventories.AddRange(inventoryItems);
        await context.SaveChangesAsync();
    }
}
