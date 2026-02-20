namespace Shop.Domain.Entities;

/// <summary>
/// Base entity with common properties for all domain entities.
/// </summary>
public abstract class BaseEntity
{
    public int Id { get; set; }
}
