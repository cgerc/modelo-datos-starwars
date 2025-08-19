from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__= 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    favorites: Mapped[list["Favorite"]] = relationship(
        "Favorite", back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

    class Planet(db.Model):
        __tablename__= 'planet'
        id: Mapped[int] = mapped_column(primary_key=True)
        name: Mapped[str] = mapped_column(String, nullable=False)
        diameter: Mapped[int] = mapped_column(Integer, nullable=True)
        climate: Mapped[str] = mapped_column(String, nullable=True)
        population: Mapped[int] = mapped_column(Integer, nullable=True)
        favorites: Mapped[list["Favorite"]] = relationship(
            "Favorite", back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "climate": self.climate,
            "population": self.population
        }

    class Character(db.Model):
        __tablename__ = 'character'
        id: Mapped[int] = mapped_column(primary_key=True)
        name: Mapped[str] = mapped_column(String, nullable=False)
        species: Mapped[str] = mapped_column(String, nullable=True)
        homeworld_id: Mapped[int] = mapped_column(ForeignKey(
            'planet.id', ondelete='SET NULL'), nullable=True)
        homeworld: Mapped["Planet"] = relationship("Planet")
        favorites: Mapped[list["Favorite"]] = relationship("Favorite", back_populates="character")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "species": self.species,
            "homeworld": self.homeworld.name if self.homeworld else None
        }
