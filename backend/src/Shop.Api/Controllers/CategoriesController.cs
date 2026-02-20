using Microsoft.AspNetCore.Mvc;
using Shop.Application.DTOs;
using Shop.Application.Interfaces;

namespace Shop.Api.Controllers;

[ApiController]
[Route("api/v1/[controller]")]
public class CategoriesController : ControllerBase
{
    private readonly ICategoryService _categoryService;

    public CategoriesController(ICategoryService categoryService)
    {
        _categoryService = categoryService;
    }

    /// <summary>
    /// List all product categories.
    /// </summary>
    [HttpGet]
    [ProducesResponseType(typeof(IEnumerable<CategoryDto>), StatusCodes.Status200OK)]
    public async Task<ActionResult<IEnumerable<CategoryDto>>> GetCategories(CancellationToken cancellationToken = default)
    {
        var categories = await _categoryService.GetAllCategoriesAsync(cancellationToken);
        return Ok(categories);
    }

    /// <summary>
    /// Get a specific category by its ID.
    /// </summary>
    [HttpGet("{id:int}")]
    [ProducesResponseType(typeof(CategoryDto), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<ActionResult<CategoryDto>> GetCategory(int id, CancellationToken cancellationToken = default)
    {
        var category = await _categoryService.GetCategoryByIdAsync(id, cancellationToken);

        if (category is null)
            return NotFound(new { message = $"Category with ID {id} not found" });

        return Ok(category);
    }
}
