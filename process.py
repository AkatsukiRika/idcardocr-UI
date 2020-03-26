import sys
import cv2
from PyQt5.QtWidgets import QMessageBox

idnum = sys.argv[1]
try:
    tmp_img = cv2.imread("./idcard_db/%s.jpg" % idnum)
    print("./idcard_db/%s.jpg" % idnum)
    cv2.imshow("处理结果", tmp_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    exit(0)
except:
    print("Error")
