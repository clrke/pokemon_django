from django.contrib import admin

from pokemon.models import PokemonSpecies, Pokemon, PokemonType, DamageMultiplier


class DamageMultiplierInline(admin.TabularInline):
    model = DamageMultiplier
    fk_name = 'attacking_type'
    fields = ('receiving_type', 'multiplier')
    min_num = 0
    extra = 0


@admin.register(PokemonType)
class PokemonTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fields = ('name',)
    inlines = (DamageMultiplierInline,)


@admin.register(PokemonSpecies)
class PokemonSpeciesAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_type_set_display', 'next_evolution', 'evolution_level',)
    fields = ('name', 'type_set', 'next_evolution', 'evolution_level',)


@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'species', 'level', 'gender',)
    fields = ('nickname', 'species', 'level', 'gender',)
