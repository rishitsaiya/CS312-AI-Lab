/*
* @file botTemplate.cpp
* @author Arun Tejasvi Chaganty <arunchaganty@gmail.com>
* @date 2010-02-04
* Template for users to create their own bots
*/

#include <chrono>
#include "Othello.h"
#include "OthelloPlayer.h"
#include "OthelloBoard.h"

//
#define HeuristicFunNo 3
//

using namespace std;
using namespace Desdemona;

#define INT_MIN -2147483648
#define INT_MAX +2147483647

auto start = chrono::steady_clock::now();

class MyBot : public OthelloPlayer
{
public:
    MyBot(Turn turn);

    virtual Move play(const OthelloBoard &board);
    virtual int minMaxAlgo(OthelloBoard &board, Turn turn, int depth, Move move, int Min, int Max);
    virtual int heuristicForMinMax(OthelloBoard &board, int mode);
};

MyBot::MyBot(Turn turn) : OthelloPlayer(turn) {}

Move MyBot::play(const OthelloBoard &board)
{
    start = chrono::steady_clock::now();
    list<Move> nextMoves = board.getValidMoves(turn);
    Move bestMove = *nextMoves.begin();
    int bestScore = INT_MIN;
    int depth = 3;

    // while (depth++) // While 2 seconds not over || full board explored
    // {
    for (Move nextMove : nextMoves)
    {
        OthelloBoard gameBoard = OthelloBoard(board);
        int heuristicValue = minMaxAlgo(gameBoard, this->turn, depth, nextMove, INT_MIN, INT_MAX);

        if (heuristicValue > bestScore)
        {
            bestMove = nextMove;
            bestScore = heuristicValue;
        }

        if (heuristicValue == INT_MIN) // Time up, return best move so far!
            return bestMove;
    }
    // }
    //
    printf("Selecting move : (%d, %d)\n", bestMove.x, bestMove.y);
    //
    return bestMove;
}

int MyBot::minMaxAlgo(OthelloBoard &board, Turn turn, int depth, Move move, int Min, int Max)
{
    if (chrono::duration_cast<chrono::milliseconds>(chrono::steady_clock::now() - start).count() > 1600)
        return INT_MIN;

    OthelloBoard gameBoard = OthelloBoard(board);
    gameBoard.makeMove(turn, move);
    list<Move> moveTree = gameBoard.getValidMoves(other(turn));

    if (depth == 0)
        return heuristicForMinMax(gameBoard, HeuristicFunNo);

    //
    printf("Exploring : (%d, %d),\t depth = %d,\t No. children - %d \n", move.x, move.y, depth, moveTree.size());
    int branchNodes = 0;
    for (Move child : moveTree)
    {
        OthelloBoard intermediateBoard = OthelloBoard(board);
        intermediateBoard.makeMove(turn, move);
        printf("Child - %d ==> (%d, %d) :\t Heuristic Value: %d\n", branchNodes, child.x, child.y, heuristicForMinMax(intermediateBoard, HeuristicFunNo));
        branchNodes++;
    }
    //

    int bestValue = (this->turn == turn) ? INT_MAX : INT_MIN;

    if (this->turn == turn)
    {
        for (Move move : moveTree)
        {
            bestValue = min(bestValue, minMaxAlgo(gameBoard, other(turn), depth - 1, move, Min, Max));
            if (Min >= min(Max, bestValue))
                break;
        }
    }
    else
    {
        for (Move move : moveTree)
        {
            bestValue = max(bestValue, minMaxAlgo(gameBoard, other(turn), depth - 1, move, Min, Max));
            if (Max <= max(bestValue, Min))
                break;
        }
    }
    return bestValue;
}

int MyBot::heuristicForMinMax(OthelloBoard &board, int mode)
{
    // 1616 -351 116 053
    // -351 -181 -006 -023
    // 116 -006  051  006
    // 053 -023 -006 -001

    int oppoPossibleMoves = board.getValidMoves(other(this->turn)).size();
    int myPossibleMoves = board.getValidMoves(this->turn).size();

    int diffenceMoves = myPossibleMoves - oppoPossibleMoves;

    switch (mode)
    {
    case 3:
        return diffenceMoves;
    case 1:
    {
        if (this->turn == BLACK)
            return (board.getBlackCount() - board.getRedCount());
        return (board.getRedCount() - board.getBlackCount());
    }
    case 2:
    {
        int myPositionValue = 0;
        int oppPositionValue = 0;

        int x0[] = {0, 0, 7, 7};
        int y0[] = {0, 7, 0, 7};

        for (int i = 0; i < 4; ++i)
        {
            if (board.get(x0[i], y0[i]) == this->turn)
                myPositionValue += 1616;
            else if (board.get(x0[i], y0[i]) == other(this->turn))
                oppPositionValue += 1616;
        }

        int x1[] = {1, 0, 7, 1, 0, 6, 6, 7};
        int y1[] = {0, 1, 1, 7, 6, 0, 7, 6};

        for (int i = 0; i < 8; ++i)
        {
            if (board.get(x1[i], y1[i]) == this->turn)
                myPositionValue -= 351;
            else if (board.get(x1[i], y1[i]) == other(this->turn))
                oppPositionValue -= 351;
        }

        int x2[] = {2, 0, 7, 2, 0, 5, 5, 7};
        int y2[] = {0, 2, 2, 7, 5, 0, 7, 5};

        for (int i = 0; i < 8; ++i)
        {
            if (board.get(x2[i], y2[i]) == this->turn)
                myPositionValue += 116;
            else if (board.get(x2[i], y2[i]) == other(this->turn))
                oppPositionValue += 116;
        }

        int x3[] = {3, 0, 7, 3, 0, 4, 4, 7};
        int y3[] = {0, 3, 3, 7, 4, 0, 7, 4};

        for (int i = 0; i < 8; ++i)
        {
            if (board.get(x3[i], y3[i]) == this->turn)
                myPositionValue += 53;
            else if (board.get(x3[i], y3[i]) == other(this->turn))
                oppPositionValue += 53;
        }

        int x4[] = {1, 1, 6, 6};
        int y4[] = {1, 6, 1, 6};

        for (int i = 0; i < 4; ++i)
        {
            if (board.get(x4[i], y4[i]) == this->turn)
                myPositionValue -= 181;
            else if (board.get(x4[i], y4[i]) == other(this->turn))
                oppPositionValue -= 181;
        }

        // int x5[] = {2, 1, 6, 5, 1, 5, 6, 2};
        // int y5[] = {1, 2, 5, 6, 5, 1, 2, 6};

        // for (int i = 0; i < 8; ++i)
        // {
        //     if (board.get(x5[i], y5[i]) == this->turn)
        //         myPositionValue -= 6;
        //     else if (board.get(x5[i], y5[i]) == other(this->turn))
        //         oppPositionValue -= 6;
        // }

        int x6[] = {2, 1, 6, 5, 1, 5, 6, 2, 2, 2, 5, 5};
        int y6[] = {1, 2, 5, 6, 5, 1, 2, 6, 3, 4, 3, 4};

        for (int i = 0; i < 12; ++i)
        {
            if (board.get(x6[i], y6[i]) == this->turn)
                myPositionValue -= 6;
            else if (board.get(x6[i], y6[i]) == other(this->turn))
                oppPositionValue -= 6;
        }

        int x7[] = {3, 1, 6, 4, 1, 4, 6, 3};
        int y7[] = {1, 3, 4, 6, 4, 1, 3, 6};

        for (int i = 0; i < 8; ++i)
        {
            if (board.get(x7[i], y7[i]) == this->turn)
                myPositionValue -= 23;
            else if (board.get(x7[i], y7[i]) == other(this->turn))
                oppPositionValue -= 23;
        }

        int x8[] = {2, 2, 5, 5};
        int y8[] = {2, 5, 2, 5};

        for (int i = 0; i < 4; ++i)
        {
            if (board.get(x8[i], y8[i]) == this->turn)
                myPositionValue += 51;
            else if (board.get(x8[i], y8[i]) == other(this->turn))
                oppPositionValue += 51;
        }

        int x9[] = {3, 3, 4, 4};
        int y9[] = {3, 4, 3, 4};

        for (int i = 0; i < 4; ++i)
        {
            if (board.get(x9[i], y9[i]) == this->turn)
                myPositionValue -= 1;
            else if (board.get(x9[i], y9[i]) == other(this->turn))
                oppPositionValue -= 1;
        }

        int x10[] = {3, 3, 4, 4};
        int y10[] = {2, 5, 2, 5};

        for (int i = 0; i < 4; ++i)
        {
            if (board.get(x10[i], y10[i]) == this->turn)
                myPositionValue += 7;
            else if (board.get(x10[i], y10[i]) == other(this->turn))
                oppPositionValue += 7;
        }

        return (myPositionValue - oppPositionValue);
    }
    default:
        return (board.getBlackCount() - board.getRedCount());
    }
}

// The following lines are _very_ important to create a bot module for Desdemona
extern "C"
{
    OthelloPlayer *createBot(Turn turn)
    {
        return new MyBot(turn);
    }

    void destroyBot(OthelloPlayer *bot)
    {
        delete bot;
    }
}
