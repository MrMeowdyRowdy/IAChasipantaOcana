import math

class BlockGame:
    def __init__(self, initial_piles):
        self.initial_piles = initial_piles

    def initial_state(self):
        """
        Returns the starting state of the game.
        """
        return [self.initial_piles]

    def print_state(self, piles):
        """
        Print the current state of the game.
        """
        print("Current piles:", piles)

    def player(self, piles):
        """
        Returns the current player.
        """
        return len(piles) % 2  # Alternate players based on the number of piles

    def actions(self, piles):
        """
        Returns all possible actions for the current player.
        """
        possible_actions = []
        for pile_index, pile in enumerate(piles):
            if pile > 2:
                for i in range(1, pile):
                    if pile - i != i:  # Check if pile can be divided into two different numbers
                        possible_actions.append((pile_index, pile - i, i))
        return possible_actions

    def result(self, piles, action):
        """
        Returns the new state of the game after applying the action.
        """
        new_piles = piles[:]
        pile_index, pile_value_1, pile_value_2 = action
        new_piles[pile_index] -= pile_value_1
        new_piles.append(pile_value_1)
        new_piles.append(pile_value_2)
        new_piles.pop(pile_index)  # Remove original pile
        return new_piles

    def winner(self, piles):
        """
        Determines if there's a winner.
        """
        return not any(pile > 2 for pile in piles)

    def terminal(self, piles):
        """
        Checks if the game is over.
        """
        return self.winner(piles) or not any(pile > 2 for pile in piles)

    def utility(self, piles):
        """
        Returns the utility value of the current state.
        """
        if self.winner(piles):
            return 1 if len(piles) % 2 == 0 else -1
        return 0

    def max_value(self, piles, alpha, beta):
        """
        Returns the maximum value for the current player on the board
        using alpha-beta pruning.
        """
        if self.terminal(piles):
            return self.utility(piles)
        v = -math.inf
        for action in self.actions(piles):
            v = max(v, self.min_value(self.result(piles, action), alpha, beta))
            alpha = max(alpha, v)
            if alpha >= beta:
                break
        return v

    def min_value(self, piles, alpha, beta):
        """
        Returns the minimum value for the current player on the board
        using alpha-beta pruning.
        """
        if self.terminal(piles):
            return self.utility(piles)
        v = math.inf
        for action in self.actions(piles):
            v = min(v, self.max_value(self.result(piles, action), alpha, beta))
            beta = min(beta, v)
            if alpha >= beta:
                break
        return v

    def minimax(self, piles):
        """
        Returns the optimal action for the current player on the board
        using the minimax algorithm with alpha-beta pruning.
        """
        if self.terminal(piles):
            return None
        if self.player(piles) == 0:  # Max player
            v = -math.inf
            opt_action = None
            for action in self.actions(piles):
                new_value = self.min_value(self.result(piles, action), -math.inf, math.inf)
                if new_value > v:
                    v = new_value
                    opt_action = action
            return opt_action
        else:  # Min player
            v = math.inf
            opt_action = None
            for action in self.actions(piles):
                new_value = self.max_value(self.result(piles, action), -math.inf, math.inf)
                if new_value < v:
                    v = new_value
                    opt_action = action
            return opt_action

def main():
    num_piles = int(input("Enter the number of piles: "))
    game = BlockGame(num_piles)  # Initial number of piles
    piles = game.initial_state()
    game.print_state(piles)
    while not game.terminal(piles):
        if game.player(piles) == 0:
            move = game.minimax(piles)
            print("Computer's move:", move[1], move[2])
        else:
            if len(piles) > 1:
                while True:
                    pile_index = int(input("Choose your pile (0 to {}): ".format(len(piles) - 1)))
                    if pile_index >= 0 and pile_index < len(piles) and piles[pile_index] > 2:
                        break
                    print("Invalid pile index or pile cannot be divided. Choose again.")
                print("Choose how to divide the pile (pile1, pile2):")
                while True:
                    pile1, pile2 = map(int, input().split())
                    if 0 < pile1 < piles[pile_index] and 0 < pile2 < piles[pile_index] and pile1 != pile2:
                        break
                    print("Invalid division. Choose again.")
                move = (pile_index, pile1, pile2)
            else:
                print("Only one pile remains. It must be divided.")
                while True:
                    pile1, pile2 = map(int, input("Choose how to divide the pile (pile1, pile2): ").split())
                    if pile1 + pile2 == piles[0] and pile1 != pile2:
                        break
                    print("Invalid division. Choose again.")
                move = (0, pile1, pile2)
        piles = game.result(piles, move)
        game.print_state(piles)
    if game.utility(piles) == 1:
        print("Player wins!")
    else:
        print("Computer wins!")

if __name__ == "__main__":
    main()
