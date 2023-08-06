import _MechEye

class Roi:
    def __init__(self, impl):
        if not isinstance(impl, _MechEye.Roi):
            raise TypeError(
                "Unsupported type for argument impl. Got {}, expected {}".format(
                    type(impl), type(_MechEye.Roi)
                )
            )
        self.__impl = impl

    def __str__(self):
        return str(self.__impl)

    def impl(self):
        return self.__impl

    def x(self):
        return str(self.__impl.x())
    
    def y(self):
        return str(self.__impl.y())

    def width(self):
        return str(self.__impl.width())

    def height(self):
        return str(self.__impl.height())
    

    