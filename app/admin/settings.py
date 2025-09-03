from starlette_admin.contrib.sqla import Admin

from app.admin.auth import JSONAuthProvider
from app.admin.views import UserAdminView, ArticleAdminView
from app.database import engine
from app.models.user import User
from app.models.article import Article


admin = Admin(
    engine=engine,
    title="Medium Clone Admin",
    base_url="/admin",
    auth_provider=JSONAuthProvider(login_path="/login", logout_path="/logout"),
)

# Register views
admin.add_view(UserAdminView(User, icon="fa fa-user"))
admin.add_view(ArticleAdminView(Article, icon="fa fa-newspaper"))
