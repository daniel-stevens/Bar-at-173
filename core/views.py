# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.utils import timezone
from .models import User, Drink, Session, Consumption

def get_active_session():
    """Helper to get the current active session (session with no end_time)."""
    try:
        return Session.objects.get(end_time__isnull=True)
    except Session.DoesNotExist:
        return None

def kiosk_user_select(request):
    """View for kiosk to select a user."""
    session = get_active_session()
    if not session:
        # If no active session, show a message
        return render(request, 'kiosk_no_session.html')
    users = User.objects.filter(is_active=True).order_by('first_name')
    return render(request, 'kiosk_user_select.html', {'session': session, 'users': users})

def kiosk_drink_select(request, user_id):
    """View to select a drink for the given user in the current session."""
    session = get_active_session()
    if not session:
        return redirect('kiosk')  # no session, redirect to home (which will show message)
    # Get user or 404 if not found
    user = get_object_or_404(User, pk=user_id, is_active=True)
    # # We might ensure staff/admin users are not listed in kiosk
    # if not user.is_active or user.is_staff:
    #     return HttpResponseForbidden("Invalid user")
    # Get available drinks for this session
    drinks = session.drinks.all().order_by('name')
    context = {'session': session, 'user': user, 'drinks': drinks}
    return render(request, 'kiosk_drink_select.html', context)

def log_consumption(request, user_id, drink_id):
    """Process logging a drink consumption. Expects POST (from kiosk interface)."""
    if request.method != 'POST':
        # Disallow GET requests to log consumption to prevent accidental logs via simple link
        return HttpResponseForbidden("Invalid request method.")
    session = get_active_session()
    if not session:
        return HttpResponseForbidden("No active session.")
    user = get_object_or_404(User, pk=user_id, is_active=True)
    drink = get_object_or_404(Drink, pk=drink_id)
    # Validate that the drink is offered in the current session
    if drink not in session.drinks.all():
        return HttpResponseForbidden("Drink not available in this session.")
    # Create the consumption record
    Consumption.objects.create(user=user, drink=drink, session=session,
                               price_pence=drink.price_pence, timestamp=timezone.now())
    # Redirect back to kiosk main page (user selection) with a success message
    # (We could use Django messages framework to flash a "Logged!" message)
    return redirect('kiosk')


from django.db.models import Count

def scoreboard_view(request, session_id=None):
    """Display the leaderboard for the current session, or a given session."""
    # Determine which session to show
    if session_id:
        session = get_object_or_404(Session, pk=session_id)
    else:
        session = get_active_session()
    if not session:
        # No active session and no session_id given
        return render(request, 'scoreboard.html', {'session': None})
    # Get all consumption logs for this session
    logs = Consumption.objects.select_related('user', 'drink').filter(session=session)
    # Aggregate total drinks per user, and per user per drink
    user_totals = {}    # map user -> total drinks
    user_drinks = {}    # map user -> { drink -> count }
    for log in logs:
        user = log.user
        drink = log.drink
        user_totals[user] = user_totals.get(user, 0) + 1
        # count per drink
        if user not in user_drinks:
            user_drinks[user] = {}
        user_drinks[user][drink] = user_drinks[user].get(drink, 0) + 1
    # Sort users by total desc
    leaderboard = sorted(user_totals.items(), key=lambda item: item[1], reverse=True)
    # leaderboard is list of (user, total) sorted by total
    context = {
        'session': session,
        'leaderboard': leaderboard,
        'user_drinks': user_drinks,
        'now': timezone.now()  # could be used to show last update time
    }
    # If this is an HTMX request (partial update), render a fragment without full layout
    if request.headers.get('HX-Request'):
        return render(request, '_scoreboard_table.html', context)
    else:
        return render(request, 'scoreboard.html', context)

