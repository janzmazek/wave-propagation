from source.constructor import Constructor
from source.model import Model
from source.view import View
from source.controller import Controller

if __name__ == '__main__':
    constructor = Constructor()
    model = Model()
    view = View()
    controller = Controller(constructor, model, view)

    view.mainloop()
