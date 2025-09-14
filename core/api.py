from ninja import NinjaAPI

api = NinjaAPI()

@api.get("/hello")
def hello(request):
    return {"message": "Hello World from Django Ninja!"}

@api.get("/add")
def add(request, a: int, b: int):
    return {"result": a + b}