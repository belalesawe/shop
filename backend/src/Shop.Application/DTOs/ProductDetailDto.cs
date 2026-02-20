namespace Shop.Application.DTOs;

/// <summary>
/// Detailed data transfer object for Product with inventory info.
/// </summary>
public class ProductDetailDto
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string? Description { get; set; }
    public decimal Price { get; set; }
    public int? CategoryId { get; set; }
    public string? CategoryName { get; set; }
    public DateTime CreatedAt { get; set; }
    public int StockQuantity { get; set; }
    public int StockReserved { get; set; }
    public int StockAvailable { get; set; }
}
