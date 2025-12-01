from dishka import Provider, provide, Scope

from application.interactors.external.list_file import ListFileInteractor
from application.interactors.external.postfile import PostFileInteractor
from application.interactors.login_user import LoginUserInteractor
from application.interactors.logout_user import LogoutUserInteractor
from application.interactors.register_user import RegisterUserInteractor


class InteractorProvider(Provider):
    scope = Scope.REQUEST

    register_user = provide(RegisterUserInteractor)
    login_user = provide(LoginUserInteractor)
    logout_user = provide(LogoutUserInteractor)
    post_file = provide(PostFileInteractor)
    list_file = provide(ListFileInteractor)
