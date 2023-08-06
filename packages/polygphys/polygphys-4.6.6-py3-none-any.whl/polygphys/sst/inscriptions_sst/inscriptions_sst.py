# -*- coding: utf-8 -*-
"""Transmettre les nouvelles inscriptions au SIMDUT."""

# Bibliothèque standard
from datetime import datetime
from pathlib import Path
import time

# Bibliothèque PIPy
import pandas as pd
import schedule

# Bibliothèques maison
from polygphys.outils.reseau import OneDrive
from polygphys.outils.reseau.msforms import MSFormConfig, MSForm
from polygphys.outils.reseau.courriel import Courriel


class SSTSIMDUTInscriptionConfig(MSFormConfig):

    def default(self):
        return (Path(__file__).parent / 'inscription.cfg').open().read()


class SSTSIMDUTInscriptionForm(MSForm):

    def nettoyer(self, cadre):
        cadre = self.convertir_champs(cadre)

        return cadre.loc[:, ['date', 'Prénom', 'Nom', 'Courriel',
                             'Matricule', 'Département', 'Langue',
                             'Statut', 'Professeur ou supérieur immédiat']]

    def action(self, cadre):
        try:
            destinataire = self.config.get('courriel', 'destinataire')
            pièces_jointes = []
            message = 'Bonjour! Il n\'y a pas eu de nouvelles inscriptions cette semaine. Bonne journée!'
            html = f'<p>{message}</p>'

            if not cadre.empty:
                français = cadre.loc[cadre.Langue == 'Français',
                                     ['Prénom',
                                      'Nom',
                                      'Courriel',
                                      'Matricule',
                                      'Département',
                                      'Langue',
                                      'Statut']]
                english = cadre.loc[cadre.Langue == 'English',
                                    ['Prénom',
                                     'Nom',
                                     'Courriel',
                                     'Matricule',
                                     'Département',
                                     'Langue',
                                     'Statut']]

                français.to_excel('simdut_français.xlsx', index=False)
                english.to_excel('simdut_english.xlsx', index=False)

                if not français.empty:
                    pièces_jointes.append('simdut_français.xlsx')
                if not english.empty:
                    pièces_jointes.append('simdut_english.xlsx')

                message = 'Bonjour! Voici les nouvelles inscriptions à faire pour le SIMDUT. Bonne journée!'

                html = f'<p>{message}</p>'
                if not français.empty:
                    html += f'<hr/>{français.to_html(index=False)}'
                if not english.empty:
                    html += f'<hr/>{english.to_html(index=False)}'
        except Exception as e:
            message = f'L\'erreur {e} s\'est produite.'
            html = f'<p>{message}</p>'

        courriel = Courriel(destinataire,
                            self.config.get('courriel', 'expéditeur'),
                            self.config.get('courriel', 'objet'),
                            message,
                            html,
                            pièces_jointes=pièces_jointes)
        courriel.envoyer(self.config.get('courriel', 'serveur'))


def main():
    chemin_config = Path('~').expanduser() / 'simdut.cfg'
    config = SSTSIMDUTInscriptionConfig(chemin_config)

    dossier = OneDrive('',
                       config.get('onedrive', 'organisation'),
                       config.get('onedrive', 'sous-dossier'),
                       partagé=True)
    fichier = dossier / config.get('formulaire', 'nom')
    config.set('formulaire', 'chemin', str(fichier))

    formulaire = SSTSIMDUTInscriptionForm(config)

    formulaire.mise_à_jour()


if __name__ == '__main__':
    main()
