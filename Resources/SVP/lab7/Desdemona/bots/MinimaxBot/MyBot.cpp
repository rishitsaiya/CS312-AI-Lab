/*
* @file botTemplate.cpp
* @author Arun Tejasvi Chaganty <arunchaganty@gmail.com>
* @date 2010-02-04
* Template for users to create their own bots
*/

#include "Othello.h"
#include "OthelloBoard.h"
#include "OthelloPlayer.h"
#include <cstdlib>
#include <limits.h>
#include <chrono>

using namespace std;
using namespace Desdemona;

auto start = chrono::steady_clock::now();
int time_taken(){
    return ( chrono::duration_cast<chrono::milliseconds>(chrono::steady_clock::now() - start).count() );
}


class MyBot: public OthelloPlayer
{
    public:
        /**
         * Initialisation routines here
         * This could do anything from open up a cache of "best moves" to
         * spawning a background processing thread. 
         */
        MyBot( Turn turn );

        /**
         * Play something 
         */
        virtual Move play(const OthelloBoard& board );
        virtual int minimax(OthelloBoard& board, Turn turn, int depth, Move move);
        virtual int heuristic( OthelloBoard &board, int mode );
    private:
        
};

MyBot::MyBot( Turn turn )
    : OthelloPlayer( turn )
{
}

Move MyBot::play(const OthelloBoard& board)
{
    start = chrono::steady_clock::now();
    list<Move> moves = board.getValidMoves( turn );
    Move bestMove = *moves.begin();
    int bestScore = INT_MIN; 
    int maxDepth = 0;
    while(++maxDepth){// While 2 seconds not over || full board explored

        for (Move move: moves) 
        {
            OthelloBoard newBoard = OthelloBoard(board);
            int evaluated = minimax(newBoard, this->turn, maxDepth, move);
            
            if(evaluated == INT_MIN){ // Time up, return best move so far!
                return bestMove;
            }
            
            if(evaluated > bestScore){ 
                bestMove = move; 
                bestScore = evaluated;
            }
            
            
        } 
    }
    return bestMove;
}

int MyBot::minimax(OthelloBoard& board, Turn turn, int depth, Move move){
    
    if(time_taken() > 1600){
        return INT_MIN;
    }

    
    OthelloBoard newBoard = OthelloBoard(board);
    newBoard.makeMove(turn, move);
    list<Move> children = newBoard.getValidMoves(other(turn));
    
    if(depth == 0){
        return heuristic(newBoard, 3);
    }
    
    if(this->turn == turn){ // minimizingPlayer, Note: Convention seems to be interchanged, but, turn updated after making move only 
        int best = INT_MAX;
        for (Move child: children) 
        {
            int val = minimax(newBoard, other(turn), depth-1, child);
            best = min(val, best); 
            // beta = min(best, beta); 
            // if (beta <= alpha) 
            //     break;
        }  
        return best;
    }
    else // maximizing player
    {
        int best = INT_MIN;
        for (Move child: children) 
        {
            int val = minimax(newBoard, other(turn), depth-1, child);
            if(val == INT_MIN){
                return INT_MIN;
            }
            best = max(val, best); 
            // alpha = max(best, alpha);  
            // if (beta <= alpha) 
            //     break; 
        }  
        return best;
    }
}


int MyBot::heuristic( OthelloBoard &board, int mode ) {
    int x[] = {0, 0, 7, 7};
    int y[] = {0, 7, 0, 7};
    int myCorners = 0, oppCorners = 0;
    int myMoves = board.getValidMoves(this->turn).size();
    int oppMoves = board.getValidMoves(other(this->turn)).size();

    switch(mode){
        case 1: {// Coin Parity
            if(this->turn == BLACK)
                return ( board.getBlackCount() - board.getRedCount() );
            return ( board.getRedCount() - board.getBlackCount() );
            break;
        }

        case 2: {// Corners Captured
            for(int i=0; i<4; ++i){
                if(board.get(x[i], y[i]) == this->turn)
                    myCorners ++;
                else if(board.get(x[i], y[i]) == other(this->turn))
                    oppCorners++;
            }
            return ( myCorners - oppCorners );
        }

        case 3: {// Mobility
            return ( myMoves - oppMoves );
        }

        default: {
            return ( board.getBlackCount() - board.getRedCount() );
            break;
        }
    }
}


// The following lines are _very_ important to create a bot module for Desdemona
extern "C" {
    OthelloPlayer* createBot( Turn turn )
    {
        return new MyBot( turn );
    }

    void destroyBot( OthelloPlayer* bot )
    {
        delete bot;
    }
}

