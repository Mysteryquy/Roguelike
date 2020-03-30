from src import generator
import monster_gen


def invoke_command(level, command):
    arguments = command.split()
    for c in arguments:
        print(c)
    if command[0] == "gen_worm":
        level.objects.append(monster_gen.gen_pest_worm((int(arguments[1]), int(arguments[2]))))
    elif command[0] == "gen_item":
        generator.gen_item((int(arguments[1]), int(arguments[2])))
