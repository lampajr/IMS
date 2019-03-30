import time
from termcolor import cprint, colored


def get_time():
    return int(round(time.time() * 1000))


def monitor(agents):
    header = "*       AGENT-NAME       **          STATUS         **                      DESCRIPTION                       *"
    # 13
    width = len(header)

    border = width * '*'

    cprint(text=border)
    cprint(text=header)
    for ag in agents:
        line = generate_line(ag)
        cprint(text=line)

    cprint(text=border)


def generate_line(agent):
    name = agent.agent_name
    length_name = len(name)

    if agent.occupied:
        status = colored("occupied", "blue")
    elif agent.invalidated:
        status = colored("failed", "red")
    else:
        status = colored("available", "green")

    length_status = len(status)

    description = ""
    if agent.occupied:
        task_name = agent.current_task.name
        description = "executing " + task_name

    length_description = len(description)

    template = "*" + 24*" " + "*"
    start = int(13 - (length_name/2))
    result_name = ""
    for idx, c in enumerate(template):
        if start <= idx < start + length_name:
            result_name += name[idx-start]
        else:
            result_name += c

    start = int(14 - (length_status / 2))
    result_status = ""
    for idx, c in enumerate(template):
        if start <= idx < start + length_status:
            result_status += status[idx-start]
        else:
            result_status += c

    start = int(29 - (length_description / 2))
    result_description = ""
    for idx, c in enumerate(template):
        if start <= idx < start + length_description:
            result_description += description[idx-start]
        else:
            result_description += c

    return result_name + result_status + result_description
