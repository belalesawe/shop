using Shop.Domain.Entities;

namespace Shop.Domain.Interfaces;

/// <summary>
/// Repository interface for Product aggregate.
/// </summary>
public interface IProductRepository
{
    Task<IEnumerable<Product>> GetAllAsync(CancellationToken cancellationToken = default);
    Task<Product?> GetByIdAsync(int id, CancellationToken cancellationToken = default);
    Task<IEnumerable<Product>> SearchAsync(string? searchTerm, int? categoryId, CancellationToken cancellationToken = default);
    Task<Product> AddAsync(Product product, CancellationToken cancellationToken = default);
}
