namespace Shop.Domain.Entities;

/// <summary>
/// Tracks product inventory levels and reservations.
/// </summary>
public class Inventory
{
    public int ProductId { get; set; }
    public int Quantity { get; set; }
    public int Reserved { get; set; }
    public DateTime LastUpdated { get; set; } = DateTime.UtcNow;

    // Navigation properties
    public Product Product { get; set; } = null!;

    /// <summary>
    /// Gets the available quantity (total minus reserved).
    /// </summary>
    public int Available => Quantity - Reserved;
}
