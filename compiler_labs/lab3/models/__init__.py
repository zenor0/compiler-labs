class Snippet:
    def __init__(self, code: str):
        self.code = code
        
    def __str__(self) -> str:
        return f"<CODE, {self.code}>"