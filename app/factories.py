import random
import uuid

import factory

from app.schemas.quay import Quay
from app.schemas.route import TripRoute, Terminal
from app.schemas.trip import Trip, Line, Tenant
from app.schemas.vehicle import Vehicle, VehicleInDb


class VehicleInDbFactory(factory.Factory):
    class Meta(object):
        model = VehicleInDb

    id = factory.LazyFunction(uuid.uuid4)


class LineFactory(factory.Factory):
    class Meta(object):
        model = Line

    id = factory.LazyFunction(uuid.uuid4)
    name = factory.Sequence(lambda n: f'Line {n}')
    short_name = factory.LazyAttribute(lambda line: line.name)
    number = factory.LazyAttribute(lambda line: line.name.split(' ')[-1])


class TerminalFactory(factory.Factory):
    class Meta(object):
        model = Terminal

    name = factory.Faker('street_name')
    code = factory.Faker('street_suffix')


class TripRouteFactory(factory.Factory):
    class Meta(object):
        model = TripRoute

    id = factory.Faker('uuid4')
    start_terminus = factory.SubFactory(TerminalFactory)
    end_terminus = factory.SubFactory(TerminalFactory)


class QuayFactory(factory.Factory):
    class Meta(object):
        model = Quay

    id = factory.LazyFunction(uuid.uuid4)
    name = factory.Faker('street_name')


class TenantFactory(factory.Factory):
    class Meta(object):
        model = Tenant

    name = factory.Faker('company')


class TripFactory(factory.Factory):
    class Meta(object):
        model = Trip

    vehicle = factory.SubFactory(VehicleInDbFactory)
    eta = factory.Faker('pyint', min_value=60, max_value=60 * 60)
    line: Line = factory.SubFactory(LineFactory)
    route: TripRoute = factory.SubFactory(TripRouteFactory)
    quays: list[Quay] = factory.List([QuayFactory() for _ in range(random.randint(1, 15))])
    tenant: Tenant = factory.SubFactory(TenantFactory)
