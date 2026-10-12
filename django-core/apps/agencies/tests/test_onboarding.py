import uuid

import pytest

from apps.agencies.application import InvalidAgencyTransition, approve_agency, submit_for_approval
from apps.agencies.infrastructure.models import AgencyModel, AgencyStatus, KycDocument


@pytest.fixture
def agency(db: None) -> AgencyModel:
    return AgencyModel.objects.create(name="VN Realty", email="vn@example.com", phone="0901", canton="VN")


@pytest.mark.django_db
def test_agency_onboarding_requires_approval(agency: AgencyModel) -> None:
    submit_for_approval(agency.id)
    approved = approve_agency(agency.id, uuid.uuid4())
    assert approved.status == AgencyStatus.APPROVED
    assert approved.approved_at is not None


@pytest.mark.django_db
def test_approval_cannot_skip_submission(agency: AgencyModel) -> None:
    with pytest.raises(InvalidAgencyTransition):
        approve_agency(agency.id, uuid.uuid4())


@pytest.mark.django_db
def test_kyc_document_is_attached_to_agency(agency: AgencyModel) -> None:
    document = KycDocument.objects.create(agency=agency, document_type="business_license", storage_key="kyc/a.pdf", checksum="a" * 64)
    assert agency.kyc_documents.get().id == document.id
