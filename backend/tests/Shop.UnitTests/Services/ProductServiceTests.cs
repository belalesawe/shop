using Moq;
using Shop.Application.Services;
using Shop.Domain.Entities;
using Shop.Domain.Interfaces;

namespace Shop.UnitTests.Services;

public class ProductServiceTests
{
    private readonly Mock<IProductRepository> _mockRepo;
    private readonly ProductService _service;

    public ProductServiceTests()
    {
        _mockRepo = new Mock<IProductRepository>();
        _service = new ProductService(_mockRepo.Object);
    }

    private static List<Product> GetSampleProducts()
    {
        var electronics = new Category { Id = 1, Name = "Electronics" };
        var clothing = new Category { Id = 2, Name = "Clothing" };

        return new List<Product>
        {
            new()
            {
                Id = 1,
                Name = "Headphones",
                Description = "Wireless headphones",
                Price = 79.99m,
                CategoryId = 1,
                Category = electronics,
                CreatedAt = DateTime.UtcNow,
                Inventory = new Inventory { ProductId = 1, Quantity = 50, Reserved = 5 }
            },
            new()
            {
                Id = 2,
                Name = "T-Shirt",
                Description = "Cotton t-shirt",
                Price = 19.99m,
                CategoryId = 2,
                Category = clothing,
                CreatedAt = DateTime.UtcNow,
                Inventory = new Inventory { ProductId = 2, Quantity = 100, Reserved = 0 }
            }
        };
    }

    [Fact]
    public async Task GetAllProductsAsync_ReturnsAllProducts()
    {
        var products = GetSampleProducts();
        _mockRepo.Setup(r => r.GetAllAsync(It.IsAny<CancellationToken>()))
            .ReturnsAsync(products);

        var result = await _service.GetAllProductsAsync();

        var dtos = result.ToList();
        Assert.Equal(2, dtos.Count);
        Assert.Equal("Headphones", dtos[0].Name);
        Assert.Equal("T-Shirt", dtos[1].Name);
    }

    [Fact]
    public async Task GetAllProductsAsync_MapsPropertiesToDto()
    {
        var products = GetSampleProducts();
        _mockRepo.Setup(r => r.GetAllAsync(It.IsAny<CancellationToken>()))
            .ReturnsAsync(products);

        var result = (await _service.GetAllProductsAsync()).ToList();

        var dto = result[0];
        Assert.Equal(1, dto.Id);
        Assert.Equal("Headphones", dto.Name);
        Assert.Equal("Wireless headphones", dto.Description);
        Assert.Equal(79.99m, dto.Price);
        Assert.Equal(1, dto.CategoryId);
        Assert.Equal("Electronics", dto.CategoryName);
    }

    [Fact]
    public async Task GetAllProductsAsync_WhenEmpty_ReturnsEmptyList()
    {
        _mockRepo.Setup(r => r.GetAllAsync(It.IsAny<CancellationToken>()))
            .ReturnsAsync(new List<Product>());

        var result = await _service.GetAllProductsAsync();

        Assert.Empty(result);
    }

    [Fact]
    public async Task GetProductByIdAsync_ReturnsProductDetail()
    {
        var product = GetSampleProducts()[0];
        _mockRepo.Setup(r => r.GetByIdAsync(1, It.IsAny<CancellationToken>()))
            .ReturnsAsync(product);

        var result = await _service.GetProductByIdAsync(1);

        Assert.NotNull(result);
        Assert.Equal(1, result.Id);
        Assert.Equal("Headphones", result.Name);
        Assert.Equal(50, result.StockQuantity);
        Assert.Equal(5, result.StockReserved);
        Assert.Equal(45, result.StockAvailable);
    }

    [Fact]
    public async Task GetProductByIdAsync_WhenNotFound_ReturnsNull()
    {
        _mockRepo.Setup(r => r.GetByIdAsync(999, It.IsAny<CancellationToken>()))
            .ReturnsAsync((Product?)null);

        var result = await _service.GetProductByIdAsync(999);

        Assert.Null(result);
    }

    [Fact]
    public async Task GetProductByIdAsync_WithNullInventory_ReturnsZeroStock()
    {
        var product = new Product
        {
            Id = 1,
            Name = "No Inventory",
            Price = 10m,
            Inventory = null
        };
        _mockRepo.Setup(r => r.GetByIdAsync(1, It.IsAny<CancellationToken>()))
            .ReturnsAsync(product);

        var result = await _service.GetProductByIdAsync(1);

        Assert.NotNull(result);
        Assert.Equal(0, result.StockQuantity);
        Assert.Equal(0, result.StockReserved);
        Assert.Equal(0, result.StockAvailable);
    }

    [Fact]
    public async Task SearchProductsAsync_DelegatesToRepository()
    {
        var products = GetSampleProducts().Take(1);
        _mockRepo.Setup(r => r.SearchAsync("head", null, It.IsAny<CancellationToken>()))
            .ReturnsAsync(products);

        var result = await _service.SearchProductsAsync("head", null);

        var dtos = result.ToList();
        Assert.Single(dtos);
        Assert.Equal("Headphones", dtos[0].Name);
        _mockRepo.Verify(r => r.SearchAsync("head", null, It.IsAny<CancellationToken>()), Times.Once);
    }

    [Fact]
    public async Task SearchProductsAsync_ByCategoryId_DelegatesToRepository()
    {
        var products = GetSampleProducts().Where(p => p.CategoryId == 1);
        _mockRepo.Setup(r => r.SearchAsync(null, 1, It.IsAny<CancellationToken>()))
            .ReturnsAsync(products);

        var result = await _service.SearchProductsAsync(null, 1);

        var dtos = result.ToList();
        Assert.Single(dtos);
        Assert.Equal("Electronics", dtos[0].CategoryName);
    }
}
