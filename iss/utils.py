import issdjango.models
import iss.models


def update_iss_organizations():
    """Update the ISS Organizations from the issdjango data.
    """
    for source_org in issdjango.models.Organizations.objects.all():
        try:
            target_org = iss.models.Organization.objects.get(
                account_num=source_org.account_num)
        except iss.models.Organization.DoesNotExist:
            target_org = iss.models.Organization.objects.create(
                account_num=source_org.account_num)

        target_org.sf_id = source_org.sf_id
        target_org.org_name = source_org.org_name
        target_org.picklist_name = source_org.picklist_name
        target_org.exclude_from_website = source_org.exclude_from_website
        target_org.is_defunct = source_org.is_defunct
        target_org.is_member = source_org.is_member
        target_org.member_type = source_org.member_type
        target_org.business_member_level = source_org.business_member_level
        target_org.sector = source_org.sector
        target_org.org_type = source_org.org_type
        target_org.carnegie_class = source_org.carnegie_class
        target_org.class_profile = source_org.class_profile
        target_org.setting = source_org.setting
        target_org.longitude = source_org.longitude
        target_org.latitude = source_org.latitude
        target_org.street = source_org.street
        target_org.city = source_org.city
        target_org.state = source_org.state
        target_org.postal_code = source_org.postal_code
        target_org.country = source_org.country
        target_org.country_iso = source_org.country_iso
        target_org.website = source_org.website
        target_org.sustainability_website = source_org.sustainability_website
        target_org.enrollment_fte = source_org.enrollment_fte
        target_org.stars_participant_status = (
            source_org.stars_participant_status)
        target_org.pilot_participant = source_org.pilot_participant
        target_org.is_signatory = source_org.is_signatory

        target_org.save()
