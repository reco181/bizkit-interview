from flask import Blueprint, request

from .data.search_data import USERS


bp = Blueprint("search", __name__, url_prefix="/search")


@bp.route("")
def search():
    return search_users(request.args.to_dict()), 200


def search_users(args):
    """Search users database

    Parameters:
        args: a dictionary containing the following search parameters:
            id: string
            name: string
            age: string
            occupation: string

    Returns:
        a list of users that match the search parameters
    """

    # Implement search here!
    if not args:
        return USERS

    # Define the priority order based on the order of args
    priority_order = list(args.keys())

    search_results = []
    for user in USERS:
        match_priorities = []
        
        # Iterate through each search parameter in order of priority
        for i, key in enumerate(priority_order):
            # Check for ID match
            if key == "id" and user["id"] == args["id"]:
                match_priorities.append(len(priority_order) - i)
            # Check for name match (case-insensitive)
            elif key == "name" and args["name"].lower() in user["name"].lower():
                match_priorities.append(len(priority_order) - i)
            # Check for age match (within 1 year range)
            elif key == "age" and int(args["age"]) - 1 <= user["age"] <= int(args["age"]) + 1:
                match_priorities.append(len(priority_order) - i)
            # Check for occupation match (case-insensitive)
            elif key == "occupation" and args["occupation"].lower() in user["occupation"].lower():
                match_priorities.append(len(priority_order) - i)
        
        # If the user matched any criteria, add them to the search results
        if match_priorities:
            # Use the highest priority match for this user
            search_results.append((max(match_priorities), user))

    # Sort the results based on match priority (descending) and then by id
    sorted_results = sorted(search_results, key=lambda x: (-x[0], x[1]["id"]))
    
    # Return only the user dictionaries, without the match priority
    return [user for _, user in sorted_results]
