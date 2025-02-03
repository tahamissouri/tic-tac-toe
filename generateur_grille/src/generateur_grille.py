#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  generateur_grille.py
#  generateur_grille version 1.0
#  Created by Ingenuity i/o on 2025/01/30
#
# "no description"
#
import ingescape as igs


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class GenerateurGrille(metaclass=Singleton):
    def __init__(self):
        # inputs
        self.grilleI = None






