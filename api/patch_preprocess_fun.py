from torchvision import transforms
import config_fun
import sys

vgg = {'mean': [0.485, 0.456, 0.406], 'std': [0.229, 0.224, 0.225]}
inception = {'mean': [0.485, 0.456, 0.406], 'std': [0.229, 0.224, 0.225]}
resnet = {'mean': [0.485, 0.456, 0.406], 'std': [0.229, 0.224, 0.225]}

class Rotate45(object):

    def __init__(self):
        self.degrees = 45

    def __call__(self, img):
        size = img.size
        img = img.rotate(self.degrees, expand=True)
        W = img.width
        H = img.height
        L = int(W/4)
        U = int(H/4)
        R = int(W/4*3)
        D = int(H/4*3)
        img = img.crop((L, U, R, D))
        img = img.resize(size)
        return img

def get_input_size(cfg):
    if cfg.model == 'vgg':
        return 224
    elif cfg.model == 'googlenet':
        return 299
    elif cfg.model == 'resnet':
        return 224
    else:
        print('not support the model: ' + cfg.model)
        sys.exit(-1)


def get_mean_std(cfg):
    if cfg.model == 'vgg':
        return vgg
    elif cfg.model == 'googlenet':
        return inception
    elif cfg.model == 'resnet':
        return resnet
    else:
        print('not support the model: ' + cfg.model)
        sys.exit(-1)


def get_train_val_compose():
    cfg = config_fun.config()
    input_size = get_input_size(cfg)
    info = get_mean_std(cfg)
    normalize = transforms.Normalize(mean=info['mean'],
                                     std=info['std'])
    compose = transforms.Compose([
        transforms.ToPILImage(),
        transforms.RandomResizedCrop(input_size),
        transforms.RandomHorizontalFlip(),
        transforms.RandomVerticalFlip(),
        Rotate45(),
        transforms.ToTensor(),
        normalize,
    ])
    return compose


def get_h5_compose():
    cfg = config_fun.config()
    input_size = get_input_size(cfg)
    info = get_mean_std(cfg)
    normalize = transforms.Normalize(mean=info['mean'],
                                     std=info['std'])
    compose = transforms.Compose([
        transforms.ToPILImage(),
        transforms.RandomResizedCrop(input_size),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        normalize,
    ])
    return compose

