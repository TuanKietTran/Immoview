import pytest

from apps.agencies.infrastructure.models import AgencyModel
from apps.agencies.performance import can_add_seat
from apps.shared.models import Membership, Role, User


@pytest.mark.django_db
def test_seat_limit_blocks_new_membership() -> None:
    agency = AgencyModel.objects.create(name="A", email="a@e.com", phone="1", canton="VN", seat_limit=1)
    user = User.objects.create_user(email="u@e.com", password="x")
    Membership.objects.create(agency=agency, user=user, role=Role.AGENT)
    assert can_add_seat(agency.id) is False
