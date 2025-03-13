from fastapi import APIRouter

router = APIRouter(prefix="/test", tags=["test"])


@router.post("/")
async def test():
    print("Test endpoint reached!")
    return {"message": "Hello World"}
