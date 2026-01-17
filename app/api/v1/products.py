from app.api.base.products import BaseProductRouter

# Create v1 router by inheriting from base
base_router = BaseProductRouter()
router = base_router.router

# v1 specific customizations (if any)
# For now, v1 uses the base implementation exactly
