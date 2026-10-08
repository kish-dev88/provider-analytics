from datetime import datetime
from .models import Provider
PROVIDERS=[
Provider(id=1,name="Rocky Dean Buckham",npi="1234567890",change_type="Status",severity="Critical",confidence=97,status="Review",old_value="ACTIVE",proposed_value="Potential license-status exception",payer_address="Seattle, WA",nppes_address="Seattle, WA",pecos_address="Seattle, WA",payer_specialty="Registered Nurse",nppes_specialty="Registered Nurse",pecos_specialty="Nursing",payer_status="ACTIVE",nppes_status="ACTIVE",pecos_enrollment="ENROLLED",submitted_by="Priya S.",submitted_at="Today · 08:14 AM",agent_reason="State credential evidence indicates a potential licensure-status issue. Identity confidence is 97%. Because provider status can affect network and compliance controls, reviewer approval is required before the Provider Master is changed."),
Provider(id=2,name="Maria Gonzalez",npi="1456789012",change_type="Address",severity="High",confidence=96,status="Submitted",old_value="100 Main St, Dallas, TX",proposed_value="220 Main St, Dallas, TX",payer_address="100 Main St, Dallas, TX",nppes_address="220 Main St, Dallas, TX",pecos_address="220 Main St, Dallas, TX",payer_specialty="Cardiology",nppes_specialty="Cardiology",pecos_specialty="Cardiology",payer_status="ACTIVE",nppes_status="ACTIVE",pecos_enrollment="ENROLLED",submitted_by="David R.",submitted_at="Today · 08:02 AM",agent_reason="NPPES and PECOS independently corroborate the same new address. Identity confidence is 96%. Proposed action: update the payer address after workflow approval."),
Provider(id=3,name="James Wilson",npi="1678901234",change_type="Specialty",severity="High",confidence=91,status="Submitted",old_value="Internal Medicine",proposed_value="Cardiology",payer_address="Austin, TX",nppes_address="Austin, TX",pecos_address="Austin, TX",payer_specialty="Internal Medicine",nppes_specialty="Cardiology",pecos_specialty="Cardiology",payer_status="ACTIVE",nppes_status="ACTIVE",pecos_enrollment="ENROLLED",submitted_by="Priya S.",submitted_at="Today · 07:54 AM",agent_reason="NPPES and PECOS agree on Cardiology while the payer master lists Internal Medicine. Identity confidence is 91%. Specialty change should be reviewed before updating the master."),
Provider(id=4,name="Sarah Patel",npi="1789012345",change_type="Phone",severity="Medium",confidence=88,status="Submitted",old_value="(312) 555-0190",proposed_value="(312) 555-0172",payer_address="Chicago, IL",nppes_address="Chicago, IL",pecos_address="Chicago, IL",payer_specialty="Family Medicine",nppes_specialty="Family Medicine",pecos_specialty="Family Medicine",payer_status="ACTIVE",nppes_status="ACTIVE",pecos_enrollment="ENROLLED",submitted_by="Anita K.",submitted_at="Yesterday · 04:42 PM",agent_reason="Phone information differs from NPPES. Identity confidence is 88%. Address and specialty corroborate the provider identity."),
Provider(id=5,name="Robert Chen",npi="1890123456",change_type="Taxonomy",severity="Medium",confidence=94,status="Submitted",old_value="Primary Care",proposed_value="Internal Medicine",payer_address="Boston, MA",nppes_address="Boston, MA",pecos_address="Boston, MA",payer_specialty="Primary Care",nppes_specialty="Internal Medicine",pecos_specialty="Internal Medicine",payer_status="ACTIVE",nppes_status="ACTIVE",pecos_enrollment="ENROLLED",submitted_by="David R.",submitted_at="Yesterday · 03:18 PM",agent_reason="NPPES and PECOS indicate a taxonomy different from the payer master. Identity confidence is 94%. Review the proposed taxonomy update."),
Provider(id=6,name="Linda Thompson",npi="1901234567",change_type="Address",severity="Low",confidence=84,status="Submitted",old_value="Denver, CO",proposed_value="Aurora, CO",payer_address="Denver, CO",nppes_address="Denver, CO",pecos_address="Aurora, CO",payer_specialty="Pediatrics",nppes_specialty="Pediatrics",pecos_specialty="Pediatrics",payer_status="ACTIVE",nppes_status="ACTIVE",pecos_enrollment="ENROLLED",submitted_by="Anita K.",submitted_at="Yesterday · 02:06 PM",agent_reason="PECOS shows a different practice city while NPPES matches the payer. Identity confidence is 84%. Additional evidence is recommended before changing the master.")]
SOURCE_HEALTH={"NPPES":"Oct 8, 2026 · 06:00 AM","PECOS":"Oct 8, 2026 · 05:45 AM","State Medical Boards":"Oct 8, 2026 · 05:30 AM","Client Provider Master Roster":"Oct 8, 2026 · 05:15 AM"}
CHANGE_EVENTS=186
def get_providers(): return PROVIDERS
def get_provider(i): return next((p for p in PROVIDERS if p.id==i),None)
def submit_change(i,v):
    p=get_provider(i)
    if p: p.proposed_value=v; p.status="Submitted"
    return p
def bulk_approve(ids):
    approved=[]
    for i in ids:
        p=get_provider(i)
        if p: p.status="Approved"; approved.append(p.id)
    return approved
def refresh_source(source):
    now=datetime.now().strftime("%b %d, %Y · %I:%M %p").replace(" 0"," ")
    SOURCE_HEALTH[source]=now
    return now
