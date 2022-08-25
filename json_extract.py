def json_extractor():
    # open and read json file in to a data fram
    with open('2022.json') as json_file:
        data = json.load(json_file,
    df = json_normalize(data, max_level=4)

    for patent in df.rows:
        print(patent[0])
#   return
