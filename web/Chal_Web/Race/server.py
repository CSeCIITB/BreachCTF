from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import random
import uvicorn
import threading
import time


app = FastAPI()

# Allow all origins for development (restrict this in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with ["http://localhost"] if needed
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Define a simple model for the election
votes = {
    "Candidate A": 0,
    "Candidate B": 0,
    "Candidate C": 0,
}
timeSinceLastVote = 0
timeBetweenVotes = 2

def my_async_function():
    print("Async function started internally")
    while True:
        randval = random.random()
        c1 = randval < 0.99
        c2 = randval < 0.40
        if c2:
            votes["Candidate A"] += 1
        elif c1:
            votes["Candidate B"] += 1
        else:
            votes["Candidate C"] += 1
        # print("Async function is running")
        global timeSinceLastVote
        timeSinceLastVote += 0.2
        time.sleep(0.2)  # Runs every 1 second
monies = {
    "Candidate A": 0,
    "Candidate B": 0,
    "Candidate C": 0,
}

# Define a request model
class Choice(BaseModel):
    selected_option: str
    donation: float | str
    
def track_votes(name):
    global timeSinceLastVote
    votes[name] += 1
    with open("votes.txt", "a") as f:
        f.write(f"{name} {votes[name]}\n")
    time.sleep(random.uniform(0.5, 1))
    timeSinceLastVote = 0
    

@app.post("/submit/")
async def submit_choice(choice: Choice):
    global timeSinceLastVote
    global timeBetweenVotes

    s = ""

    # Simulate race conditions with artificial delay
    delay = random.uniform(0.01, 0.05)  # Random delay up to 50ms
    time.sleep(delay)  

    if timeSinceLastVote < timeBetweenVotes:
        return {"message": "Please wait before voting again."}

    try:
        # Another artificial delay before updating `monies`
        time.sleep(random.uniform(0.01, 0.05))
        monies[choice.selected_option] += float(choice.donation)
    except:
        with open("charity_donations.txt", "a") as f:
            f.write(f"{choice.selected_option} {choice.donation}\n")
        s = "Donation failed. Given to charity instead "
    

    # Another artificial delay before updating `votes`
    
    threading.Thread(target=track_votes, args=(choice.selected_option,), daemon=True).start()
    
    # time.sleep(random.uniform(0.01, 0.5))
    # with open("votes.txt", "a") as f:
    #     f.write(f"{choice.selected_option} {votes[choice.selected_option]}\n")
    # # votes[choice.selected_option] += 1
    # time.sleep(random.uniform(1, 5))

    # # Simulate updating global variable (unsafe)
    # timeSinceLastVote = 0

    print(f"Vote for {choice.selected_option} received")
    print(f"Current votes: {votes[choice.selected_option]}")
    s += f"Vote for {choice.selected_option} received"
    return {"message": s}
            

@app.get("/votes/")
async def get_election():
    return {
        "message": f"Candidate A {votes["Candidate A"]}, Candidate B {votes["Candidate B"]}, Candidate C {votes["Candidate C"]}"
    }


async def startup():
    await uvicorn.run(app, host="127.0.0.1", port=8000)
    

def test():
    while True:
        print("Test function running")
        time.sleep(1)
        
        # await asyncio.sleep(1)

# Simulate some async work
if __name__ == "__main__":
    with open("charity_donations.txt", "w") as f:
        f.write("charity donations\n")
    # asyncio.run(background_task())  # Start the background task
    threading.Thread(target=my_async_function, daemon=True).start()
    
    uvicorn.run(app, host="127.0.0.1", port=8000)
    
    
    
    # loop = asyncio.get_event_loop()
    # loop.create_task(votes_updater_server())  # Schedule the updater task
    # asyncio.run(test())
