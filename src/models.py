from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(80), unique=False, nullable=True)
    # Relación con los favoritos de personas
    favorites_people = db.relationship('UserFavoritePeople', back_populates='user')
    # Relación con los favoritos de planetas
    favorites_planets = db.relationship('UserFavoritePlanets', back_populates='user')
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorites_people": [favorite.serialize() for favorite in self.favorites_people],
            "favorites_planets": [favorite.serialize() for favorite in self.favorites_planets]
        }


class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    hair_color = db.Column(db.String(80), unique=False, nullable=False)
    favorites_by_users = db.relationship('UserFavoritePeople', back_populates='person')

    def __repr__(self):
        return '<People %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "hair_color": self.hair_color
        }


class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    climate = db.Column(db.String(80), unique=False, nullable=False)
    favorites_by_users = db.relationship('UserFavoritePlanets', back_populates='planet')

    def __repr__(self):
        return '<Planets %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate
        }


class UserFavoritePlanets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    favorite_planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relación con `User`
    user = db.relationship('User', back_populates='favorites_planets')
    # Relación con `Planets`
    planet = db.relationship('Planets', back_populates='favorites_by_users')

    def __repr__(self):
        return '<UserFavoritePlanets %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "favorite_planet_id": self.favorite_planet_id,
            "planet": self.planet.serialize()  # Incluye los detalles del planeta
        }


class UserFavoritePeople(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    favorite_people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relación con `User`
    user = db.relationship('User', back_populates='favorites_people')
    # Relación con `People`
    person = db.relationship('People', back_populates='favorites_by_users')

    def __repr__(self):
        return '<UserFavoritePeople %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "favorite_people_id": self.favorite_people_id,
            "person": self.person.serialize()  # Incluye los detalles de la persona
        }
