<h3 align="center">
  WongKinYiu/yolov7 as independent package
</h3>

Bindings for yolov7 project (https://github.com/WongKinYiu/yolov7)

Example of usage:
```Python
from yolov7_package import Yolov7Detector
import cv2

if __name__ == '__main__':
    img = cv2.imread('img.jpg')
    det = Yolov7Detector(traced=False)
    classes, boxes, scores = det.detect(img)
    img = det.draw_on_image(img, boxes[0], scores[0], classes[0])

    cv2.imshow("image", img)
    cv2.waitKey()
```

You can use traced=True option to download and infer traced FP16 version of yolov7 model!
