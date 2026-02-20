using Shop.Application.DTOs;

namespace Shop.Application.Interfaces;

/// <summary>
/// Application service interface for category operations.
/// </summary>
public interface ICategoryService
{
    Task<IEnumerable<CategoryDto>> GetAllCategoriesAsync(CancellationToken cancellationToken = default);
    Task<CategoryDto?> GetCategoryByIdAsync(int id, CancellationToken cancellationToken = default);
}
