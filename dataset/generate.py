import os
import re
import requests
import urllib3
import utils

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
__import__("dotenv").load_dotenv()

current_directory = os.path.dirname(os.path.realpath(__file__))
examples = []


def read_file():
    with open(current_directory + "/../static_data/ppl_queries.md", "r") as f:
        i, example = 0, []
        while True:
            line = f.readline()
            if line.startswith("======="):
                break
        while True:
            line = f.readline()
            if line.startswith("======="):
                break
            i += 1
            example.append(line.strip())
            if i == 4:
                examples.append(example)
                example = []
                i = 0


def write_file(examples):
    with open(current_directory + "/ppl_samples.txt", "w") as f:
        for query in [q for q in examples]:
            f.write(query + "\n")


def request_ppl(ppl):
    response = requests.post(
        "https://search.otel.lijshu.people.aws.dev/_plugins/_ppl",
        json={"query": ppl},
        verify=False,
        auth=(os.getenv("OS_USERNAME"), os.getenv("OS_PASSWORD")),
    )
    return response


def convert_time(query):
    return re.sub(r"'now-[^']+'", f"'{str(utils.rand_time())}'", query)


read_file()

for example in examples:
    # example[0] = "Current time is " + str(utils.rand_time()) + ". " + example[0]
    query = convert_time(example[2])
    print('❗query:', query)
    response = request_ppl(query)
    if response.status_code != 200:
        print("⚡：", example[0], query)
        print(response.json())

# write_file([q for example in examples for q in example])