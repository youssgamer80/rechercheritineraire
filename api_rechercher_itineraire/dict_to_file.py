import json
a =[[('fraternite', -4.0182667, 5.344239), ('abobo', -4.029007, 5.435487), ('Gare de bassam', -4.0026642, 5.3003494)], [('fraternite', -4.0182667, 5.344239), ('abobo', -4.029007, 5.435487)], [('fraternite', -4.0182667, 5.344239), ('indenie', -4.0224767, 5.3404293)]]

js = json.dumps(a)

# Open new json file if not exist it will create
fp = open('test.json', 'a')
fp.truncate(0)
# write to json file
fp.write(js)

# close the connection
fp.close()