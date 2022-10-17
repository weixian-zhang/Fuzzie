from datagen import DataGenerator

class NaughtyBoolGenerator(DataGenerator):
    
    def __init__(self) -> None:
        super().__init__()
        self.data = [True, False, None, 0, 1, 'true', 'false', 'yes', 'no', '1', '0', 't', 'f', 'T', 'F', 'TRUE', 'FALSE', '', None]