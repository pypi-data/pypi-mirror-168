"""Dataclasses to use and configure planning and scheduling with."""

import math
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Union

from serde import field, serde

name_field = field(default=None, skip_if_default=True)


class Distribution(ABC):
    """Abstract base class for distributions."""

    @abstractmethod
    def cdf(self, x: float = 1.0) -> float:
        """Cumulative probability density function of this distribution."""


@serde
@dataclass
class WeibullDistribution(Distribution):
    """Weibull distribution (2-parameter).

    Arguments:
        alpha: Shape parameter.
        mtbf: Mean time between failure.
    """

    alpha: float = 2.0
    mtbf: float = 10.0

    @property
    def beta(self) -> float:
        """Weibull scale parameter."""
        return self.mtbf / math.gamma(1 + 1 / self.alpha)

    def cdf(self, x: float = 1.0) -> float:
        return 1 - math.exp(1) ** -((x / self.beta) ** self.alpha)


Distributions = Union[WeibullDistribution, Distribution]


@serde
@dataclass
class Task:
    """Maintenance task to apply to a component.

    Arguments:
        name: Name for this action.
        rejuvenation: Rejuvenation factor between [0.0-1.0]. Percentage of age that is
            regained. Therefore, 1.0 would mean a full replacement.
        duration: Duration of the maintenance. Usually in years.
        cost: Cost of the maintenance. Usually expressed in a currency or equivalent.
    """

    name: Optional[str] = name_field
    rejuvenation: float = 1.0
    duration: float = 1.0
    cost: float = 1.0


@serde
@dataclass
class Maintenance:
    """Maintenance task scheduled at a point in time."""

    name: Optional[str] = name_field
    task: Task = field(default_factory=Task)
    time: float = 1.0


@serde
@dataclass
class Component:
    """Component with a failure distribution.

    Arguments:
        name: Name of this component.
        age: Starting age offset (usually in years).
        distribution: Failure distribution to use.
        maintenance: List of maintenance tasks that should be applied over this
            component's lifespan.
    """

    name: Optional[str] = name_field
    age: float = 0.0
    distribution: Distributions = field(default_factory=WeibullDistribution)
    maintenance: list[Maintenance] = field(default_factory=list)

    def get_ordered_maintenance(self) -> list[Maintenance]:
        """Maintenance tasks sorted in time."""
        return sorted(self.maintenance, key=lambda m: m.time)

    def cdf(self, x: float = 1.0) -> float:
        """Cumulative failure probability density function incorporating maintenance."""
        return self.distribution.cdf(self.get_age_at(x))

    def get_age_at(self, x: float = 1.0) -> float:
        """Effective age at a point in time given the currently set schedule."""
        age = float(self.age)
        last_time = 0.0
        for m in self.get_ordered_maintenance():
            if m.time > x:
                # Maintenance is yet to happen.
                break
            # Apply rejuvenation with the then actual age.
            age = (age + m.time - last_time) * (1.0 - m.task.rejuvenation)
            last_time = m.time
        # Add remaining time since last maintenance.
        age += x - last_time
        return age


@serde
@dataclass
class System:
    """A system consisting of multiple components.

    Arguments:
        name: Name of this system.
        components: Components of this system.
    """

    name: Optional[str] = name_field
    components: list[Component] = field(default_factory=lambda: [Component()])

    def cdf(self, x: float = 1.0) -> float:
        """Cumulative failure probability density function as the sum of its
        components' respective function incorporating maintenance.
        """
        return sum(c.cdf(x) for c in self.components)

    def get_ordered_maintenance(self) -> list[Maintenance]:
        """Get all maintenance ordered in time."""
        return sorted(
            [m for c in self.components for m in c.maintenance], key=lambda m: m.time
        )
