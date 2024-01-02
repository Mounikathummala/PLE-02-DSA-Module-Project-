import json
import random
import time
import os

def update_leaderboard(leaderboard, user_name, wpm, category):
    user_found = False

    for entry in leaderboard:
        if entry['username'] == user_name and entry['category'] == category:
           
            entry['wpm'] = max(entry['wpm'], wpm)
            user_found = True

    if not user_found:
       
        leaderboard.append({'username': user_name, 'wpm': wpm, 'category': category})

  
    leaderboard.sort(key=lambda x: x['wpm'], reverse=True)

  
    with open('leaderboard.json', 'w') as file:
        json.dump({'leaderboard': leaderboard}, file, indent=4)

def show_leaderboard():
    # Display the leaderboard from the JSON file
    with open('leaderboard.json', 'r') as file:
        data = json.load(file)
        leaderboard = data.get('leaderboard', [])

    print("\nLeaderboard:")
    for entry in leaderboard:
        print(f"{entry['username']} ({entry['category']}): {entry['wpm']} WPM")

def load_categories_from_json(file_path):
    
    with open(file_path, 'r') as file:
        categories_data = json.load(file)
    return categories_data

def start_typing_test(words, category, challenge_mode=False, time_limit=None):
    print("\n Get ready! Type the following words :")
    input("Press Enter to start when you are ready...")

    start_time = time.time()
    words_typed = 0
    wrong_words_typed = []

    if not challenge_mode:
        for word in words:
            user_input = input(f"{word} ")

            if user_input.lower() == 'ctrl+q':
                print("\n Typing test aborted.")
                return 0, 0, []

            if user_input.strip() != word:
                wrong_words_typed.append(word)

            words_typed += 1
    else:
        # Challenge mode with a fixed time limit
        while time.time() - start_time < time_limit:
            target_word = random.choice(words)
            user_input = input(f"{target_word} ")

            if user_input.lower() == 'ctrl+q':
                print("\nTyping test aborted.")
                return 0, 0, []

            if user_input.strip() != target_word:
                wrong_words_typed.append(target_word)

            words_typed += 1

    end_time = time.time()
    time_taken = end_time - start_time
    wpm = int((words_typed / time_taken) * 60)

    print("\nTyping test completed!")
    print(f"Words Typed: {words_typed}")
    print(f"Time Taken: {round(time_taken, 2)} seconds")
    print(f"Words Per Minute: {wpm} WPM")

    return words_typed, wpm, wrong_words_typed

def main():
    categories_data = load_categories_from_json('word_categories.json')

    if not os.path.exists('leaderboard.json'):
        with open('leaderboard.json', 'w') as file:
            json.dump({'leaderboard': []}, file, indent=4)

    while True:
        print("\n Welcome to Typing Master!")
        user_name = input("Enter your username: ")
        option = input("Choose an option:\n1. Start Typing Test\n2. Show Leaderboard\n3. Exit\n")

        if option == '1':
            category = input("Choose a typing category:\n" + ', '.join(categories_data.keys()) + "\n")
            if category not in categories_data:
                print("Invalid category. Please choose a valid category.")
                continue

            challenge_mode_option = input("Do you want to play in challenge mode? (yes/no): ")
            challenge_mode = challenge_mode_option.lower() == 'yes'

            time_limit = None
            if challenge_mode:
                try:
                    time_limit = float(input("Enter the time limit for challenge mode (in seconds): "))
                except ValueError:
                    print("Invalid input. Using default time limit.")

            words = categories_data[category]

            words_typed, wpm, wrong_words_typed = start_typing_test(words, category, challenge_mode, time_limit)
            if words_typed > 0:
                with open('leaderboard.json', 'r') as file:
                    data = json.load(file)
                    leaderboard = data.get('leaderboard', [])

                update_leaderboard(leaderboard, user_name, wpm, category)

                print("\nWords Typed Incorrectly:")
                if (len(wrong_words_typed)==0):
                    print(0)
                else:
                    print(", ".join(wrong_words_typed))

        elif option == '2':
            show_leaderboard()

        elif option == '3':
            print("Thank you for playing. Goodbye!")
            break

        else:
            print("Invalid option. Please choose a valid option.")

        play_again = input("Do you want to play again? (yes/no): ")
        if play_again.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
