import torch
import cv2
import torch.nn as nn
import numpy as np
from scipy.interpolate import griddata
class Dewarping(object):
  def __init__(self,path_model,device='cpu'):
    self.device=device
    self.model=torch.jit.load(path_model,device)
    if device!='cpu':
      self.model.to(torch.device(self.device))
    else :  self.model.to(torch.device(self.device))
  def dewarp_predict(self, im):
    perturbed_img=im.copy()
    perturbed_img = cv2.resize(perturbed_img, (960, 1024))
    # im=self.image_detect(im)
    im = cv2.resize(im, (992, 992), interpolation=cv2.INTER_LINEAR)
    im = im.transpose(2, 0, 1)
    im = torch.from_numpy(im).float().unsqueeze(0)
    if self.device!='cpu':im=im.to(torch.device(self.device))
    outputs,outputs_segment =  self.model(im)
    pred_regress = outputs.data.cpu().numpy().transpose(0, 2, 3, 1)
    pred_segment = outputs_segment.data.round().int().cpu().numpy()
    fiducial_points=pred_regress[0]
    segment=pred_segment[0]
    # resize
    fiducial_points = fiducial_points / [992, 992] * [960, 1024]

    x, y = fiducial_points[:, :, 0].flatten().astype(int), fiducial_points[:, :, 1].flatten().astype(int)
    img_draw = perturbed_img.copy()
    for i in range(len(x)):
      img_draw = cv2.circle(img_draw, (x[i], y[i]), radius=0, color=(0, 0, 255), thickness=3)

    col_gap = 1 #4
    row_gap = col_gap# col_gap + 1 if col_gap < 6 else col_gap
    # fiducial_point_gaps = [1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60]  # POINTS NUM: 61, 31, 21, 16, 13, 11, 7, 6, 5, 4, 3, 2
    fiducial_point_gaps = [1, 2, 3, 5, 6, 10, 15, 30]        # POINTS NUM: 31, 16, 11, 7, 6, 4, 3, 2
    sshape = fiducial_points[::fiducial_point_gaps[row_gap], ::fiducial_point_gaps[col_gap], :]
    segment_h, segment_w = segment * [fiducial_point_gaps[col_gap], fiducial_point_gaps[row_gap]]
    fiducial_points_row, fiducial_points_col = sshape.shape[:2]
    im_x, im_y = np.mgrid[0:(fiducial_points_col - 1):complex(fiducial_points_col),
                  0:(fiducial_points_row - 1):complex(fiducial_points_row)]

    tshape = np.stack((im_x, im_y), axis=2) * [segment_w, segment_h]
    tshape = tshape.reshape(-1, 2)
    sshape = sshape.reshape(-1, 2)

    output_shape = (segment_h * (fiducial_points_col - 1), segment_w * (fiducial_points_row - 1))
    grid_x, grid_y = np.mgrid[0:output_shape[0] - 1:complex(output_shape[0]),
                      0:output_shape[1] - 1:complex(output_shape[1])]
    # grid_z = griddata(tshape, sshape, (grid_y, grid_x), method='cubic').astype('float32')
    grid_ = griddata(tshape, sshape, (grid_y, grid_x), method='linear').astype('float32')
    flat_img = cv2.remap(perturbed_img, grid_[:, :, 0], grid_[:, :, 1], cv2.INTER_CUBIC)
    flat_img = flat_img.astype(np.uint8)
    return img_draw,flat_img

# model = Dewarping('wrapped_rnn.pt')
# im=cv2.imread('81_72.jpg')
# x1,x2=model.dewarp_predict(im)
# cv2.imshow('lo', x1)
#
# # waits for user to press any key
# # (this is necessary to avoid Python kernel form crashing)
# cv2.waitKey(0)
#
# # closing all open windows
# cv2.destroyAllWindows()