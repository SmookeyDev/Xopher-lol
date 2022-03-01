    from winstealer import *
    from commons.utils import *
    from commons.skills import *
    from commons.items import *
    from commons.targeting import *
    from evade import checkEvade
    import json, time, math
    import urllib3, json, urllib, ssl
     
     
    winstealer_script_info = {
        "script": "T3Jhin",
        "author": "tefan#7872// github - 1nteg3r",
        "description": "for jhin",
        "target_champ": "jhin",
    }
    combo_key = 57
    laneclear_key = 47
     
    Q_Enabled = True
    W_Enabled = True
    E_Enabled = True
    E_CC_Enabled = True
    R_Enabled = True
    W_Jungle_Steal = True
    W_Kill_Steal = True
    Q_Kill_Minion = True
    Q_Only_Reloading = True
    Q_Range = 555
    W_Range = 2420 # 2520 Original
    E_Range = 755
    R_Range = 3050 # 3500 Original
     
    last_positions = []
    last_pos_id = []
     
     
    def winstealer_load_cfg(cfg):
        cfg.get_bool("Q", Q_Enabled)
        cfg.get_bool("W", W_Enabled)
        cfg.get_bool("W_KS", W_Kill_Steal)
        cfg.get_bool("W_KS_JG", W_Jungle_Steal)
        cfg.get_bool("E", E_Enabled)
        cfg.get_bool("E_CC_Enabled", E_CC_Enabled)
        cfg.get_bool("Q_KS_MINION", Q_Kill_Minion)
        cfg.get_bool("Q_ONLY_RELOAD", Q_Only_Reloading)
        cfg.get_bool("R", R_Enabled)
     
    def winstealer_save_cfg(cfg):
        cfg.get_bool("Q", Q_Enabled)
        cfg.get_bool("W", W_Enabled)
        cfg.get_bool("W_KS", W_Kill_Steal)
        cfg.get_bool("W_KS_JG", W_Jungle_Steal)
        cfg.get_bool("E", E_Enabled)
        cfg.get_bool("E_CC_Enabled", E_CC_Enabled)
        cfg.get_bool("Q_KS_MINION", Q_Kill_Minion)
        cfg.get_bool("Q_ONLY_RELOAD", Q_Only_Reloading)
        cfg.get_bool("R", R_Enabled)
     
     
    def winstealer_draw_settings(game, ui):
        global Q_Enabled, W_Enabled, E_Enabled, R_Enabled, W_Jungle_Steal, W_Kill_Steal, E_CC_Enabled, Q_Kill_Minion, Q_Only_Reloading
        ui.text("Made with <3 by tefan#7872")
        
        if ui.treenode("[Q] Dancing Grenade"):
            Q_Enabled = ui.checkbox('Enabled [Q]', Q_Enabled)
            Q_Kill_Minion = ui.checkbox("[Q] Killable Minion ", Q_Kill_Minion)
            Q_Only_Reloading = ui.checkbox("[Q] Only If Reloading ", Q_Only_Reloading)
            ui.treepop()
        if ui.treenode("[W] Deadly Flourish"):
            W_Enabled = ui.checkbox('Enabled [W]', W_Enabled)
            W_Kill_Steal = ui.checkbox('[W] Kill Steal', W_Kill_Steal)
            ui.treepop()
        if ui.treenode("[E] Captive Audience"):
            E_Enabled = ui.checkbox('Enabled [E]', E_Enabled)
            E_CC_Enabled = ui.checkbox("[E] On CC'd Targets", E_CC_Enabled)
            ui.treepop()
        if ui.treenode("[R] Curtain Call"):
            R_Enabled = ui.checkbox('Enabled Auto Fire [R] Shots', R_Enabled)
            ui.treepop()
     
     
     
     
     
    def is_immobile(game, target):
    	for buff in target.buffs:
     
    		if 'snare' in buff.name.lower():
    			return True
    		elif 'stun' in buff.name.lower():
    			return True
    		elif 'suppress' in buff.name.lower():
    			return True
    		elif 'root' in buff.name.lower():
    			return True
    		elif 'taunt' in buff.name.lower():
    			return True
    		elif 'sleep' in buff.name.lower():
    			return True
    		elif 'knockup' in buff.name.lower():
    			return True
    		elif 'binding' in buff.name.lower():
    			return True
    		elif 'morganaq' in buff.name.lower():
    			return True
    		elif 'jhinw' in buff.name.lower():
    			return True
    	return False
     
    class Fake_target():
        def __init__(self, name, pos, gameplay_radius):
            self.name = name
            self.pos = pos
            self.gameplay_radius = gameplay_radius
     
    def predict_pos(target, duration):
        """Predicts the target's new position after a duration"""
        target_direction = target.pos.sub(target.prev_pos).normalize()
        # In case the target wasn't moving
        if math.isnan(target_direction.x):
            target_direction.x = 0.0
        if math.isnan(target_direction.y):
            target_direction.y = 0.0
        if math.isnan(target_direction.z):
            target_direction.z = 0.0
        if target_direction.x == 0.0 and target_direction.z == 0.0:
            return target.pos
        # Target movement speed
        target_speed = target.movement_speed
        # The distance that the target will have traveled after the given duration
        distance_to_travel = target_speed * duration
        return target.pos.add(target_direction.scale(distance_to_travel))
     
    # Get player stats from local server
    ssl._create_default_https_context = ssl._create_unverified_context
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    def getPlayerStats():
        response = urllib.request.urlopen("https://127.0.0.1:2999/liveclientdata/activeplayer").read()
        stats = json.loads(response)
        return stats
     
     
    def QDamage(game, target):
        damage = 0
        ap = getPlayerStats()["championStats"]["abilityPower"]
        ad = getPlayerStats()["championStats"]["attackDamage"]
        if game.player.Q.level == 1:
            damage = 45 +  0.35 * ad + 0.60 * ap
        elif game.player.Q.level == 2:
            damage = 80 +  0.35 * ad + 0.60 * ap
        elif game.player.Q.level == 3:
            damage = 95 +  0.35 * ad + 0.60 * ap
        elif game.player.Q.level == 4:
            damage = 120 +  0.35 * ad + 0.60 * ap
        elif game.player.Q.level == 5:
            damage = 145 +  0.35 * ad + 0.60 * ap
        return damage
     
    def WDamage(game, target):
        # Calculate raw E damage on target
        w_lvl = game.player.W.level
        if w_lvl == 0:
            return 0
        ap = getPlayerStats()["championStats"]["abilityPower"]
        ad = getPlayerStats()["championStats"]["attackDamage"]
        min_dmg = [60, 95, 130, 165, 200]
        missing_hp = (target.max_health - target.health)
        missing_hp_pct = (missing_hp / target.max_health) * 100
        increased_pct = 0.015 * missing_hp_pct
        if increased_pct > 1:
            increased_pct = 1
        w_damage = (1 + increased_pct) * (min_dmg[w_lvl - 1] + 0.50 * ad)
     
        # Reduce damage based on target's magic resist
        mr = target.magic_resist
        if mr >= 0:
            dmg_multiplier = 100 / (100 + mr)
        else:
            dmg_multiplier = 2 - 100 / (100 - mr)
        w_damage *= dmg_multiplier
        return w_damage
     
     
     
     
     
     
    def lasthit_q(game):
     
        Q = getSkill(game , "Q")
        before_cpos = game.get_cursor()
     
        if not IsReady(game, Q):
            return
        
        if Q_Kill_Minion:
            Current_Target = GetBestMinionsInRange(game, Q_Range)
     
            if Current_Target is None:
                return
            
            if  QDamage(game, Current_Target) > Current_Target.health and not Q_Only_Reloading:
                game.move_cursor(game.world_to_screen(Current_Target.pos))
                game.press_right_click()
                Q.trigger(False)
                game.move_cursor(before_cpos)
            
            elif QDamage(game, Current_Target) > Current_Target.health and Q_Only_Reloading and getBuff(game.player, 'JhinPassiveReload'):
                game.move_cursor(game.world_to_screen(Current_Target.pos))
                game.press_right_click()
                Q.trigger(False)
                game.move_cursor(before_cpos)
     
    def Qcombo(game):
     
        Q = getSkill(game , "Q")
        W = getSkill(game , "W")
        E = getSkill(game , "E")
        R = getSkill(game , "R")
        before_cpos = game.get_cursor()
     
        if Q_Enabled and IsReady(game, Q) and game.player.mana > 50:
     
            target =GetBestTargetsInRange(game, Q_Range)
            if ValidTarget(target):
                game.move_cursor(game.world_to_screen(target.pos))
                game.press_right_click()
                Q.trigger(False)
                time.sleep(0.02)
                game.move_cursor(before_cpos)
                game.press_right_click()
     
    def WCombo(game):
        Q = getSkill(game , "Q")
        W = getSkill(game , "W")
        E = getSkill(game , "E")
        R = getSkill(game , "R")
        before_cpos = game.get_cursor()
     
        if W_Enabled and IsReady(game, W) and game.player.mana > 70:
            target = GetBestTargetsInRange(game, W_Range)
     
            if target:
                if getBuff(target, 'jhinespotteddebuff') or is_immobile(game, target):
                    w_travel_time = W_Range / 2000
                    predicted_pos = predict_pos(target, w_travel_time)
                    predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
                    if ValidTarget(target):
                        game.move_cursor(game.world_to_screen(predicted_target.pos))
                        time.sleep(0.5)
                        W.trigger(False)
                        time.sleep(0.1)
                        game.move_cursor(before_cpos)
     
    def ECombo(game):
        Q = getSkill(game , "Q")
        W = getSkill(game , "W")
        E = getSkill(game , "E")
        R = getSkill(game , "R")
        before_cpos = game.get_cursor()
     
        if E_Enabled and IsReady(game, E) and game.player.mana > 50 :
     
            target = GetBestTargetsInRange(game, E_Range)
            if ValidTarget(target):
                e_travel_time = E_Range / 1
                predicted_pos = predict_pos(target, e_travel_time)
                predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
                game.move_cursor(game.world_to_screen(predicted_target.pos))
                E.trigger(False)
                game.move_cursor(before_cpos)
     
    def ECCombo(game):
        Q = getSkill(game , "Q")
        W = getSkill(game , "W")
        E = getSkill(game , "E")
        R = getSkill(game , "R")
        before_cpos = game.get_cursor()
        if E_CC_Enabled and IsReady (game, E) and game.player.mana > 50:
            target = GetBestTargetsInRange (game, E_Range)
            if target is not None:
                if is_immobile (game, target):
                    game.move_cursor (game.world_to_screen (target.pos)) 
                    E.trigger (False)
                    time.sleep (0.01)
                    game.move_cursor (before_cpos)
     
     
    def Killsteal(game):
     
        W = getSkill(game , "W")
        r_spell = getSkill(game, "R")
        before_cpos = game.get_cursor()
        
        target = GetBestTargetsInRange(game, W_Range)
        if ValidTarget(target) and IsReady(game, W) and not r_spell.name == "jhinrshot":
            if game.player.pos.distance(target.pos) <= W_Range and target.health < WDamage(game, target): #checks if damage is enough to ks the enemy, calcukated above as RDamage
                w_travel_time = W_Range / 3000
                predicted_pos = predict_pos(target, w_travel_time)
                predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
                if ValidTarget(target):
                    game.move_cursor(game.world_to_screen(predicted_target.pos))
                    time.sleep(0.1)
                    W.trigger(False)
                    time.sleep(0.1)
                    game.move_cursor(before_cpos)
                
     
     
     
     
     
     
                
     
     
                
     
     
            
     
     
    def winstealer_update(game, ui):
        r_spell = getSkill(game, "R")
        before_cpos = game.get_cursor()
        self = game.player
     
        if self.is_alive and self.is_visible and not game.isChatOpen:
            if game.was_key_pressed(laneclear_key):
                lasthit_q(game)
            if game.was_key_pressed(combo_key):
                Qcombo(game)
                WCombo(game)
                ECombo(game)
                ECCombo(game)
            if W_Kill_Steal:
                Killsteal(game)
            if R_Enabled and r_spell.name == "jhinrshot":
                target = GetBestTargetsInRange(game, R_Range)
                if ValidTarget(target):
                   r_travel_time = R_Range / 5000
                   predicted_pos = predict_pos(target, r_travel_time)
                   predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
                   game.move_cursor(game.world_to_screen(predicted_target.pos))
                   r_spell.trigger(False)
                   game.move_cursor(before_cpos)