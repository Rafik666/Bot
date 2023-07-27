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


