# Structure Of The Project

Voici une petite représentation visuelle de la structure globale du projet:



## Description:

| Fichier / Dossier     | Description                                                                                                                                                      |
|-----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| app/                  | Contient le code essentiel pour le fonctionnement de l'application.                                                                                             |
| api/                  | Contient tous les fichiers contenant les points de terminaison ou endpoints de chaque entité (users, places ...), organisé par version.                         |
| models/               | Contient les classes de la logique métier.                                                                                                                      |
| services/             | Contient la façade dans laquelle est gérer toutes les interactions entre les différentes couches.                                                               |
| persistence/          | Contient le fichier repository où est implémenté le "in-memory repository", qui va être remplacé plus tard par une vraie base de données utilisant SQL Alchemy. |
| run<space>.py                | C'est le fichier qui sert à lancer l'application Flask. <br>On peut lancer l'application avec la commande suivante: python3 run<space>.py                                                                                                             |
| config<space>.py             | Configure les variables d'environnement et les paramètres de l'application.                                                                                     |
| requirements.txt      | C'est un fichier qui sert aux utilisateurs à bien configurer leur environnement pour que l'application puisse se lancer et fonctionner. Il liste les packages essentiels python.<br>Voici la commande pour installer ces packages: pip install -r requirements.txt                                                                                   |
| README<space>.md             | Vous êtes dans ce fichier qui sert à documenter et avoir un apperçu globale du projet.                                                                          |
| __init __.py           | Ils sont présents un peu partout, cela indique à Python que de traiter les répertoires dans lesquels ils se trouvent comme des paquets importables              |
| repository<space>.py         | Contient toutes les méthodes pour intéragir avec une base de données qui ici est pour le moment "InMemoryRepository"                                            |
| facade<space>.py             | Gère la communication entre les différentes couches: le Presentation Layer, La Business Logic Layer et le Persistence Layer.                                   |



# Core Models:

Comme vous avez pu le voir dans le diagramme de classe, il existe plusieurs entités essentielles au bon fonctionnement de l'applicattion, qui sont au coeur de la logique métier.
Nous les avons initialisé dans le dossier "models", dans des fichiers portant leur nom respectif.
Voici une description complète du rôle de chaque entité, et de leur fonctionnement.




# BaseModel:
Cette entité contient tous les attributs et méthodes communes aux autres entités.

### Relations:
Toutes les autres entités héritent de cette classe.

### Structure:

| Attribut        | Type     | Description                                 |
|-----------------|----------|---------------------------------------------|
| `id`            | UUID     | Identifiant unique de l'objet               |
| `created_at`    | datetime | Date de création de l'objet                 |
| `updated_at`    | datetime | Date de mise à jour de l'objet              |

| Méthode             | Description                                                    | Paramètres  |    Retour   |
|---------------------|----------------------------------------------------------------|-------------|-------------|
| `create(data)`      |Créer un objet avec ses informations                            |data         |None         |
| `read(id)`          |Lit les informations d'un objet                                 |id           |None         |
| `update(data)`      |Met à jour le informations d'un objet                           |data         |None         |
| `delete(id)`        |Supprime un objet                                               |id           |None         |




# User:
Cette entité représente un utilisateur inscrit et enregistré dans l'application.

### Relations:
L'utilisateur hérite de la classe BaseModel.
L'utilisateur peut avoir plusieurs logements et avis.
Si l'utilisateur supprime son compte, les logements qui lui étaient associés disparaissent mais ses avis resteront.

### Structure:

| Attribut        | Type     | Description                                 |
|-----------------|----------|---------------------------------------------|
| `first_name`    | string   | Prénom de l'utilisateur                     |
| `last_name`     | string   | Nom de famille de l'utilisateur             |
| `email`         | string   | Adresse email (unique, validée)             |
| `password_hash` | string   | Mot de passe haché                          |
| `is_admin`      | boolean  | Rôle (`user` ou `admin`)                    |

| Méthode             | Description                                                    | Paramètres  |    Retour   |
|---------------------|----------------------------------------------------------------|-------------|-------------|
| `add_review()`      |Ajoute un avis dans la liste d'avis de l'utilisateur            |None         |None         |
| `add_place()`       |Ajoute une location dans la liste de logements de l'utilisateur |None         |None         |

### Exemple d'utilisation:

from app.models.user import User

def test_user_creation():
    user = User(first_name="John", last_name="Doe", email="john.doe@example.com")
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example.com"
    assert user.is_admin is False  # Default value
    print("User creation test passed!")

test_user_creation()


# Place:
Cette entité représente les locations mises à disposition sur l'application.

### Relations:
Le logement peut avoir plusieurs commodités et avis.
Si le logement disparait, les avis disparaissent aussi.
Si le propriétaire du logement supprime son compte, celui-ci est supprimé également.

### Structure:

| Attribut      | Type     | Description                                      |
|---------------|----------|--------------------------------------------------|
| `title`       | string   | Titre du lieu                                    |
| `description` | string   | Description textuelle du lieu                    |
| `price`       | float    | Prix associé au lieu (ex. location, entrée)      |
| `latitude`    | float    | Latitude géographique                            |
| `longitude`   | float    | Longitude géographique                           |
| `owner`       | User     | Propriétaire du lieu (instance de `User`)        |
| `reviews`     | list     | Liste des avis associés à ce lieu (`Review`)     |
| `amenities`   | list     | Liste des équipements disponibles (`Amenity`)    |

| Méthode           | Description                                 | Paramètres             | Retour     |
|-------------------|---------------------------------------------|------------------------|------------|
| `add_review()`    | Ajoute un avis à la liste `reviews`.        | `review: Review`       | `None`     |
| `add_amenity()`   | Ajoute un équipement à la liste `amenities`.| `amenity: Amenity`     | `None`     |




# Review:
Cette entité représente les avis laissés sur les logements, pour pouvoir juger de la qulaité du logement.

### Relations:
Un avis ne peut provenir que d'un seul utilisateur mais celui-ci peut en écrire plusieurs.
Il peut y avoir plusieurs avis sur un même logement.
Si le logement disparait, les avis sur cette habitation disparaîssent.
Si l'utilisateur supprime son compte, son avis reste.

### Structure:

| Attribut   | Type     | Description                                      |
|------------|----------|--------------------------------------------------|
| `text`     | string   | Commentaire rédigé par l'utilisateur             |
| `rating`   | int      | Note attribuée au lieu (généralement entre 1–5)  |
| `owner`    | User     | Auteur de l'avis (instance de `User`)            |
| `place`    | Place    | Lieu concerné par l'avis (instance de `Place`)   |

### Exemple  d'utilisation avec place et review:

from app.models.place import Place
from app.models.user import User
from app.models.review import Review

def test_place_creation():
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
    place = Place(title="Cozy Apartment", description="A nice place to stay", price=100, latitude=37.7749, longitude=-122.4194, owner=owner)

    # Adding a review
    review = Review(text="Great stay!", rating=5, place=place, user=owner)
    place.add_review(review)

    assert place.title == "Cozy Apartment"
    assert place.price == 100
    assert len(place.reviews) == 1
    assert place.reviews[0].text == "Great stay!"
    print("Place creation and relationship test passed!")

test_place_creation()




## Amenity:
Entité représentant les commodités associées à un logement. (piscine, wi-fi...)

### Relations:
Un logement peut avoir plusieurs commodités.
Il peut y avoir la même commodité sur plusieurs logements.

### Structure:

| Attribut | Type   | Description                            |
|----------|--------|----------------------------------------|
| `name`   | string | Nom de l'équipement ou commodité       |

### Exemple d'utilisation:

from amenity import Amenity

def test_amenity_creation():
    amenity = Amenity(name="Wi-Fi")
    assert amenity.name == "Wi-Fi"
    print("Amenity creation test passed!")

test_amenity_creation()
