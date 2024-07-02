import os
import django
from django.db.models import F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom, Character


# Create queries within functions


def create_pet(name: str, species: str):
    new_pet = Pet.objects.create(name=name, species=species)

    new_pet.save()

    return str(new_pet)


def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool):
    new_artifact = Artifact.objects.create(
        name=name,
        origin=origin,
        age=age,
        description=description,
        is_magical=is_magical
    )

    new_artifact.save()

    return str(new_artifact)


def rename_artifact(artifact: Artifact, new_name: str):
    if artifact.is_magical and artifact.age > 250:
        artifact.name = new_name

    artifact.save()


def delete_all_artifacts():
    Artifact.objects.all().delete()


def show_all_locations():
    locations = Location.objects.all().order_by('-id')

    return "\n".join(str(l) for l in locations)


def new_capital():
    new_capital = Location.objects.first()

    new_capital.is_capital = True

    new_capital.save()


def get_capitals():
    return Location.objects.filter(is_capital=True).values('name')


def delete_first_location():
    Location.objects.first().delete()


def apply_discount():
    cars = Car.objects.all()

    for car in cars:
        car_year = car.year
        car_price = float(car.price)

        discount_percentage = sum([int(x) for x in str(car_year)]) / 100

        discount = car_price * discount_percentage

        car.price_with_discount = car_price - discount

        car.save()


def get_recent_cars():
    manufactured_cars = Car.objects.filter(year__gt=2020)

    return manufactured_cars.values('model', 'price_with_discount')


def delete_last_car():
    Car.objects.last().delete()


def show_unfinished_tasks():
    incomplete_tasks = Task.objects.filter(is_finished=False)

    return '\n'.join([str(t) for t in incomplete_tasks])


def complete_odd_tasks():
    all_tasks = Task.objects.all()

    for task in all_tasks:
        if task.id % 2 != 0:
            task.is_finished = True

        task.save()


def encode_and_replace(text: str, task_title: str):
    encoded_text = ''.join([chr(ord(t) - 3) for t in text])

    Task.objects.filter(title=task_title).update(description=encoded_text)




def get_deluxe_rooms():
    deluxe_rooms = []

    rooms = HotelRoom.objects.all()

    for room in rooms:
        if room.room_type == 'Deluxe' and room.id % 2 == 0:
            deluxe_rooms.append(room)

    return "\n".join(str(r) for r in deluxe_rooms)


def increase_room_capacity():
    rooms = HotelRoom.objects.all().order_by('id')
    length_rooms = len(HotelRoom.objects.all())

    for i in range(length_rooms):
        if not rooms[i].is_reserved:
            continue

        if length_rooms == 1 or i == 0:
            rooms[0].capacity += rooms[0].id
            print(rooms[0].capacity)
        else:
            if not rooms[i - 1].is_reserved:
                rooms[i].capacity += rooms[i - 1].capacity

    HotelRoom.objects.bulk_update(rooms, ['capacity'])


def reserve_first_room():
    first_room = HotelRoom.objects.first()

    first_room.is_reserved = True

    first_room.save()


def delete_last_room():
    last_room = HotelRoom.objects.last()

    if not last_room.is_reserved:
        last_room.delete()


delete_last_room()

def update_characters():
    Character.objects.filter(class_name='Mage').update(
        level=F('level') + 3,
        intelligence=F('intelligence') - 7,
    )

    Character.objects.filter(class_name='Warrior').update(
        hit_points=F('hit_points') / 2,
        dexterity=F('dexterity ') + 4
    )

    Character.objects.filter(class_name__in=["Assassin", "Scout"]).update(
        inventory='The inventory is empty'
    )


def fuse_characters(first_character: Character, second_character: Character):
    name = f"{first_character.name} {second_character.name}"
    class_name = "Fusion"
    level = (first_character.level + second_character.level) // 2
    strength = (first_character.strength + second_character.strength) * 1.2
    dexterity = (first_character.dexterity + second_character.dexterity) * 1.4
    intelligence = (first_character.intelligence + second_character.intelligence) * 1.5
    hit_points = first_character.hit_points + second_character.hit_points
    inventory = None

    if first_character.class_name in ["Mage", "Scout"]:
        inventory = "Bow of the Elven Lords, Amulet of Eternal Wisdom"
    else:
        inventory = "Dragon Scale Armor, Excalibur"

    new_character = Character.objects.create(
        name=name,
        class_name=class_name,
        level=level,
        strength=strength,
        dexterity=dexterity,
        intelligence=intelligence,
        hit_points=hit_points,
        inventory=inventory,
    )

    first_character.delete()
    second_character.delete()


def grand_dexterity():
    Character.objects.update(dexterity=30)


def grand_intelligence():
    Character.objects.update(intelligence=40)


def grand_strength():
    Character.objects.update(strength=50)


def delete_characters():
    Character.objects.filter(inventory="The inventory is empty").delete()
