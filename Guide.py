class Guide():
    def __init__(self,file):
        self.title,self.author,self.releaseDate,self.content= self.readFile(file)

    def readFile(self,file):
        with open(file,"r",encoding="utf-8") as file:
            lines = file.read().splitlines()
            title = lines[0]
            author=lines[1]
            releaseDate=lines[2]
            content=lines[3:]
        return  title,author,releaseDate,content

