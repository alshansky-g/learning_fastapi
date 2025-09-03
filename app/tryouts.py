from fastapi import BackgroundTasks, FastAPI, Response

app = FastAPI()


def write_notification(email: str, message=""):
    with open("log.txt", "w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(
        write_notification, email, message="some notification"
    )
    return {"message": f"Notification to {email} sent in the background"}


@app.get("/set-cookie")
def set_cookie(response: Response):
    response.set_cookie(
        key="user_id", value="12345", max_age=3600, httponly=True, secure=True
    )
    return {"message": "Cookie has been set!"}


@app.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("user_id")
    return {"message": "Logged out successfully"}
