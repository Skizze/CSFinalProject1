from controller import *

def main() -> None:
    '''
    main method to run remote program
    '''
    app = QApplication([])
    window = Controller()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()