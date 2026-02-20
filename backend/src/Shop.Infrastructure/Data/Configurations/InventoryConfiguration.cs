using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using Shop.Domain.Entities;

namespace Shop.Infrastructure.Data.Configurations;

public class InventoryConfiguration : IEntityTypeConfiguration<Inventory>
{
    public void Configure(EntityTypeBuilder<Inventory> builder)
    {
        builder.ToTable("inventory");

        builder.HasKey(i => i.ProductId);

        builder.Property(i => i.Quantity)
            .IsRequired()
            .HasDefaultValue(0);

        builder.Property(i => i.Reserved)
            .IsRequired()
            .HasDefaultValue(0);

        builder.Property(i => i.LastUpdated)
            .IsRequired();
    }
}
