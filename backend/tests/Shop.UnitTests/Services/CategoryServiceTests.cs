using Moq;
using Shop.Application.Services;
using Shop.Domain.Entities;
using Shop.Domain.Interfaces;

namespace Shop.UnitTests.Services;

public class CategoryServiceTests
{
    private readonly Mock<ICategoryRepository> _mockRepo;
    private readonly CategoryService _service;

    public CategoryServiceTests()
    {
        _mockRepo = new Mock<ICategoryRepository>();
        _service = new CategoryService(_mockRepo.Object);
    }

    private static List<Category> GetSampleCategories()
    {
        return new List<Category>
        {
            new() { Id = 1, Name = "Electronics", Description = "Electronic devices" },
            new() { Id = 2, Name = "Clothing", Description = "Apparel and fashion" },
            new() { Id = 3, Name = "Books", Description = "Physical and digital books" }
        };
    }

    [Fact]
    public async Task GetAllCategoriesAsync_ReturnsAllCategories()
    {
        var categories = GetSampleCategories();
        _mockRepo.Setup(r => r.GetAllAsync(It.IsAny<CancellationToken>()))
            .ReturnsAsync(categories);

        var result = await _service.GetAllCategoriesAsync();

        var dtos = result.ToList();
        Assert.Equal(3, dtos.Count);
    }

    [Fact]
    public async Task GetAllCategoriesAsync_MapsPropertiesToDto()
    {
        var categories = GetSampleCategories();
        _mockRepo.Setup(r => r.GetAllAsync(It.IsAny<CancellationToken>()))
            .ReturnsAsync(categories);

        var result = (await _service.GetAllCategoriesAsync()).ToList();

        var dto = result[0];
        Assert.Equal(1, dto.Id);
        Assert.Equal("Electronics", dto.Name);
        Assert.Equal("Electronic devices", dto.Description);
    }

    [Fact]
    public async Task GetAllCategoriesAsync_WhenEmpty_ReturnsEmptyList()
    {
        _mockRepo.Setup(r => r.GetAllAsync(It.IsAny<CancellationToken>()))
            .ReturnsAsync(new List<Category>());

        var result = await _service.GetAllCategoriesAsync();

        Assert.Empty(result);
    }

    [Fact]
    public async Task GetCategoryByIdAsync_ReturnsCategory()
    {
        var category = GetSampleCategories()[0];
        _mockRepo.Setup(r => r.GetByIdAsync(1, It.IsAny<CancellationToken>()))
            .ReturnsAsync(category);

        var result = await _service.GetCategoryByIdAsync(1);

        Assert.NotNull(result);
        Assert.Equal(1, result.Id);
        Assert.Equal("Electronics", result.Name);
        Assert.Equal("Electronic devices", result.Description);
    }

    [Fact]
    public async Task GetCategoryByIdAsync_WhenNotFound_ReturnsNull()
    {
        _mockRepo.Setup(r => r.GetByIdAsync(999, It.IsAny<CancellationToken>()))
            .ReturnsAsync((Category?)null);

        var result = await _service.GetCategoryByIdAsync(999);

        Assert.Null(result);
    }

    [Fact]
    public async Task GetCategoryByIdAsync_WithNullDescription_ReturnsNullDescription()
    {
        var category = new Category { Id = 1, Name = "Simple", Description = null };
        _mockRepo.Setup(r => r.GetByIdAsync(1, It.IsAny<CancellationToken>()))
            .ReturnsAsync(category);

        var result = await _service.GetCategoryByIdAsync(1);

        Assert.NotNull(result);
        Assert.Null(result.Description);
    }
}
