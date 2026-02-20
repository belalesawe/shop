using Shop.Domain.Entities;

namespace Shop.UnitTests.Domain;

public class ProductTests
{
    [Fact]
    public void Product_DefaultValues_AreCorrect()
    {
        var product = new Product();

        Assert.Equal(0, product.Id);
        Assert.Equal(string.Empty, product.Name);
        Assert.Null(product.Description);
        Assert.Equal(0m, product.Price);
        Assert.Null(product.CategoryId);
        Assert.Null(product.Category);
        Assert.Null(product.Inventory);
        Assert.True(product.CreatedAt <= DateTime.UtcNow);
    }

    [Fact]
    public void Product_CanSetProperties()
    {
        var now = DateTime.UtcNow;
        var product = new Product
        {
            Id = 1,
            Name = "Test Product",
            Description = "A test product",
            Price = 29.99m,
            CategoryId = 5,
            CreatedAt = now
        };

        Assert.Equal(1, product.Id);
        Assert.Equal("Test Product", product.Name);
        Assert.Equal("A test product", product.Description);
        Assert.Equal(29.99m, product.Price);
        Assert.Equal(5, product.CategoryId);
        Assert.Equal(now, product.CreatedAt);
    }

    [Fact]
    public void Product_InheritsFromBaseEntity()
    {
        var product = new Product();
        Assert.IsAssignableFrom<BaseEntity>(product);
    }

    [Fact]
    public void Product_CanHaveNullCategory()
    {
        var product = new Product
        {
            Name = "Uncategorized Product",
            Price = 10.00m,
            CategoryId = null
        };

        Assert.Null(product.CategoryId);
        Assert.Null(product.Category);
    }

    [Fact]
    public void Product_CanAssociateWithCategory()
    {
        var category = new Category { Id = 1, Name = "Electronics" };
        var product = new Product
        {
            Id = 1,
            Name = "Test",
            Price = 10m,
            CategoryId = category.Id,
            Category = category
        };

        Assert.Equal(1, product.CategoryId);
        Assert.Equal("Electronics", product.Category.Name);
    }
}
