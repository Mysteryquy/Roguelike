


    def move_towards_point(self, x: int, y: int) -> None:
        """
        moves this actor towards a point
        :param x: x of the point
        :param y: y of the point
        """
        dx = x - self.x
        dy = y - self.y

        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        self.creature.move(dx, dy)

    def move_away(self, other: Actor) -> None:
        """
        moves this actor away from the given actor
        :param other: actor this actor should move away from
        """
        dx = self.x - other.x
        dy = self.y - other.y

        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        self.creature.move(dx, dy)

