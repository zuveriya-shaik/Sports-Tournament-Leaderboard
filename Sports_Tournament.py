# Parsing the game record with specific column widths
def parse_game_record(record):
    team_a_name = record[0:12].strip()
    team_a_score = int(record[12:14].strip())
    team_b_name = record[20:32].strip()
    team_b_score = int(record[32:34].strip())
    return team_a_name, team_a_score, team_b_name, team_b_score


# Build a dictionary to store the results of who defeated whom
def build_results_dict(game_records):
    results = {}
    for record in game_records:
        try:
            team_a_name, team_a_score, team_b_name, team_b_score = parse_game_record(record)
        except ValueError:
            continue

        # Record the winner
        if team_a_score > team_b_score:
            if team_a_name not in results:
                results[team_a_name] = set()
            results[team_a_name].add(team_b_name)
        else:
            if team_b_name not in results:
                results[team_b_name] = set()
            results[team_b_name].add(team_a_name)
    return results


# Function to check if a team has defeated another team (directly or indirectly)
def has_defeated(team_a, team_b, results, visited=None):
    if visited is None:
        visited = set()

    # If team A directly defeated team B
    if team_a in results and team_b in results[team_a]:
        return "directly"

    # Mark team A as visited
    visited.add(team_a)

    # Check indirect victory by exploring team A's victories
    if team_a in results:
        for defeated_team in results[team_a]:
            if defeated_team not in visited:
                result = has_defeated(defeated_team, team_b, results, visited)
                if result:
                    return "indirectly"

    return None


# Input the game records (20 records)
n = 2
game_records = []
for i in range(n):
    record = input(f"Enter game record {i+1} (e.g., CHENNAI 99 KOLKATA 50): ")
    game_records.append(record)

# Build the results dictionary
results = build_results_dict(game_records)

# Input the query records (10 queries)
m = 1
query_records = []
for i in range(m):
    team_a_name = input(f"Enter team A for query {i+1}: ").strip()
    team_b_name = input(f"Enter team B for query {i+1}: ").strip()
    query_records.append((team_a_name, team_b_name))

# Process the queries
for team_a, team_b in query_records:
    if team_a == team_b:
        print(f"{team_a} and {team_b} are the same team.")
    else:
        result = has_defeated(team_a, team_b, results)
        if result:
            print(f"{team_a} has {result} defeated {team_b}.")
        else:
            print(f"Neither {team_a} nor {team_b} has defeated each other directly or indirectly.")
