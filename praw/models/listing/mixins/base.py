"""Provide the BaseListingMixin class."""
from typing import Any, Dict, Iterator, Union
from urllib.parse import urljoin

from ....util import _deprecate_args
from ...base import PRAWBase
from ..generator import ListingGenerator


def _prepare(praw_object, arguments_dict, target):
    """Fix for :class:`.Redditor` methods that use a query param rather than subpath."""
    if praw_object.__dict__.get("_listing_use_sort"):
        PRAWBase._safely_add_arguments(arguments_dict, "params", sort=target)
        return praw_object._path
    return urljoin(praw_object._path, target)


class BaseListingMixin(PRAWBase):
    """Adds minimum set of methods that apply to all listing objects."""

    VALID_TIME_FILTERS = {"all", "day", "hour", "month", "week", "year"}

    @staticmethod
    def _validate_time_filter(time_filter):
        """Validate ``time_filter``.

        :raises: :py:class:`ValueError` if ``time_filter`` is not valid.

        """
        if time_filter not in BaseListingMixin.VALID_TIME_FILTERS:
            valid_time_filters = ", ".join(BaseListingMixin.VALID_TIME_FILTERS)
            raise ValueError(f"time_filter must be one of: {valid_time_filters}")

    @_deprecate_args("time_filter")
    def controversial(
        self,
        *,
        time_filter: str = "all",
        **generator_kwargs: Union[str, int, Dict[str, str]],
    ) -> Iterator[Any]:
        """Return a :class:`.ListingGenerator` for controversial items.

        :param time_filter: Can be one of: ``"all"``, ``"day"``, ``"hour"``,
            ``"month"``, ``"week"``, or ``"year"`` (default: ``"all"``).

        :raises: :py:class:`ValueError` if ``time_filter`` is invalid.

        Additional keyword arguments are passed in the initialization of
        :class:`.ListingGenerator`.

        This method can be used like:

        .. code-block:: python

            reddit.domain("imgur.com").controversial(time_filter="week")
            reddit.multireddit("samuraisam", "programming").controversial(time_filter="day")
            reddit.redditor("spez").controversial(time_filter="month")
            reddit.redditor("spez").comments.controversial(time_filter="year")
            reddit.redditor("spez").submissions.controversial(time_filter="all")
            reddit.subreddit("all").controversial(time_filter="hour")

        """
        self._validate_time_filter(time_filter)
        self._safely_add_arguments(generator_kwargs, "params", t=time_filter)
        url = _prepare(self, generator_kwargs, "controversial")
        return ListingGenerator(self._reddit, url, **generator_kwargs)

    def hot(self, **generator_kwargs: Union[str, int, Dict[str, str]]) -> Iterator[Any]:
        """Return a :class:`.ListingGenerator` for hot items.

        Additional keyword arguments are passed in the initialization of
        :class:`.ListingGenerator`.

        This method can be used like:

        .. code-block:: python

            reddit.domain("imgur.com").hot()
            reddit.multireddit("samuraisam", "programming").hot()
            reddit.redditor("spez").hot()
            reddit.redditor("spez").comments.hot()
            reddit.redditor("spez").submissions.hot()
            reddit.subreddit("all").hot()

        """
        generator_kwargs.setdefault("params", {})
        url = _prepare(self, generator_kwargs, "hot")
        return ListingGenerator(self._reddit, url, **generator_kwargs)

    def new(self, **generator_kwargs: Union[str, int, Dict[str, str]]) -> Iterator[Any]:
        """Return a :class:`.ListingGenerator` for new items.

        Additional keyword arguments are passed in the initialization of
        :class:`.ListingGenerator`.

        This method can be used like:

        .. code-block:: python

            reddit.domain("imgur.com").new()
            reddit.multireddit("samuraisam", "programming").new()
            reddit.redditor("spez").new()
            reddit.redditor("spez").comments.new()
            reddit.redditor("spez").submissions.new()
            reddit.subreddit("all").new()

        """
        generator_kwargs.setdefault("params", {})
        url = _prepare(self, generator_kwargs, "new")
        return ListingGenerator(self._reddit, url, **generator_kwargs)

    @_deprecate_args("time_filter")
    def top(
        self,
        *,
        time_filter: str = "all",
        **generator_kwargs: Union[str, int, Dict[str, str]],
    ) -> Iterator[Any]:
        """Return a :class:`.ListingGenerator` for top items.

        :param time_filter: Can be one of: ``"all"``, ``"day"``, ``"hour"``,
            ``"month"``, ``"week"``, or ``"year"`` (default: ``"all"``).

        :raises: :py:class:`ValueError` if ``time_filter`` is invalid.

        Additional keyword arguments are passed in the initialization of
        :class:`.ListingGenerator`.

        This method can be used like:

        .. code-block:: python

            reddit.domain("imgur.com").top(time_filter="week")
            reddit.multireddit("samuraisam", "programming").top(time_filter="day")
            reddit.redditor("spez").top(time_filter="month")
            reddit.redditor("spez").comments.top(time_filter="year")
            reddit.redditor("spez").submissions.top(time_filter="all")
            reddit.subreddit("all").top(time_filter="hour")

        """
        self._validate_time_filter(time_filter)
        self._safely_add_arguments(generator_kwargs, "params", t=time_filter)
        url = _prepare(self, generator_kwargs, "top")
        return ListingGenerator(self._reddit, url, **generator_kwargs)
