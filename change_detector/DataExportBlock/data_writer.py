from abc import abstractmethod

class DataWriter():

    @abstractmethod
    def write_file(self, coordinates, mask_path1, mask_path2, destination):
        pass

    def class_value_to_name(self, class_value):
        if class_value == 0:
            return "buildings"
        elif class_value == 1:
            return "water"
        elif class_value == 2:
            return "farmland"
        elif class_value == 3:
            return "forest"
        elif class_value == 4:
            return "grass"
        elif class_value == 5:
            return "clouds"
        elif class_value == 6:
            return "ignore"