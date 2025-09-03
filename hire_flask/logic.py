import json, os
from datetime import datetime

# ---------------- File Paths ----------------
PROFILES_FILE = "profile.json"
MESSAGES_FILE = "messages.json"
REQUESTS_FILE = "requests.json"
ACHIEVEMENTS_FILE = "achievements.json"

# ---------------- Helpers ----------------
def ensure_file(path, default):
    """Make sure JSON file exists with default content."""
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(default, f, indent=4)

def load_json(path, default=[]):
    ensure_file(path, default)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# ---------------- Profiles ----------------
def load_profiles():
    return load_json(PROFILES_FILE)

def save_profiles(profiles):
    save_json(PROFILES_FILE, profiles)

def add_profile(name, age, address, contact, occupation, image="default.png"):
    profiles = load_profiles()
    profiles.append({
        "name": name,
        "age": age,
        "address": address,
        "contact": contact,
        "occupation": occupation,
        "image": image,
        "rating_sum": 0,
        "num_votes": 0,
        "hire_count": 0,
        "achievements": []
    })
    save_profiles(profiles)

def rate_profile(profile_name, rating):
    profiles = load_profiles()
    for p in profiles:
        if p["name"] == profile_name:
            p["rating_sum"] += rating
            p["num_votes"] += 1
            break
    save_profiles(profiles)

def get_leaderboard():
    profiles = load_profiles()
    for p in profiles:
        p["avg_rating"] = (p["rating_sum"] / p["num_votes"]) if p["num_votes"] > 0 else 0
    return sorted(profiles, key=lambda x: (x["avg_rating"], x["hire_count"]), reverse=True)

# ---------------- Messages ----------------
def load_messages():
    return load_json(MESSAGES_FILE)

def save_messages(messages):
    save_json(MESSAGES_FILE, messages)

def send_message(sender, receiver, message):
    messages = load_messages()
    messages.append({
        "sender": sender,
        "receiver": receiver,
        "message": message,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    save_messages(messages)

def get_chat(user1, user2):
    messages = load_messages()
    return [m for m in messages if (m["sender"] == user1 and m["receiver"] == user2) or (m["sender"] == user2 and m["receiver"] == user1)]

# ---------------- Hire Requests ----------------
def load_requests():
    return load_json(REQUESTS_FILE)

def save_requests(requests):
    save_json(REQUESTS_FILE, requests)

def send_hire_request(sender, receiver):
    requests = load_requests()
    requests.append({
        "sender": sender,
        "receiver": receiver,
        "status": "pending",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    save_requests(requests)

def get_requests_for_user(user):
    requests = load_requests()
    return [r for r in requests if r["receiver"] == user]

def update_request_status(sender, receiver, new_status):
    requests = load_requests()
    for r in requests:
        if r["sender"] == sender and r["receiver"] == receiver:
            r["status"] = new_status
            break
    save_requests(requests)

# ---------------- Achievements ----------------
def load_achievements():
    return load_json(ACHIEVEMENTS_FILE)

def save_achievements(achievements):
    save_json(ACHIEVEMENTS_FILE, achievements)

def add_achievement(profile_name, achievement):
    profiles = load_profiles()
    for p in profiles:
        if p["name"] == profile_name:
            p["achievements"].append(achievement)
            break
    save_profiles(profiles)
