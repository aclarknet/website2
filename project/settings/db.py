from .base import *

FOUR_O_3 = "Sorry, you are not allowed to see or do that."

DOC_TYPES = [
    ("Invoice", "Invoice"),
    ("Estimate", "Estimate"),
    ("Proposal", "Proposal"),
    ("Statement of Work", "Statement of Work"),
    ("Task Order", "Task Order"),
    ("Independent Government Cost Estimate", "Independent Government Cost Estimate"),
]

SEARCH_FIELDS = {
    "account": ("name",),
    "client": ("name", "address", "description", "url"),
    "company": (),
    "contact": ("first_name", "last_name", "email", "phone", "address", "client__name"),
    "invoice": (
        "doc_type",
        "issue_date",
        "start_date",
        "end_date",
        "last_payment_date",
        "subject",
        "ein",
        "po_number",
        "sa_number",
        "client__name",
        "project__name",
        "note__text",
    ),
    "note": ("title", "text"),
    "profile": (),
    "project": ("name",),
    "report": ("name",),
    "service": (),
    "Site_Configuration": (),
    "task": (),
    "testimonial": (),
    "time": (
        "client__name",
        "date",
        "project__name",
        "hours",
        "description",
        "user__username",
    ),
    "user": ("username",),
}

MAIL_FROM = "aclark.net@aclark.net"
MAIL_TO = "aclark@aclark.net"

LOUNGE_AWAY = True
# LOUNGE_AWAY = False
