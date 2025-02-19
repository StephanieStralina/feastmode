from .models import Party, Rsvp

def get_rsvp(party, user_id):
    try:
        rsvp = party.rsvp.get(user_id=user_id)
        return rsvp
    except Rsvp.DoesNotExist:
        return None