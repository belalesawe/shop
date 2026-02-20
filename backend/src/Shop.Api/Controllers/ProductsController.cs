using Microsoft.AspNetCore.Mvc;
using Shop.Application.DTOs;
using Shop.Application.Interfaces;

namespace Shop.Api.Controllers;

[ApiController]
[Route("api/v1/[controller]")]
public class ProductsController : ControllerBase
{
    private readonly IProductService _productService;

    public ProductsController(IProductService productService)
    {
        _productService = productService;
    }

    /// <summary>
    /// List all products, optionally filtered by search term and/or category.
    /// </summary>
    [HttpGet]
    [ProducesResponseType(typeof(IEnumerable<ProductDto>), StatusCodes.Status200OK)]
    public async Task<ActionResult<IEnumerable<ProductDto>>> GetProducts(
        [FromQuery] string? search = null,
        [FromQuery] int? categoryId = null,
        CancellationToken cancellationToken = default)
    {
        IEnumerable<ProductDto> products;

        if (!string.IsNullOrWhiteSpace(search) || categoryId.HasValue)
        {
            products = await _productService.SearchProductsAsync(search, categoryId, cancellationToken);
        }
        else
        {
            products = await _productService.GetAllProductsAsync(cancellationToken);
        }

        return Ok(products);
    }

    /// <summary>
    /// Get a specific product by its ID.
    /// </summary>
    [HttpGet("{id:int}")]
    [ProducesResponseType(typeof(ProductDetailDto), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<ActionResult<ProductDetailDto>> GetProduct(int id, CancellationToken cancellationToken = default)
    {
        var product = await _productService.GetProductByIdAsync(id, cancellationToken);

        if (product is null)
            return NotFound(new { message = $"Product with ID {id} not found" });

        return Ok(product);
    }
}
