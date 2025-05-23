import strawberry
from typing import List, Optional
from datetime import datetime
from .types import (
    Product, Sale, InventoryLog, LowStockAlert,
    SalesAnalytics, CategoryAnalytics,
    ProductInput, SaleInput, InventoryUpdateInput, LowStockAlertInput
)
from .resolvers import (
    get_products, get_product, get_sales,
    get_inventory_logs, get_low_stock_alerts,
    get_sales_analytics, create_product,
    create_sale, update_inventory, set_low_stock_alert
)

@strawberry.type
class Query:
    @strawberry.field
    async def products(
        self,
        category: Optional[str] = None
    ) -> List[Product]:
        return await get_products(category)

    @strawberry.field
    async def product(self, id: int) -> Optional[Product]:
        return await get_product(id)

    @strawberry.field
    async def sales(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Sale]:
        return await get_sales(start_date, end_date)

    @strawberry.field
    async def inventory_logs(
        self,
        product_id: int
    ) -> List[InventoryLog]:
        return await get_inventory_logs(product_id)

    @strawberry.field
    async def low_stock_alerts(
        self,
        active_only: bool = True
    ) -> List[LowStockAlert]:
        return await get_low_stock_alerts(active_only)

    @strawberry.field
    async def sales_analytics(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> SalesAnalytics:
        return await get_sales_analytics(start_date, end_date)

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_product(
        self,
        input: ProductInput
    ) -> Product:
        return await create_product(input)

    @strawberry.mutation
    async def create_sale(
        self,
        input: SaleInput
    ) -> Sale:
        return await create_sale(input)

    @strawberry.mutation
    async def update_inventory(
        self,
        input: InventoryUpdateInput
    ) -> InventoryLog:
        return await update_inventory(input)

    @strawberry.mutation
    async def set_low_stock_alert(
        self,
        input: LowStockAlertInput
    ) -> LowStockAlert:
        return await set_low_stock_alert(input)

schema = strawberry.Schema(query=Query, mutation=Mutation) 