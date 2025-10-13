from rich import print

from .models import Contact, Listing


# In-memory CRM store
CRM_DB = {
    "contacts": [],
}

# Create some dummy listings
listing1 = Listing(address="123 Maple St, Brooklyn, NY")
listing2 = Listing(address="456 Oak Ave, Queens, NY")
listing3 = Listing(address="789 Pine Blvd, Manhattan, NY")

# Create some dummy contacts
contact1 = Contact(
    name="Alice Johnson",
    # email="alice@example.com",
    phone="555-1234",
    notes=["Interested in Brooklyn listings", "Prefers 2-bedroom apartments"],
    collection=[listing1]
)

contact2 = Contact(
    name="Bob Smith",
    # email="bob.smith@example.com",
    phone="555-5678",
    notes=["Looking for investment property", "Wants a fixer-upper"],
    collection=[listing2, listing3]
)

# Add to CRM_DB
CRM_DB["contacts"].extend([contact1, contact2])

print(CRM_DB)
# --- CONTACTS ---

def create_contact(contact: Contact):
    if isinstance(contact, dict):
        contact = Contact(**contact)
    print(f"[CRM] Creating contact: {contact}")
    CRM_DB["contacts"].append(contact)
    return contact  #  f"Contact {contact.name} has been added to the CRM."

def get_contact_by_name(name: str):
    for contact in CRM_DB["contacts"]:
        if contact.name.lower() == name.lower():
            print(f"[CRM] Found contact: {contact}")
            return contact
    print(f"[CRM] Contact '{name}' not found.")
    return f"Contact '{name}' not found."

def list_contacts():
    print(f"[CRM] Listing all contacts ({len(CRM_DB['contacts'])})")
    return CRM_DB["contacts"]

def add_note_to_contact(id: str, note: str):
    print(id)
    contact = [contact for contact in CRM_DB["contacts"] if contact.id == id][0]
    contact.notes.append(note)
    print(f"[CRM] Adding note to contact: {contact}")
    return f"Note '{note}' has been added to contact '{contact.name}'."

def add_listing_to_contact(id: str, listing: Listing):
    if isinstance(listing, dict):
        listing = Listing(**listing)
    contact = [contact for contact in CRM_DB["contacts"] if contact.id == id][0]
    contact.collection.append(listing)
    print(f"[CRM] Adding listing to contact: {contact}")
    return f"Listing '{listing.address}' has been added to contact '{contact.name}'."