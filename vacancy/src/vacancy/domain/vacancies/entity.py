from datetime import UTC, datetime

from vacancy.domain.ports import Entity
from vacancy.domain.sources.value_objects import SourceId
from vacancy.domain.vacancies.enums import EmploymentType, VacancyStatus, WorkFormat
from vacancy.domain.vacancies.value_objects import Salary, VacancyId


class Vacancy(Entity[VacancyId]):
    def __init__(
        self,
        vacancy_id: VacancyId,
        source_id: SourceId,
        external_id: str | None,
        title: str,
        description: str,
        company_name: str | None,
        employment_type: EmploymentType | None,
        work_format: WorkFormat | None,
        salary: Salary | None,
        location: str | None,
        url: str,
        published_at: datetime | None,
        created_at: datetime | None,
        updated_at: datetime | None,
        status: VacancyStatus
    ) -> None:
        super().__init__(vacancy_id)
        self._source_id = source_id
        self._external_id = external_id
        self._title = title
        self._description = description
        self._company_name = company_name
        self._employment_type = employment_type
        self._work_format = work_format
        self._salary = salary
        self._location = location
        self._url = url
        self._published_at = published_at
        self._created_at = created_at
        self._updated_at = updated_at
        self._status = status

    @property
    def source_id(self) -> SourceId:
        return self._source_id

    @property
    def external_id(self) -> str | None:
        return self._external_id

    @property
    def title(self) -> str:
        return self._title

    @property
    def description(self) -> str:
        return self._description

    @property
    def company_name(self) -> str | None:
        return self._company_name

    @property
    def employment_type(self) -> EmploymentType | None:
        return self._employment_type

    @property
    def work_format(self) -> WorkFormat | None:
        return self._work_format

    @property
    def salary(self) -> Salary | None:
        return self._salary

    @property
    def location(self) -> str | None:
        return self._location

    @property
    def url(self) -> str:
        return self._url

    @property
    def published_at(self) -> datetime | None:
        return self._published_at

    @property
    def created_at(self) -> datetime | None:
        return self._created_at

    @property
    def updated_at(self) -> datetime | None:
        return self._updated_at

    @property
    def status(self) -> VacancyStatus:
        return self._status

    def archive(self) -> None:
        self._status = VacancyStatus.ARCHIVED

    def activate(self) -> None:
        self._status = VacancyStatus.ACTIVE

    def delete(self) -> None:
        self._status = VacancyStatus.DELETED

    def update_details(
        self,
        title: str | None = None,
        description: str | None = None,
        company_name: str | None = None,
        employment_type: EmploymentType | None = None,
        work_format: WorkFormat | None = None,
        salary: Salary | None = None,
        location: str | None = None,
        url: str | None = None,
    ) -> None:
        if title is not None:
            self._title = title
        if description is not None:
            self._description = description
        if company_name is not None:
            self._company_name = company_name
        if employment_type is not None:
            self._employment_type = employment_type
        if work_format is not None:
            self._work_format = work_format
        if salary is not None:
            self._salary = salary
        if location is not None:
            self._location = location
        if url is not None:
            self._url = url

    @classmethod
    def create(
        cls,
        vacancy_id: VacancyId,
        source_id: SourceId,
        external_id: str | None,
        title: str,
        description: str,
        company_name: str | None,
        employment_type: EmploymentType | None,
        work_format: WorkFormat | None,
        salary: Salary | None,
        location: str | None,
        url: str,
        published_at: datetime | None,
    ) -> "Vacancy":
        now = datetime.now(UTC)
        return cls(
            vacancy_id=vacancy_id,
            source_id=source_id,
            external_id=external_id,
            title=title,
            description=description,
            company_name=company_name,
            employment_type=employment_type,
            work_format=work_format,
            salary=salary,
            location=location,
            url=url,
            published_at=published_at,
            created_at=now,
            updated_at=now,
            status=VacancyStatus.ACTIVE,
        )

    @classmethod
    def restore(
        cls,
        vacancy_id: VacancyId,
        source_id: SourceId,
        external_id: str | None,
        title: str,
        description: str,
        company_name: str | None,
        employment_type: EmploymentType,
        work_format: WorkFormat,
        salary: Salary | None,
        location: str | None,
        url: str,
        published_at: datetime,
        created_at: datetime,
        updated_at: datetime,
        status: VacancyStatus,
    ) -> "Vacancy":
        return cls(
            vacancy_id=vacancy_id,
            source_id=source_id,
            external_id=external_id,
            title=title,
            description=description,
            company_name=company_name,
            employment_type=employment_type,
            work_format=work_format,
            salary=salary,
            location=location,
            url=url,
            published_at=published_at,
            created_at=created_at,
            updated_at=updated_at,
            status=status,
        )
