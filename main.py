### main
from PyQt5.QtWidgets import QApplication
import similar_face_finder as finder
import drag_and_drop as ddrop 
import sys

# load the pickle files
finder.load_feature_files()
app = QApplication(sys.argv)
demo = ddrop.AppDemo()
demo.show()
sys.exit(app.exec_())