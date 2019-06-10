from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import numpy as np
#import random
#from otree_tools.models.fields import ListField

author = 'Salvatore Nunnari, Bocconi University'

doc = """
Multilateral alternating-offer legislative bargaining with three-players as in the model by Baron, David and John Ferejon 1989 
and in the experiments by Frechette, Guillaume, John Kagel and Steve Lehrer 2003 (closed rule without veto players) 
or by Kagel, John, Hankyoung Sung and Eyal Winter 2010 (closed rule with a veto player).
This app implements a single instance of a (potentially infinitely repeated) bargaining game (i.e., a single "match").
"""


class Constants(BaseConstants):
    name_in_url = 'barg_three'
    players_per_group = 3
    num_rounds = 50
    budget = 25 # number of tokens to divide among committee members
    veto = True  # set to "True" for game with one veto player, set to "False" for game without veto players
    q = 2  # number of positive votes required for passage (if veto = True, this includes the veto player)
    rec_prob_1 = 1/3 # recognition probability of group member 1; if veto = True, this is the veto player
    rec_prob_2 = 1/3 # recognition probability of group member 2
    rec_prob_3 = 1/3 # recognition probability of group member 3
    discount = 0.8 # only used in end-of-round template

class Subsession(BaseSubsession):
    def creating_session(self):
        groups = self.get_groups()

        if self.round_number == 1:

            for p in self.get_players():
                p.participant.vars['alive'] = True
                p.participant.vars['agreement'] = 'No'

            for g in groups:
                g.budget = Constants.budget

                # determine identity of proposer in this round
                rand_num_prop = np.random.random()
                if rand_num_prop <= Constants.rec_prob_1:
                    g.proposer = 1
                elif rand_num_prop > Constants.rec_prob_1 and rand_num_prop <= Constants.rec_prob_1 + Constants.rec_prob_2:
                    g.proposer = 2
                else:
                    g.proposer = 3
                # g.proposer = np.random.randint(1, 4) # alternative way to randomly determine proposer with even probabilities

        else:

            for g in groups:

                g.budget = round(Constants.budget * (Constants.discount)**(self.round_number-1),2)

                # determine identity of proposer in this round
                rand_num_prop = np.random.random()
                if rand_num_prop <= Constants.rec_prob_1:
                    g.proposer = 1
                elif rand_num_prop > Constants.rec_prob_1 and rand_num_prop <= Constants.rec_prob_1 + Constants.rec_prob_2:
                    g.proposer = 2
                else:
                    g.proposer = 3
                # g.proposer = np.random.randint(1, 4) # alternative way to randomly determine proposer with even probabilities

class Group(BaseGroup):
    budget = models.FloatField()
    proposer = models.IntegerField()
    chosen_offer_to_1 = models.FloatField()
    chosen_offer_to_2 = models.FloatField()
    chosen_offer_to_3 = models.FloatField()
    allocation_to_1 = models.FloatField()
    allocation_to_2 = models.FloatField()
    allocation_to_3 = models.FloatField()

class Player(BasePlayer):

    offer_to_1 = models.FloatField(
        max=Constants.budget,
        min=0
    )
    offer_to_2 = models.FloatField(
        max=Constants.budget,
        min=0
    )
    offer_to_3 = models.FloatField(
        max=Constants.budget,
        min=0
    )

    vote = models.CharField(
        choices=['Yes', 'No'],
        verbose_name='What is you vote?',
        widget=widgets.RadioSelect
    )

    vote_no = models.IntegerField()

    def role(self):
        if self.id_in_group == 1:
            return 'Veto'
        else:
            return 'Non-Veto'