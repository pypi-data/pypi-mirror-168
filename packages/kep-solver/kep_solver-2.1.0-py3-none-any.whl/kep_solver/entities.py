"""This module contains entities (such as Donors, Recipients) within
a KEP, as well as the encapsulating Instance objects
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import ValuesView
from enum import Enum
from typing import Optional, Union

import pandas  # type: ignore

# We need numpy for NaN, as pandas won't allow None as a categorical data type,
# but will allow NaN
import numpy  # type: ignore


class KEPDataValidationException(Exception):
    """An exception that is raised when invalid data requests are made.
    This can happen if properties (such as blood group or cPRA) are
    requested when they are not known, or if changes are attempted on
    such properties.
    """

    pass


class BloodGroup(Enum):
    """The :ref:`Blood group` of a participant in a KEP."""

    O = 0  # noqa: E741
    A = 1
    B = 2
    AB = 3

    @staticmethod
    def all() -> ValuesView["BloodGroup"]:
        return _BLOODGROUPS.values()

    @staticmethod
    def from_str(bloodGroupText: str) -> "BloodGroup":
        """Given a blood group as text, return the corresponding
        BloodGroup object.

        :param bloodGroupText: the text
        :return: the BloodGroup
        """
        if bloodGroupText not in _BLOODGROUPS:
            raise Exception(f"Unknown blood group: {bloodGroupText}")
        return _BLOODGROUPS[bloodGroupText]

    def __str__(self):
        return _BG_TO_STR[self]


_BLOODGROUPS = {
    "O": BloodGroup.O,
    "A": BloodGroup.A,
    "B": BloodGroup.B,
    "AB": BloodGroup.AB,
}


_BG_TO_STR = {
    BloodGroup.O: "O",
    BloodGroup.A: "A",
    BloodGroup.B: "B",
    BloodGroup.AB: "AB",
}


class Recipient:
    """A recipient in a KEP instance."""

    def __init__(self, id: str):
        self._id: str = id
        self._age: Optional[float] = None
        self._cPRA: Optional[float] = None
        self._bloodGroup: Optional[BloodGroup] = None
        self._donors: list[Donor] = []
        self._compatibilityChance: Optional[float] = None

    def __str__(self):
        return f"R_{self._id}"

    def __repr__(self):
        return str(self)

    def longstr(self):
        """A longer string representation.

        :return: a string representation
        """
        return f"Recipient {self._id}"

    def __hash__(self):
        return hash(f"R{self._id}")

    @property
    def id(self) -> str:
        """Return the ID of this recipient."""
        return self._id

    @property
    def age(self) -> float:
        """The age of this recipient (in years), fractions allowed."""
        if self._age is None:
            raise KEPDataValidationException(f"Age of {str(self)} not known")
        return self._age

    @age.setter
    def age(self, age: float) -> None:
        if self._age is not None and self._age != age:
            raise KEPDataValidationException(f"Trying to change age of {str(self)}")
        self._age = age

    @property
    def cPRA(self) -> float:
        """The :ref:`cPRA` of this recipient, as a value between 0 and 1.

        You may have to divide by 100 if you are used to working with values from 1 to 100 inclusive.
        """
        if self._cPRA is None:
            raise KEPDataValidationException(f"cPRA of {str(self)} not known")
        return self._cPRA

    @cPRA.setter
    def cPRA(self, cPRA: float) -> None:
        if self._cPRA is not None and self._cPRA != cPRA:
            raise KEPDataValidationException(f"Trying to change cPRA of {str(self)}")
        if cPRA > 1 or cPRA < 0:
            raise KEPDataValidationException(
                f"Trying to set the cPRA of {str(self)} to an invalid value."
            )
        self._cPRA = cPRA

    @property
    def bloodGroup(self) -> BloodGroup:
        """The :ref:`Blood group` of this recipient."""
        if self._bloodGroup is None:
            raise KEPDataValidationException(f"Blood group of {str(self)} not known")
        return self._bloodGroup

    @bloodGroup.setter
    def bloodGroup(self, bloodGroup: Union[str, BloodGroup]) -> None:
        if isinstance(bloodGroup, str):
            group = BloodGroup.from_str(bloodGroup)
        else:
            group = bloodGroup
        if self._bloodGroup is not None and self._bloodGroup != group:
            raise KEPDataValidationException(
                f"Trying to change blood group of {str(self)}"
            )
        self._bloodGroup = group

    @property
    def compatibilityChance(self) -> float:
        """The :ref:`compatibility chance` of this Recipient. In other words, what is
        the likelihood that this recipient will be transplant-compatible with
        an arbitrary donor who is ABO compatible."""
        if self._compatibilityChance is None:
            raise KEPDataValidationException(
                f"compatibilityChance of {str(self)} not known"
            )
        return self._compatibilityChance

    @compatibilityChance.setter
    def compatibilityChance(self, new: float) -> None:
        if self._compatibilityChance is not None and self._compatibilityChance != new:
            raise KEPDataValidationException(
                f"Trying to change compatibilityChance of {str(self)}"
            )
        if new > 1 or new < 0:
            raise KEPDataValidationException(
                f"Trying to set the compatibilityChance of {str(self)} to an invalid value."
            )
        self._compatibilityChance = new

    def addDonor(self, donor: Donor) -> None:
        """Add a paired donor for this recipient.

        :param donor: The donor to add
        """
        self._donors.append(donor)

    def donors(self) -> list[Donor]:
        """The list of donors paired with this recipient

        :return: the list of donors
        """
        return self._donors

    def hasBloodCompatibleDonor(self) -> bool:
        """Return true if the recipient is paired with at least one
        donor who is blood-group compatible with this recipient.

        :return: true if the recipient has a blood-group compatible
            donor
        """
        for donor in self.donors():
            if donor.bloodGroupCompatible(self):
                return True
        return False

    def pairedWith(self, donor: Donor) -> bool:
        """Return true if the given donor is paired with this recipient.

        :param donor: The donor in question
        :return: true if the donor is paired with this recipient
        """
        return donor in self.donors()


class Donor:
    """A donor (directed or non-directed) in an instance."""

    def __init__(self, id: str):
        """Construct a Donor object. These are assumed to be
        directed, this can be changed with the NDD instance variable.

        :param id: An identifier for this donor.
        """
        self._id: str = id
        self._recip: Optional[Recipient] = None
        self.NDD: bool = False
        self._age: Optional[float] = None
        self._bloodGroup: Optional[BloodGroup] = None
        self._outgoingTransplants: list["Transplant"] = []

    def __eq__(self, other):
        # An instance can only have one donor of each ID.
        return self.id == other.id

    def __str__(self):
        if self.NDD:
            return f"NDD_{self._id}"
        return f"D_{self._id}"

    def __repr__(self):
        return str(self)

    def longstr(self):
        """A longer string representation.

        :return: a string representation
        """
        if self.NDD:
            return f"Non-directed donor {self._id}"
        return f"Donor {self._id}"

    def __hash__(self):
        return hash(f"D{self._id}")

    @property
    def id(self) -> str:
        """Return the ID of this donor."""
        return self._id

    @property
    def age(self) -> float:
        """The age of the donor (in years), fractions allowed."""
        if self._age is None:
            raise KEPDataValidationException(f"Age of donor {self.id} not known")
        return self._age

    @age.setter
    def age(self, age: float) -> None:
        if self._age is not None and self._age != age:
            raise KEPDataValidationException(f"Trying to change age of donor {self.id}")
        self._age = age

    @property
    def bloodGroup(self) -> BloodGroup:
        """The donor's :ref:`Blood group`"""
        if self._bloodGroup is None:
            raise KEPDataValidationException(f"Blood group of {str(self)} not known")
        return self._bloodGroup

    @bloodGroup.setter
    def bloodGroup(self, bloodGroup: Union[str, BloodGroup]) -> None:
        if isinstance(bloodGroup, str):
            group = BloodGroup.from_str(bloodGroup)
        else:
            group = bloodGroup
        if self._bloodGroup is not None and self._bloodGroup != group:
            raise KEPDataValidationException(
                f"Trying to change blood group of {str(self)}"
            )
        self._bloodGroup = group

    @property
    def recipient(self) -> Recipient:
        """The recipient paired with this donor."""
        if self.NDD:
            raise KEPDataValidationException(
                f"Tried to get recipient of non-directed donor {str(self)}."
            )
        if not self._recip:
            raise KEPDataValidationException(
                f"Donor {str(self)} is directed but has no recipient."
            )
        return self._recip

    @recipient.setter
    def recipient(self, new_recip: Recipient) -> None:
        if self._recip is not None:
            raise KEPDataValidationException(
                f"Tried to set a second recipient on donor {str(self)}"
            )
        if self.NDD:
            raise KEPDataValidationException(
                f"Tried to set recipient of non-directed donor {str(self)}."
            )
        self._recip = new_recip

    def bloodGroupCompatible(self, recipient: Recipient) -> bool:
        """Is this donor blood-group compatible with the given
        recipient.

        :param recipient: the recipient in question
        :return: True if the donor is blood-group compatible with the
            given recipient
        """
        if self.bloodGroup == BloodGroup.O:
            return True
        if recipient.bloodGroup == BloodGroup.AB:
            return True
        return recipient.bloodGroup == self.bloodGroup

    def addTransplant(self, transplant: "Transplant") -> None:
        """Add a potential transplant from this donor.

        :param transplant: the transplant object
        """
        self._outgoingTransplants.append(transplant)

    def transplants(self) -> list[Transplant]:
        """Return the list of transplants associated with this Donor.

        :return: A list of transplants
        """
        return self._outgoingTransplants


class Transplant:
    """A potential transplant."""

    def __init__(self, donor: Donor, recipient: Recipient, weight: float):
        self._donor: Donor = donor
        self._recipient: Recipient = recipient
        self._weight: float = weight

    def __str__(self):
        """Return a string representation of this transplant."""
        return f"Transplant({self.donor.id},{self.recipient.id},{self.weight})"

    @property
    def donor(self) -> Donor:
        return self._donor

    @property
    def recipient(self) -> Recipient:
        return self._recipient

    @property
    def weight(self) -> float:
        return self._weight


class Instance:
    """A KEP instance."""

    def __init__(self) -> None:
        """Create a new KEP instance."""
        self._donors: dict[str, Donor] = {}
        self._recips: dict[str, Recipient] = {}
        self._transplants: list[Transplant] = []

    def addDonor(self, donor: Donor) -> None:
        """Add a donor to the instance.

        :param donor: The Donor being added
        """
        if donor.id in self._donors:
            raise KEPDataValidationException(
                f"Trying to replace Donor {donor.id} in instance"
            )
        self._donors[donor.id] = donor

    def recipient(self, id: str, create: bool = True) -> Recipient:
        """Get a recipient from the instance by ID. If the recipient
        does not exist, create one with no details.

        :param id: the ID of the recipient
        :param create: If True, will create recipient if it doesn't
            exist. If False, and the recipient does not exist, will
            raise an exception.
        :return: the recipient
        """
        if id in self._recips:
            return self._recips[id]
        if not create:
            raise KEPDataValidationException(f"Recipient with ID '{id}' not found")
        recip = Recipient(id)
        self._recips[id] = recip
        return recip

    def addRecipient(self, recipient: Recipient) -> None:
        """Adds an already-constructed Recipient to this instance. If a
        recipient with the same ID already exists, this will throw an
        exception. This will also add the paired donors of the recipient to
        this instance.

        :param recipient: The recipient to add.
        """
        if recipient.id in self._recips:
            raise KEPDataValidationException(
                f"Tried to add a Recipient with ID '{id}' but one already exists"
            )
        self._recips[recipient.id] = recipient
        for donor in recipient.donors():
            self.addDonor(donor)

    def recipients(self) -> ValuesView[Recipient]:
        """Return a list of all recipients.

        :return: a list of recipients
        """
        return self._recips.values()

    def addTransplant(self, transplant: Transplant) -> None:
        """Add a potential transplant to this instance.

        :param transplant: The transplant
        """
        self._transplants.append(transplant)
        transplant.donor.addTransplant(transplant)

    def donors(self) -> ValuesView[Donor]:
        """Return a generator object that can iterate through donors
        in a list-like fashion. Note that this list cannot itself be
        modified.

        :return: a list of donors
        """
        return self._donors.values()

    def donor(self, id: str) -> Donor:
        """Return a donor by ID:

        :param id: a donor ID
        :return: the donor
        """
        return self._donors[id]

    def transplants(self) -> list[Transplant]:
        return self._transplants


class InstanceSet:
    """A set of instances that can be analysed for statistical properties."""

    def __init__(self, instances: list[Instance]):
        """Constructor for InstanceSet.

        :param instances: The set of instances.
        """
        self._instances = instances

    def donor_details(self) -> pandas.DataFrame:
        """Extract a table of donor properties from this set.

        :return: A pandas DataFrame with the following table headers.
            donor_id
            donor_bloodgroup
            paired_recipient_bloodgroup
            is_ndd
        """
        donor_table = {}
        for instance in self._instances:
            for donor in instance.donors():
                donor_table[donor.id] = {
                    "donor_id": donor.id,
                    "donor_bloodgroup": donor.bloodGroup,
                }
                if donor.NDD:
                    donor_table[donor.id].update(
                        {
                            "NDD": True,
                            "paired_recipient_bloodgroup": numpy.nan,
                        }
                    )
                else:
                    donor_table[donor.id].update(
                        {
                            "NDD": False,
                            "paired_recipient_bloodgroup": donor.recipient.bloodGroup,
                        }
                    )
        # Make BloodGroup columns categories, so even if a blood group is not
        # present in a population, it still appears with a count of zero in
        # summary statistics
        bg_category = pandas.CategoricalDtype(
            categories=BloodGroup.all(), ordered=False
        )
        df = pandas.DataFrame(donor_table.values())
        df["donor_bloodgroup"] = df["donor_bloodgroup"].astype(bg_category)
        df["paired_recipient_bloodgroup"] = df["paired_recipient_bloodgroup"].astype(
            bg_category
        )
        return df

    def _calculate_compatibilities(self) -> None:
        """Calculate compatibility chance for each recipient. This generally
        only makes sense if you want to perform statistical analysis on the
        results.
        """
        donors = defaultdict(set)
        compats = defaultdict(set)
        for instance in self._instances:
            for recipient in instance.recipients():
                for donor in instance.donors():
                    # Don't count paired donors
                    if recipient.pairedWith(donor):
                        continue
                    # Skip ABO incompatible
                    if not donor.bloodGroupCompatible(recipient):
                        continue
                    # This donor appears in the same instance at least once
                    donors[recipient.id].add(donor.id)
                    # Get recipients compatible with this donor, see if current
                    # recipient appears in this list
                    if recipient in [t.recipient for t in donor.transplants()]:
                        compats[recipient.id].add(donor.id)
        for instance in self._instances:
            for recipient in instance.recipients():
                if recipient.id not in compats:
                    recipient.compatibilityChance = 0
                else:
                    recipient.compatibilityChance = len(compats[recipient.id]) / len(
                        donors[recipient.id]
                    )

    def recipient_details(self, calculate_compatibility=True) -> pandas.DataFrame:
        """Extract a table of donor properties from this set.

        :param calculate_compatibiltiy: If True (default), this function will
            calculate the compatibility chance for each recipient. Otherwise, each
            recipient must have compatibility chance already determined.
        :return: A pandas DataFrame with the following table headers.
            * recipient_id
            * recipient_bloodgroup
            * cPRA
            * compatibility_chance
            * num_donors
            * has_abo_compatible_donor
        """
        if calculate_compatibility:
            self._calculate_compatibilities()
        recipient_table = {}
        for instance in self._instances:
            for recipient in instance.recipients():
                recipient_table[recipient.id] = {
                    "recipient_id": recipient.id,
                    "recipient_bloodgroup": recipient.bloodGroup,
                    "cPRA": recipient.cPRA,
                    "compatibility_chance": recipient.compatibilityChance,
                    "num_donors": len(recipient.donors()),
                    "has_abo_compatible_donor": recipient.hasBloodCompatibleDonor(),
                }
        return pandas.DataFrame(recipient_table.values())

    def __iter__(self):
        return self._instances.__iter__()
