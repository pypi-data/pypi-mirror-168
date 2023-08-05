"""Declares :class:`MemorySubjectRepository`."""
import typing

from .types import IClient
from .types import ISubject
from .types import ISubjectRepository


class MemorySubjectRepository(ISubjectRepository):
    """A :class:`ISubjectRepository` implementation that used local
    memory for storage. Mainly for testing purposes.
    """
    __module__: str = 'cbra.ext.oauth2'
    subjects: dict[int | str, ISubject] = {}

    @classmethod
    def add(cls, subject: ISubject) -> None:
        """Add a subject to the repository."""
        cls.subjects[subject.sub] = subject

    @classmethod
    def clear(cls) -> None:
        """Clears the repository of all data."""
        cls.subjects = {}

    @classmethod
    def configure(cls, subjects: dict[str, ISubject]) -> None:
        """Load a mapping of subject identifiers to subjects."""
        cls.subjects.update(subjects) # type: ignore

    def __init__(self):
        self.subjects = MemorySubjectRepository.subjects

    async def get(
        self,
        subject_id: int | str,
        client: IClient | None = None
    ) -> ISubject:
        assert client is not None # nosec
        try:
            subject = self.subjects[subject_id]
            subject.client_id = client.client_id
            return subject
        except KeyError:
            raise self.SubjectDoesNotExist