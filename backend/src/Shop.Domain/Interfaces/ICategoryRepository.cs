using Shop.Domain.Entities;

namespace Shop.Domain.Interfaces;

/// <summary>
/// Repository interface for Category entity.
/// </summary>
public interface ICategoryRepository
{
    Task<IEnumerable<Category>> GetAllAsync(CancellationToken cancellationToken = default);
    Task<Category?> GetByIdAsync(int id, CancellationToken cancellationToken = default);
}
