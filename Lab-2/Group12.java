import java.util.*;
import java.io.*;
import java.time.*;

public class Group12{

    // store all intermediate states
    public static ArrayList<BlockWorld_State> All_States = new ArrayList<BlockWorld_State>();

    // Goal State
    public static BlockWorld_State goal_State = new BlockWorld_State();

    // priority Queue to select state with best heuristic value
    public static PriorityQueue<BlockWorld_State> MaxPQueue = new PriorityQueue<BlockWorld_State>(
            new SortByHeuristicValue());

    public static boolean isSolution = false;
    public static int heuristic_fun;

    public static void main(final String args[]) {

        BlockWorld_State initial_State = new BlockWorld_State();

        // reading input file
        File input = new File(args[0]);

        try {
            heuristic_fun = Integer.parseInt(args[2]);
        } catch (Exception e) {
            heuristic_fun = 3;
        }

        // Reading input file & storing Goal State & initial states
        Scanner myReader = null;
        try {

            try {
                myReader = new Scanner(input);
            } catch (Exception e) {
                System.out.println("input file is not available");
                System.exit(0);
            }

            while (myReader.hasNextLine()) {
                myReader.nextLine();
                String line1 = myReader.nextLine();
                {
                    line1 = line1.replace('[', '\0');
                    line1 = line1.replace(']', '\0');
                    String[] allElements = line1.split(",");
                    for (String element : allElements) {
                        try {
                            goal_State.S1.push(Integer.parseInt(element.trim()));

                        } catch (Exception e) {
                        }
                    }
                }

                String line2 = myReader.nextLine();
                {
                    line2 = line2.replace('[', '\0');
                    line2 = line2.replace(']', '\0');
                    String[] allElements = line2.split(",");
                    for (String element : allElements) {
                        try {
                            goal_State.S2.push(Integer.parseInt(element.trim()));

                        } catch (Exception e) {

                        }
                    }
                }

                String line3 = myReader.nextLine();
                {
                    line3 = line3.replace('[', '\0');
                    line3 = line3.replace(']', '\0');
                    String[] allElements = line3.split(",");
                    for (String element : allElements) {
                        try {
                            goal_State.S3.push(Integer.parseInt(element.trim()));

                        } catch (Exception e) {

                        }
                    }
                }

                myReader.nextLine();
                myReader.nextLine();

                String line4 = myReader.nextLine();
                {
                    line4 = line4.replace('[', '\0');
                    line4 = line4.replace(']', '\0');
                    String[] allElements = line4.split(",");

                    for (String element : allElements) {
                        try {
                            initial_State.S1.push(Integer.parseInt(element.trim()));

                        } catch (Exception e) {

                        }
                    }

                }

                String line5 = myReader.nextLine();
                {
                    line5 = line5.replace('[', '\0');
                    line5 = line5.replace(']', '\0');
                    String[] allElements = line5.split(",");
                    for (String element : allElements) {
                        try {
                            initial_State.S2.push(Integer.parseInt(element.trim()));

                        } catch (Exception e) {

                        }
                    }
                }

                String line6 = myReader.nextLine();
                {
                    line6 = line6.replace('[', '\0');
                    line6 = line6.replace(']', '\0');
                    String[] allElements = line6.split(",");
                    for (String element : allElements) {
                        try {
                            initial_State.S3.push(Integer.parseInt(element.trim()));

                        } catch (Exception e) {

                        }
                    }
                }

            }
            myReader.close();

        } catch (Exception e) {
            e.printStackTrace();
        }

        System.out.print("Initial State :");
        initial_State.PrintBlockWorld_State();
        System.out.print("\nGoal State :");
        goal_State.PrintBlockWorld_State();
        System.out.println();

        All_States.add(initial_State);

        Instant start = Instant.now();

        // Selecting Besy for search or Hill Climbing according to inputs
        if (args[1].equals("BFS")) {
            BestFS(initial_State);
            isSolution = true;
            System.out.print("BFS:");
        } else {
            HillTop(initial_State);
            System.out.print("Hill Climbing:");
        }

        Instant finish = Instant.now();
        long timeElapsed = Duration.between(start, finish).toMillis();

        // printing all intermediate states
        for (BlockWorld_State i : All_States) {
            i.PrintBlockWorld_State();
        }

        if (isSolution == false) {
            System.out.print("\nSearch is struck in local maxima");
        }

        System.out.println("\nStates Explored : " + All_States.size());
        System.out.println("Total execution time (in Mili-Seconds) : " + timeElapsed);

    }

    // implementation of Best for search
    static void BestFS(BlockWorld_State intermediate_State) {

        // Considering possible all 6 intermediate states from any earlier state
        BlockWorld_State temp1 = new BlockWorld_State();
        BlockWorld_State temp2 = new BlockWorld_State();
        BlockWorld_State temp3 = new BlockWorld_State();
        BlockWorld_State temp4 = new BlockWorld_State();
        BlockWorld_State temp5 = new BlockWorld_State();
        BlockWorld_State temp6 = new BlockWorld_State();

        BlockWorld_State.copyStates(temp1, intermediate_State);
        BlockWorld_State.copyStates(temp2, intermediate_State);
        BlockWorld_State.copyStates(temp3, intermediate_State);
        BlockWorld_State.copyStates(temp4, intermediate_State);
        BlockWorld_State.copyStates(temp5, intermediate_State);
        BlockWorld_State.copyStates(temp6, intermediate_State);

        // if these 6 intermediate states are valid & unexplored, they will be added in
        // priority queue

        if (intermediate_State.S1.size() > 0) {
            temp1.S2.push(temp1.S1.pop());
            if (!All_States.contains(temp1) && !MaxPQueue.contains(temp1)) {
                temp1.heuristic_Function(goal_State);
                MaxPQueue.add(temp1);
            }

            temp2.S3.push(temp2.S1.pop());
            if (!All_States.contains(temp2) && !MaxPQueue.contains(temp2)) {
                temp2.heuristic_Function(goal_State);
                MaxPQueue.add(temp2);
            }

        }

        if (intermediate_State.S2.size() > 0) {
            temp3.S1.push(temp3.S2.pop());
            if (!All_States.contains(temp3) && !MaxPQueue.contains(temp3)) {
                temp3.heuristic_Function(goal_State);
                MaxPQueue.add(temp3);
            }
            temp4.S3.push(temp4.S2.pop());
            if (!All_States.contains(temp4) && !MaxPQueue.contains(temp4)) {
                temp4.heuristic_Function(goal_State);
                MaxPQueue.add(temp4);
            }
        }

        if (intermediate_State.S3.size() > 0) {
            temp5.S1.push(temp5.S3.pop());
            if (!All_States.contains(temp5) && !MaxPQueue.contains(temp5)) {
                temp5.heuristic_Function(goal_State);
                MaxPQueue.add(temp5);
            }
            temp6.S2.push(temp6.S3.pop());
            if (!All_States.contains(temp6) && !MaxPQueue.contains(temp6)) {
                temp6.heuristic_Function(goal_State);
                MaxPQueue.add(temp6);
            }
        }

        // considering top element of max priority queue
        intermediate_State = MaxPQueue.poll();

        if (!All_States.contains(intermediate_State)) {
            All_States.add(intermediate_State);
        }

        // if program finds goal state, program will stop else it will explore next
        // states
        if (intermediate_State.equals(goal_State)) {
            // intermediate_State.PrintBlockWorld_State();
        } else {
            BestFS(intermediate_State);
        }

    }

    static void HillTop(BlockWorld_State intermediate_State) {

        // for Hill Climbing, max priority queue need to be cleared before adding new
        // states
        MaxPQueue.clear();

        // Considering possible all 6 intermediate states from any earlier state &
        // current state (temp)

        BlockWorld_State temp = new BlockWorld_State();
        BlockWorld_State temp1 = new BlockWorld_State();
        BlockWorld_State temp2 = new BlockWorld_State();
        BlockWorld_State temp3 = new BlockWorld_State();
        BlockWorld_State temp4 = new BlockWorld_State();
        BlockWorld_State temp5 = new BlockWorld_State();
        BlockWorld_State temp6 = new BlockWorld_State();

        BlockWorld_State.copyStates(temp, intermediate_State);
        BlockWorld_State.copyStates(temp1, intermediate_State);
        BlockWorld_State.copyStates(temp2, intermediate_State);
        BlockWorld_State.copyStates(temp3, intermediate_State);
        BlockWorld_State.copyStates(temp4, intermediate_State);
        BlockWorld_State.copyStates(temp5, intermediate_State);
        BlockWorld_State.copyStates(temp6, intermediate_State);

        // if these 6 intermediate states are valid & unexplored, they will be added in
        // priority queue
        if (intermediate_State.S1.size() > 0) {
            temp1.S2.push(temp1.S1.pop());
            if (!All_States.contains(temp1) && !MaxPQueue.contains(temp1)) {
                temp1.heuristic_Function(goal_State);
                MaxPQueue.add(temp1);
            }

            temp2.S3.push(temp2.S1.pop());
            if (!All_States.contains(temp2) && !MaxPQueue.contains(temp2)) {
                temp2.heuristic_Function(goal_State);
                MaxPQueue.add(temp2);
            }

        }

        if (intermediate_State.S2.size() > 0) {
            temp3.S1.push(temp3.S2.pop());
            if (!All_States.contains(temp3) && !MaxPQueue.contains(temp3)) {
                temp3.heuristic_Function(goal_State);
                MaxPQueue.add(temp3);
            }
            temp4.S3.push(temp4.S2.pop());
            if (!All_States.contains(temp4) && !MaxPQueue.contains(temp4)) {
                temp4.heuristic_Function(goal_State);
                MaxPQueue.add(temp4);
            }
        }

        if (intermediate_State.S3.size() > 0) {
            temp5.S1.push(temp5.S3.pop());
            if (!All_States.contains(temp5) && !MaxPQueue.contains(temp5)) {
                temp5.heuristic_Function(goal_State);
                MaxPQueue.add(temp5);
            }
            temp6.S2.push(temp6.S3.pop());
            if (!All_States.contains(temp6) && !MaxPQueue.contains(temp6)) {
                temp6.heuristic_Function(goal_State);
                MaxPQueue.add(temp6);
            }
        }

        temp = MaxPQueue.poll();

        // if program finds valid next state it will continue else program will stop
        if (temp.heuristic_Value > intermediate_State.heuristic_Value) {

            intermediate_State = temp;

            if (!All_States.contains(intermediate_State)) {
                All_States.add(intermediate_State);
            }

            if (intermediate_State.equals(goal_State)) {
                isSolution = true;
            } else {
                HillTop(intermediate_State);
            }
        } else {
            // System.out.println("No Solution");
            // System.exit(0);
        }

    }
}

// Comparator for max priority queue (for comparing class-objects)
class SortByHeuristicValue implements Comparator<BlockWorld_State> {
    public int compare(BlockWorld_State s1, BlockWorld_State s2) {
        if (s1.heuristic_Value > s2.heuristic_Value)
            return -1;
        else if (s1.heuristic_Value < s2.heuristic_Value)
            return 1;
        return 0;
    }
}

// class for each state
class BlockWorld_State {

    // three stacks of each state
    Stack<Integer> S1 = new Stack<Integer>();
    Stack<Integer> S2 = new Stack<Integer>();
    Stack<Integer> S3 = new Stack<Integer>();

    // heuristic_Value for each state calculated from heuristic function
    int heuristic_Value = 0;

    static void copyStates(BlockWorld_State state1, BlockWorld_State state2) {
        state1.S1 = (Stack<Integer>) state2.S1.clone();
        state1.S2 = (Stack<Integer>) state2.S2.clone();
        state1.S3 = (Stack<Integer>) state2.S3.clone();
        state1.heuristic_Value = state2.heuristic_Value;
    }

    // .equals function for comparing objects
    @Override
    public boolean equals(Object obj) {

        BlockWorld_State that = (BlockWorld_State) obj;
        boolean isequal = this.S1.equals(that.S1) && this.S2.equals(that.S2) && this.S3.equals(that.S3);

        return isequal;
    }

    // multiple heuristic Functions it will select one of these according to input
    int heuristic_Function(BlockWorld_State goal_State) {

        // 1st heuristic Function :
        /*
         * In intermediate state, depending on number matching-positions of blocks with
         * goal state heuristic value will be higher. (here all matching-positions have
         * same weightage-1000)
         */
        if (Group12.heuristic_fun == 1) {
            int heuristic_value_temp = 0;

            for (int i = 0; i < goal_State.S1.size(); i++) {
                int temp1 = goal_State.S1.elementAt(i);
                int temp2 = -1;

                try {
                    temp2 = S1.elementAt(i);
                } catch (Exception e) {
                    temp2 = -1;
                }

                if (temp1 == temp2) {
                    heuristic_value_temp += 1000;
                }
            }

            for (int i = 0; i < goal_State.S2.size(); i++) {

                int temp2 = -1;

                try {
                    temp2 = S2.elementAt(i);
                } catch (Exception e) {
                    temp2 = -1;
                }

                if (goal_State.S2.elementAt(i) == temp2) {
                    heuristic_value_temp += 1000;
                }

            }

            for (int i = 0; i < goal_State.S3.size(); i++) {

                int temp1 = goal_State.S3.elementAt(i);

                int temp2 = -1;

                try {
                    temp2 = S3.elementAt(i);
                } catch (Exception e) {
                    temp2 = -1;
                }

                if (temp1 == temp2) {
                    heuristic_value_temp += 1000;
                }

            }

            heuristic_Value = heuristic_value_temp;

            return heuristic_value_temp;
        }
        // 2nd heuristic Function :
        /*
         * In intermediate state, depending on number matching-positions of blocks with
         * goal state + for non-matching positions if block is in same as goal-stack,
         * heuristic value will be higher. (here all matching-positions have
         * weightage-1000 & if block is in same goal-stack will have weigtage of 100)
         */
        else if (Group12.heuristic_fun == 2) {
            int heuristic_value_temp = 0;

            for (int i = 0; i < goal_State.S1.size(); i++) {
                int temp1 = goal_State.S1.elementAt(i);
                int temp2 = -1;

                try {
                    temp2 = S1.elementAt(i);
                } catch (Exception e) {
                    temp2 = -1;
                }

                if (temp1 == temp2) {
                    heuristic_value_temp += 1000;
                } else if (goal_State.S1.contains(temp2)) {
                    heuristic_value_temp += 100;
                } else {
                    break;
                }
            }

            for (int i = 0; i < goal_State.S2.size(); i++) {

                int temp2 = -1;

                try {
                    temp2 = S2.elementAt(i);
                } catch (Exception e) {
                    temp2 = -1;
                }

                if (goal_State.S2.elementAt(i) == temp2) {
                    heuristic_value_temp += 1000;
                } else if (goal_State.S1.contains(temp2)) {
                    heuristic_value_temp += 100;
                } else {
                    break;
                }

            }

            for (int i = 0; i < goal_State.S3.size(); i++) {

                int temp1 = goal_State.S3.elementAt(i);

                int temp2 = -1;

                try {
                    temp2 = S3.elementAt(i);
                } catch (Exception e) {
                    temp2 = -1;
                }

                if (temp1 == temp2) {
                    heuristic_value_temp += 1000;
                } else if (goal_State.S1.contains(temp2)) {
                    heuristic_value_temp += 100;
                } else {
                    break;
                }

            }

            heuristic_Value = heuristic_value_temp;

            return heuristic_value_temp;
        }
        // 3rd heuristic Function :
        /*
         * In intermediate state, if base of stacks matches, it will check further add
         * gives higher heuristic value otherwise it will skip ( for each block matching
         * from base to goal-state will have same weightage of 1000)
         */
        else if (Group12.heuristic_fun == 3) {
            int heuristic_value_temp = 0;

            for (int i = 0; i < goal_State.S1.size(); i++) {
                int temp1 = goal_State.S1.elementAt(i);
                int temp2 = -1;

                try {
                    temp2 = S1.elementAt(i);
                } catch (Exception e) {
                    temp2 = -1;
                }

                if (temp1 == temp2) {
                    heuristic_value_temp += 1000;
                } else {
                    break;
                }
            }

            for (int i = 0; i < goal_State.S2.size(); i++) {

                int temp2 = -1;

                try {
                    temp2 = S2.elementAt(i);
                } catch (Exception e) {
                    temp2 = -1;
                }

                if (goal_State.S2.elementAt(i) == temp2) {
                    heuristic_value_temp += 1000;
                } else {
                    break;
                }

            }

            for (int i = 0; i < goal_State.S3.size(); i++) {

                int temp1 = goal_State.S3.elementAt(i);

                int temp2 = -1;

                try {
                    temp2 = S3.elementAt(i);
                } catch (Exception e) {
                    temp2 = -1;
                }

                if (temp1 == temp2) {
                    heuristic_value_temp += 1000;
                } else {
                    break;
                }

            }

            heuristic_Value = heuristic_value_temp;

            return heuristic_value_temp;
        }
        return heuristic_Value;

    }

    // to print any state
    public void PrintBlockWorld_State() {

        System.out.println();
        // System.out.println("Heuristic Value : " + this.heuristic_Value);

        System.out.print("[");
        for (int l = 0; l < S1.size(); l++) {
            System.out.print(S1.elementAt(l));

            if (l + 1 != S1.size()) {
                System.out.print(", ");
            }
        }
        System.out.print("]");
        System.out.println();
        System.out.print("[");
        for (int l = 0; l < S2.size(); l++) {
            System.out.print(S2.elementAt(l));

            if (l + 1 != S2.size()) {
                System.out.print(", ");
            }
        }
        System.out.print("]");
        System.out.println();
        System.out.print("[");
        for (int l = 0; l < S3.size(); l++) {
            System.out.print(S3.elementAt(l));

            if (l + 1 != S3.size()) {
                System.out.print(", ");
            }
        }
        System.out.print("]");
        System.out.println();

    }

    public BlockWorld_State() {
    }

}