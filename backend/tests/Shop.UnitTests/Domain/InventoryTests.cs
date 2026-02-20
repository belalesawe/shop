using Shop.Domain.Entities;

namespace Shop.UnitTests.Domain;

public class InventoryTests
{
    [Fact]
    public void Inventory_DefaultValues_AreCorrect()
    {
        var inventory = new Inventory();

        Assert.Equal(0, inventory.ProductId);
        Assert.Equal(0, inventory.Quantity);
        Assert.Equal(0, inventory.Reserved);
        Assert.True(inventory.LastUpdated <= DateTime.UtcNow);
    }

    [Fact]
    public void Inventory_Available_ReturnsCorrectValue()
    {
        var inventory = new Inventory
        {
            ProductId = 1,
            Quantity = 50,
            Reserved = 10
        };

        Assert.Equal(40, inventory.Available);
    }

    [Fact]
    public void Inventory_Available_WhenFullyReserved_ReturnsZero()
    {
        var inventory = new Inventory
        {
            ProductId = 1,
            Quantity = 20,
            Reserved = 20
        };

        Assert.Equal(0, inventory.Available);
    }

    [Fact]
    public void Inventory_Available_WhenNoReservations_ReturnsFullQuantity()
    {
        var inventory = new Inventory
        {
            ProductId = 1,
            Quantity = 100,
            Reserved = 0
        };

        Assert.Equal(100, inventory.Available);
    }

    [Fact]
    public void Inventory_Available_WhenEmpty_ReturnsZero()
    {
        var inventory = new Inventory
        {
            ProductId = 1,
            Quantity = 0,
            Reserved = 0
        };

        Assert.Equal(0, inventory.Available);
    }
}
