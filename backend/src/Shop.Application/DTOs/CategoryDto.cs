namespace Shop.Application.DTOs;

/// <summary>
/// Data transfer object for Category.
/// </summary>
public class CategoryDto
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string? Description { get; set; }
}
