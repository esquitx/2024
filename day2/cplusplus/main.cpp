#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <stdexcept>
#include <sstream>

using namespace std;

bool is_monotic(vector<int> level)
{
    bool is_increasing = true;
    bool is_decresing = true;
    for (size_t i = 0; i < level.size() - 1; i++)
    {
        if (level[i] >= level[i + 1])
        {
            is_increasing = false;
        }

        if (level[i] <= level[i + 1])
        {
            is_decresing = false;
        }
    }

    return is_increasing || is_decresing;
}

bool is_increase_valid(vector<int> level)
{
    for (size_t i = 0; i < level.size() - 1; i++)
    {
        int diff = abs(level[i] - level[i + 1]);
        if ((diff < 1) || (diff > 3))
        {
            return false;
        }
    }
    return true;
}

bool part1(vector<int> level)
{
    if (is_increase_valid(level) && is_monotic(level))
        return true;
    else
        return false;
}

bool part2(vector<int> level)
{

    if (part1(level))
    {
        return true;
    }
    else
    {
        for (size_t i = 0; i < level.size(); i++)
        {
            vector<int> new_level = level;
            new_level.erase(new_level.begin() + i);
            if (is_increase_valid(new_level) && is_monotic(new_level))
            {
                return true;
            }
        }
    }
}

int main()
{
    try
    {
        cout << "Advent of Code 2024 - Day 2\n\n";

        // We do it a bit different than python
        // -> check in a level by level basis (since each line is independent)
        // i.e. part1 checks for monotonic and increasing for level, adds to count1
        // i.e. part2 checks par1 and checks for removing one element and adds to count2

        ifstream file("../../input.txt");
        if (!file.is_open())
            throw runtime_error("Could not open input.txt");

        int count1 = 0;
        int count2 = 0;
        string line;
        while (getline(file, line))
        {
            vector<int> level;
            int number;
            istringstream iss(line);
            while (iss >> number)
            {
                level.push_back(number);
            }

            if (part1(level))
            {
                count1++;
            }

            if (part2(level))
            {
                count2++;
            }
        }

        cout << "Part 1: " << endl;
        cout << "SOLUTION: " << count1 << endl;
        cout << "Part 2: " << endl;
        cout << "SOLUTION: " << count2 << endl;

        return 0;
    }
    catch (const exception &e)
    {
        cerr << "Error: " << e.what() << '\n';
        return 1;
    }
}