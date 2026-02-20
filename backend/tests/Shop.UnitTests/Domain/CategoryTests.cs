using Shop.Domain.Entities;

namespace Shop.UnitTests.Domain;

public class CategoryTests
{
    [Fact]
    public void Category_DefaultValues_AreCorrect()
    {
        var category = new Category();

        Assert.Equal(0, category.Id);
        Assert.Equal(string.Empty, category.Name);
        Assert.Null(category.Description);
        Assert.NotNull(category.Products);
        Assert.Empty(category.Products);
    }

    [Fact]
    public void Category_CanSetProperties()
    {
        var category = new Category
        {
            Id = 1,
            Name = "Electronics",
            Description = "Electronic devices and gadgets"
        };

        Assert.Equal(1, category.Id);
        Assert.Equal("Electronics", category.Name);
        Assert.Equal("Electronic devices and gadgets", category.Description);
    }

    [Fact]
    public void Category_InheritsFromBaseEntity()
    {
        var category = new Category();
        Assert.IsAssignableFrom<BaseEntity>(category);
    }

    [Fact]
    public void Category_ProductsCollection_IsInitialized()
    {
        var category = new Category { Id = 1, Name = "Test" };

        Assert.NotNull(category.Products);
        Assert.IsType<List<Product>>(category.Products);
    }

    [Fact]
    public void Category_CanContainMultipleProducts()
    {
        var category = new Category { Id = 1, Name = "Electronics" };
        var products = new List<Product>
        {
            new() { Id = 1, Name = "Product A", Price = 10m },
            new() { Id = 2, Name = "Product B", Price = 20m },
            new() { Id = 3, Name = "Product C", Price = 30m }
        };
        category.Products = products;

        Assert.Equal(3, category.Products.Count);
    }
}
