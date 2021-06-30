from convenience import *


class Manager:
    def __init__(self):
        self.players = []

    def create_player(self, player_id):
        new_player = Player(player_id)
        self.players.append(new_player)
        return new_player

    def start_tick_thread(self):
        thread = Thread(target=self.tick_thread)
        thread.start()

    def tick_thread(self):
        while 1:
            time.sleep(2)
            print("Tick!")
            self.tick()

    def tick(self):
        for player in self.players:
            for land in player.lands:
                for building in land.buildings:
                    building.tick()


class Player:
    def __init__(self, player_id):
        self.id = player_id
        self.lands = [Land() for _ in range(1)]
        print("Created player")


class Land:
    def __init__(self):
        self.noise_matrix = []
        self.generate_tiles()
        self.buildings = []

    def __repr__(self):
        final_str = "\n 0123456789\n"
        char_dict = {
            0.2: "~",
            0.5: "-",
            0.7: "F",
            0.9: "M",
            1.0: "S"
        }

        for x in range(10):
            final_str += str(x)
            for y in range(10):
                value = self.noise_matrix[x][y]
                for k, v in char_dict.items():
                    if value < k:
                        final_str += v
                        break

            final_str += "\n"
        return f"<Land, tiles: {final_str}>"

    def create_building(self, x, y, clazz):
        self.buildings.append(clazz(x, y))
        print(f"Created building {clazz}")

    def get_tile_at(self, x, y):
        char_dict = {
            0.2: "~",
            0.5: "-",
            0.7: "F",
            0.9: "M",
            1.0: "S"
        }
        return char_dict[self.noise_matrix[x][y]]

    def generate_tiles(self):
        noise_generator = PerlinNoise(octaves=2, seed=None)
        print("generating noise matrix")
        noise_matrix = []
        size = 10
        for x in range(size):
            noise_matrix.append([])
            for y in range(size):
                noise = round(float(noise_generator((x/size, y/size))) + 0.5, 1)
                noise_matrix[x].append(noise)

            print(noise_matrix[x])

        self.noise_matrix = noise_matrix
        print("generated noise matrix")


class Building:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def tick(self):
        pass


class Palace(Building):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.population = 1
        self.resources = {
            "food": 5,
            "wood": 0
        }

    def tick(self):
        if self.resources["food"] < self.population:
            self.population += 1
            print("Population increased")


manager = Manager()
manager.start_tick_thread()
PLAYER = None

def main():
    global PLAYER
    PLAYER = manager.create_player("MainPlayer")
    print(PLAYER.lands[0])
    while 1:
        input_str = input("> ")
        input_split = input_str.split()
        if input_split[0] == "create":  # create
            PLAYER = manager.create_player(input_split[1])

        elif input_split[0] == "show":
            print(PLAYER.lands[0])

        elif input_split[0] == "build":
            x, y = int(input_split[2]), int(input_split[3])
            if input_split[1] == "palace":
                if PLAYER.lands[0].get_tile_at(x, y) == "-":
                    print(f"building palace at {x} {y}")
                    PLAYER.lands[0].create_building(x, y, Palace)
                else:
                    print("invalid tile for palace")

while 1:
    try:
        main()
    except Exception as ex:
        traceback.print_exception(type(ex), ex, ex.__traceback__)
