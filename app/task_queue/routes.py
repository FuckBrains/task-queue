from .. import app
from .tasks import addition, random_numbers


@app.route("/")
def index():
    result = addition.delay(2, 5)
    print(result.get())
    new = random_numbers.delay()
    print(new.get())
    return "Sent"

