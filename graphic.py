from pygame import Surface



class ImageSheet():
    def __init__(self, name: str, images: dict[Surface]):
        self._images: dict[Surface] = images
        self._sheet = []
        for key, image in self._images.items():
            if name in key:
                self.sheet.append(image)
        self._frames: int = len(self._sheet)

    @property
    def frames(self) -> int:
        return self._frames
    
    @property
    def sheet(self) -> list[Surface]:
        return self._sheet
    


