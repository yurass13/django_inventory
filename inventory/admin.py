from django.contrib import admin

from .models import (
    Country,
    Supplier,
    ProductModel,
    ProductPrototype,

    Employee,
    Storage,

    Inventory,
)


admin.site.register([
        Country,
        Supplier,
        ProductModel,
        ProductPrototype,

        Employee,
        Storage,

        # FIXME layout on admin panel need to be separated on storage as subindex with ListView
        Inventory,
    ]
)