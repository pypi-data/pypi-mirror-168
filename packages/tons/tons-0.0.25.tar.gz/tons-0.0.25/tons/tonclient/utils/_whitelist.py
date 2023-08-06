from typing import Optional
from pydantic import BaseModel, validator

from ._exceptions import WhitelistContactAlreadyExistsError, WhitelistContactDoesNotExistError
from tons.tonsdk.utils import Address, InvalidAddressError
from tons.utils import storage


class WhitelistContact(BaseModel):
    name: str
    address: str

    class Config:
        validate_assignment = True

    @validator('address')
    def validate_address(cls, v, values, **kwargs):
        if v:
            try:
                Address(v)
                return v

            except InvalidAddressError as e:
                raise ValueError(e)


class Whitelist:
    def __init__(self, whitelist_path: str):
        self.whitelist_path = whitelist_path

        try:
            contacts_json = storage.read_json(whitelist_path)
        except FileNotFoundError:
            self.contacts = []
        else:
            if contacts_json:
                self.contacts = [WhitelistContact.parse_obj(contact)
                                 for contact in contacts_json]
            else:
                self.contacts = []

    def add_contact(self, name: str, address: str, save: bool = False):
        address = Address(address).to_string(True, True, True)

        names = {contact.name for contact in self.contacts}
        addresses = {contact.address for contact in self.contacts}

        if name in names:
            raise WhitelistContactAlreadyExistsError(
                f"Contact with the name '{name}' already exists")
        if address in addresses:
            raise WhitelistContactAlreadyExistsError(
                f"Contact with the address {address} already exists")

        self.contacts.append(WhitelistContact(name=name,
                                              address=address))

        if save:
            self.save()

    def get_contact(self, name: str, raise_none: bool = False) -> Optional[WhitelistContact]:
        contact = next(
            (contact for contact in self.contacts if contact.name == name), None)
        if contact is None and raise_none:
            raise WhitelistContactDoesNotExistError(
                f"Contact with the name {name} does not exist")

        return contact

    def edit_contact(self, name: str, new_name: Optional[str], new_address: Optional[str], save: bool = False):
        contact = self.get_contact(name, raise_none=True)
        contact_idx = self.contacts.index(contact)

        if new_name:
            self.contacts[contact_idx].name = new_name

        if new_address:
            self.contacts[contact_idx].address = new_address

        if save:
            self.save()

    def delete_contact(self, name: str, save: bool = False):
        contact = self.get_contact(name, raise_none=True)
        self.contacts.remove(contact)

        if save:
            self.save()

    def save(self):
        contacts = [contact.dict() for contact in sorted(self.contacts, key=lambda contact: contact.name)]
        storage.save_json(self.whitelist_path, contacts)
