from django.contrib import admin

from store.models import Item, Store


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """Item Admin."""

    list_display = (
        "name",
        "price",
    )
    search_fields = ("name",)


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    """Store Admin."""

    list_display = (
        "name",
        "amount_of_items",
    )
    search_fields = ("name",)

    def amount_of_items(self, obj: Store):
        """Get the amount of items registered on a Store."""
        return obj.items.all().count()
