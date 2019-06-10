from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random

class Proposal(Page):
    def is_displayed(self):
        return self.participant.vars['alive'] == True

    form_model = 'player'
    form_fields = ['offer_to_1','offer_to_2','offer_to_3','offer_to_4','offer_to_5']

    def error_message(self, values):
      if values['offer_to_1'] + values['offer_to_2'] + values['offer_to_3'] + values['offer_to_4'] + values['offer_to_5'] != self.group.budget:
                    return 'Your provisional allocation proposal must add up to {}'.format(self.group.budget)

class ProposalWaitPage(WaitPage):
    def is_displayed(self):
        return self.participant.vars['alive'] == True

    def after_all_players_arrive(self):
        group = self.group
        if group.proposer == 1:
            group.chosen_offer_to_1 = group.get_player_by_id(1).offer_to_1
            group.chosen_offer_to_2 = group.get_player_by_id(1).offer_to_2
            group.chosen_offer_to_3 = group.get_player_by_id(1).offer_to_3
            group.chosen_offer_to_4 = group.get_player_by_id(1).offer_to_4
            group.chosen_offer_to_5 = group.get_player_by_id(1).offer_to_5
        elif group.proposer == 2:
            group.chosen_offer_to_1 = group.get_player_by_id(2).offer_to_1
            group.chosen_offer_to_2 = group.get_player_by_id(2).offer_to_2
            group.chosen_offer_to_3 = group.get_player_by_id(2).offer_to_3
            group.chosen_offer_to_4 = group.get_player_by_id(2).offer_to_4
            group.chosen_offer_to_5 = group.get_player_by_id(2).offer_to_5
        elif group.proposer == 3:
            group.chosen_offer_to_1 = group.get_player_by_id(3).offer_to_1
            group.chosen_offer_to_2 = group.get_player_by_id(3).offer_to_2
            group.chosen_offer_to_3 = group.get_player_by_id(3).offer_to_3
            group.chosen_offer_to_4 = group.get_player_by_id(3).offer_to_4
            group.chosen_offer_to_5 = group.get_player_by_id(3).offer_to_5
        elif group.proposer == 4:
            group.chosen_offer_to_1 = group.get_player_by_id(4).offer_to_1
            group.chosen_offer_to_2 = group.get_player_by_id(4).offer_to_2
            group.chosen_offer_to_3 = group.get_player_by_id(4).offer_to_3
            group.chosen_offer_to_4 = group.get_player_by_id(4).offer_to_4
            group.chosen_offer_to_5 = group.get_player_by_id(4).offer_to_5
        else:
            group.chosen_offer_to_1 = group.get_player_by_id(5).offer_to_1
            group.chosen_offer_to_2 = group.get_player_by_id(5).offer_to_2
            group.chosen_offer_to_3 = group.get_player_by_id(5).offer_to_3
            group.chosen_offer_to_4 = group.get_player_by_id(5).offer_to_4
            group.chosen_offer_to_5 = group.get_player_by_id(5).offer_to_5

class Vote(Page):
    def is_displayed(self):
        return self.participant.vars['alive'] == True

    form_model = 'player'
    form_fields = ['vote']

class VoteWaitPage(WaitPage):
    def is_displayed(self):
        return self.participant.vars['alive'] == True

    def after_all_players_arrive(self):
        group = self.group
        players = group.get_players()
        for p in players:
            if p.vote == "No":
                p.vote_no = 1
            else:
                p.vote_no = 0
        veto_votes_no = group.get_player_by_role('Veto').vote_no
        votes_no = [p.vote_no for p in players]

        if (Constants.veto == True and sum(votes_no) < Constants.q and veto_votes_no == 0) or (Constants.veto == False and sum(votes_no) < Constants.q):
            group.allocation_to_1 = group.chosen_offer_to_1
            group.allocation_to_2 = group.chosen_offer_to_2
            group.allocation_to_3 = group.chosen_offer_to_3
            group.allocation_to_4 = group.chosen_offer_to_4
            group.allocation_to_5 = group.chosen_offer_to_5

            for p in players:
                p.participant.vars['agreement'] = 'Yes'
                if p.id_in_group==1:
                    p.payoff = group.allocation_to_1
                elif p.id_in_group==2:
                    p.payoff = group.allocation_to_2
                elif p.id_in_group == 3:
                    p.payoff = group.allocation_to_3
                elif p.id_in_group == 4:
                    p.payoff = group.allocation_to_4
                else:
                    p.payoff = group.allocation_to_5

        elif (Constants.veto == True and veto_votes_no == 1 and self.round_number == Constants.num_rounds) or (sum(votes_no) >= Constants.q and self.round_number == Constants.num_rounds):
            group.allocation_to_1 = 0
            group.allocation_to_2 = 0
            group.allocation_to_3 = 0
            group.allocation_to_4 = 0
            group.allocation_to_5 = 0

            for p in players:
                p.participant.vars['agreement'] = 'Yes'
                if p.id_in_group == 1:
                    p.payoff = group.allocation_to_1
                elif p.id_in_group == 2:
                    p.payoff = group.allocation_to_2
                elif p.id_in_group == 3:
                    p.payoff = group.allocation_to_3
                elif p.id_in_group == 4:
                    p.payoff = group.allocation_to_4
                else:
                    p.payoff = group.allocation_to_5

class Results(Page):
    def is_displayed(self):
        return self.participant.vars['alive'] == True
    timeout_seconds = 30

    def vars_for_template(self):
        return {
            'vote1': self.group.get_player_by_id(1).vote,
            'vote2': self.group.get_player_by_id(2).vote,
            'vote3': self.group.get_player_by_id(3).vote,
            'vote4': self.group.get_player_by_id(4).vote,
            'vote5': self.group.get_player_by_id(5).vote,
            'agreement': self.participant.vars['agreement']
        }

    def before_next_page(self):
        if self.participant.vars['agreement'] == 'Yes':
            self.participant.vars['alive'] = False

page_sequence = [
    Proposal,
    ProposalWaitPage,
    Vote,
    VoteWaitPage,
    Results
]
