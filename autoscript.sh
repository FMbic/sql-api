#!/bin/bash

URL="127.1:5000/users"


# Function to create a new user
create_user() {
    read -p "Enter name: " name
    read -p "Enter email: " email
    response=$(curl -s -X POST $URL -H "Content-Type: application/json" -d "{\"name\": \"$name\", \"email\": \"$email\"}")
    echo "Create User Response: $response"
}

# Function to get all users
get_users() {
    response=$(curl -s -X GET $URL)
    echo "Get Users Response: $response"
#    echo $response 
}

# Function to update a user
update_user() {
    get_users
    read -p "Enter the ID of the user to update: " user_id
    read -p "Enter new name (leave empty to keep unchanged): " name
    read -p "Enter new email (leave empty to keep unchanged): " email
    data="{"
    if [ ! -z "$name" ]; then
        data+="\"name\": \"$name\""
    fi
    if [ ! -z "$email" ]; then
        [ "${#data}" -gt 1 ] && data+=", "
        data+="\"email\": \"$email\""
    fi
    data+="}"
    response=$(curl -s -X PATCH $URL/$user_id -H "Content-Type: application/json" -d "$data")
    echo "Update User Response: $response"
}

# Function to delete a user
delete_user() {
    get_users
    read -p "Enter the ID of the user to delete: " user_id
    response=$(curl -s -X DELETE $URL/$user_id)
    echo "Delete User Response: $response"
}


# Main script execution
main() {
    read -p "Do you want to add, modify, delete a user or get a list of users? (add/modify/delete/get): " action
    case $action in
        add)
            create_user
            ;;
        modify)
            update_user
            ;;
        delete)
            delete_user
            ;;
        get)
            get_users
            ;;
        *)
            echo "Invalid action. Please enter 'add', 'modify', or 'delete'."
            ;;
    esac
}

main
