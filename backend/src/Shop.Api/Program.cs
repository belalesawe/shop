using Microsoft.EntityFrameworkCore;
using Shop.Application.Interfaces;
using Shop.Application.Services;
using Shop.Domain.Interfaces;
using Shop.Infrastructure.Data;
using Shop.Infrastructure.Repositories;

var builder = WebApplication.CreateBuilder(args);

// Database
var connectionString = builder.Configuration.GetConnectionString("DefaultConnection")
    ?? "Data Source=ecommerce.db";
builder.Services.AddDbContext<ShopDbContext>(options =>
    options.UseSqlite(connectionString));

// Application services
builder.Services.AddScoped<IProductRepository, ProductRepository>();
builder.Services.AddScoped<ICategoryRepository, CategoryRepository>();
builder.Services.AddScoped<IProductService, ProductService>();
builder.Services.AddScoped<ICategoryService, CategoryService>();

// CORS
builder.Services.AddCors(options =>
{
    options.AddDefaultPolicy(policy =>
    {
        policy.WithOrigins(
                builder.Configuration.GetSection("Cors:AllowedOrigins").Get<string[]>()
                ?? new[] { "http://localhost:3000" })
            .AllowAnyHeader()
            .AllowAnyMethod();
    });
});

// Controllers and Swagger
builder.Services.AddControllers()
    .AddJsonOptions(options =>
    {
        options.JsonSerializerOptions.PropertyNamingPolicy =
            System.Text.Json.JsonNamingPolicy.SnakeCaseLower;
    });
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(options =>
{
    options.SwaggerDoc("v1", new Microsoft.OpenApi.Models.OpenApiInfo
    {
        Title = "E-Commerce Shop API",
        Version = "v1",
        Description = "Product catalog and e-commerce backend API"
    });
});

var app = builder.Build();

// Seed database on startup
using (var scope = app.Services.CreateScope())
{
    var context = scope.ServiceProvider.GetRequiredService<ShopDbContext>();
    await ShopDbContextSeed.SeedAsync(context);
}

// Configure middleware pipeline
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseCors();

app.UseAuthorization();

app.MapControllers();

// Health check endpoint
app.MapGet("/", () => new { status = "healthy", service = "ecommerce-shop-api" });

app.Run();

// Make Program class accessible for integration tests
public partial class Program { }
