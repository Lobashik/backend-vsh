from backend.app.api.auth import router as auth_router
from backend.app.api.gallery import router as gallery_router
from backend.app.api.images import router as images_router
from backend.app.api.users import router as users_router

routers = [auth_router, users_router, images_router, gallery_router]