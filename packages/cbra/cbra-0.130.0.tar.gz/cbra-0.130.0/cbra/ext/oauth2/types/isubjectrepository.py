"""Declares :class:`ISubjectRepository`."""
from typing import Any

from ..exceptions import SubjectDoesNotExist # type: ignore
from .iclient import IClient
from .isubject import ISubject


class ISubjectRepository:
    __module__: str = 'cbra.ext.oauth2.types'
    SubjectDoesNotExist: type[BaseException] = SubjectDoesNotExist

    @classmethod
    def new(cls, **kwargs: Any) -> type['ISubjectRepository']:
        return type(cls.__name__, (cls,), kwargs)

    async def get(
        self,
        client: IClient,
        subject_id: Any,
        force_public: bool = False
    ) -> ISubject | None:
        """Return a :class:`ISubject` implementation for the client specified
        by `client_id` and `subject_id`. If `client_id` is ``None``, no properties
        specific to a client/subject relationship are loaded onto the resulting
        :class:`ISubject` instance.
        """
        raise NotImplementedError

    async def persist(self, client: Any, obj: Any | Any) -> ISubject:
        raise NotImplementedError