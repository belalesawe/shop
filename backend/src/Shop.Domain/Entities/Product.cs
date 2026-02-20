namespace Shop.Domain.Entities;

/// <summary>
/// Product in the e-commerce catalog.
/// </summary>
public class Product : BaseEntity
{
    public string Name { get; set; } = string.Empty;
    public string? Description { get; set; }
    public decimal Price { get; set; }
    public int? CategoryId { get; set; }
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

    // Navigation properties
    public Category? Category { get; set; }
    public Inventory? Inventory { get; set; }
}
