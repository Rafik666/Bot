def subtraction(bd, id, bid):
    old_values= bd.base.execute(f"SELECT money FROM players WHERE id={id}").fetchone()[0]
    
    bd.base.execute(f'UPDATE players SET money = {old_values-bid} WHERE id={id}')
    bd.base.commit()

def addition(bd, id, win):
    old_values= bd.base.execute(f"SELECT money FROM players WHERE id={id}").fetchone()[0]
    
    bd.base.execute(f'UPDATE players SET money = {old_values+win} WHERE id={id}')
    bd.base.commit()

def winnings_money(bd, id, win):
    old_values= bd.base.execute(f"SELECT win FROM players WHERE id={id}").fetchone()[0]
    
    bd.base.execute(f'UPDATE players SET win = {old_values+win} WHERE id={id}')
    bd.base.commit()


def losting_money(bd, id, lost):
    old_values = bd.base.execute(f'SELECT lost FROM players WHERE id={id}').fetchone()[0]
    bd.base.execute(f'UPDATE players SET lost = {old_values+lost} WHERE id={id}')
    bd.base.commit()

