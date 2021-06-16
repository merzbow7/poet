from flask import request, redirect, abort, url_for
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user

from app import app, db
from models import User, Role, Poem, Foto


class AccessModelView:
    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                current_user.has_role('admin')
                )

    def _handle_view(self, name, **kwargs):
        """
            Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


class BaseAdminModelView(AccessModelView, ModelView):
    pass


class AdminIndex(AccessModelView, AdminIndexView):
    pass


class PoemModelView(BaseAdminModelView):
    form_columns = ['title', 'epigraph', 'poem', 'postscriptum']


class UserModelView(BaseAdminModelView):
    form_columns = ['email', 'password', 'first_name', 'last_name', 'active', 'confirmed_at', 'roles']


class RoleModelView(BaseAdminModelView):
    pass


class FotoModelView(BaseAdminModelView):
    form_columns = ['description', 'img']


admin = Admin(app, "Home", url='/', index_view=AdminIndex(name="Admin"))

admin.add_view(UserModelView(User, db.session))
admin.add_view(RoleModelView(Role, db.session))
admin.add_view(PoemModelView(Poem, db.session))
admin.add_view(FotoModelView(Foto, db.session))
