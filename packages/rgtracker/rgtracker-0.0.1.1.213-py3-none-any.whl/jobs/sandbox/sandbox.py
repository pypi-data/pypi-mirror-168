
GB("StreamReader"). \
    aggregate([],
              lambda a, r: a + [r['value']],
              lambda a, r: a + r). \
    run('ST:5MINUTES:W:::UD', trimStream=False, fromId="1663581774050")

# register(
# prefix=f'ST:1MINUTE:{dimension}:::PG',
# convertToStr=True,
# collect=True,
# onFailedPolicy='abort',
# onFailedRetryInterval=1,
# batch=1,
# duration=0,
# trimStream=False)

# run('ST:1MINUTE::::PG', trimStream=False)
