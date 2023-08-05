import re
from typing_extensions import Self
from contextlib import contextmanager
from typing import TYPE_CHECKING, Any, Dict, List, Union, Callable, Optional, Generator

from nonebot.typing import overrides
from githubkit.utils import UNSET, Unset
from nonebot.message import handle_event
from githubkit import GitHub, AppAuthStrategy, TokenAuthStrategy, OAuthAppAuthStrategy

from nonebot.adapters import Bot as BaseBot

from .config import OAuthApp, GitHubApp
from .message import Message, MessageSegment
from .event import Event, CommitCommentCreated
from .utils import APIContext, get_attr_or_item

if TYPE_CHECKING:
    from githubkit.rest import RestNamespace
    from githubkit.rest.types import AppPermissionsType

    from .adapter import Adapter


def _check_at_me(bot: "GitHubBot", event: Event) -> None:
    try:
        message = event.get_message()
    except Exception:
        return

    # ensure message not empty
    if not message:
        message.append(MessageSegment.markdown(""))
        return

    if message[0].type != "markdown":
        return
    if not bot._app_slug:
        return

    seg = message[0]
    text = str(seg).lstrip()
    if text.startswith(f"@{bot._app_slug}"):
        message[0] = MessageSegment.markdown(text[len(bot._app_slug) + 1 :].lstrip())
        event.to_me = True


def _check_nickname(bot: "Bot", event: Event) -> None:
    try:
        message = event.get_message()
    except Exception:
        return

    # ensure message not empty
    if not message:
        message.append(MessageSegment.markdown(""))
        return

    if message[0].type != "markdown":
        return

    seg = message[0]
    text = str(seg).lstrip()

    if nicknames := {nickname for nickname in bot.config.nickname if nickname}:
        # check if the user is calling me with my nickname
        nickname_regex = "|".join(nicknames)
        if m := re.match(rf"^({nickname_regex})([\s,，]*|$)", text, re.IGNORECASE):
            event.to_me = True
            message[0] = MessageSegment.markdown(text[m.end() :])


async def send(
    bot: "Bot", event: Event, message: Union[str, Message, MessageSegment]
) -> Any:
    msg = message if isinstance(message, Message) else Message(message)
    if isinstance(event, CommitCommentCreated):
        return await bot.rest.repos.async_create_commit_comment(
            owner=event.payload.repository.owner.login,
            repo=event.payload.repository.name,
            commit_sha=event.payload.comment.commit_id,
            body=msg.extract_plain_text(),
        )

    owner: Optional[str] = None
    repo: Optional[str] = None
    if repository := get_attr_or_item(event.payload, "repository"):
        owner_user = get_attr_or_item(repository, "owner")
        owner = get_attr_or_item(owner_user, "login")
        repo = get_attr_or_item(repository, "name")

    number: Optional[int] = None
    if issue := get_attr_or_item(event.payload, "issue"):
        number = get_attr_or_item(issue, "number")
    elif pull_request := get_attr_or_item(event.payload, "pull_request"):
        number = get_attr_or_item(pull_request, "number")

    if owner and repo and number:
        return await bot.rest.issues.async_create_comment(
            owner=owner, repo=repo, issue_number=number, body=msg.extract_plain_text()
        )

    raise RuntimeError(
        f"Cannot guess reply target for event type {event.__class__.__name__}"
    )


class Bot(BaseBot):
    adapter: "Adapter"

    send_handler: Callable[
        ["Bot", Event, Union[str, Message, MessageSegment]], Any
    ] = send

    if TYPE_CHECKING:
        rest: RestNamespace

        async def async_graphql(
            self, query: str, variables: Optional[Dict[str, Any]] = None
        ) -> Dict[str, Any]:
            ...

    @overrides(BaseBot)
    def __init__(self, adapter: "Adapter", app: Union[GitHubApp, OAuthApp]):
        super().__init__(adapter, app.id)
        self.app = app
        self._github: GitHub
        self._ctx_github: Optional[GitHub] = None

    def __getattr__(self, name: str) -> APIContext:
        return APIContext(self, (name,))

    @property
    def github(self) -> GitHub:
        return self._ctx_github or self._github

    async def handle_event(self, event: Event) -> None:
        await handle_event(self, event)

    @overrides(BaseBot)
    async def send(
        self, event: Event, message: Union[str, Message, MessageSegment]
    ) -> Any:
        return await self.__class__.send_handler(self, event, message)


class OAuthBot(Bot):
    @overrides(Bot)
    def __init__(self, adapter: "Adapter", app: OAuthApp):
        super().__init__(adapter, app)
        self._github: GitHub[OAuthAppAuthStrategy] = GitHub(
            OAuthAppAuthStrategy(app.client_id, app.client_secret),
            base_url=self.adapter.github_config.github_base_url,
            accept_format=self.adapter.github_config.github_accept_format,
            previews=self.adapter.github_config.github_previews,
            timeout=self.config.api_timeout,
        )

    @contextmanager
    def as_web_user(
        self, code: str, redirect_uri: Optional[str] = None
    ) -> Generator[Self, None, None]:
        if self._ctx_github is not None:
            raise RuntimeError("Can not enter context twice.")
        self._ctx_github = self._github.with_auth(
            self._github.auth.as_web_user(code, redirect_uri)
        )
        try:
            yield self
        finally:
            self._ctx_github = None

    @contextmanager
    def as_user(self, token: str) -> Generator[Self, None, None]:
        if self._ctx_github is not None:
            raise RuntimeError("Can not enter context twice.")
        self._ctx_github = GitHub(TokenAuthStrategy(token))
        try:
            yield self
        finally:
            self._ctx_github = None

    @overrides(Bot)
    async def handle_event(self, event: Event) -> None:
        _check_nickname(self, event)
        await super().handle_event(event)


class GitHubBot(Bot):
    @overrides(Bot)
    def __init__(self, adapter: "Adapter", app: GitHubApp):
        super().__init__(adapter, app)
        self._github: GitHub[AppAuthStrategy] = GitHub(
            AppAuthStrategy(
                app.app_id, app.private_key, app.client_id, app.client_secret
            ),
            base_url=self.adapter.github_config.github_base_url,
            accept_format=self.adapter.github_config.github_accept_format,
            previews=self.adapter.github_config.github_previews,
            timeout=self.config.api_timeout,
        )
        self._app_slug: Optional[str] = None

    async def _get_self_info(self):
        res = await self._github.rest.apps.async_get_authenticated()
        self._app_slug = (
            slug if isinstance((slug := res.parsed_data.slug), str) else None
        )

    @contextmanager
    def as_oauth_app(self) -> Generator[Self, None, None]:
        if self._ctx_github is not None:
            raise RuntimeError("Can not enter context twice.")
        self._ctx_github = self._github.with_auth(self._github.auth.as_oauth_app())
        try:
            yield self
        finally:
            self._ctx_github = None

    @contextmanager
    def as_installation(
        self,
        installation_id: int,
        repositories: Union[Unset, List[str]] = UNSET,
        repository_ids: Union[Unset, List[int]] = UNSET,
        permissions: Union[Unset, "AppPermissionsType"] = UNSET,
    ) -> Generator[Self, None, None]:
        if self._ctx_github is not None:
            raise RuntimeError("Can not enter context twice.")
        self._ctx_github = self._github.with_auth(
            self._github.auth.as_installation(
                installation_id, repositories, repository_ids, permissions
            )
        )
        try:
            yield self
        finally:
            self._ctx_github = None

    @contextmanager
    def as_web_user(
        self, code: str, redirect_uri: Optional[str] = None
    ) -> Generator[Self, None, None]:
        if self._ctx_github is not None:
            raise RuntimeError("Can not enter context twice.")
        self._ctx_github = self._github.with_auth(
            self._github.auth.as_oauth_app().as_web_user(code, redirect_uri)
        )
        try:
            yield self
        finally:
            self._ctx_github = None

    @contextmanager
    def as_user(self, token: str) -> Generator[Self, None, None]:
        if self._ctx_github is not None:
            raise RuntimeError("Can not enter context twice.")
        self._ctx_github = GitHub(TokenAuthStrategy(token))
        try:
            yield self
        finally:
            self._ctx_github = None

    @overrides(Bot)
    async def handle_event(self, event: Event) -> None:
        _check_at_me(self, event)
        _check_nickname(self, event)
        await super().handle_event(event)
