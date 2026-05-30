from pprint import pprint


def print_chunk(chunk: dict):
    if 'agent' in chunk:
        pprint(chunk['agent']['messages'][0].content)
    if 'tools' in chunk:
        pprint(chunk['tools']['messages'][0].content)
