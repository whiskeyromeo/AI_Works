
        def min_value(game, m_depth, alpha, beta):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            moves = game.get_legal_moves()
            best_move = (-1,-1)
            if not moves:
                return self.score(game, self), best_move
            if m_depth == 0:
                best_move = moves[random.randint(0, len(moves))-1]
                return self.score(game, self), best_move
            best_score = float('inf')
            for move in moves:
                score, c_move = max_value(game.forecast_move(move), m_depth-1, alpha, beta)
                if score < best_score:
                    best_score = score
                    best_move = move
                if best_score <= alpha:
                    return best_score, best_move
                beta = min(beta, best_score)

            return best_score, best_move

        def max_value(game, m_depth, alpha, beta):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            moves = game.get_legal_moves()
            if not moves:
                return self.score(game, self), (-1,-1)
            if m_depth == 0:
                best_move = moves[random.randint(0, len(moves))-1]
                return self.score(game, self), best_move

            best_score = float('-inf')
            best_move = (-1,-1)
            for move in moves:
                score,c_move = min_value(game.forecast_move(move), m_depth-1, alpha, beta)
                if score > best_score:
                    best_score = score
                    best_move = move
                if best_score >= beta:
                    return best_score, best_move
                alpha = max(alpha, best_score)
            return best_score, best_move

        def AlphaBetaSearch(game, depth, alpha, beta):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            player_moves = game.get_legal_moves()
            if not player_moves: 
                return (-1,-1)
            if depth == 0:
                return player_moves[random.randint(0, len(moves))-1]
            best_score, best_move = max_value(game, depth, alpha, beta)
            return best_move
        
        if len(game.get_legal_moves()) == (game.width*game.height):
            best_move = (math.ceil(game.width/2), math.ceil(game.height/2))
        else:
            best_move = AlphaBetaSearch(game, depth, alpha, beta)
        
        return best_move