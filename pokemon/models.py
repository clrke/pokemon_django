from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class PokemonType(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class DamageMultiplier(models.Model):
    attacking_type = models.ForeignKey(PokemonType, models.CASCADE, "strengths")
    receiving_type = models.ForeignKey(PokemonType, models.CASCADE, "weaknesses")
    multiplier = models.FloatField()

    def __str__(self):
        return f"{self.attacking_type} -> {self.receiving_type}: {self.multiplier}x"


class PokemonSpecies(models.Model):
    class Meta:
        verbose_name_plural = 'Pokemon species'

    name = models.CharField(max_length=16)
    type_set = models.ManyToManyField(PokemonType, "species_set")
    next_evolution = models.ForeignKey('self', models.SET_NULL, "preevolution_set", null=True, blank=True)
    evolution_level = models.PositiveIntegerField(validators=[
        MinValueValidator(2),
        MaxValueValidator(100),
    ], null=True, blank=True)

    def get_type_set_display(self):
        return ', '.join(map(lambda t: t.name, self.type_set.all()))

    def __str__(self):
        return self.name


class PokemonGender(models.TextChoices):
    MALE = 'M'
    FEMALE = 'F'


class Pokemon(models.Model):
    class Meta:
        verbose_name_plural = 'Pokemon'

    MALE = 'M'
    FEMALE = 'F'

    GENDER = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )

    nickname = models.CharField(max_length=16)
    species = models.ForeignKey(PokemonSpecies, models.CASCADE, "pokemon_set")
    level = models.PositiveIntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(100),
    ])
    gender = models.CharField(choices=GENDER, max_length=1)

    def __str__(self):
        return f"{self.nickname} ({self.species.name})"

    def save(self, **kwargs):
        if self.species.evolution_level and self.level >= self.species.evolution_level:
            self.species = self.species.next_evolution

        return super().save(**kwargs)
