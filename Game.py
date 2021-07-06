class Match():
    def __init__(self, duration, season, patch, id, blue, red, summoner, side):
        self.duration = duration
        self.season = season
        self.patch = patch
        self.id = id
        self.blue = blue
        self.red = red
        self.summoner = summoner
        self.side = side

    def __str__(self):
        return f'duration: {self.duration}\nseason: {self.season}\npatch: {self.patch}\nid: {self.id}\nblue: {self.blue}\nred: {self.red}\nside: {self.side}\nsummoner: \n{self.summoner}\n'

    def to_dict(self):
        return {
            'duration' : self.duration,
            'season' : self.season,
            'patch' : self.patch,
            'id' : self.id,
            'blue' : self.blue,
            'red' : self.red,
            'summoner' : self.summoner,
            'side' : self.side
        }

    def winning_side(self):
        return self.side if self.summoner.stats.win else not self.side


class Summoner():
    def __init__(self, summoner_spell_d, summoner_spell_f, runes, stats, champion):
        self.summoner_spell_d = summoner_spell_d
        self.summoner_spell_f = summoner_spell_f
        self.runes = runes
        self.stats = stats
        self.champion = champion


    def __str__(self):
        return f'\tsummoner_spell_d: {self.summoner_spell_d}\n\tsummoner_spell_f: {self.summoner_spell_f}\n\trunes: {self.runes}\n\tstats: {self.stats}\n'

    def __repr__(self):
        return f'\tsummoner_spell_d: {self.summoner_spell_d}\n\tsummoner_spell_f: {self.summoner_spell_f}\n\trunes: {self.runes}\n\tstats: {self.stats}\n'

class Stats():
    def __init__(self, stats):
        self.assists = stats.assists
        self.combat_player_score = stats.combat_player_score
        self.damage_dealt_to_objectives = stats.damage_dealt_to_objectives
        self.damage_dealt_to_turrets = stats.damage_dealt_to_turrets
        self.damage_self_mitigated = stats.damage_self_mitigated
        self.deaths = stats.deaths
        self.double_kills = stats.double_kills
        self.first_blood_assist = stats.first_blood_assist
        self.first_blood_kill = stats.first_blood_kill
        try:
            self.first_inhibitor_assist = stats.first_inhibitor_assist
            self.first_inhibitor_kill = stats.first_inhibitor_kill
        except:
            self.first_inhibitor_assist = None
            self.first_inhibitor_kill = None
        try:
            self.first_tower_assist = stats.first_tower_assist
            self.first_tower_kill = stats.first_tower_kill
        except:
            self.first_tower_assist = None
            self.first_tower_kill = None
        self.gold_earned = stats.gold_earned
        self.gold_spent = stats.gold_spent
        self.inhibitor_kills = stats.inhibitor_kills
        self.items = stats.items
        self.kda = stats.kda
        self.killing_sprees = stats.killing_sprees
        self.kills = stats.kills
        self.largest_critical_strike = stats.largest_critical_strike
        self.largest_killing_spree = stats.largest_killing_spree
        self.largest_multi_kill = stats.largest_multi_kill
        self.level = stats.level
        self.longest_time_spent_living = stats.longest_time_spent_living
        self.magic_damage_dealt = stats.magic_damage_dealt
        self.magic_damage_dealt_to_champions = stats.magic_damage_dealt_to_champions
        self.magical_damage_taken = stats.magical_damage_taken
        self.penta_kills = stats.penta_kills
        self.physical_damage_dealt = stats.physical_damage_dealt
        self.physical_damage_dealt_to_champions = stats.physical_damage_dealt_to_champions
        self.physical_damage_taken = stats.physical_damage_taken
        self.quadra_kills = stats.quadra_kills
        self.time_CCing_others = stats.time_CCing_others
        self.total_damage_dealt = stats.total_damage_dealt
        self.total_damage_dealt_to_champions = stats.total_damage_dealt_to_champions
        self.total_damage_taken = stats.total_damage_taken
        self.total_heal = stats.total_heal
        self.total_minions_killed = stats.total_minions_killed
        self.total_player_score = stats.total_player_score
        self.total_score_rank = stats.total_score_rank
        self.total_time_crowd_control_dealt = stats.total_time_crowd_control_dealt
        self.total_units_healed = stats.total_units_healed
        self.triple_kills = stats.triple_kills
        self.true_damage_dealt = stats.true_damage_dealt
        self.true_damage_dealt_to_champions = stats.true_damage_dealt_to_champions
        self.true_damage_taken = stats.true_damage_taken
        self.turret_kills = stats.turret_kills
        self.win = stats.win
