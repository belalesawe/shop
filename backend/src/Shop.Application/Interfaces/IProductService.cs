using Shop.Application.DTOs;

namespace Shop.Application.Interfaces;

/// <summary>
/// Application service interface for product catalog operations.
/// </summary>
public interface IProductService
{
    Task<IEnumerable<ProductDto>> GetAllProductsAsync(CancellationToken cancellationToken = default);
    Task<ProductDetailDto?> GetProductByIdAsync(int id, CancellationToken cancellationToken = default);
    Task<IEnumerable<ProductDto>> SearchProductsAsync(string? searchTerm, int? categoryId, CancellationToken cancellationToken = default);
}
