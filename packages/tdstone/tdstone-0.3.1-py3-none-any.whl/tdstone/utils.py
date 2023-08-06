import teradataml as tdml

def execute_querydictionary(query_dict):
    con_tdml = tdml.get_context()
    for k in query_dict.keys():
        try:
            con_tdml.execute(query_dict[k])
        except Exception as e:
            print(f'Error with {k}')
            print(e)
    return