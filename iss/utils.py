import issdjango.models
import iss.models


def update_iss_organizations():
    """Update the ISS Organizations from the issdjango data.
    """
    for source in issdjango.models.Organizations.objects.all():
        try:
            target = iss.models.Organization.objects.get(
                account_num=source.account_num)
        except iss.models.Organization.DoesNotExist:
            target = iss.models.Organization(
                account_num=source.account_num)

        target.sf_id = source.sf_id
        target.org_name = source.org_name
        target.picklist_name = source.picklist_name
        target.exclude_from_website = source.exclude_from_website
        target.is_defunct = source.is_defunct
        target.is_member = source.is_member
        if source.member_type is not None:
            target.member_type = source.member_type
        else:
            target.member_type = ""
        target.business_member_level = source.business_member_level
        target.sector = source.sector
        target.org_type = source.org_type
        if source.carnegie_class is not None:
            target.carnegie_class = source.carnegie_class
        else:
            target.carnegie_class = ""
        if source.class_profile is not None:
            target.class_profile = source.class_profile
        else:
            target.class_profile = ""
        if source.setting is not None:
            target.setting = source.setting
        else:
            target.setting = ""
        if source.longitude is not None:
            target.longitude = source.longitude
        else:
            target.longitude = ""
        if source.latitude is not None:
            target.latitude = source.latitude
        else:
            target.latitude = ""
        if source.street is not None:
            target.street = source.street
        else:
            target.street = ""
        if source.city is not None:
            target.city = source.city
        else:
            target.city = ""
        target.state = source.state
        if source.postal_code is not None:
            target.postal_code = source.postal_code
        else:
            target.postal_code = ""
        target.country = source.country
        if source.country_iso is not None:
            target.country_iso = source.country_iso
        else:
            target.country_iso = ""
        if source.website is not None:
            target.website = source.website
        else:
            target.website = ""
        if source.sustainability_website is not None:
            target.sustainability_website = source.sustainability_website
        else:
            target.sustainability_website = ""
        target.enrollment_fte = source.enrollment_fte
        target.stars_participant_status = source.stars_participant_status
        target.pilot_participant = source.pilot_participant
        target.is_signatory = source.is_signatory

        target.save()
