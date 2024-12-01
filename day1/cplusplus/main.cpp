#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <stdexcept>

using namespace std;

pair<vector<int>, vector<int>> read_input(const string &filename = "../../input.txt")
{
    ifstream file(filename);
    if (!file)
    {
        throw runtime_error("Cannot open input file: " + filename);
    }

    vector<int> col1, col2;
    int a, b;
    while (file >> a >> b)
    {
        col1.push_back(a);
        col2.push_back(b);
    }
    return {col1, col2};
}

void part1()
{

    // WHY AUTO?
    // tells compiler to automatically deduce the type
    // but this removes type safety...
    // so better not use
    pair<vector<int>, vector<int>> columns = read_input();
    vector<int> sorted1 = columns.first;
    vector<int> sorted2 = columns.second;

    sort(sorted1.begin(), sorted1.end());
    sort(sorted2.begin(), sorted2.end());

    int sum = 0;
    for (size_t i = 0; i < sorted1.size(); ++i)
    {
        sum += abs(sorted1[i] - sorted2[i]);
    }

    cout << "PART 1\nSOLUTION: " << sum << "\n\n";
}

void part2()
{
    pair<vector<int>, vector<int>> columns = read_input();
    vector<int> c1 = columns.first;
    vector<int> c2 = columns.second;

    int score = 0;
    for (const int x : c1)
    {
        score += x * count(c2.cbegin(), c2.cend(), x);
    }

    cout << "PART 2\nSOLUTION: " << score << "\n\n";
}

int main()
{
    try
    {
        cout << "Advent of Code 2024 - Day 1\n\n";
        part1();
        part2();
        return 0;
    }
    catch (const exception &e)
    {
        cerr << "Error: " << e.what() << '\n';
        return 1;
    }
}