using Shop.Application.DTOs;
using Shop.Application.Interfaces;
using Shop.Domain.Entities;
using Shop.Domain.Interfaces;

namespace Shop.Application.Services;

/// <summary>
/// Application service for product catalog operations.
/// </summary>
public class ProductService : IProductService
{
    private readonly IProductRepository _productRepository;

    public ProductService(IProductRepository productRepository)
    {
        _productRepository = productRepository;
    }

    public async Task<IEnumerable<ProductDto>> GetAllProductsAsync(CancellationToken cancellationToken = default)
    {
        var products = await _productRepository.GetAllAsync(cancellationToken);
        return products.Select(MapToDto);
    }

    public async Task<ProductDetailDto?> GetProductByIdAsync(int id, CancellationToken cancellationToken = default)
    {
        var product = await _productRepository.GetByIdAsync(id, cancellationToken);
        if (product is null)
            return null;

        return MapToDetailDto(product);
    }

    public async Task<IEnumerable<ProductDto>> SearchProductsAsync(string? searchTerm, int? categoryId, CancellationToken cancellationToken = default)
    {
        var products = await _productRepository.SearchAsync(searchTerm, categoryId, cancellationToken);
        return products.Select(MapToDto);
    }

    private static ProductDto MapToDto(Product product) => new()
    {
        Id = product.Id,
        Name = product.Name,
        Description = product.Description,
        Price = product.Price,
        CategoryId = product.CategoryId,
        CategoryName = product.Category?.Name,
        CreatedAt = product.CreatedAt
    };

    private static ProductDetailDto MapToDetailDto(Product product) => new()
    {
        Id = product.Id,
        Name = product.Name,
        Description = product.Description,
        Price = product.Price,
        CategoryId = product.CategoryId,
        CategoryName = product.Category?.Name,
        CreatedAt = product.CreatedAt,
        StockQuantity = product.Inventory?.Quantity ?? 0,
        StockReserved = product.Inventory?.Reserved ?? 0,
        StockAvailable = product.Inventory?.Available ?? 0
    };
}
