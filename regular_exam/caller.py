import os
from datetime import date

import django
from django.db.models import Q, Count, F, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import Astronaut, Spacecraft, Mission


def get_astronauts(search_string=None):
    if search_string is None:
        return ''

    name_query = Q(name__icontains=search_string)
    phone_number_query = Q(phone_number__icontains=search_string)

    astronauts_matches = Astronaut.objects.filter(
        name_query | phone_number_query
    ).order_by('name')

    if not astronauts_matches:
        return ''

    result = []

    for a in astronauts_matches:
        if a.is_active:
            status = 'Active'
        else:
            status = 'Inactive'

        result.append(f'Astronaut: {a.name}, phone number: {a.phone_number}, status: {status}')

    return '\n'.join(result)


def get_top_astronaut():
    greatest_astronaut = Astronaut.objects.get_astronauts_by_missions_count().first()

    if not greatest_astronaut or not greatest_astronaut.missions.exists():
        return "No data."

    return f"Top Astronaut: {greatest_astronaut.name} with {greatest_astronaut.missions.count()} missions."


def get_top_commander():
    top_commander = (Astronaut.objects
                     .prefetch_related('commander_missions__astronauts')
                     .annotate(count_missions=Count('commander_missions'))
                     .order_by('-count_missions', 'phone_number')
                     .first())

    if not top_commander or not top_commander.commander_missions.exists():
        return "No data."

    return f"Top Commander: {top_commander.name} with {top_commander.commander_missions.count()} commanded missions."


def get_most_used_spacecraft():
    most_used_spacecraft = (Spacecraft.objects
                            .prefetch_related('spacecraft_missions__astronauts')
                            .annotate(count_missions=Count('spacecraft_missions'))
                            .order_by('-count_missions', 'name')
                            .first())

    if not most_used_spacecraft or not most_used_spacecraft.spacecraft_missions.exists():
        return "No data."

    all_missions = most_used_spacecraft.spacecraft_missions.all()
    unique_astronauts = []

    for m in all_missions:
        for a in m.astronauts.all():
            if a not in unique_astronauts:
                unique_astronauts.append(a)

    return (
        f"The most used spacecraft is: {most_used_spacecraft.name}, manufactured by {most_used_spacecraft.manufacturer},"
        f" used in {most_used_spacecraft.count_missions} missions, astronauts on missions: {len(unique_astronauts)}.")


def get_last_completed_mission():
    last_mission = Mission.objects.filter(
        status='Completed'
    ).order_by('-launch_date').first()

    if not last_mission:
        return "No data."

    commander_name = last_mission.commander.name if last_mission.commander and last_mission.commander.name else 'TBA'

    astronauts = ', '.join([a.name for a in last_mission.astronauts.order_by('name')])

    total_spacewalks = 0

    for a in last_mission.astronauts.all():
        total_spacewalks += a.spacewalks

    return (f"The last completed mission is: {last_mission.name}. Commander: {commander_name}."
            f" Astronauts: {astronauts}. Spacecraft: {last_mission.spacecraft.name}."
            f" Total spacewalks: {total_spacewalks}.")


def decrease_spacecrafts_weight():
    # Step 1: Filter unique spacecrafts currently assigned to planned missions
    planned_spacecrafts = Spacecraft.objects.filter(
        spacecraft_missions__status='Planned'
    ).distinct()

    # Step 2: Further filter spacecrafts that weigh at least 200.0 kg
    eligible_spacecrafts = planned_spacecrafts.filter(weight__gte=200.0)

    # If no spacecrafts are eligible, return the no changes message
    if not eligible_spacecrafts.exists():
        return "No changes in weight."

    # Step 3: Decrease their weight by 200.0 kg
    num_of_spacecrafts_affected = eligible_spacecrafts.update(weight=F('weight') - 200.0)

    # Step 4: Calculate the new average weight of all spacecrafts
    avg_weight = Spacecraft.objects.all().aggregate(avg_weight=Avg('weight'))['avg_weight']

    # Step 5: Format the average weight to the first decimal place
    avg_weight = f"{avg_weight:.1f}"

    # Step 6: Return the formatted string
    return f"The weight of {num_of_spacecrafts_affected} spacecrafts has been decreased. The new average weight of all spacecrafts is {avg_weight}kg"


