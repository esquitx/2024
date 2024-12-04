#include <iostream>
#include <fstream>
#include <sstream>
using namespace std;

string read_data(string filename = "../../input.txt")
{
    ifstream file(filename);
    stringstream buffer;
    buffer << file.rdbuf();
    string s = buffer.str();

    // add padding
    return "################" + s + "################";
}

int getDigits(const string &data, int &i)
{
    string num = "";
    while (i < data.length() && isdigit(data[i]))
    {
        num += data[i];
        i++;
    }
    return num.empty() ? -1 : stoi(num);
}

int part1(string data)
{
    int n = (int)data.length();
    int sum = 0;
    for (int i = 0; i < n; i++)
    {
        if (data.substr(i, 4) == "mul(")
        {
            i += 4;
            int x = getDigits(data, i);
            if (data[i] == ',')
            {
                i++;
                int y = getDigits(data, i);
                if (data[i] == ')')
                {
                    if (x != -1 && y != -1)
                    {
                        sum += x * y;
                    }
                }
            }
        }
    }
    return sum;
}

int part2(string data)
{
    int n = (int)data.length();
    int sum = 0;
    bool enabled = true;
    for (int i = 0; i < n; i++)
    {
        // do check
        if (data.substr(i, 4) == "do()" && !enabled)
        {
            enabled = true;
            i += 3;
            continue;
        }

        // don't check
        if (data.substr(i, 7) == "don't()" && enabled)
        {
            enabled = false;
            i += 6;
            continue;
        }

        if (enabled && data.substr(i, 4) == "mul(")
        {
            i += 4;
            int x = getDigits(data, i);
            if (data[i] == ',')
            {
                i++;
                int y = getDigits(data, i);
                if (data[i] == ')')
                {
                    if (x != -1 && y != -1)
                    {
                        sum += x * y;
                    }
                }
            }
        }
    }
    return sum;
}

int main()
{
    string data = read_data();

    cout << "Part 1: " << part1(data) << endl;
    cout << "Part 2: " << part2(data) << endl;

    return 0;
}